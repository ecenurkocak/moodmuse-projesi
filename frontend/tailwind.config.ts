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
        'bg-main': '#F8F7FA',
        'card-bg': '#FFFFFF',
        'text-main': '#374151',
        'text-secondary': '#6B7280',
        'primary': '#52277b',
        'primary-hover': '#422063',
        'border-color': '#E0BBE4',
        'accent-violet': '#D291BC',
        'accent-pink': '#FEC8D8',
      },
    },
  },
  plugins: [],
}
export default config
