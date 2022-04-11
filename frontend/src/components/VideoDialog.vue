<script setup lang="ts">
import { useStore } from "@/stores/global";
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

const { execute, data, isFetching } = useFetch("videos", { immediate: false })
  .get()
  .json();

// fetch videos each time the dialog is shown
watch(dialog, () => dialog.value && execute());

// set the globally selected video and close the dialog
const setVideo = (video: string) => {
  store.video = video;
  dialog.value = false;
};
</script>

<template>
  <v-dialog v-model="dialog" scrollable fullscreen>
    <slot></slot>
    <v-card class="d-flex flex-column">
      <v-toolbar color="primary" fixed>
        <v-toolbar-title>Select Video</v-toolbar-title>
        <v-spacer />
        <v-btn icon dark @click="dialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text
        v-if="isFetching"
        class="d-flex flex-column pb-4 align-center justify-center flex-grow-1"
      >
        <v-progress-circular indeterminate color="primary" />
      </v-card-text>
      <v-card-text
        v-else
        class="pt-0"
        style="overflow-y: scroll; height: calc(100vh - 56px)"
      >
        <FileBrowser
          style="margin: auto; max-width: 680px"
          :items="data"
          @selected="setVideo"
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
