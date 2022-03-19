<script setup lang="ts">
import {
  usePreferredColorScheme,
  useStorage,
  type BasicColorSchema
} from "@vueuse/core";
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import SettingsMenu from "./components/SettingsMenu.vue";

const showSettings = ref(false);

// compute which theme to use
const themeMode = useStorage<BasicColorSchema>("theme", "auto");
const systemTheme = usePreferredColorScheme();
const theme = computed(() =>
  themeMode.value == "auto" ? systemTheme.value : themeMode.value
);

// handle tracking active tab
const route = useRoute();
const tab = ref(window.location.pathname.substring(1) || "extract");
const items = ["extract", "label", "analyse"];

watch(route, () => {
  if (route.name == "home") {
    tab.value = "extract";
  } else {
    tab.value = route.name as string;
  }
});
</script>

<template>
  <v-app :theme="theme">
    <SettingsMenu v-model="showSettings" v-model:theme="themeMode" />

    <v-system-bar app fixed color="primary-darken-1">
      <v-icon class="pr-3">mdi-movie</v-icon>
      <span>Hello_World.mp4</span>
      <v-spacer />
    </v-system-bar>

    <v-app-bar color="primary" density="compact" flat app>
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

    <v-main>
      <router-view v-slot="{ Component }">
        <transition>
          <keep-alive>
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
.v-toolbar[app] {
  margin-top: 24px !important;
}
.v-system-bar[app] {
  top: 0px;
  z-index: 1005;
}
.v-main {
  margin-top: 24px;
}
.v-application {
  min-height: 100vh;
}
</style>
