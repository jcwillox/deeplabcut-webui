<script setup lang="ts">
import ProjectBrowser from "@/components/ProjectBrowser.vue";
import { useFetch } from "@/utils";
import { useVModel } from "@vueuse/core";
import { watch } from "vue";

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const dialog = useVModel(props, "modelValue", emit);

const { execute, data, isFetching } = useFetch("/projects", {
  immediate: false
})
  .get()
  .json();

// fetch projects each time the dialog is shown
watch(dialog, () => dialog.value && execute());
</script>

<template>
  <v-dialog v-model="dialog" width="800px" max-width="calc(100% - 16px)">
    <template #activator="props">
      <slot name="activator" v-bind="props" />
    </template>
    <v-card>
      <v-toolbar color="primary" density="comfortable">
        <v-toolbar-title>Select Project</v-toolbar-title>
        <v-btn icon="mdi-close" @click="dialog = false" />
      </v-toolbar>
      <ProjectBrowser
        :items="data"
        :loading="isFetching"
        height="calc(100vh - 104px)"
        @selected="dialog = false"
      />
    </v-card>
  </v-dialog>
</template>
