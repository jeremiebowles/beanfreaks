# Site Overview

## Purpose
Beanfreaks is a static Astro site for a local health‑food retailer. It is optimized for fast page loads, simple content updates, and deterministic styling via Tailwind.

## Tech Stack
- Astro (static output)
- Tailwind CSS (compiled to `dist/tw.css`)
- Minimal JS (only where needed)

## Build & Deploy
- Build command: `npm run build`
- Output directory: `dist/`
- CSS output: `dist/tw.css`

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
