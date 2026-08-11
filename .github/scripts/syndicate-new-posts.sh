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

textlog_api_url="${TEXTLOG_API_URL:-https://textlog.cc/api/v1}"
textlog_api_url="${textlog_api_url%/}"
textlog_token="${TEXTLOG_TOKEN:-}"

# Bridgy-publish targets: front-matter token -> brid.gy publish path
bridgy_targets=(mastodon bluesky)

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

# Extracts the raw block for a given front-matter key: the key's own
# line plus any following indented "- item" lines (YAML block-style
# array). Stops at the next top-level key or the closing "---".
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

# True if front-matter key (scalar, inline array, or YAML block array)
# contains `value` as a whole word, case-insensitive.
front_matter_list_contains() {
  local key="$1"
  local value="$2"
  local file="$3"
  local block
  block="$(front_matter_block "$key" "$file")"
  [[ -z "$block" ]] && return 1
  block="$(printf '%s\n' "$block" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' ' ')"
  [[ " ${block} " == *" ${value,,} "* ]]
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

syndicate_to_bridgy() {
  local source_url="$1"
  local target="$2"
  local target_url
  local status_code

  target_url="${bridgy_publish_base}/${target}"
  status_code=$(curl -sS -o /tmp/bridgy_publish_response -w "%{http_code}" \
    --data-urlencode "source=${source_url}" \
    --data-urlencode "target=${target_url}" \
    "${bridgy_webmention_url}")
  echo "  ${target}: ${status_code}"
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

syndicate_to_textlog() {
  local source_url="$1"
  local title="$2"
  local body
  local jsontext
  local status_code

  if [[ -z "$textlog_token" ]]; then
    echo "  textlog: skipped (secret not set)"
    return 0
  fi

  body="${title}
${source_url}"
  jsontext="{\"body\":\"$(json_escape "$body")\"}"

  status_code=$(curl -sS -X POST -o /tmp/textlog_response -w "%{http_code}" \
    -H "authorization: Bearer ${textlog_token}" \
    -H 'content-type: application/json' \
    -d "${jsontext}" \
    "${textlog_api_url}/posts")

  if [[ "$status_code" == "200" || "$status_code" == "201" ]]; then
    echo "  textlog: $status_code"
  else
    echo "  textlog: FAILED $status_code - $(cat /tmp/textlog_response)"
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

  echo "Post: $source_url"

  for target in "${bridgy_targets[@]}"; do
    if front_matter_list_contains syndicate "$target" "$file"; then
      syndicate_to_bridgy "$source_url" "$target"
    else
      echo "  ${target}: skipped"
    fi
  done

  if front_matter_list_contains syndicate rss "$file"; then
    syndicate_to_rss_chat "$source_url" "$title" || exit_code=1
  else
    echo "  rss.chat: skipped"
  fi

  if front_matter_list_contains syndicate textlog "$file"; then
    syndicate_to_textlog "$source_url" "$title" || exit_code=1
  else
    echo "  textlog: skipped"
  fi
done

exit "$exit_code"
