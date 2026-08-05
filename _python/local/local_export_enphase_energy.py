#!/usr/bin/env python3
"""
Enphase daily energy pull for a Jekyll site's _data/energy.yml.

Designed to be run via VS Code's Run button (or a terminal) irregularly -
weekly, monthly, whatever - and it backfills every missing day between the
last entry already saved and yesterday in one go.

First run: config.ENPHASE_REFRESH_TOKEN will be empty, so this script walks
you through the one-time interactive login (prints a URL, you paste back a
code) and writes the resulting refresh token into config.py itself. Every
run after that just uses and, if Enphase rotates it, rewrites that token -
no separate token file.
"""
import base64
import os
import re
import sys
import urllib.parse
from datetime import date, datetime, timedelta

import requests
import yaml

import config  # noqa: E402  (config.py lives alongside this script)

TOKEN_URL = "https://api.enphaseenergy.com/oauth/token"
API_BASE = "https://api.enphaseenergy.com/api/v4"
# Fixed placeholder redirect used by Enphase for apps with no callback server
# of their own (there is no field to configure this in the developer portal).
REDIRECT_URI = "https://api.enphaseenergy.com/oauth/redirect_uri"
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "config.py")

# ---------------------------------------------------------------------------
# Config file writing (refresh token lives inside config.py, not a separate file)
# ---------------------------------------------------------------------------


def save_refresh_token_to_config(token: str) -> None:
    with open(CONFIG_PATH) as f:
        content = f.read()

    pattern = re.compile(r'^ENPHASE_REFRESH_TOKEN\s*=.*$', re.MULTILINE)
    new_line = f'ENPHASE_REFRESH_TOKEN = "{token}"'

    if pattern.search(content):
        content = pattern.sub(new_line, content, count=1)
    else:
        content = content.rstrip("\n") + f"\n{new_line}\n"

    with open(CONFIG_PATH, "w") as f:
        f.write(content)

    # Keep the in-memory config in sync for the rest of this run.
    config.ENPHASE_REFRESH_TOKEN = token


# ---------------------------------------------------------------------------
# OAuth
# ---------------------------------------------------------------------------


def interactive_login() -> dict:
    print("\nNo working refresh token - need a one-time interactive login.\n")

    # ENPHASE_AUTH_URL from the portal already includes response_type and
    # client_id (that's how Enphase displays it) - only redirect_uri needs
    # appending here, not the whole param set again.
    separator = "&" if "?" in config.ENPHASE_AUTH_URL else "?"
    auth_url = (f"{config.ENPHASE_AUTH_URL}{separator}"
                f"redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}")
    print("Open this URL, log in, and approve the app:\n")
    print(auth_url)
    print(
        "\nYou'll land on a URL containing '?code=XXXXX'. Copy just the code.")

    code = input("\nPaste the authorization code here: ").strip()

    basic = base64.b64encode(
        f"{config.ENPHASE_CLIENT_ID.strip()}:{config.ENPHASE_CLIENT_SECRET.strip()}"
        .encode()).decode()
    resp = requests.post(
        TOKEN_URL,
        params={
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": code.strip(),
        },
        headers={"Authorization": f"Basic {basic}"},
        timeout=30,
    )
    if resp.status_code != 200:
        print(
            f"ERROR: authorization code exchange failed ({resp.status_code}): {resp.text}",
            file=sys.stderr)
        sys.exit(1)
    return resp.json()


def refresh_access_token(refresh_token: str):
    """Returns token data dict on success, or None if the refresh token is
    missing/invalid so the caller can fall back to interactive login."""
    if not refresh_token:
        return None

    basic = base64.b64encode(
        f"{config.ENPHASE_CLIENT_ID.strip()}:{config.ENPHASE_CLIENT_SECRET.strip()}"
        .encode()).decode()
    resp = requests.post(
        TOKEN_URL,
        params={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token.strip()
        },
        headers={"Authorization": f"Basic {basic}"},
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"Refresh token didn't work ({resp.status_code}): {resp.text}")
        return None
    return resp.json()


def get_access_token() -> str:
    existing_refresh_token = getattr(config, "ENPHASE_REFRESH_TOKEN", "") or ""
    token_data = refresh_access_token(existing_refresh_token)

    if token_data is None:
        token_data = interactive_login()

    new_refresh_token = token_data.get("refresh_token")
    if new_refresh_token and new_refresh_token != existing_refresh_token:
        save_refresh_token_to_config(new_refresh_token)
        print("Refresh token saved to config.py.")

    return token_data["access_token"]


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------


def fetch_daily_series(endpoint: str, access_token: str, start_date: date,
                       end_date: date):
    resp = requests.get(
        f"{API_BASE}/systems/{config.ENPHASE_SYSTEM_ID}/{endpoint}",
        params={
            "key": config.ENPHASE_API_KEY,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    if resp.status_code != 200:
        print(
            f"WARNING: {endpoint} fetch failed ({resp.status_code}): {resp.text}",
            file=sys.stderr)
        return None
    return resp.json()


def series_value_for_offset(data: dict, key: str, offset: int):
    """Pull the value at position `offset` days after the series' start_date."""
    if data is None:
        return None
    series = data.get(key)
    if not isinstance(series, list):
        print(f"WARNING: expected a list under '{key}' but got: {series!r}",
              file=sys.stderr)
        return None
    if offset >= len(series):
        return None
    val = series[offset]
    return None if val is None or val < 0 else val


def wh_to_kwh(wh):
    return None if wh is None else round(wh / 1000, 2)


# ---------------------------------------------------------------------------
# energy.yml handling
# ---------------------------------------------------------------------------


def load_energy_data(path: str) -> list:
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
            return data or []
    except FileNotFoundError:
        return []


def save_energy_data(path: str, entries: list) -> None:
    entries_sorted = sorted(entries, key=lambda e: e["date"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(entries_sorted,
                  f,
                  default_flow_style=False,
                  sort_keys=False,
                  allow_unicode=True)


def determine_start_date(existing_entries: list) -> date:
    if existing_entries:
        last_date = max(e["date"] for e in existing_entries)
        return last_date + timedelta(days=1)
    backfill = getattr(config, "BACKFILL_START_DATE", None)
    if backfill:
        return datetime.strptime(backfill, "%Y-%m-%d").date()
    return date.today() - timedelta(days=1)


def self_sufficiency_pct(used_kwh, imported_kwh):
    if used_kwh is None or imported_kwh is None or used_kwh == 0:
        return None
    return round((used_kwh - imported_kwh) / used_kwh * 100, 2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    existing_entries = load_energy_data(config.ENERGY_DATA_PATH)
    start_date = determine_start_date(existing_entries)
    end_date = date.today() - timedelta(
        days=1)  # never include today - still partial

    if start_date > end_date:
        print("Already up to date - nothing to fetch.")
        return

    print(
        f"Fetching {start_date.isoformat()} through {end_date.isoformat()}...")

    access_token = get_access_token()

    gen_data = fetch_daily_series("energy_lifetime", access_token, start_date,
                                  end_date)
    used_data = fetch_daily_series("consumption_lifetime", access_token,
                                   start_date, end_date)
    export_data = fetch_daily_series("energy_export_lifetime", access_token,
                                     start_date, end_date)
    import_data = fetch_daily_series("energy_import_lifetime", access_token,
                                     start_date, end_date)
    battery_data = fetch_daily_series("battery_lifetime", access_token,
                                      start_date, end_date)

    entries_by_date = {e["date"]: e for e in existing_entries}

    num_days = (end_date - start_date).days + 1
    for offset in range(num_days):
        d = start_date + timedelta(days=offset)

        generated_kwh = wh_to_kwh(
            series_value_for_offset(gen_data, "production", offset))
        used_kwh = wh_to_kwh(
            series_value_for_offset(used_data, "consumption", offset))
        exported_kwh = wh_to_kwh(
            series_value_for_offset(export_data, "export", offset))
        imported_kwh = wh_to_kwh(
            series_value_for_offset(import_data, "import", offset))
        battery_charged_kwh = wh_to_kwh(
            series_value_for_offset(battery_data, "charge", offset))
        battery_discharged_kwh = wh_to_kwh(
            series_value_for_offset(battery_data, "discharge", offset))

        entries_by_date[d] = {
            "date": d,
            "generated_kwh": generated_kwh,
            "used_kwh": used_kwh,
            "exported_kwh": exported_kwh,
            "imported_kwh": imported_kwh,
            "battery_charged_kwh": battery_charged_kwh,
            "battery_discharged_kwh": battery_discharged_kwh,
            "self_sufficiency_pct":
            self_sufficiency_pct(used_kwh, imported_kwh),
        }

    save_energy_data(config.ENERGY_DATA_PATH, list(entries_by_date.values()))
    print(f"\nSaved {num_days} day(s) to {config.ENERGY_DATA_PATH}.")


if __name__ == "__main__":
    main()
