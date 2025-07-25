import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'bg-main': '#F8F7FA',         // Lavanta Sisi (Yeni)
        'card-bg': '#FFFFFF',         // Saf Beyaz
        'text-main': '#374151',       // Koyu Kurşun (Okunabilirlik için)
        'text-secondary': '#6B7280',  // Gri
        'primary': '#957DAD',         // Lavanta Moru
        'primary-hover': '#806B9A',   // Lavanta Moru (Koyu Ton)
        'border-color': '#E0BBE4',    // Thistle
        'accent-violet': '#D291BC',   // Pastel Menekşe
        'accent-pink': '#FEC8D8',     // Pamuk Şekeri
      },
    },
  },
  plugins: [],
}
export default config 