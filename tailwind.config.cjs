/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx,md,mdx}", "./dist/**/*.html"],
  theme: { extend: {} },
  plugins: [require("@tailwindcss/typography")],
};
