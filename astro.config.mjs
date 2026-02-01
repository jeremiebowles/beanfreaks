import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import sitemap from "@astrojs/sitemap";

// GitHub Pages project site (repo name is also the sub-path)
export default defineConfig({
  site: "https://jeremiebowles.github.io",
  base: "/beanfreaks",

  // Make GitHub Pages life easier: no leading-underscore asset folder,
  // and always emit a real stylesheet link we can verify in View Source.
  build: {
    assets: "assets",
    inlineStylesheets: "never",
  },

  trailingSlash: "always",

  integrations: [tailwind(), sitemap()],
});
