#!/usr/bin/env python3
"""
Fetch replies from rss.chat and store them as Jekyll data files.

Flow:
  1. Fetch the main feed (MAIN_FEED_URL).
  2. For each <item>, pull the post URL out of <description> (an <a href="...">)
     and the comment feed URL + count out of <source:comments>.
  3. If count > 0, fetch that comment feed and parse each reply <item>.
  4. Merge new replies into _data/replies/<slug>.yml, deduped by guid.
  5. Exit code / stdout indicate whether anything changed, so the Action
     knows whether to commit.
"""

import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import bleach
import yaml

MAIN_FEED_URL = "https://demo.rss.chat/users/thechelsuk/rss.xml"
DATA_DIR = Path("../_data/replies")

NS = {"source": "https://source.scripting.com/"}

HREF_RE = re.compile(r'href=["\']([^"\']+)["\']')

# Allowlist for reply body HTML. Anything not listed here is stripped
# (tags removed but their text content kept; see bleach docs).
ALLOWED_TAGS = [
    "p", "a", "strong", "em", "b", "i", "br", "ul", "ol", "li", "blockquote",
    "code", "pre"
]
ALLOWED_ATTRS = {"a": ["href", "rel"]}
ALLOWED_SCHEMES = ["http", "https", "mailto"]


def sanitize_html(raw_html: str) -> str:
    """Strip anything not on the allowlist (scripts, event handlers, iframes,
    style attrs, javascript: URLs, etc). Also forces rel=nofollow ugc noopener
    on links so spam replies don't pass SEO value or open tab-nabbing vectors."""
    cleaned = bleach.clean(
        raw_html or "",
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_SCHEMES,
        strip=True,
    )
    return bleach.linkify(
        cleaned,
        callbacks=[
            lambda attrs, new: attrs.__setitem__(
                (None, "rel"), "nofollow ugc noopener") or attrs
        ],
        skip_tags=["pre", "code"],
    )


def sanitize_url(url: str | None) -> str | None:
    """Only allow http(s) URLs through to href attributes. Blocks javascript:,
    data:, and other schemes that could be used for attribute-based XSS."""
    if not url:
        return None
    scheme = urlparse(url).scheme.lower()
    return url if scheme in ("http", "https") else None


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": "thechels-reply-sync/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def slugify_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    slug = path.replace("/", "-") or "index"
    return re.sub(r"[^a-zA-Z0-9\-]", "-", slug)


def extract_post_url(description: str) -> str | None:
    match = HREF_RE.search(description or "")
    return match.group(1) if match else None


def parse_main_feed(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    for item in root.iterfind(".//item"):
        description = (item.findtext("description") or "").strip()
        post_url = extract_post_url(description)

        comments = item.find("source:comments", NS)
        if comments is None or post_url is None:
            continue

        try:
            count = int(comments.get("count", "0"))
        except ValueError:
            count = 0

        feed_url = comments.get("feedUrl")
        if not feed_url or count < 1:
            continue

        yield post_url, feed_url


def parse_comment_feed(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    for item in root.iterfind(".//item"):
        guid = item.findtext("guid")
        if not guid:
            continue

        source_el = item.find("source")
        author = source_el.text.strip(
        ) if source_el is not None and source_el.text else "Anonymous"
        author_url = source_el.get("url") if source_el is not None else None

        yield {
            "guid":
            guid,
            # author is plain text stored as-is; Jekyll/Liquid does not
            # auto-escape output, so the include must use the `escape` filter
            "author":
            bleach.clean(author, tags=[], strip=True),
            "author_url":
            sanitize_url(author_url),
            "pub_date": (item.findtext("pubDate") or "").strip(),
            "html":
            sanitize_html((item.findtext("description") or "").strip()),
            "markdown":
            bleach.clean((item.findtext("source:markdown", namespaces=NS)
                          or "").strip(),
                         tags=[],
                         strip=True),
            "in_reply_to": (item.findtext("source:inReplyTo", namespaces=NS)
                            or "").strip(),
        }


def load_existing(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or []


def save(path: Path, replies: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(replies, fh, sort_keys=False, allow_unicode=True, width=1000)


def sync() -> bool:
    changed = False

    main_xml = fetch(MAIN_FEED_URL)

    for post_url, feed_url in parse_main_feed(main_xml):
        try:
            comment_xml = fetch(feed_url)
        except Exception as exc:  # noqa: BLE001
            print(f"WARN: failed to fetch {feed_url}: {exc}", file=sys.stderr)
            continue

        new_replies = list(parse_comment_feed(comment_xml))
        if not new_replies:
            continue

        slug = slugify_url(post_url)
        data_path = DATA_DIR / f"{slug}.yml"
        existing = load_existing(data_path)
        existing_guids = {r["guid"] for r in existing}

        added = [r for r in new_replies if r["guid"] not in existing_guids]
        if not added:
            continue

        merged = existing + added
        merged.sort(key=lambda r: r.get("pub_date", ""))
        save(data_path, merged)

        print(f"{slug}: added {len(added)} reply(ies)")
        changed = True

    return changed


if __name__ == "__main__":
    did_change = sync()
    # Used by the Action to decide whether to commit.
    print("CHANGED" if did_change else "NO_CHANGE")
    sys.exit(0)
