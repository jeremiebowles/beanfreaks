/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{astro,html,js,jsx,ts,tsx,md,mdx}",
    "./dist/**/*.html"
  ],
  theme: {
    extend: {
      colors: {
        cream: "rgb(var(--bf-cream) / <alpha-value>)",
        ink: "rgb(var(--bf-ink) / <alpha-value>)",
        leaf: "rgb(var(--bf-leaf) / <alpha-value>)",
        moss: "rgb(var(--bf-moss) / <alpha-value>)",
        oat: "rgb(var(--bf-oat) / <alpha-value>)",
        clay: "rgb(var(--bf-clay) / <alpha-value>)",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        serif: ["Fraunces", "ui-serif", "Georgia", "serif"],
      },
      boxShadow: {
        soft: "0 10px 30px rgba(15, 23, 42, 0.08)",
      },
    },
  },
  plugins: [],
};
