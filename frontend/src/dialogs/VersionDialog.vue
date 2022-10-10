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
  <v-dialog v-model="dialog" width="570px" max-width="calc(100% - 8px)">
    <template #activator="props">
      <slot name="activator" v-bind="props" />
    </template>
    <v-card>
      <v-toolbar density="comfortable">
        <v-toolbar-title>About</v-toolbar-title>
        <v-btn icon="mdi-close" @click="dialog = false" />
      </v-toolbar>
      <v-card-text class="overflow-y-auto pb-4">
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
tbody > tr > td:first-child {
  font-weight: bold;
}
</style>
