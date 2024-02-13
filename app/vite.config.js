import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    VitePWA({ 
      registerType: "autoUpdate",
      includeAssets: ["pwa-192x192.png", "pwa-512x512.png", "pwa-maskable-192x192.png", "pwa-maskable-512x512.png"],
      manifest: {
        "name": "Contests",
        "short_name": "Contests",
        "icons": [
          {
            "src": "/pwa-192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any"
          },
          {
            "src": "/pwa-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any"
          },
          {
            "src": "/pwa-maskable-192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "maskable"
          },
          {
            "src": "/pwa-maskable-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable"
          }
        ],
        "start_url": "/",
        "display": "standalone",
        "background_color": "#FFFFFF",
        "theme_color": "#FFFFFF",
        "description": "Ongoing and Upcoming Contests on AtCoder, CodeChef, Codeforces, GeeksforGeeks and LeetCode"
      }
    })
  ],
  base: './'
})
