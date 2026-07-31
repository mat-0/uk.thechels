#!/usr/bin/env bash

set -euo pipefail

before_sha="${1:?before sha is required}"
current_sha="${2:?current sha is required}"

base_url="${BASE_URL:-https://thechels.uk}"
bridgy_webmention_url="${BRIDGY_WEBMENTION_URL:-https://brid.gy/publish/webmention}"
bridgy_publish_base="${bridgy_webmention_url%/webmention}"

rss_chat_url="${RSS_CHAT_URL:-}"
rss_chat_username="${RSS_CHAT_USERNAME:-}"
rss_chat_email="${RSS_CHAT_EMAIL:-}"
rss_chat_code="${RSS_CHAT_CODE:-}"
rss_chat_url="${rss_chat_url%/}"

targets=(mastodon bluesky)

front_matter_value() {
  local key="$1"
  local file="$2"
  awk -F ':' -v key="$key" '
    BEGIN { in_front_matter = 0 }
    /^---[[:space:]]*$/ {
      if (in_front_matter) { exit }
      in_front_matter = 1
      next
    }
    in_front_matter {
      field = $1
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", field)
      if (tolower(field) == tolower(key)) {
        sub(/^[^:]+:[[:space:]]*/, "", $0)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", $0)
        gsub(/^["\047]|["\047]$/, "", $0)
        print $0
        exit
      }
    }
  ' "$file"
}

# Extracts the raw block for a given front-matter key, preserving any
# following indented list lines (for YAML block-style arrays). Returns
# the key's own line content plus any subsequent "  - item" lines, up
# until a line that is not indented (i.e. the next top-level key) or
# the closing "---".
front_matter_block() {
  local key="$1"
  local file="$2"
  awk -v key="$key" '
    BEGIN { in_front_matter = 0; in_block = 0 }
    /^---[[:space:]]*$/ {
      if (in_front_matter) { exit }
      in_front_matter = 1
      next
    }
    !in_front_matter { next }
    {
      if (in_block) {
        if ($0 ~ /^[[:space:]]+-/) {
          print
          next
        } else if ($0 ~ /^[[:space:]]*$/) {
          next
        } else {
          exit
        }
      }
      line = $0
      sub(/^[[:space:]]+/, "", line)
      split(line, parts, ":")
      field = parts[1]
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", field)
      if (tolower(field) == tolower(key)) {
        print
        in_block = 1
      }
    }
  ' "$file"
}

should_syndicate_post() {
  local file="$1"
  local syndicate
  syndicate="$(front_matter_value syndicate "$file" | tr '[:upper:]' '[:lower:]')"
  [[ "$syndicate" == "true" ]]
}

# True if front matter `class` (scalar, inline array, or YAML block
# array) contains "rss" as a whole word, case-insensitive.
has_rss_class() {
  local file="$1"
  local block
  block="$(front_matter_block class "$file")"
  [[ -z "$block" ]] && return 1
  # Strip YAML list punctuation so words are space-separated, then
  # match "rss" as a standalone token (avoids matching "rssfeed" etc).
  block="$(printf '%s\n' "$block" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' ' ')"
  [[ " ${block} " == *" rss "* ]]
}

post_title() {
  local file="$1"
  front_matter_value title "$file"
}

post_source_url() {
  local file="$1"
  local filename
  local slug
  filename="$(basename "$file")"
  slug="${filename%.md}"
  slug="$(printf '%s' "$slug" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//')"
  printf '%s/%s\n' "${base_url%/}" "$slug"
}

syndicate_post() {
  local source_url="$1"
  local target
  local target_url
  local status_code

  echo "Syndicating: $source_url"

  for target in "${targets[@]}"; do
    target_url="${bridgy_publish_base}/$target"
    status_code=$(curl -sS -o /tmp/bridgy_publish_response -w "%{http_code}" \
      --data-urlencode "source=${source_url}" \
      --data-urlencode "target=${target_url}" \
      "${bridgy_webmention_url}")
    echo "  ${target}: ${status_code}"
  done
}

json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  printf '%s' "$s"
}

syndicate_to_rss_chat() {
  local source_url="$1"
  local title="$2"
  local description
  local jsontext
  local status_code

  if [[ -z "$rss_chat_url" || -z "$rss_chat_email" || -z "$rss_chat_code" ]]; then
    echo "  rss.chat: skipped (secrets not set)"
    return 0
  fi

  local description_html
  description_html="<p><a href=\"${source_url}\">${source_url}</a></p>"
  description="$(json_escape "$description_html")"

  jsontext="{\"description\":\"${description}\",\"title\":\"$(json_escape "$title")\"}"

  status_code=$(curl -sS -G -o /tmp/rsschat_response -w "%{http_code}" \
    --data-urlencode "jsontext=${jsontext}" \
    --data-urlencode "emailaddress=${rss_chat_email}" \
    --data-urlencode "emailcode=${rss_chat_code}" \
    "${rss_chat_url}/newpost")

  if [[ "$status_code" == "200" ]]; then
    echo "  rss.chat (${rss_chat_username}): $status_code"
  else
    echo "  rss.chat (${rss_chat_username}): FAILED $status_code - $(cat /tmp/rsschat_response)"
    return 1
  fi
}

if [[ "$before_sha" == "0000000000000000000000000000000000000000" ]]; then
  echo "No previous commit range available, skipping syndication."
  exit 0
fi

mapfile -t new_posts < <(git diff --diff-filter=A --name-only "$before_sha" "$current_sha" -- _posts/)

if [[ ${#new_posts[@]} -eq 0 ]]; then
  echo "No new posts detected, skipping syndication."
  exit 0
fi

exit_code=0

for file in "${new_posts[@]}"; do
  source_url="$(post_source_url "$file")"
  title="$(post_title "$file")"
  [[ -z "$title" ]] && title="$source_url"

  if should_syndicate_post "$file"; then
    syndicate_post "$source_url"
  else
    echo "Skipping mastodon/bluesky: $source_url"
  fi

  if has_rss_class "$file"; then
    syndicate_to_rss_chat "$source_url" "$title" || exit_code=1
  else
    echo "Skipping rss.chat: $source_url"
  fi
done

exit "$exit_code"
