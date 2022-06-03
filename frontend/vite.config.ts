import vue from "@vitejs/plugin-vue";
import { execSync } from "child_process";
import { fileURLToPath, URL } from "url";
import { defineConfig } from "vite";
import { VitePWA } from "vite-plugin-pwa";
import vuetify from "vite-plugin-vuetify";

const quoteCommand = (command: string) => {
  return JSON.stringify(execSync(command).toString());
};

// https://vitejs.dev/config/
export default defineConfig({
  base: process.env.VITE_BASE || "/",
  define: {
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    __COMMIT__: quoteCommand("git rev-parse HEAD"),
    __BRANCH__: quoteCommand("git rev-parse --abbrev-ref HEAD"),
    __VERSION__: quoteCommand("git describe --tags --dirty --always")
  },
  server: {
    proxy: {
      "^/docs.*$": {
        target: "http://localhost:3001",
        changeOrigin: true,
        rewrite: path => path.replace(/^\/docs/, "/deeplabcut-webui/docs")
      }
    }
  },
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
