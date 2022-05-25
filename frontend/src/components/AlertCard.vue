<script setup lang="ts">
defineProps<{
  title?: string;
  subtitle?: string;
  icon: string;
  color: string;
}>();
</script>

<template>
  <v-card variant="contained-text" density="comfortable" :color="color">
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
  </v-card>
</template>
