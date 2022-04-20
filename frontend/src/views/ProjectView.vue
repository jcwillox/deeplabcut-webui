<script lang="ts">
export default {
  name: "ProjectView"
};
</script>

<script setup lang="ts">
import { useStore } from "@/stores/global";
import { useFetch } from "@/utils/fetch";
import { ref } from "vue";
import VideoDialog from "../components/VideoDialog.vue";

const store = useStore();
const dialog = ref(false);

const { isFetching, error, data } = useFetch("/projects").get().json();
</script>

<template>
  <v-container class="d-flex flex-column" style="max-width: 640px">
    <v-autocomplete
      v-model="store.project"
      label="Project"
      color="primary"
      class="pb-3"
      :items="data"
      :loading="isFetching"
      :hide-details="!error"
      :error-messages="error || ''"
      clearable
    ></v-autocomplete>
    <v-text-field
      class="pb-3"
      label="Video"
      color="primary"
      :disabled="!store.project"
      :model-value="store.video"
      @click.stop="dialog = true"
      hide-details
      readonly
    ></v-text-field>
    <VideoDialog v-model="dialog"></VideoDialog>
  </v-container>
</template>

<style scoped>
:deep(.v-input__details) {
  margin-bottom: 0;
}
</style>
