"""
Fetch all product image URLs from Viridian's Shopify JSON API.
Updates viridian.json: replaces single `image` field with `images` array.
"""
import json
import time
import urllib.request

DATA_PATH = 'src/data/viridian.json'
BASE_URL  = 'https://www.viridian-nutrition.com/products/{handle}.json'

with open(DATA_PATH) as f:
    data = json.load(f)

for slug, product in data.items():
    handle = product['handle']
    url = BASE_URL.format(handle=handle)
    print(f'Fetching {handle} ...', end=' ', flush=True)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read())
        images = [img['src'].split('?')[0] for img in payload['product']['images']]
        print(f'{len(images)} image(s)')
    except Exception as e:
        print(f'ERROR: {e}')
        # Keep existing single image as fallback
        images = [product['image'].split('?')[0]]

    product['images'] = images
    # Remove old single-image field
    product.pop('image', None)
    time.sleep(0.4)

with open(DATA_PATH, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('\nDone. viridian.json updated.')
