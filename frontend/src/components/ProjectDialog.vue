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
  <v-dialog v-model="dialog">
    <template #activator="props">
      <slot name="activator" v-bind="props" />
    </template>
    <v-card class="parent">
      <v-toolbar color="primary" class="toolbar-fixed">
        <v-toolbar-title>Select Project</v-toolbar-title>
        <v-btn icon="mdi-close" @click="dialog = false" />
      </v-toolbar>
      <v-card-content
        v-if="isFetching"
        class="d-flex align-center justify-center"
      >
        <v-progress-circular color="primary" indeterminate />
      </v-card-content>
      <v-card-content v-else class="overflow-y-auto pa-0">
        <ProjectBrowser
          :items="data"
          height="calc(100vh - 104px)"
          @selected="dialog = false"
        />
      </v-card-content>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.v-card.parent {
  min-width: 800px;
  height: calc(100vh - 48px);
}
@media screen and (max-width: 800px) {
  .v-card.parent {
    min-width: initial;
    max-width: calc(100vw - 24px);
  }
}
</style>
