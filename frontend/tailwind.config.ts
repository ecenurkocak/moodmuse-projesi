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
        'primary': '#52277b',         // Yeni Ana Renk (Koyu Mor)
        'primary-hover': '#422063',   // Yeni Ana Rengin Koyu Tonu
        'border-color': '#E0BBE4',    // Thistle
        'accent-violet': '#D291BC',   // Pastel Menekşe
        'accent-pink': '#FEC8D8',     // Pamuk Şekeri
      },
    },
  },
  plugins: [],
}
export default config
