#!/usr/bin/env bash
# Usage: ./scripts/unsplash.sh "search query" output-filename
# Downloads top Unsplash results for a query, lets you pick one,
# saves to public/img/posts/ as both JPG and WebP.
#
# Requires: curl, ffmpeg, python3
# Reads UNSPLASH_ACCESS_KEY from .env in project root

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found at $ENV_FILE"
  exit 1
fi

source "$ENV_FILE"

if [ -z "$UNSPLASH_ACCESS_KEY" ]; then
  echo "Error: UNSPLASH_ACCESS_KEY not set in .env"
  exit 1
fi

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 \"search query\" output-filename"
  echo "Example: $0 \"hemp seeds\" hemp-seeds"
  exit 1
fi

QUERY="$1"
FILENAME="$2"
OUTPUT_DIR="$PROJECT_ROOT/public/img/posts"
ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")

echo "Searching Unsplash for: $QUERY"
echo ""

RESPONSE=$(curl -s "https://api.unsplash.com/search/photos?query=${ENCODED_QUERY}&per_page=5&orientation=landscape&client_id=${UNSPLASH_ACCESS_KEY}")

python3 << PYEOF
import json, sys

data = json.loads('''$RESPONSE''')
results = data.get('results', [])

if not results:
    print("No results found.")
    sys.exit(1)

for i, photo in enumerate(results):
    desc = photo.get('description') or photo.get('alt_description') or 'No description'
    photographer = photo['user']['name']
    print(f"[{i+1}] {desc[:70]}")
    print(f"     Photo by {photographer} on Unsplash")
    print()
PYEOF

read -p "Pick a number (1-5), or q to quit: " CHOICE

if [ "$CHOICE" = "q" ]; then
  echo "Cancelled."
  exit 0
fi

if ! [[ "$CHOICE" =~ ^[1-5]$ ]]; then
  echo "Invalid choice."
  exit 1
fi

INDEX=$((CHOICE - 1))

DOWNLOAD_URL=$(python3 << PYEOF
import json
data = json.loads('''$RESPONSE''')
results = data.get('results', [])
photo = results[$INDEX]
# Trigger the download endpoint as required by Unsplash API guidelines
print(photo['urls']['regular'])
PYEOF
)

DOWNLOAD_ENDPOINT=$(python3 << PYEOF
import json
data = json.loads('''$RESPONSE''')
results = data.get('results', [])
photo = results[$INDEX]
print(photo['links']['download_location'])
PYEOF
)

PHOTOGRAPHER=$(python3 << PYEOF
import json
data = json.loads('''$RESPONSE''')
results = data.get('results', [])
photo = results[$INDEX]
print(photo['user']['name'])
PYEOF
)

# Trigger download tracking (required by Unsplash guidelines)
curl -s "${DOWNLOAD_ENDPOINT}&client_id=${UNSPLASH_ACCESS_KEY}" > /dev/null

JPG_PATH="$OUTPUT_DIR/${FILENAME}.jpg"
WEBP_PATH="$OUTPUT_DIR/${FILENAME}.webp"

echo "Downloading..."
curl -s "$DOWNLOAD_URL" -o "$JPG_PATH"

echo "Converting to WebP..."
ffmpeg -y -i "$JPG_PATH" -q:v 85 "$WEBP_PATH" 2>/dev/null

echo ""
echo "Saved:"
echo "  $JPG_PATH"
echo "  $WEBP_PATH"
echo ""
echo "Attribution: Photo by $PHOTOGRAPHER on Unsplash"
echo "Image path for post frontmatter: /img/posts/${FILENAME}.webp"
