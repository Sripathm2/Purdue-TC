#!/usr/bin/env bash
# mirror_urls.sh
# Download N home pages (and all required resources) from a list of URLs.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <urls.txt>"
  exit 1
fi

URL_FILE="$1"
if [[ ! -f "$URL_FILE" ]]; then
  echo "Error: file not found: $URL_FILE"
  exit 1
fi

# Ask the user how many URLs to download
read -rp "How many URLs should I download? " N

# Validate N is a positive integer
if ! [[ "$N" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: please enter a positive integer."
  exit 1
fi

# Prepare output directory
OUT_ROOT="mirrors"
mkdir -p "$OUT_ROOT"

# Read first N non-empty, non-comment lines
mapfile -t URLS < <(grep -v '^[[:space:]]*#' "$URL_FILE" | grep -v '^[[:space:]]*$' | head -n "$N")

if [[ ${#URLS[@]} -eq 0 ]]; then
  echo "No URLs found to download."
  exit 0
fi

echo "Will download ${#URLS[@]} URLs into '$OUT_ROOT/'."

# User-Agent to reduce blocks from some sites
UA_STR="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# Loop and fetch each homepage plus all required assets
for url in "${URLS[@]}"; do
  # Normalize whitespace
  url="$(echo "$url" | tr -d '\r' | xargs)"
  [[ -z "$url" ]] && continue

  # Extract host for per-site folder
  host="$(echo "$url" | awk -F/ '{print $3}')"
  [[ -z "$host" ]] && host="unknown_host"

  site_dir="$OUT_ROOT/$host"
  mkdir -p "$site_dir"

  echo "==> Downloading: $url"
  # Notes on flags:
  # --page-requisites    : fetch CSS/JS/images etc. needed to render the page
  # --convert-links      : rewrite links for local offline viewing
  # --adjust-extension   : save .html extensions where appropriate
  # --span-hosts         : allow fetching requisites from CDNs/other hosts
  # --timestamping       : skip unchanged files on reruns
  # --tries/timeout      : be resilient to hiccups
  # --no-verbose         : cleaner logs; remove if you want more detail
  wget \
    --page-requisites \
    --convert-links \
    --adjust-extension \
    --span-hosts \
    --timestamping \
    --timeout=30 \
    --tries=2 \
    --user-agent="$UA_STR" \
    --no-verbose \
    --directory-prefix="$site_dir" \
    "$url" || {
      echo "Warning: failed to mirror $url" >&2
    }
done

mv ./mirrors ./web
mkdir -p ../data
mv ./web ../data/

echo "Done. Open the saved .html files under '$../data/web/<host>/' to view pages offline."
