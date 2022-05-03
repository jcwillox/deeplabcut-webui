import AboutView from "@/views/AboutView.vue";
import ExtractView from "@/views/ExtractView.vue";
import LabelView from "@/views/LabelView.vue";
import ProjectView from "@/views/ProjectView.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "project"
    },
    {
      path: "/project",
      name: "project",
      component: ProjectView
    },
    {
      path: "/extract",
      name: "extract",
      component: ExtractView
    },
    {
      path: "/label",
      name: "label",
      component: LabelView
    },
    {
      path: "/analyse",
      name: "analyse",
      component: AboutView
    }
  ]
});

export default router;
