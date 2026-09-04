import pathlib
import os
import datetime
import re
import hashlib
import feedparser

ROOT = pathlib.Path(__file__).parent.parent.resolve()
RSS_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCwK4oZ8hw9RS6tZKEjw_qLw"
OUTPUT_FOLDER = ROOT / "_posts"

# ================= HELPER FUNCTIONS =================


def get_video_id(entry):
    """
    Extracts the video ID from the XML custom element yt:videoId.
    Returns just the video ID (e.g. '9l1GQ7fQwIg').
    """
    # Primary source: XML custom element
    video_id = entry.get('yt:videoId')

    if video_id:
        return video_id.strip()

    # Fallback to link parsing only if custom ID is missing
    link = entry.get('link')
    if link:
        # Handle standard YouTube format
        video_id = extract_id_from_link(link)
        if video_id:
            return video_id
    return None


def extract_id_from_link(link):
    """
    Safely extracts the video ID from various YouTube URL formats.
    Returns None if extraction fails.
    """
    # Standard watch URL
    parts = link.split('v=')
    if len(parts) > 1:
        # Get the string after v=
        video_id = parts[1].split('&')[0].split('?')[0]
        # Remove any trailing chars (like t for YouTube short)
        video_id = re.sub(r'[^a-zA-Z0-9_-]', '', video_id)
        if len(video_id) == 11:
            return video_id

    # Shorts URL format (e.g., youtube.com/shorts/sQtW_IPB-Yk)
    if '/shorts/' in link:
        parts = link.split('/shorts/')
        if len(parts) > 1:
            video_id = parts[1].split('/')[0]
            video_id = re.sub(r'[^a-zA-Z0-9_-]', '', video_id)
            if len(video_id) == 11:
                return video_id

    # Watch URL alternative (e.g., youtube.com/watch?v=...)
    if 'watch' in link and 'shorts' not in link:
        parts = link.split('watch')
        if len(parts) > 1:
            parts = parts[1].split('v=')
            if len(parts) > 1:
                video_id = parts[1].split('&')[0]
                video_id = re.sub(r'[^a-zA-Z0-9_-]', '', video_id)
                if len(video_id) == 11:
                    return video_id

    return None


def parse_date(entry):
    """
    Parses the date from RSS entry.
    Returns a string in 'yyyy-mm-dd' format only (no time).
    Handles both str and datetime objects.
    """
    pub_date = entry.published

    # feedparser returns datetime object or ISO8601 string
    if isinstance(pub_date, str):
        try:
            # Handle timezone formats correctly
            dt = datetime.datetime.fromisoformat(
                pub_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    elif hasattr(pub_date, 'strftime'):
        dt = pub_date
    else:
        dt = datetime.datetime.now()

    # Format: 'yyyy-mm-dd' only (no time)
    return dt.strftime('%Y-%m-%d')


def get_year(date_str):
    """
    Extracts the year for the folder path.
    """
    if date_str and len(date_str) > 4:
        return date_str[:4]
    else:
        return datetime.datetime.now().strftime('%Y')


def clean_title_for_file(title):
    """
    Removes special characters to create a valid Markdown filename.
    Replaces spaces with hyphens.
    """
    # Remove anything that isn't alphanumeric or space/hyphen
    title = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    return title.lower().replace(' ', '-')


def get_unique_filename(year, date_str, title, video_id):
    """
    Generates the filename with the hash to prevent duplicates.
    Format: year/yyyymmdd-title-hash.md

    Folder: _posts/2025/
    Filename: 2025-04-18-shortkeys-title-hash.md
    """
    clean_title_for_filename = clean_title_for_file(title)

    # Hash the video ID to ensure uniqueness even if title changes
    video_id_hash = get_video_id_hash(video_id)

    # Filename: yyyy-mm-dd-title-hash.md
    filename = f"{date_str}-video-{clean_title_for_filename}-{video_id_hash}.md"
    return f"{year}/{filename}"


def get_video_id_hash(video_id):
    """Returns the filename-safe identifier derived from a video ID."""
    return hashlib.sha256(video_id.encode()).hexdigest()[:8]


def post_exists_for_video(video_id):
    """Checks every generated post, regardless of its date or title."""
    video_id_hash = get_video_id_hash(video_id)
    filename_suffix = f"-{video_id_hash}.md"

    return any(
        path.name.endswith(filename_suffix)
        for path in OUTPUT_FOLDER.rglob("*.md"))


def create_front_matter(entry):
    """
    Generates the Front Matter YAML.
    Includes only: layout, title, date, source, type.
    NO author, NO tags, NO categories, NO permalink.
    """
    title = entry.title
    link = entry.link
    video_id = get_video_id(entry)

    # Parse date for display
    date_str = parse_date(entry)
    year_folder = get_year(date_str)

    # Construct Front Matter
    fm_content = f"""---
title: "{title}"
date: "{date_str}"
layout: post
source: "{link}"
type: video
---
"""

    return fm_content


def generate_body(video_url):
    """
    Generates the Markdown body content.
    Single line link only.
    """
    return f"[Watch on Youtube]({video_url})\n"


def save_post_to_jekyll(fm_content, body_content, filename, video_id=None):
    """
    Writes the file to the correct directory structure.
    """
    file_content = fm_content + body_content

    # Construct file path inside _posts folder
    file_path = os.path.join(OUTPUT_FOLDER, filename)

    if os.path.exists(file_path) or (video_id
                                     and post_exists_for_video(video_id)):
        print(f"✓ Skipping existing file: {file_path}")
        return

    # Ensure parent directories exist (e.g. _posts/2025)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
    except Exception as e:
        print(f"x Failed to write file {file_path}: {e}")


def process_entry(entry):
    """
    Pure function. Handles the logic for one entry.
    This is what you can test locally with mock entries.
    """
    title = entry.title
    link = entry.link
    video_id = get_video_id(entry)

    fm_content = create_front_matter(entry)
    body_content = generate_body(link)
    filename = get_unique_filename(get_year(parse_date(entry)),
                                   parse_date(entry), title, video_id)

    return fm_content, body_content, filename


def run_main():
    """
    Main entry point.
    Parses RSS and writes files.
    """
    # Parse feed entries
    feed = feedparser.parse(RSS_FEED_URL)
    entries = feed.entries

    if not entries:
        print("No entries found in RSS feed.")
        return

    print(f"Found {len(entries)} videos to process.")

    for entry in entries:
        try:
            # Process content
            fm, body, filename = process_entry(entry)

            # Save file
            save_post_to_jekyll(fm, body, filename, get_video_id(entry))

        except Exception as e:
            # Only print the error message, not the entire entry
            error_msg = str(e)
            print(f"x Error processing entry: {error_msg}")
            continue

    print("Script finished.")


# ================= MAIN EXECUTION =================
if __name__ == "__main__":
    run_main()
