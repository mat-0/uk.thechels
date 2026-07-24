#!/usr/bin/env python3
"""
Export Zwift activities to Jekyll-formatted markdown files.

Requires:
    pip install zwift-client

Usage:
    python zwift_to_jekyll.py

Config:
    Create config.py alongside this script with:
        PLAYER_ID = 123456
        USERNAME = "your-zwift-username"
        PASSWORD = "your-zwift-password"

Behaviour:
    - Pulls all activities on first run.
    - On subsequent runs, activities already exported (matched by Zwift
      activity ID embedded in the filename) are skipped, so only new
      activities are written.
"""

import datetime as dt
import re
import sys
from pathlib import Path

from zwift import Client

try:
    import config
except ImportError:
    sys.exit("Missing config.py. See docstring for required fields.")

OUTPUT_DIR = Path("_rides")
PAGE_SIZE = 50  # activities fetched per API call

# Candidate keys the Zwift API has been observed to use for each field.
# First matching key found in the activity dict wins.
FIELD_MAP = {
    "Distance": (["distanceInMeters"], "m_to_km"),
    "Duration": (["movingTimeInMs", "elapsedTimeInMs",
                  "duration"], "duration"),
    "Calories": (["calories"], None),
    "Avg power": (["avgWatts", "avg_watts"], "watts"),
    "Max power": (["maxWatts", "max_watts"], "watts"),
    "Avg heart rate": (["avgHeartRate", "avg_heart_rate"], "bpm"),
    "Max heart rate": (["maxHeartRate", "max_heart_rate"], "bpm"),
    "Avg cadence": (["avgCadence", "avg_cadence"], "rpm"),
    "Max cadence": (["maxCadence", "max_cadence"], "rpm"),
    "Elevation gain": (["totalElevation", "elevationGain", "climbing"], "m"),
    "Avg speed": (["avgSpeed", "avg_speed"], "kph"),
    "Max speed": (["maxSpeed", "max_speed"], "kph"),
}


def first_value(activity, keys):
    for key in keys:
        if key in activity and activity[key] is not None:
            return activity[key], key
    return None, None


def as_float(value):
    """API fields are sometimes strings, sometimes numbers. Normalise to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fmt_m_to_km(value):
    value = as_float(value)
    if value is None:
        return None
    return f"{value / 1000:.2f} km"


def fmt_duration(value, source_key):
    value = as_float(value)
    if value is None:
        return None
    if source_key in ("movingTimeInMs", "elapsedTimeInMs"):
        seconds = value / 1000
    elif source_key == "duration":
        # Zwift's activity "duration" field is in minutes
        seconds = value * 60
    else:
        seconds = value
    return str(dt.timedelta(seconds=int(seconds)))


def fmt_watts(value):
    value = as_float(value)
    if value is None:
        return None
    return f"{value:.0f} W"


def fmt_bpm(value):
    value = as_float(value)
    if value is None:
        return None
    return f"{value:.0f} bpm"


def fmt_rpm(value):
    value = as_float(value)
    if value is None:
        return None
    return f"{value:.0f} rpm"


def fmt_m(value):
    value = as_float(value)
    if value is None:
        return None
    return f"{value:.0f} m"


def fmt_kph(value):
    value = as_float(value)
    if value is None:
        return None
    return f"{value:.1f} kph"


FORMATTERS = {
    "m_to_km": fmt_m_to_km,
    "watts": fmt_watts,
    "bpm": fmt_bpm,
    "rpm": fmt_rpm,
    "m": fmt_m,
    "kph": fmt_kph,
}


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def parse_start_date(activity):
    raw = activity.get("startDate") or activity.get("start_date")
    if not raw:
        return dt.datetime.now()
    # Zwift typically returns ISO 8601, sometimes with a trailing Z
    raw = raw.replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(raw)
    except ValueError:
        return dt.datetime.now()


def existing_ids(output_dir):
    ids = set()
    if not output_dir.exists():
        return ids
    for f in output_dir.glob("*.md"):
        match = re.search(r"-(\d+)\.md$", f.name)
        if match:
            ids.add(match.group(1))
    return ids


def build_markdown(activity):
    activity_id = str(activity["id"])
    name = activity.get("name") or "Untitled ride"
    start = parse_start_date(activity)

    lines = [
        "---",
        "layout: ride",
        f'title: "{name}"',
        f"date: {start.strftime('%Y-%m-%d %H:%M').strip()}",
        f"zwift_id: {activity_id}",
        f"zwift_url: https://zwift.com/uk/activity/{activity_id}",
        f"type: ride",
        f"tags: [rides]",
        "---",
        "",
    ]

    for label, (keys, formatter_name) in FIELD_MAP.items():
        value, matched_key = first_value(activity, keys)
        if value is None:
            continue
        if formatter_name == "duration":
            value = fmt_duration(value, matched_key)
        elif formatter_name:
            value = FORMATTERS[formatter_name](value)
        if value is None:
            continue
        lines.append(f"- {label}: {value}")

    return "\n".join(lines) + "\n", start, activity_id, name


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    already_exported = existing_ids(OUTPUT_DIR)

    client = Client(config.USERNAME, config.PASSWORD)
    activity_api = client.get_activity(config.PLAYER_ID)

    start = 0
    new_count = 0
    while True:
        batch = activity_api.list(start=start, limit=PAGE_SIZE)
        if not batch:
            break

        for meta in batch:
            activity_id = str(meta["id"])
            if activity_id in already_exported:
                continue

            # metadata from list() is often thinner than get_activity();
            # fetch the full record for richer stats
            try:
                full = activity_api.get_activity(activity_id)
            except Exception:
                full = meta

            content, ride_date, aid, name = build_markdown(full)
            filename = f"{ride_date.strftime('%Y-%m-%d')}-{slugify(name)}-{aid}.md"
            (OUTPUT_DIR / filename).write_text(content, encoding="utf-8")
            already_exported.add(aid)
            new_count += 1
            print(f"Wrote {filename}")

        start += PAGE_SIZE

    print(f"Done. {new_count} new activity file(s) written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
