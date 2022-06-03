<script setup lang="ts">
import { useStore } from "@/stores";
import { ref } from "vue";
import VideoDialog from "./VideoDialog.vue";

const store = useStore();
const dialog = ref(false);
</script>

<template>
  <v-system-bar
    v-if="store.project"
    color="primary-darken-1"
    class="flex-grow-0 pl-0"
  >
    <v-btn
      v-if="store.project"
      :ripple="false"
      class="ml-2 mr-2 pl-1 pr-1"
      variant="text"
      size="small"
    >
      <v-icon left>mdi-folder</v-icon>
      {{ store.project }}
    </v-btn>
    <span v-if="store.cVideo">
      <span>/</span>
      <VideoDialog v-model="dialog">
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            class="ml-1 mr-2 px-1"
            variant="text"
            size="small"
            @click.stop="dialog = true"
          >
            <v-icon left>mdi-movie</v-icon>
            {{ store.cVideo }}
          </v-btn>
        </template>
      </VideoDialog>
    </span>
    <v-spacer />
    <v-btn
      icon="mdi-close"
      variant="text"
      size="x-small"
      class="ml-2"
      @click="store.resetProject"
    ></v-btn>
  </v-system-bar>
</template>

<style scoped>
.v-btn {
  text-transform: none;
  font-weight: 400;
}
</style>
