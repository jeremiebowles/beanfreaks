/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}",
    "./dist/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        bf: {
          cream: "#F6F2E7",
          oat: "#EFE7D3",
          ink: "#1D1C18",
          leaf: "#2F6A4F",
          moss: "#3E7E5C",
          soil: "#4B3F35",
          sun: "#CAA253",
          berry: "#7F3B46",
        },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        serif: ["Fraunces", "ui-serif", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};
