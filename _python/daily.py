import feedparser
import pathlib
import helper
import os
import datetime
import re

ROOT = pathlib.Path(__file__).parent.parent.resolve()
SOURCE = ROOT / "_pages/daily.md"
OUTPUT_FOLDER = ROOT / "_posts"

FILE_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
FM_DATE = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
FILENAME = f"{FILE_DATE}-daily-rundown.md"


def strip_front_matter(text):
    fm_pattern = r'^---\s*\n.*?\n---\s*\n'
    return re.sub(fm_pattern, '', text, flags=re.DOTALL)


def read_source_file(path: pathlib.Path) -> str:
    """Read the markdown source file and return its contents."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"x Failed to read source file {path}: {e}")


def strip_front_matter_md(text: str) -> str:
    """Remove YAML front matter from markdown text."""
    fm_pattern = r'^---\s*\n.*?\n---\s*\n'
    return re.sub(fm_pattern, '', text, flags=re.DOTALL).lstrip('\n')


def build_front_matter(date: str, title: str, permalink: str) -> str:
    """Build the Jekyll front matter block."""
    return (
        f"---\nlayout: post\ndate: {date}\ntype: daily\ntitle: {title}\npermalink: {permalink}\robots: noindex\n---\n\n"
    )


def ensure_output_dir(year: str) -> pathlib.Path:
    """Ensure the output directory for the year exists and return its Path."""
    year_folder = OUTPUT_FOLDER / year
    if not year_folder.exists():
        year_folder.mkdir(parents=True, exist_ok=True)
    return year_folder


def build_output_path(year_folder: pathlib.Path,
                      file_date: str) -> pathlib.Path:
    """Build the output file path for the post."""
    filename = f"{file_date}-daily-rundown-for-{file_date}.md"
    return year_folder / filename


def write_post_file(path: pathlib.Path, front_matter: str, body: str) -> None:
    """Write the front matter and body to the output file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(body)
        print(f"✓ Created: {path}")
    except Exception as e:
        raise RuntimeError(f"x Failed to write file {path}: {e}")


def generate_daily_post() -> pathlib.Path:
    """
    Orchestrate the daily post generation. Returns the output path.
    """
    raw_content = read_source_file(SOURCE)
    body_content = strip_front_matter_md(raw_content)
    title = f"Daily Rundown for {FILE_DATE}"
    permalink = f"/{FILE_DATE}-daily-rundown"
    fm_content = build_front_matter(FM_DATE, title, permalink)
    year = FILE_DATE.split('-')[0]
    year_folder = ensure_output_dir(year)
    output_path = build_output_path(year_folder, FILE_DATE)
    write_post_file(output_path, fm_content, body_content)
    return output_path


if __name__ == "__main__":
    try:
        generate_daily_post()
    except Exception as e:
        print(e)
