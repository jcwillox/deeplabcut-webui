<script setup lang="ts">
import { ref } from "vue";

const dialog = ref(false);
const buildTime = __BUILD_TIME__;
const commit = __COMMIT__;
const branch = __BRANCH__;
const version = __VERSION__;
</script>

<template>
  <v-dialog v-model="dialog">
    <template #activator="{ props }">
      <v-btn v-bind="props" icon>
        <v-icon>mdi-information</v-icon>
        <v-tooltip activator="parent" anchor="bottom">About</v-tooltip>
      </v-btn>
    </template>
    <v-toolbar class="rounded-t" fixed>
      <v-toolbar-title>About</v-toolbar-title>
      <v-spacer />
      <v-btn @click="dialog = false" icon="mdi-close" />
    </v-toolbar>
    <v-card class="parent rounded-t-0" elevation="0">
      <v-card-text>
        <div><b>Version:</b> {{ version }}</div>
        <div><b>Branch:</b> {{ branch }}</div>
        <div><b>Commit:</b> {{ commit }}</div>
        <div><b>Built At:</b> {{ buildTime }}</div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.v-card.parent {
  width: 500px;
}

@media screen and (max-width: 500px) {
  .v-card.parent {
    width: 100vw;
  }
}
</style>
