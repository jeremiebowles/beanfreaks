# Beanfreaks (Astro → GitHub Pages Project Pages)

This repack is built to be boringly reliable:
- **Project Pages base path**: `/beanfreaks/`
- **Deterministic Tailwind build**: outputs a single `dist/tw.css`
- **No Astro Tailwind integration**
- **Canonical layout**: `src/layouts/base.astro` only

## Install

```bash
npm ci
```

## Build

```bash
npm run build
```

This runs:
1) `astro build`
2) `tailwindcss` against the built `dist/**/*.html` to produce `dist/tw.css`
3) writes `dist/.nojekyll`

## Local preview with base path

```bash
npm run build
rm -rf dist/beanfreaks
mkdir -p dist/beanfreaks
rsync -a --delete --exclude 'beanfreaks/' dist/ dist/beanfreaks/
python3 -m http.server -d dist 4321
# open http://localhost:4321/beanfreaks/
```

## Images

`public/img/logo.png` is included.

The other required images are included as tiny placeholders so the site builds. **Overwrite them** with your real photos:

- hero.jpg
- store-roath.jpg
- store-canton.jpg
- store-royal.jpg
- product-aloe.jpg
- product-turmeric.jpg
- product-chickpeas.jpg
- product-vitamins.jpg

## GitHub Pages workflow

See `.github/workflows/pages.yml`.

In the repo settings: **Pages → Build and deployment → GitHub Actions**.
