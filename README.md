# Beanfreaks Astro starter (deterministic Tailwind)

## What you get
- Astro static site configured for GitHub Pages Project Pages (`/beanfreaks/`)
- Deterministic CSS: always builds a single `dist/tw.css` (no hashed CSS)
- A cosy, clean health-food-shop design system (cream/ink/leaf/turmeric)
- Starter pages: Home, Roath, Canton, Royal Arcade, Contact, Posts
- Image credits: see CREDITS.md

## Local dev
```bash
npm install
npm run dev
```

## CI / production build
The GitHub Actions workflow uses `npm install` while you're iterating.

If you want fully deterministic installs later:
1) Run `npm install` once locally to generate `package-lock.json`.
2) Commit it.
3) Change the workflow from `npm install` to `npm ci`.

Build steps:
```bash
npm install
npm run build
```

## Replace placeholder images
Drop real JPGs into `public/img/` keeping the same filenames.
