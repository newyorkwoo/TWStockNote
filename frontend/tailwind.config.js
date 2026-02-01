/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'nasdaq-blue': '#1E40AF',
        'nasdaq-green': '#10B981',
        'nasdaq-red': '#EF4444',
      }
    },
  },
  plugins: [],
}
