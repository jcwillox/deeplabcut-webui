<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
  <v-app>
    <v-app-bar color="#1867c0" density="compact" class="text-white" flat app>
      <template v-slot:prepend>
        <v-app-bar-nav-icon />
      </template>
      <v-app-bar-title tag="div">DLC</v-app-bar-title>
      <template v-slot:append>
        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <v-system-bar>
        <v-icon class="pr-3">mdi-movie</v-icon>
        <span>Hello_World.mp4</span>
        <v-spacer />
      </v-system-bar>
      <RouterView />
    </v-main>
  </v-app>
</template>
