"""
Download Viridian product images, convert to WebP, update viridian.json with local paths.

Filtering rules (applied after always keeping index 0):
  Skip filenames containing (case-insensitive):
    - Amazon_Universal_Carousel
    - Lifestyle / _lifestyle
    - carousel_   (square marketing carousel crops)
    - Festive_

Cap at 3 images per product.
Output: public/img/viridian/{slug}-{index}.webp at 600px wide.
"""
import json
import os
import re
import time
import urllib.request
from pathlib import Path
from PIL import Image

DATA_PATH   = Path('src/data/viridian.json')
OUTPUT_DIR  = Path('public/img/viridian')
WIDTH       = 600
QUALITY     = 80
MAX_IMAGES  = 3

SKIP_PATTERNS = re.compile(
    r'(amazon_universal_carousel|_lifestyle|lifestyle[-_]|carousel_|festive_)',
    re.IGNORECASE,
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(DATA_PATH) as f:
    data = json.load(f)

for slug, product in data.items():
    raw_urls = product.get('images', [])
    if not raw_urls:
        print(f'{slug}: no images, skipping')
        continue

    # Always keep index 0; filter the rest
    kept_urls = [raw_urls[0]]
    for url in raw_urls[1:]:
        fname = url.split('/')[-1]
        if not SKIP_PATTERNS.search(fname):
            kept_urls.append(url)
        if len(kept_urls) >= MAX_IMAGES:
            break

    local_paths = []
    for idx, url in enumerate(kept_urls):
        out_path = OUTPUT_DIR / f'{slug}-{idx}.webp'
        print(f'  [{idx}] {url.split("/")[-1]} → {out_path.name}', end=' ')

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read()

            from io import BytesIO
            img = Image.open(BytesIO(raw)).convert('RGB')

            # Resize to WIDTH, preserving aspect ratio
            orig_w, orig_h = img.size
            scale = WIDTH / orig_w
            new_h = round(orig_h * scale)
            img = img.resize((WIDTH, new_h), Image.LANCZOS)
            img.save(out_path, 'WEBP', quality=QUALITY, method=6)

            size_kb = out_path.stat().st_size // 1024
            print(f'({orig_w}×{orig_h} → {WIDTH}×{new_h}, {size_kb}KB)')
            local_paths.append(f'/img/viridian/{out_path.name}')
            time.sleep(0.3)

        except Exception as e:
            print(f'ERROR: {e}')
            # Fall back to keeping the remote URL if download fails
            local_paths.append(url)

    product['images'] = local_paths
    print(f'{slug}: {len(local_paths)} image(s) saved')

with open(DATA_PATH, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('\nDone. viridian.json updated with local paths.')
