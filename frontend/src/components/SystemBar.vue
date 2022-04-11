<script setup lang="ts">
import { useStore } from "@/stores/global";
import { ref } from "vue";
import VideoDialog from "./VideoDialog.vue";

const store = useStore();
const dialog = ref(false);
</script>

<template>
  <v-system-bar
    v-if="store.project"
    app
    color="primary-darken-1"
    class="flex-grow-0 pl-0"
  >
    <v-btn v-if="store.project" variant="text" size="small" :ripple="false">
      <v-icon left>mdi-folder</v-icon>
      {{ store.project }}
    </v-btn>
    <span v-if="store.video">
      <span class="pr-1">/</span>
      <v-btn variant="text" size="small" @click.stop="dialog = true">
        <v-icon left>mdi-movie</v-icon>
        {{ store.video }}
      </v-btn>
    </span>
    <v-spacer />
    <v-icon @click="store.resetProject">mdi-close</v-icon>

    <VideoDialog v-model="dialog"> </VideoDialog>
  </v-system-bar>
</template>

<style scoped>
.v-btn {
  text-transform: none;
  font-weight: 400;
}
.mdi-close {
  cursor: pointer;
  opacity: 1 !important;
}
</style>
