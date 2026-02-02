/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx,md,mdx}", "./dist/**/*.html"],
  theme: {
    extend: {
      colors: {
        cream: "rgb(var(--cream) / <alpha-value>)",
        paper: "rgb(var(--paper) / <alpha-value>)",
        ink: "rgb(var(--ink) / <alpha-value>)",
        muted: "rgb(var(--muted) / <alpha-value>)",
        leaf: "rgb(var(--leaf) / <alpha-value>)",
        moss: "rgb(var(--moss) / <alpha-value>)",
        clay: "rgb(var(--clay) / <alpha-value>)",
        turmeric: "rgb(var(--turmeric) / <alpha-value>)",
        berry: "rgb(var(--berry) / <alpha-value>)"
      }
    }
  },
  plugins: [require('@tailwindcss/typography')]
};
