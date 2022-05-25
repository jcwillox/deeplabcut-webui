import vue from "@vitejs/plugin-vue";
import vuetify from "@vuetify/vite-plugin";
import { fileURLToPath, URL } from "url";
import { defineConfig } from "vite";
import { VitePWA } from "vite-plugin-pwa";

// https://vitejs.dev/config/
export default defineConfig({
  base: process.env.VITE_BASE || "/",
  plugins: [
    vue({
      reactivityTransform: true
    }),
    vuetify(),
    VitePWA({
      workbox: {
        navigateFallbackDenylist: [RegExp("^.*\\/docs.*$")]
      },
      manifest: {
        name: "DeepLabCut WebUI",
        short_name: "DLC WebUI",
        icons: [
          {
            src: "icon.svg",
            type: "image/svg+xml",
            sizes: "any"
          },
          {
            src: "icon-192.png",
            type: "image/png",
            sizes: "192x192"
          },
          {
            src: "icon-512.png",
            type: "image/png",
            sizes: "512x512"
          }
        ]
      }
    })
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  }
});
