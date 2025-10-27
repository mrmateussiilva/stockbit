// Configuração do Vite para desenvolvimento com Docker
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: true,
    },
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'lucide-react', 'recharts'],
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})