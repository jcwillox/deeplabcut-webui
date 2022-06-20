<script setup lang="ts">
import ProjectDialog from "@/dialogs/ProjectDialog.vue";
import VideoDialog from "@/dialogs/VideoDialog.vue";
import { useStore } from "@/stores";
import { useHotkeys } from "@/utils";
import { ref } from "vue";

const store = useStore();
const dialogProject = ref(false);
const dialogVideo = ref(false);

useHotkeys("shift+v", () => {
  dialogVideo.value = !dialogVideo.value;
});
useHotkeys("shift+p", () => {
  dialogProject.value = !dialogProject.value;
});
</script>

<template>
  <v-system-bar
    v-if="store.project"
    color="primary-darken-1"
    class="flex-grow-0 pl-0"
  >
    <ProjectDialog v-if="store.project" v-model="dialogProject">
      <template #activator="{ props }">
        <v-btn
          v-bind="props"
          size="small"
          variant="text"
          class="ml-1 pl-2 pr-1"
          prepend-icon="mdi-folder"
        >
          {{ store.project }}
          <v-tooltip activator="parent" location="bottom start">
            Quick switch project <kbd>Shift</kbd><kbd>P</kbd>
          </v-tooltip>
        </v-btn>
      </template>
    </ProjectDialog>
    <span v-if="store.cVideo">
      <span class="mx-1">/</span>
      <VideoDialog v-model="dialogVideo">
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            size="small"
            variant="text"
            class="pl-2 pr-1"
            prepend-icon="mdi-movie"
          >
            {{ store.cVideo }}
            <v-tooltip activator="parent" location="bottom">
              Quick switch video <kbd>Shift</kbd><kbd>V</kbd>
            </v-tooltip>
          </v-btn>
        </template>
      </VideoDialog>
    </span>
    <v-spacer />
    <v-btn
      icon="mdi-close"
      variant="text"
      size="x-small"
      @click="store.resetProject"
    />
  </v-system-bar>
</template>

<style scoped>
.v-btn {
  text-transform: none;
  font-weight: 400;
}
</style>
