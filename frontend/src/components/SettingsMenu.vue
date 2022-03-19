<script setup lang="ts">
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
  <v-navigation-drawer v-model="show" temporary position="right" :width="300">
    <v-toolbar>
      <v-toolbar-title>Settings</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click.stop="show = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-container>
      <v-select
        :items="['Auto', 'Light', 'Dark']"
        v-model="themeName"
        label="Theme"
      >
      </v-select>
    </v-container>
  </v-navigation-drawer>
</template>
