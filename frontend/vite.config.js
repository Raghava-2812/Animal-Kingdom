/**
 * Vite Configuration for Animal Kingdom Knowledge Graph Frontend.
 *
 * Configures:
 * - React plugin for JSX compilation and Fast Refresh.
 * - Tailwind CSS Vite integration plugin.
 * - Development server listening on port 5173.
 * - API reverse proxy routing `/api` requests to the FastAPI backend (http://localhost:8000).
 */

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    port: 5173,
    // Development proxy to avoid CORS friction when running frontend and backend locally
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
