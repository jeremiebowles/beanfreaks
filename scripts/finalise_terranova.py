"""
Finalise terranova.json:
  1. Add 'from' prices from sales CSV data
  2. Download product images, convert to WebP, save locally
  3. Update images field to local paths
"""

import json, pathlib, time, re, urllib.request
from io import BytesIO
from PIL import Image

DATA_PATH  = pathlib.Path('src/data/terranova.json')
OUTPUT_DIR = pathlib.Path('public/img/terranova')
WIDTH      = 600
QUALITY    = 80

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Lowest 'from' price per slug, derived from sales CSV analysis
FROM_PRICES = {
    'easy-iron-20mg':               '6.51',
    'vitamin-d3-k2':               '18.74',
    'living-multivitamin-man':     '19.38',
    'magnesium-100mg':             '14.77',
    'b-complex-vitamin-c':         '12.38',
    'full-spectrum-multivitamin':  '18.26',
    'probiotic-complex':           '12.78',
    'zinc-15mg':                    '9.30',
    'digestive-enzymes-microflora':'19.38',
    'life-drink':                  '23.60',
    'vitamin-d3':                   '9.95',
    'vitamin-c-250mg':             '14.22',
    'digestive-enzyme-complex':    '15.00',
    'vitamin-b12-500mcg':          '12.71',
    'living-multivitamin-sport':   '17.58',
    'quercetin-nettle':            '21.62',
    'beauty-complex':              '15.74',
    'living-multinutrient':        '18.87',
    'prenatal-multivitamin':       '14.84',
    'glucosamine-boswellia-msm':   '11.88',
}

with open(DATA_PATH) as f:
    data = json.load(f)

for slug, product in data.items():
    print(f'\n{slug}')

    # Add price
    product['price'] = FROM_PRICES.get(slug, '')

    # Download and convert images
    remote_urls = product.get('images', [])
    local_paths = []

    for idx, url in enumerate(remote_urls):
        out_path = OUTPUT_DIR / f'{slug}-{idx}.webp'
        print(f'  [{idx}] {url.split("/")[-1]} → {out_path.name}', end=' ', flush=True)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read()
            img = Image.open(BytesIO(raw)).convert('RGB')
            orig_w, orig_h = img.size
            scale = WIDTH / orig_w
            new_h = round(orig_h * scale)
            img = img.resize((WIDTH, new_h), Image.LANCZOS)
            img.save(out_path, 'WEBP', quality=QUALITY, method=6)
            size_kb = out_path.stat().st_size // 1024
            print(f'({orig_w}×{orig_h} → {WIDTH}×{new_h}, {size_kb}KB)')
            local_paths.append(f'/img/terranova/{out_path.name}')
            time.sleep(0.3)
        except Exception as e:
            print(f'ERROR: {e}')
            local_paths.append(url)

    product['images'] = local_paths

with open(DATA_PATH, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'\nDone. {DATA_PATH} updated.')
