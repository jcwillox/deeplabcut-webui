// Styles
import "@mdi/font/css/materialdesignicons.css";
// Vuetify
import { createVuetify } from "vuetify";
import "vuetify/styles";
import { loadFonts } from "./webfontloader";

loadFonts();

export default createVuetify({
  theme: {
    variations: {
      colors: ["primary", "secondary"],
      lighten: 1,
      darken: 2
    },
    themes: {
      light: {
        colors: {
          primary: "#2196F3",
          secondary: "#E91E63"
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: "#212121",
          secondary: "#E91E63"
        }
      }
    }
  }
});
