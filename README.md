# Beanfreaks (Astro + deterministic Tailwind)

Project Pages under `/beanfreaks/` with deterministic CSS output:

- Build output: `dist/`
- CSS output: `dist/tw.css`
- Layout links CSS via: `import.meta.env.BASE_URL + "tw.css"`

## Build
```bash
npm ci
npm run build
```

## Local preview with the same base path
```bash
rm -rf dist/beanfreaks
mkdir -p dist/beanfreaks
rsync -a --delete --exclude 'beanfreaks/' dist/ dist/beanfreaks/
python3 -m http.server -d dist 4321
# open http://localhost:4321/beanfreaks/
```
