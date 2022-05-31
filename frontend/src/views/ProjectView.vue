<script lang="ts">
export default {
  name: "ProjectView"
};
</script>

<script setup lang="ts">
import { useStore } from "@/stores";
import { useFetch } from "@/utils/fetch";
import { watchEffect } from "vue";
import FileBrowser from "../components/FileBrowser.vue";

const store = useStore();

const {
  isFetching,
  error,
  data: projects
} = useFetch("/projects").get().json();

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
</script>

<template>
  <v-container
    v-if="!store.project"
    class="d-flex flex-column"
    style="max-width: 640px"
  >
    <v-autocomplete
      v-model="store.project"
      label="Project"
      color="primary"
      class="pb-3"
      item-title="name"
      :items="projects"
      :loading="isFetching"
      :hide-details="!error"
      :error-messages="error || ''"
      clearable
    ></v-autocomplete>
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
      <FileBrowser
        v-else
        class="pa-0 mt-2"
        :items="videos"
        @selected="store.setVideo"
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
