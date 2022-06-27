import { useStore } from "@/stores";
import ExtractView from "@/views/ExtractView.vue";
import LabelView from "@/views/LabelView.vue";
import ProjectView from "@/views/ProjectView.vue";
import { createRouter, createWebHistory } from "vue-router";

const hasProjectVideo = () => {
  const store = useStore();
  if (!(store.project && store.cVideo)) {
    return false;
  }
};

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
      component: ExtractView,
      beforeEnter: hasProjectVideo
    },
    {
      path: "/label",
      name: "label",
      component: LabelView,
      beforeEnter: hasProjectVideo
    }
  ]
});

router.beforeEach(() => {
  // forcefully hide tooltip before navigating due to vuetify bug
  const el = document.querySelector<HTMLElement>(
    ".v-tooltip.v-overlay--active > .v-overlay__content"
  );
  if (el) {
    el.style.display = "none";
  }
});

export default router;
