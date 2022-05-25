<script setup lang="ts">
import DialogBackend from "@/components/BackendDialog.vue";
import type { BasicColorSchema } from "@vueuse/core";
import { capitalize, computed, ref } from "vue";

const props = defineProps<{
  modelValue: boolean;
  theme: BasicColorSchema;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "update:theme", value: BasicColorSchema): void;
}>();

const dialogBackend = ref(false);

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
  <v-navigation-drawer v-model="show" :width="300" position="right" temporary>
    <v-toolbar>
      <v-toolbar-title>Settings</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn @click.stop="show = false" icon="mdi-close" />
    </v-toolbar>
    <v-container>
      <v-select
        label="Theme"
        v-model="themeName"
        :items="['Auto', 'Light', 'Dark']"
        hide-details
      />
      <v-card
        v-ripple
        title="Backend"
        subtitle="Configuration"
        variant="contained-text"
        style="cursor: pointer; user-select: none"
        @click="dialogBackend = true"
      >
        <template #append>
          <v-avatar>
            <v-icon size="32">mdi-chevron-right</v-icon>
          </v-avatar>
        </template>
      </v-card>
      <DialogBackend v-model="dialogBackend" />
    </v-container>
  </v-navigation-drawer>
</template>

<style scoped>
.v-container > *:not(:last-child) {
  margin-bottom: 8px;
}
</style>
