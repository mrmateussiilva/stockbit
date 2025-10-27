// Configuração do Vite para desenvolvimento com Docker
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Base path para assets - usar absoluto em produção
  base: '/',
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
    sourcemap: false, // Desabilitar em produção para build mais rápido
    cssCodeSplit: true, // Separar CSS em arquivos
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log em produção
      },
    },
    rollupOptions: {
      output: {
        // Organizar os arquivos de output
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        // Garantir que todos os assets sejam servidos com paths absolutos
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        },
      },
    },
    // Garantir que o CSS seja gerado corretamente
    cssMinify: true,
  },
})