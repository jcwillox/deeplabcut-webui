import { createRouter, createWebHistory } from "vue-router";
import AboutView from "@/views/AboutView.vue";
import ExtractView from "@/views/ExtractView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      redirect: () => {
        return { name: "extract" };
      }
    },
    {
      path: "/extract",
      name: "extract",
      component: ExtractView
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
