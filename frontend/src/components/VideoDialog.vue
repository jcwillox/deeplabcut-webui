<script setup lang="ts">
import { useStore } from "@/stores";
import { useFetch } from "@/utils";
import { computed, watch } from "vue";
import FileBrowser from "./FileBrowser.vue";

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const store = useStore();
const dialog = computed({
  get: () => props.modelValue,
  set: value => {
    emit("update:modelValue", value);
  }
});

const { execute, data, isFetching } = useFetch("/videos", { immediate: false })
  .get()
  .json();

// fetch videos each time the dialog is shown
watch(dialog, () => dialog.value && execute());

// set the globally selected video and close the dialog
const setVideo = (video: string) => {
  dialog.value = false;
  store.setVideo(video);
};
</script>

<template>
  <v-dialog v-model="dialog">
    <template #activator="props">
      <slot name="activator" v-bind="props" />
    </template>
    <v-card class="parent">
      <v-toolbar color="primary" class="toolbar-fixed">
        <v-toolbar-title>Select Video</v-toolbar-title>
        <v-btn density="default" icon="mdi-close" @click="dialog = false" />
      </v-toolbar>
      <v-card-content
        v-if="isFetching"
        class="d-flex align-center justify-center"
      >
        <v-progress-circular color="primary" indeterminate />
      </v-card-content>
      <v-card-content v-else class="overflow-y-auto py-0">
        <FileBrowser :items="data" @selected="setVideo" />
      </v-card-content>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.v-card.parent {
  width: 800px;
  height: calc(100vh - 48px);
}

@media screen and (max-width: 800px) {
  .v-card.parent {
    width: calc(100vw - 24px);
  }
}
</style>
