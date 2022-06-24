<script lang="ts">
export default {
  name: "ProjectView"
};
</script>

<script setup lang="ts">
import ProjectBrowser from "@/components/ProjectBrowser.vue";
import VideoBrowser from "@/components/VideoBrowser.vue";
import { useStore } from "@/stores";
import { useFetch } from "@/utils/fetch";
import { onActivated, watchEffect } from "vue";

const store = useStore();
const {
  isFetching: isFetchingProjects,
  execute: fetchProjects,
  data: projects
} = useFetch("/projects", { immediate: false }).get().json();

const {
  isFetching: isFetchingVideos,
  execute: fetchVideos,
  data: videos
} = useFetch("/videos", { immediate: false }).get().json();

watchEffect(() => {
  if (store.project) {
    videos.value = null;
    fetchVideos();
  } else {
    fetchProjects();
  }
});

onActivated(() => {
  if (store.project && !isFetchingVideos.value) {
    fetchVideos();
  }
});
</script>

<template>
  <v-container
    v-if="!store.project"
    class="pa-0"
    style="max-width: 1000px"
    fluid
  >
    <ProjectBrowser
      :items="projects"
      :loading="isFetchingProjects"
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
      <VideoBrowser
        :items="videos"
        :loading="isFetchingVideos"
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
