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

const { isFetching, data } = useFetch("/projects").get().json();
</script>

<template>
  <v-container class="d-flex flex-column" style="max-width: 640px">
    <v-autocomplete
      v-model="store.project"
      :items="data"
      :loading="isFetching"
      class="pb-3"
      label="Project"
      color="primary"
      hide-details
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

<style scoped></style>
