<script setup lang="ts">
import { useStore } from "@/stores/global";
import {
  type BasicColorSchema,
  usePreferredColorScheme,
  useStorage
} from "@vueuse/core";
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import SettingsMenu from "./components/SettingsMenu.vue";
import SystemBar from "./components/SystemBar.vue";

const store = useStore();
const showProject = computed(() => !store.project || !store.video);
const showSettings = ref(false);

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
  showProject.value ? ["project"] : ["extract", "label", "analyse"]
);

watch(
  [() => store.project, () => store.video],
  ([newProject, newVideo]) => {
    if (!newProject || !newVideo) {
      router.push({ name: "project" });
    } else if (newProject && newVideo && route.name == "project") {
      router.push({ name: "extract" });
    }
  },
  { immediate: true }
);

// bind route to active tab
watch(
  route,
  () => {
    if (route.name) {
      tab.value = route.name.toString();
    }
  },
  { immediate: true }
);
</script>

<template>
  <v-app :theme="theme">
    <SettingsMenu v-model="showSettings" v-model:theme="themeMode" />

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

      <template v-slot:append>
        <v-btn icon="mdi-cog" @click.stop="showSettings = true"></v-btn>
      </template>
    </v-app-bar>

    <v-main class="pa-0">
      <router-view v-slot="{ Component }">
        <transition>
          <keep-alive exclude="ProjectView">
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
.v-application {
  min-height: 100vh;
}
.v-table--fixed-header th {
  z-index: 1;
}
</style>
