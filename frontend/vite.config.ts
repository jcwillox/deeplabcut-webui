import vue from "@vitejs/plugin-vue";
import vuetify from "@vuetify/vite-plugin";
import { fileURLToPath, URL } from "url";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  base: process.env.VITE_BASE || "/",
  plugins: [
    vue({
      reactivityTransform: true
    }),
    vuetify()
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  }
});
