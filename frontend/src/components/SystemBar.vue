<script setup lang="ts">
import { useStore } from "@/stores";
import { ref } from "vue";
import VideoDialog from "./VideoDialog.vue";
import { useRouter } from "vue-router";

const store = useStore();
const dialog = ref(false);
const router = useRouter();
</script>

<template>
  <v-system-bar
    v-if="store.project"
    color="primary-darken-1"
    class="flex-grow-0 pl-0"
  >
    <v-btn
      v-if="store.project"
      size="small"
      variant="text"
      class="ml-1 pl-2 pr-1"
      prepend-icon="mdi-folder"
      @click="router.push({ name: 'project' })"
    >
      {{ store.project }}
    </v-btn>
    <span v-if="store.cVideo">
      <span class="mx-1">/</span>
      <VideoDialog v-model="dialog">
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            size="small"
            variant="text"
            class="pl-2 pr-1"
            prepend-icon="mdi-movie"
            @click.stop="dialog = true"
          >
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
