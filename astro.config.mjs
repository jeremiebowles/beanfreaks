import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://jeremiebowles.github.io",
  base: "/beanfreaks",

  // avoid the default "_astro" folder entirely
  build: { assets: "assets" },

  integrations: [tailwind(), sitemap()],
});

