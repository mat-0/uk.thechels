#!/usr/bin/env python3
"""
Interactively pick one of the last 5 Jekyll posts and syndicate it to rss.chat.

Reads server credentials from config.py, which must define:
    RSS_CHAT_URL
    RSS_CHAT_USERNAME
    RSS_CHAT_EMAIL
    RSS_CHAT_CODE

Usage:
    python3 post-to-rsschat.py [--posts-dir _posts] [--base-url https://thechels.uk]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import requests

try:
    import config
except ImportError:
    sys.exit("config.py not found. Create one with RSS_CHAT_URL, "
             "RSS_CHAT_USERNAME, RSS_CHAT_EMAIL, RSS_CHAT_CODE.")

REQUIRED_CONFIG = [
    "RSS_CHAT_URL",
    "RSS_CHAT_USERNAME",
    "RSS_CHAT_EMAIL",
    "RSS_CHAT_CODE",
]


def check_config():
    missing = [
        name for name in REQUIRED_CONFIG if not getattr(config, name, None)
    ]
    if missing:
        sys.exit(f"config.py is missing: {', '.join(missing)}")


def front_matter(text):
    """Return dict of front matter keys (simple key: value pairs only)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip().strip('"').strip("'")
        data[key] = value
    return data


def slug_from_filename(filename):
    stem = Path(filename).stem
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)


def load_recent_posts(posts_dir, count=5):
    files = sorted(Path(posts_dir).rglob("*.md"),
                   key=lambda f: f.name,
                   reverse=True)[:count]
    posts = []
    for f in files:
        fm = front_matter(f.read_text(encoding="utf-8"))
        posts.append({
            "file": f,
            "title": fm.get("title", slug_from_filename(f.name)),
            "slug": slug_from_filename(f.name),
        })
    return posts


def choose_post(posts):
    print("\nMost recent posts:\n")
    for i, post in enumerate(posts, start=1):
        print(f"  {i}. {post['title']}")
    print()

    while True:
        choice = input(
            f"Choose a post to syndicate (1-{len(posts)}, or q to quit): "
        ).strip()
        if choice.lower() == "q":
            sys.exit(0)
        if choice.isdigit() and 1 <= int(choice) <= len(posts):
            return posts[int(choice) - 1]
        print("Invalid choice, try again.")


def build_description(title, source_url):
    return f'<p><a href="{source_url}">{source_url}</a></p>'


def post_to_rsschat(title, source_url):
    description = build_description(title, source_url)
    payload = {
        "jsontext": json.dumps({
            "description": description,
            "title": title
        }),
        "emailaddress": config.DEMO_RSS_CHAT_EMAIL,
        "emailcode": config.DEMO_RSS_CHAT_CODE,
    }

    url = config.DEMO_RSS_CHAT_URL.rstrip("/") + "/newpost"
    response = requests.post(url, params=payload, timeout=15)

    if response.status_code == 200:
        print(f"\nPosted as {config.DEMO_RSS_CHAT_USERNAME}: {source_url}")
        try:
            item = response.json()
            if "guid" in item:
                print(f"rss.chat permalink: {item['guid']}")
        except ValueError:
            pass
    else:
        print(f"\nFAILED ({response.status_code}): {response.text}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posts-dir",
                        default="_posts",
                        help="Path to Jekyll _posts directory")
    parser.add_argument(
        "--base-url",
        default=None,
        help=
        "Site base URL (falls back to config.BASE_URL, then https://thechels.uk)"
    )
    args = parser.parse_args()

    check_config()

    base_url = args.base_url or getattr(config, "BASE_URL",
                                        "https://thechels.uk")
    base_url = base_url.rstrip("/")

    posts_dir = Path(args.posts_dir)
    if not posts_dir.is_dir():
        sys.exit(f"Posts directory not found: {posts_dir}")

    posts = load_recent_posts(posts_dir)
    if not posts:
        sys.exit(f"No posts found in {posts_dir}")

    post = choose_post(posts)
    source_url = f"{base_url}/{post['slug']}"

    print(f"\nAbout to post:\n  Title: {post['title']}\n  URL:   {source_url}")
    confirm = input("Confirm? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    post_to_rsschat(post["title"], source_url)


if __name__ == "__main__":
    main()
