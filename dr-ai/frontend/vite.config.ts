import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: 'rj8vq174-5173.uks1.devtunnels.ms',
    port: 5173
  },
  optimizeDeps: {
    include: ['@tailwindcss/forms']
  }
})
