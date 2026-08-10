/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#0a0a14',
        surface: 'rgba(255, 255, 255, 0.05)',
        primary: {
          DEFAULT: '#8b5cf6',
          glow: 'rgba(139, 92, 246, 0.3)'
        },
        accent: '#06b6d4',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          'from': { boxShadow: '0 0 10px rgba(139, 92, 246, 0.2)' },
          'to': { boxShadow: '0 0 20px rgba(139, 92, 246, 0.6)' },
        }
      }
    },
  },
  plugins: [],
}
