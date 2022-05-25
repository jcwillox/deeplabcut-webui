<script setup lang="ts">
import { ref } from "vue";

const dialog = ref(false);
const buildTime = __BUILD_TIME__;
const localBuildTime = new Date(__BUILD_TIME__).toLocaleString();
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
    <v-card class="parent rounded-t-0 text-no-wrap pb-2" elevation="0">
      <v-card-text>
        <v-table>
          <tbody>
            <tr>
              <td>Version</td>
              <td>{{ version }}</td>
            </tr>
            <tr>
              <td>Branch</td>
              <td>{{ branch }}</td>
            </tr>
            <tr>
              <td>Commit</td>
              <td>{{ commit }}</td>
            </tr>
            <tr>
              <td>Build Time</td>
              <td>{{ buildTime }}</td>
            </tr>
            <tr>
              <td>Build Time (Local)</td>
              <td>{{ localBuildTime }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.v-card.parent {
  width: 570px;
}

tbody > tr > td:first-child {
  font-weight: bold;
}

@media screen and (max-width: 570px) {
  .v-card.parent {
    width: 100vw;
  }
}
</style>
