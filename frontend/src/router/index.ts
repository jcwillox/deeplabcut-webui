import { createRouter, createWebHistory } from "vue-router";
import AboutView from "../views/AboutView.vue";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView
    },
    {
      path: "/extract",
      name: "extract",
      component: HomeView
    },
    {
      path: "/label",
      name: "label",
      component: AboutView
    },
    {
      path: "/analyse",
      name: "analyse",
      component: AboutView
    }
  ]
});

export default router;
