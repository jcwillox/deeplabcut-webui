<script setup lang="ts">
import SettingsMenu from "@/components/SettingsMenu.vue";
import SnackbarPWA from "@/components/SnackbarPWA.vue";
import SystemBar from "@/components/SystemBar.vue";
import VersionDialog from "@/dialogs/VersionDialog.vue";
import { useFrames, useStore } from "@/stores";
import { clearUrlCache, useHotkeys } from "@/utils";
import {
  usePreferredColorScheme,
  useStorage,
  type BasicColorSchema
} from "@vueuse/core";
import { computed, ref, watch } from "vue";
import { RouterView, useRoute, useRouter } from "vue-router";
import { useTheme } from "vuetify";

const store = useStore();
const frames = useFrames();
const showProject = computed(() => !store.project || !store.cVideo);
const showSettings = ref(false);

// compute which theme to use
const theme = useTheme();
const themeMode = useStorage<BasicColorSchema>("theme", "auto");
const systemTheme = usePreferredColorScheme();

watch([themeMode, systemTheme], () => {
  if (themeMode.value == "auto") {
    theme.global.name.value = systemTheme.value === "dark" ? "dark" : "light";
  } else {
    theme.global.name.value = themeMode.value;
  }
  if (theme.global.name.value === "light") {
    document.documentElement.classList.remove("v-theme--dark");
    document.documentElement.classList.add("v-theme--light");
  } else {
    document.documentElement.classList.remove("v-theme--light");
    document.documentElement.classList.add("v-theme--dark");
  }
});

// handle tracking active tab
const route = useRoute();
const router = useRouter();
const tab = ref("");
const tabs = ["project", "extract", "label"];
const items = computed(() => (showProject.value ? tabs.slice(0, 1) : tabs));

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
        return "/guide/select-video/";
      }
      return "/guide/select-project/";
    case "extract":
      return "/guide/extracting/";
    case "label":
      return "/guide/labelling/";
    default:
      return "";
  }
};

const openDocs = () => {
  window.location.assign(import.meta.env.BASE_URL + "docs" + getDocsPage());
};

// define hotkeys
tabs.forEach((value, index) => {
  useHotkeys(`shift+${index + 1}`, () => {
    router.push({ name: value });
  });
});
useHotkeys("shift+w", store.resetProject);
</script>

<template>
  <v-app>
    <SettingsMenu v-model="showSettings" v-model:theme="themeMode" />
    <SnackbarPWA />
    <SystemBar />

    <v-app-bar color="primary" density="compact" class="position-relative" flat>
      <template v-slot:prepend>
        <v-tabs v-model="tab">
          <v-tab
            v-for="(item, index) in items"
            :key="item"
            :value="item"
            :to="'/' + item"
          >
            {{ item }}
            <v-tooltip activator="parent" location="bottom">
              <kbd>Shift</kbd><kbd>{{ index + 1 }}</kbd>
            </v-tooltip>
          </v-tab>
        </v-tabs>
      </template>

      <v-spacer />

      <v-btn @click="openDocs" icon>
        <v-icon>mdi-help-circle</v-icon>
        <v-tooltip activator="parent" location="bottom" text="Help" />
      </v-btn>
      <VersionDialog>
        <template #activator="{ props }">
          <v-btn v-bind="props" icon>
            <v-icon>mdi-information</v-icon>
            <v-tooltip activator="parent" location="bottom" text="About" />
          </v-btn>
        </template>
      </VersionDialog>
      <v-btn class="mr-n3" @click.stop="showSettings = true" icon>
        <v-icon>mdi-cog</v-icon>
        <v-tooltip
          activator="parent"
          location="bottom end"
          class="settings"
          text="Settings"
        />
      </v-btn>
    </v-app-bar>

    <v-main class="pa-0">
      <router-view #default="{ Component }">
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
*::-webkit-scrollbar {
  width: 16px;
}

*::-webkit-scrollbar-thumb {
  background-color: rgba(var(--v-theme-on-background), 0.2);
  border: 4px solid transparent;
  border-radius: 8px;
  background-clip: padding-box;
  pointer-events: none;
}

html.v-theme--light > body::-webkit-scrollbar {
  background-color: rgb(238, 238, 238);
}

@supports (overflow: overlay) {
  html {
    overflow-y: overlay !important;
  }
  html.v-theme--light > body::-webkit-scrollbar {
    background-color: unset;
  }
}

.v-table--fixed-header th {
  z-index: 1;
}
.v-overlay header.v-toolbar.v-theme--dark.bg-primary {
  background: rgb(var(--v-theme-on-surface-variant)) !important;
}
.v-tooltip kbd {
  border-radius: 3px;
  background: rgb(var(--v-theme-surface-variant));
  color: rgb(var(--v-kbd-color));
  font-size: 85%;
  font-weight: normal;
  font-family: inherit;
  padding: 0.2em 0.4rem;
}
.v-tooltip kbd:not(:first-child) {
  margin-left: 2px;
}
.toolbar-fixed {
  top: 0;
  position: sticky;
  flex-shrink: 0;
  z-index: 1;
}
.cursor-pointer {
  cursor: pointer;
}
</style>
