<script setup lang="ts">
import SettingsMenu from "@/components/SettingsMenu.vue";
import SnackbarPWA from "@/components/SnackbarPWA.vue";
import SystemBar from "@/components/SystemBar.vue";
import VersionDialog from "@/components/VersionDialog.vue";
import { useFrames, useStore } from "@/stores";
import { clearUrlCache } from "@/utils";
import {
  usePreferredColorScheme,
  useStorage,
  type BasicColorSchema
} from "@vueuse/core";
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const store = useStore();
const frames = useFrames();
const showProject = computed(() => !store.project || !store.cVideo);
const showSettings = ref(false);

// ensure all pages except project view are unmounted when switching or closing a project
const keepAliveExclusion = computed(() =>
  store.project ? ["ProjectView"] : undefined
);
const keepAliveInclusion = computed(() =>
  store.project ? undefined : ["ProjectView"]
);

// compute which theme to use
const themeMode = useStorage<BasicColorSchema>("theme", "auto");
const systemTheme = usePreferredColorScheme();
const theme = computed(() =>
  themeMode.value == "auto" ? systemTheme.value : themeMode.value
);

// handle tracking active tab
const route = useRoute();
const router = useRouter();
const tab = ref("");

const items = computed(() =>
  showProject.value ? ["project"] : ["project", "extract", "label"]
);

// redirect to project selection screen when no project is selected
watch(
  [() => store.project, () => store.cVideo],
  ([newProject, newVideo]) => {
    if (!newProject || !newVideo) {
      router.push({ name: "project" });
    }
  },
  { immediate: true }
);

// track video changes
watch(() => store.video, clearUrlCache);

// bind route to active tab
watch(
  route,
  () => {
    if (route && route.name) {
      tab.value = route.name.toString();
      frames.handleRouteChange(route.name);
    }
  },
  { immediate: true }
);

// handle opening relevant documentation page
const getDocsPage = () => {
  switch (route.name) {
    case "project":
      if (store.project) {
        return "/guide/video/";
      }
      return "/guide/project/";
    case "extract":
      return "/guide/extract/";
    case "label":
      return "/guide/label/";
    default:
      return "";
  }
};

const openDocs = () => {
  window.location.assign(import.meta.env.BASE_URL + "docs" + getDocsPage());
};
</script>

<template>
  <v-app :theme="theme">
    <SettingsMenu v-model="showSettings" v-model:theme="themeMode" />
    <SnackbarPWA />
    <SystemBar />

    <v-app-bar color="primary" density="compact" class="position-relative" flat>
      <template v-slot:prepend>
        <v-tabs v-model="tab">
          <v-tab
            v-for="item in items"
            :key="item"
            :value="item"
            :to="'/' + item"
          >
            {{ item }}
          </v-tab>
        </v-tabs>
      </template>

      <v-spacer />

      <v-btn @click="openDocs" icon>
        <v-icon>mdi-help-circle</v-icon>
        <v-tooltip activator="parent" anchor="bottom">Help</v-tooltip>
      </v-btn>
      <VersionDialog />
      <v-btn class="mr-n3" @click.stop="showSettings = true" icon>
        <v-icon>mdi-cog</v-icon>
        <v-tooltip activator="parent" anchor="bottom" class="settings">
          Settings
        </v-tooltip>
      </v-btn>
    </v-app-bar>

    <v-main class="pa-0">
      <router-view v-slot="{ Component }">
        <transition>
          <keep-alive
            :exclude="keepAliveExclusion"
            :include="keepAliveInclusion"
          >
            <component :is="Component" />
          </keep-alive>
        </transition>
      </router-view>
    </v-main>
  </v-app>
</template>

<style>
html {
  overflow-y: auto !important;
}
.v-table--fixed-header th {
  z-index: 1;
}
div.v-tooltip.settings > div {
  transform: translate(-12px);
}
</style>
