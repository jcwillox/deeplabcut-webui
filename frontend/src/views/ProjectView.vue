<script lang="ts">
export default {
  name: "ProjectView"
};
</script>

<script setup lang="ts">
import type { Column } from "@/components/FileBrowser.vue";
import FileBrowser from "@/components/FileBrowser.vue";
import VideoBrowser from "@/components/VideoBrowser.vue";
import { useStore } from "@/stores";
import { useFetch } from "@/utils/fetch";
import { watchEffect } from "vue";

const store = useStore();
const { data: projects } = useFetch("/projects").get().json();

const {
  isFetching: isFetchingVideos,
  execute,
  data: videos
} = useFetch("/videos", { immediate: false }).get().json();

watchEffect(() => {
  if (store.project) {
    execute();
  }
});

const columns: Column[] = [
  {
    type: "icon",
    default: "mdi-folder"
  },
  {
    field: "name"
  },
  {
    name: "Multi-animal",
    field: "multi_animal",
    type: "icon",
    getter: (value: boolean) => {
      return value ? "mdi-check" : "mdi-close";
    }
  },
  {
    field: "scorer"
  },
  {
    field: "accessed",
    type: "unix"
  },
  {
    field: "created",
    type: "unix"
  }
];
</script>

<template>
  <v-container
    v-if="!store.project"
    class="pa-0"
    style="max-width: 1000px"
    fluid
  >
    <FileBrowser
      v-model:selected="store.project"
      :items="projects"
      :columns="columns"
      class="pa-0 ma-2"
      height="calc(100vh - 48px - 16px)"
    />
  </v-container>
  <v-container
    v-else
    class="d-flex flex-row pa-0"
    style="max-width: 1280px; height: calc(100vh - 72px)"
    fluid
  >
    <div class="ma-2 d-flex flex-column" style="flex-grow: 5">
      <h2 class="text-center">{{ store.project }}</h2>
      <div
        v-if="isFetchingVideos"
        class="d-flex justify-center align-center flex-grow-1"
      >
        <v-progress-circular indeterminate color="primary" />
      </div>
      <VideoBrowser
        v-else
        :items="videos"
        class="pa-0 mt-2"
        height="calc(100vh - 131px)"
      />
    </div>
    <v-divider vertical />
    <div class="d-flex flex-column" style="flex-grow: 1">
      <v-btn
        class="ma-2"
        color="red"
        variant="text"
        @click="store.resetProject"
      >
        Close Project
        <v-tooltip activator="parent" location="bottom">
          <kbd>Shift</kbd><kbd>W</kbd>
        </v-tooltip>
      </v-btn>
      <v-divider />
    </div>
    <v-divider vertical />
  </v-container>
</template>

<style scoped>
:deep(.v-input__details) {
  margin-bottom: 0;
}
</style>
