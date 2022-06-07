<script setup lang="ts">
import { useFrames } from "@/stores";
import { createCachedUrl } from "@/utils";
import { useVModel } from "@vueuse/core";

const props = defineProps<{
  modelValue?: boolean;
  index: number;
}>();

const frames = useFrames();
const dialog = useVModel(props, "modelValue");
const imgIndex = useVModel(props, "index");
</script>

<template>
  <v-dialog v-model="dialog">
    <template #activator="props">
      <slot name="activator" v-bind="props" />
    </template>
    <v-card style="height: calc(100vh - 48px)">
      <v-toolbar color="primary" class="toolbar-fixed">
        <v-toolbar-title>Frames</v-toolbar-title>
        <v-btn icon="mdi-close" @click="dialog = false" />
      </v-toolbar>
      <v-card-content class="overflow-y-auto">
        <v-row class="text-center" justify="center" align="center">
          <v-col v-for="(frame, i) in frames.items" :key="frame" cols="auto">
            <v-img
              v-ripple
              :style="i === imgIndex && { border: '4px solid yellowgreen' }"
              :src="createCachedUrl(frames.framesUrl, frame)"
              :width="250"
              class="cursor-pointer"
              @click="
                imgIndex = i;
                dialog = false;
              "
            >
              <template #placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular
                    indeterminate
                    color="grey-lighten-5"
                  ></v-progress-circular>
                </v-row>
              </template>
            </v-img>
            {{ frame }}
          </v-col>
        </v-row>
      </v-card-content>
    </v-card>
  </v-dialog>
</template>
