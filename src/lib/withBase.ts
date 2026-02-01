/**
 * Prefix a path with Astro's configured BASE_URL.
 *
 * Works for GitHub Pages project sites (e.g. /beanfreaks/) and normal root sites (/).
 *
 * Usage: withBase('stores/') -> '/beanfreaks/stores/'
 */
export function withBase(path: string = ""): string {
  const baseRaw = (import.meta as any).env?.BASE_URL ?? "/";
  const base = baseRaw.endsWith("/") ? baseRaw : `${baseRaw}/`;
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${base}${clean}`;
}
