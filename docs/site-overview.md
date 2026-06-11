# Site Overview

## Purpose
Beanfreaks is a static Astro site for a local health‑food retailer. It is optimized for fast page loads, simple content updates, and deterministic styling via Tailwind.

## Tech Stack
- Astro (static output)
- Tailwind CSS (processed via PostCSS/Vite, inlined into each HTML page)
- Minimal JS (only where needed)

## Build & Deploy
- Build command: `npm run build`
- Output directory: `dist/`
- CSS is inlined into every HTML page via `build.inlineStylesheets: 'always'` — there is no separate `tw.css` file. This eliminates the render-blocking stylesheet request and reduces LCP element render delay significantly.

## Key Content Areas
- Home: `src/pages/index.astro`
  - Featured products (“In‑store picks”)
- History: `src/pages/history/index.astro`
  - Image timeline + captions
- Stores:
  - Roath: `src/pages/roath/index.astro`
  - Canton: `src/pages/canton/index.astro`
  - Royal Arcade: `src/pages/royal/index.astro`
- Contact: `src/pages/contact/index.astro`
- Posts (blog):
  - Index: `src/pages/posts/index.astro`
  - Entry: `src/pages/posts/[slug].astro`

## Layouts & Components
- Base layout: `src/layouts/base.astro`
  - Handles title, description, canonical, Open Graph, Twitter cards
- Navigation: `src/components/Nav.astro`
  - Responsive nav with special handling for small landscape
- Footer: `src/components/Footer.astro`
- Section header: `src/components/SectionHeader.astro`

## Assets
- Public assets live in `public/`
- History images: `public/img/history/`
- Large images must be < 25 MiB for Cloudflare Pages.

## Image Guidelines
All images should be WebP, quality 80, method 6 (Pillow defaults). Size to **display dimensions × 2 (for retina), then no larger**. The most common mistake is encoding full portrait-height images for containers that use `object-cover` with a short fixed height — those extra pixels are decoded, transferred, and thrown away.

Specific targets for each use case:
- **Hero image** (`h-[320px] sm:h-[420px]`, half-width on lg): max ~840×560 px
- **Feature cards** (`h-28 sm:h-32`, 4-col grid): max ~800×300 px — keep width for retina, crop height hard
- **Product cards** (`h-56`, 3-col grid): max ~700×450 px
- **Blog post heroes** (full-width, various heights): max 1200×800 px as produced by `scripts/download_hero_images.py`
- **Store/history images**: resize to max 1200px on the longest edge before saving

Crop strategy: scale so the image covers the target rectangle (`max(tw/orig_w, th/orig_h)`), then center-crop. This matches what `object-cover` does at runtime and ensures no blank space.

Do not add `srcset` or `<picture>` responsive breakpoints unless a specific image is clearly too large on mobile and too small on desktop — the overhead of maintaining multiple variants is not worth it for this site at its current traffic level.

## SEO
- `Base` includes description, canonical, Open Graph, Twitter
- Store pages include schema.org `HealthFoodStore`
- Posts index and store pages have custom descriptions

## DNS / Hosting Notes
- Site is hosted on Cloudflare Pages
- `www` should CNAME to `beanfreaks.pages.dev`
- Apex should 301 redirect to `https://www.beanfreaks.com`

## Session Notes
- See `docs/session-log.md` for recent changes and current status.
