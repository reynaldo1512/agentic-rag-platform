/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0F1115",
        surface: "#161922",
        accent: "#5EE6B0",
        danger: "#FF6B6B",
        muted: "#7B8294",
      },
      fontFamily: {
        display: ["'JetBrains Mono'", "monospace"],
        body: ["'Inter'", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
