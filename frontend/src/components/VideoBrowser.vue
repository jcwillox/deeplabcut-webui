<script setup lang="ts">
import type { Column, ItemBase } from "@/components/FileBrowser.vue";
import FileBrowser from "@/components/FileBrowser.vue";
import { useStore } from "@/stores";
import { computed } from "vue";

defineProps<{
  items?: ItemBase[] | null;
  height?: string;
}>();

const emit = defineEmits<{
  (e: "selected", selected: string): void;
}>();

const store = useStore();
const video = computed({
  get: () => store.video,
  set: value => {
    store.setVideo(value);
    emit("selected", value);
  }
});

const columns: Column[] = [
  {
    type: "icon",
    default: "mdi-movie"
  },
  {
    field: "name"
  },
  {
    field: "size",
    type: "bytes",
    shrink: true
  },
  {
    name: "Labelled / Extracted",
    align: "center",
    shrink: true,
    getter: (_, item) => {
      return `${item.labelled} / ${item.extracted}`;
    }
  },
  {
    field: "accessed",
    type: "unix",
    shrink: true
  },
  {
    field: "created",
    type: "unix",
    shrink: true
  }
];
</script>

<template>
  <FileBrowser
    v-model:selected="video"
    :items="items"
    :columns="columns"
    :height="height"
  />
</template>
