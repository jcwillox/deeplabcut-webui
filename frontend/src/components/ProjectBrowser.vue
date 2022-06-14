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
const project = computed({
  get: () => store.project,
  set: value => {
    store.resetProject();
    store.project = value;
    emit("selected", value);
  }
});

const columns: Column[] = [
  {
    type: "icon",
    default: "mdi-folder"
  },
  {
    field: "name"
  },
  {
    name: "Multi-animal",
    field: "multi_animal",
    type: "icon",
    getter: (value: boolean) => {
      return value ? "mdi-check" : "mdi-close";
    }
  },
  {
    field: "scorer"
  },
  {
    field: "accessed",
    type: "unix"
  },
  {
    field: "created",
    type: "unix"
  }
];
</script>

<template>
  <FileBrowser
    v-model:selected="project"
    :items="items"
    :columns="columns"
    :height="height"
  />
</template>
