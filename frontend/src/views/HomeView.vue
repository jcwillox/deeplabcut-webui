<script setup lang="ts">
import TheWelcome from "@/components/TheWelcome.vue";
import { RouterLink } from "vue-router";
</script>

<template>
  <main>
    To <RouterLink to="/about">About</RouterLink>
    <TheWelcome />
  </main>
</template>
