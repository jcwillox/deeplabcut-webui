<script setup lang="ts">
import { ref } from "vue";

defineProps<{
  title?: string;
  subtitle?: string;
  icon: string;
  color: string;
  details?: string;
}>();

const show = ref(false);
</script>

<template>
  <v-card variant="tonal" density="comfortable" :color="color">
    <template #title>
      <slot name="title">
        {{ title }}
      </slot>
    </template>
    <template #subtitle>
      <slot name="subtitle">
        {{ subtitle }}
      </slot>
    </template>
    <template #prepend>
      <v-avatar style="color: inherit">
        <v-icon>{{ icon }}</v-icon>
      </v-avatar>
    </template>
    <template v-if="details" #append>
      <v-btn
        :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'"
        variant="plain"
        @click="show = !show"
      ></v-btn>
    </template>
    <v-expand-transition>
      <div v-show="show">
        <v-divider />
        <v-card-text>
          {{ details }}
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<style scoped>
.v-card-text {
  padding-bottom: 0.5rem;
  white-space: pre;
  overflow-x: auto;
}
</style>
