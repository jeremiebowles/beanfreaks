"""
Scrape Terra Nova product pages (WooCommerce) for the top 20 products.
Outputs src/data/terranova.json in the same shape as viridian.json.

Shape per product:
  title, description, price (string), images (list of URLs), handle (slug)
"""

import json, re, time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

OUT_PATH = Path('src/data/terranova.json')

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Beanfreaks/1.0)'}

# Top 20 products: our clean slug → Terra Nova product URL(s)
# Where a product comes in multiple strengths, list all URLs — we merge them.
PRODUCTS = {
    'easy-iron-20mg': {
        'urls': ['https://www.terranovahealth.com/product/terranova-easy-iron-20mg-complex/'],
    },
    'vitamin-d3-k2': {
        'urls': [
            'https://www.terranovahealth.com/product/terranova-vitamin-d3-1000iu-k2-as-menaq7-50µg-complex/',
            'https://www.terranovahealth.com/product/terranova-vitamin-d3-2000iu-k2-as-menaq7-100µg-complex/',
        ],
    },
    'living-multivitamin-man': {
        'urls': ['https://www.terranovahealth.com/product/terranova-living-multivitamin-man/'],
    },
    'magnesium-100mg': {
        'urls': ['https://www.terranovahealth.com/product/terranova-magnesium-100mg-complex/'],
    },
    'b-complex-vitamin-c': {
        'urls': ['https://www.terranovahealth.com/product/terranovab-complex-with-vitamin-c/'],
    },
    'full-spectrum-multivitamin': {
        'urls': ['https://www.terranovahealth.com/product/terranovafull-spectrum-multivitamin/'],
    },
    'probiotic-complex': {
        'urls': ['https://www.terranovahealth.com/product/terranova-microflora-complex-with-fos-and-more/'],
    },
    'zinc-15mg': {
        'urls': ['https://www.terranovahealth.com/product/terranova-zinc-15mg-complex/'],
    },
    'digestive-enzymes-microflora': {
        'urls': ['https://www.terranovahealth.com/product/terranova-digestive-enzymes-with-microflora/'],
    },
    'life-drink': {
        'urls': ['https://www.terranovahealth.com/product/terranovalife-drink-227g/'],
    },
    'vitamin-d3': {
        'urls': [
            'https://www.terranovahealth.com/product/terranova-vitamin-d-1000iu-25µg-complex/',
            'https://www.terranovahealth.com/product/terranova-vitamin-d-2000iu-50µg-complex/',
        ],
    },
    'vitamin-c-250mg': {
        'urls': ['https://www.terranovahealth.com/product/terranova-vitamin-c-250mg-multi-ascorbate-complex-non-acidic/'],
    },
    'digestive-enzyme-complex': {
        'urls': ['https://www.terranovahealth.com/product/terranovadigestive-enzyme-complex/'],
    },
    'vitamin-b12-500mcg': {
        'urls': ['https://www.terranovahealth.com/product/terranova-vitamin-b12-500ug-complex-methylcobalamin/'],
    },
    'living-multivitamin-sport': {
        'urls': ['https://www.terranovahealth.com/product/terranova-living-multivitamin-sport/'],
    },
    'quercetin-nettle': {
        'urls': ['https://www.terranovahealth.com/product/terranova-quercetin-nettle-complex/'],
    },
    'beauty-complex': {
        'urls': ['https://www.terranovahealth.com/product/terranova-beauty-complex-skin-hair-nails/'],
    },
    'living-multinutrient': {
        'urls': ['https://www.terranovahealth.com/product/terranova-living-multinutrient/'],
    },
    'prenatal-multivitamin': {
        'urls': ['https://www.terranovahealth.com/product/terranova-prenatal-multivitamin/'],
    },
    'glucosamine-boswellia-msm': {
        'urls': ['https://www.terranovahealth.com/product/terranova-glucosamine-boswellia-msm-complex/'],
    },
}


def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


def scrape_product(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Title
    title_el = soup.select_one('h1.product_title') or soup.select_one('h1')
    title = clean_text(title_el.get_text()) if title_el else ''

    # Description — WooCommerce long description
    desc_el = (
        soup.select_one('div.woocommerce-product-details__short-description') or
        soup.select_one('div#tab-description') or
        soup.select_one('div.entry-content') or
        soup.select_one('div.product-description')
    )
    description = clean_text(desc_el.get_text(separator=' ')) if desc_el else ''

    # Price
    price_el = soup.select_one('p.price .woocommerce-Price-amount bdi')
    if not price_el:
        price_el = soup.select_one('.woocommerce-Price-amount bdi')
    price = ''
    if price_el:
        price_text = price_el.get_text()
        price_match = re.search(r'[\d.]+', price_text.replace(',', ''))
        price = price_match.group() if price_match else ''

    # Images — WooCommerce gallery
    images = []
    for img in soup.select('div.woocommerce-product-gallery figure img'):
        src = img.get('data-large_image') or img.get('src', '')
        if src and 'woocommerce-placeholder' not in src and src not in images:
            images.append(src)
    # Fallback: og:image
    if not images:
        og = soup.find('meta', property='og:image')
        if og and og.get('content'):
            images.append(og['content'])

    return title, description, price, images


data = {}

for slug, cfg in PRODUCTS.items():
    urls = cfg['urls']
    print(f'\n{slug}')

    all_titles = []
    all_descs = []
    all_prices = []
    all_images = []

    for url in urls:
        print(f'  Fetching {url.split("/product/")[1].rstrip("/")} ...', end=' ', flush=True)
        try:
            title, desc, price, images = scrape_product(url)
            all_titles.append(title)
            all_descs.append(desc)
            if price:
                all_prices.append(float(price))
            all_images.extend(img for img in images if img not in all_images)
            print(f'OK — "{title[:50]}" £{price} {len(images)} img(s)')
        except Exception as e:
            print(f'ERROR: {e}')
        time.sleep(0.5)

    # Use first successful title and desc; note all strengths in title if multiple
    title = all_titles[0] if all_titles else slug
    description = all_descs[0] if all_descs else ''

    # If multiple strengths, note them in title
    if len(all_titles) > 1:
        # Strip "TERRANOVA " prefix for cleanliness
        strengths = []
        for t in all_titles:
            m = re.search(r'(\d+\s*(?:iu|µg|ug|mg|mcg))', t, re.IGNORECASE)
            if m:
                strengths.append(m.group(1))
        if strengths:
            # Clean base title
            base = re.sub(r'\s*\d+\s*(?:iu|µg|ug|mg|mcg)[^\s]*', '', title, flags=re.IGNORECASE).strip()
            title = f'{base} ({" & ".join(strengths)})'

    # Strip "TERRANOVA" brand prefix from title
    title = re.sub(r'^TERRANOVA\s+', '', title, flags=re.IGNORECASE).strip()

    price_str = f'{min(all_prices):.2f}' if all_prices else ''

    data[slug] = {
        'title': title,
        'description': description,
        'price': price_str,
        'images': all_images,
        'handle': slug,
    }

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'\nDone — {len(data)} products written to {OUT_PATH}')
