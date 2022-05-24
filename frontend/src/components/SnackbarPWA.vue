<script setup lang="ts">
import { useRegisterSW } from "virtual:pwa-register/vue";
import { ref, watch } from "vue";

const show = ref(false);
const { offlineReady, needRefresh, updateServiceWorker } = useRegisterSW();

watch([offlineReady, needRefresh], () => {
  if (offlineReady.value || needRefresh.value) {
    show.value = true;
  }
});
</script>

<template>
  <v-snackbar v-model="show" timeout="-1" top right>
    <span v-if="offlineReady" class="text-white"
      >This app is ready to work offline.</span
    >
    <span v-else-if="needRefresh" class="text-white"
      >New version available, click on reload button to update.</span
    >
    <template v-slot:actions>
      <v-btn
        v-if="needRefresh"
        class="text-blue"
        @click="updateServiceWorker()"
      >
        Reload
      </v-btn>
      <v-btn
        class="text-grey-lighten-1"
        icon="mdi-close"
        size="small"
        @click="show = false"
      ></v-btn>
    </template>
  </v-snackbar>
</template>
