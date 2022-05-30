<script setup lang="ts">
import { useFrames } from "@/stores";
import { createCachedUrl } from "@/utils";
import { useVModel } from "@vueuse/core";
import { ref } from "vue";

const props = defineProps<{
  modelValue: number;
}>();

const dialog = ref(false);
const frames = useFrames();
const imgIndex = useVModel(props);
</script>

<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="props">
      <slot name="activator" v-bind="props" />
    </template>
    <v-toolbar color="primary" class="rounded-t" fixed>
      <v-toolbar-title>Frames</v-toolbar-title>
      <v-spacer />
      <v-btn @click="dialog = false" icon="mdi-close" />
    </v-toolbar>
    <v-card
      class="parent rounded-t-0 text-no-wrap pb-2"
      style="height: calc(100vh - 104px)"
      elevation="0"
    >
      <v-card-content>
        <v-row class="text-center" justify="center">
          <v-col v-for="(frame, i) in frames.items" :key="i" cols="auto">
            <div>
              <v-img
                :style="i === imgIndex && { border: '4px solid yellowgreen' }"
                :src="createCachedUrl(frames.framesUrl, frame)"
                :aspect-ratio="16 / 9"
                :width="250"
                @click="
                  imgIndex = i;
                  dialog = false;
                "
              >
                <template v-slot:placeholder>
                  <v-row
                    class="fill-height ma-0"
                    align="center"
                    justify="center"
                  >
                    <v-progress-circular
                      indeterminate
                      color="grey-lighten-5"
                    ></v-progress-circular>
                  </v-row>
                </template>
              </v-img>
            </div>
            {{ frame }}
          </v-col>
        </v-row>
      </v-card-content>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
