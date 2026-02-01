import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://jeremiebowles.github.io",
  base: "/beanfreaks",
  output: "static",
  trailingSlash: "always",
  build: { assets: "assets" },
});
