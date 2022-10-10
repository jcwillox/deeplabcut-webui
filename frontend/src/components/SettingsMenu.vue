<script setup lang="ts">
import DialogBackend from "@/dialogs/BackendDialog.vue";
import { useStore } from "@/stores";
import {
  usePreferredColorScheme,
  useStorage,
  useVModel,
  type BasicColorSchema
} from "@vueuse/core";
import { computed, watch } from "vue";
import { useTheme } from "vuetify";

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const store = useStore();
const show = useVModel(props, "modelValue", emit);

// compute which theme to use
const theme = useTheme();
const themeMode = useStorage<BasicColorSchema>("theme", "auto");
const systemTheme = usePreferredColorScheme();
const selected = computed({
  get: () => ({
    value: themeMode.value
  }),
  set: value => {
    themeMode.value = value.value;
    return value;
  }
});

const themeModes = [
  {
    title: "Auto",
    value: "auto"
  },
  {
    title: "Light",
    value: "light"
  },
  {
    title: "Dark",
    value: "dark"
  }
];

watch([themeMode, systemTheme], () => {
  if (themeMode.value == "auto") {
    theme.global.name.value = systemTheme.value === "dark" ? "dark" : "light";
  } else {
    theme.global.name.value = themeMode.value;
  }
  if (theme.global.name.value === "light") {
    document.documentElement.classList.remove("v-theme--dark");
    document.documentElement.classList.add("v-theme--light");
  } else {
    document.documentElement.classList.remove("v-theme--light");
    document.documentElement.classList.add("v-theme--dark");
  }
});
</script>

<template>
  <v-navigation-drawer v-model="show" :width="300" location="right" temporary>
    <v-toolbar density="comfortable">
      <v-toolbar-title>Settings</v-toolbar-title>
      <v-btn icon="mdi-close" @click.stop="show = false" />
    </v-toolbar>
    <v-container>
      <v-select
        label="Theme"
        v-model="selected"
        :items="themeModes"
        return-object
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
.v-card.tile-setting > :deep(.v-card-item .v-card-title) {
  font-size: 16px;
  white-space: initial;
}
.v-card.tile-setting > :deep(.v-card-item .v-card-subtitle) {
  white-space: initial;
}
.v-card.tile-setting > :deep(.v-card-item > .v-card-item__content) {
  color: rgb(var(--v-theme-on-surface));
}
</style>
