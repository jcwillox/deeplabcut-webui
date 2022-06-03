<script setup lang="ts">
export interface FileItem {
  name: string;
  folder?: boolean;
  accessed?: number;
  created?: number;
  size?: number;
  extracted?: number;
  labelled?: number;
}

defineProps<{
  items: FileItem[];
}>();

const emit = defineEmits<{
  (e: "selected", value: string): void;
}>();

const getIcon = (item: FileItem) => {
  if (item.name.toLowerCase().endsWith(".mp4")) {
    return "mdi-movie";
  } else if (item.folder) {
    return "mdi-folder";
  }
  return "mdi-file-outline";
};

const updateSelected = (selected?: string[]) => {
  if (selected && selected.length > 0) {
    emit("selected", selected[0]);
  }
};
</script>

<template>
  <v-list @update:selected="updateSelected">
    <template v-for="(item, i) in items" :key="i">
      <v-list-item
        :value="item.name"
        :prepend-icon="getIcon(item)"
        :title="item.name"
      >
        <template v-slot:subtitle>
          <div v-if="item.size">
            {{ (item.size / 1073741824).toFixed(2) }} GiB • Extracted:
            {{ item.extracted }} • Labelled: {{ item.labelled }}
          </div>
        </template>
      </v-list-item>
      <v-divider v-if="i < items.length - 1" :key="i"></v-divider>
    </template>
  </v-list>
</template>

<style scoped></style>
