<script setup lang="ts">
import DialogBackend from "@/components/BackendDialog.vue";
import type { BasicColorSchema } from "@vueuse/core";
import { capitalize, computed } from "vue";

const props = defineProps<{
  modelValue: boolean;
  theme: BasicColorSchema;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "update:theme", value: BasicColorSchema): void;
}>();

const show = computed({
  get: () => props.modelValue,
  set: value => emit("update:modelValue", value)
});

const themeName = computed({
  get: () => capitalize(props.theme),
  set: value => {
    emit("update:theme", value.toLowerCase() as BasicColorSchema);
  }
});
</script>

<template>
  <v-navigation-drawer v-model="show" :width="300" location="right" temporary>
    <v-toolbar>
      <v-toolbar-title>Settings</v-toolbar-title>
      <v-btn icon="mdi-close" @click.stop="show = false" />
    </v-toolbar>
    <v-container>
      <v-select
        v-bind="{ label: 'Theme', hideDetails: true }"
        v-model="themeName"
        :items="['Auto', 'Light', 'Dark']"
      />
      <DialogBackend>
        <template #activator="{ props }">
          <v-card
            v-bind="props"
            color="blue"
            title="Backend"
            subtitle="Configuration"
            variant="contained-text"
          >
            <template #append>
              <v-avatar style="color: inherit">
                <v-icon size="32">mdi-chevron-right</v-icon>
              </v-avatar>
            </template>
          </v-card>
        </template>
      </DialogBackend>
    </v-container>
  </v-navigation-drawer>
</template>

<style scoped>
.v-container > *:not(:last-child) {
  margin-bottom: 8px;
}
</style>
