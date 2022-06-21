<script setup lang="ts">
import DialogBackend from "@/dialogs/BackendDialog.vue";
import { useStore } from "@/stores";
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

const store = useStore();
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
        label="Theme"
        v-model="themeName"
        :items="['Auto', 'Light', 'Dark']"
        hideDetails
      />
      <v-card
        color="grey"
        variant="tonal"
        density="compact"
        class="tile-setting"
        title="Auto Select Bodypart"
        subtitle="Select the next bodypart after placing one"
        @click="store.autoSelect = !store.autoSelect"
      >
        <template #append>
          <v-switch
            v-model="store.autoSelect"
            density="compact"
            color="blue"
            hide-details
            inset
          />
        </template>
      </v-card>
      <DialogBackend>
        <template #activator="{ props }">
          <v-card
            v-bind="props"
            color="blue"
            title="Backend"
            subtitle="Configuration"
            variant="tonal"
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
.v-card.tile-setting {
  user-select: none;
}
.v-card.tile-setting > :deep(.v-card-header .v-card-title) {
  font-size: 16px;
}
.v-card.tile-setting > :deep(.v-card-header > .v-card-header-text) {
  color: rgb(var(--v-theme-on-surface));
}
.v-card.tile-setting > :deep(.v-card-header > .v-card-avatar) {
  flex-shrink: 0;
  align-self: auto;
}
</style>
