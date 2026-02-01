import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
export default defineConfig({
  site: "https://jeremiebowles.github.io",
  base: "/beanfreaks",
  output: "static",
  trailingSlash: "always",
  build: { assets: "assets" },
  integrations: [sitemap()],
});
