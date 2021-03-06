<script setup lang="ts">
import { useConfig, useFrames, useLabels } from "@/stores";
import { createCachedUrl } from "@/utils";
import { useVModel } from "@vueuse/core";
import { storeToRefs } from "pinia";

const props = defineProps<{
  modelValue?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const frames = useFrames();
const labelsStore = useLabels();
const { labelsCount } = storeToRefs(useConfig());
const { getLabelledCount } = labelsStore;
const { index } = storeToRefs(labelsStore);

const dialog = useVModel(props, "modelValue", emit);

const partiallyLabelled = (image: string) =>
  getLabelledCount(image) < labelsCount.value;
</script>

<template>
  <v-dialog v-model="dialog">
    <template #activator="props">
      <slot name="activator" v-bind="props" />
    </template>
    <v-card class="parent" style="height: calc(100vh - 48px)">
      <v-toolbar color="primary" class="toolbar-fixed">
        <v-toolbar-title>Frames</v-toolbar-title>
        <v-btn icon="mdi-close" @click="dialog = false" />
      </v-toolbar>
      <v-card-content class="overflow-y-auto">
        <v-row class="text-center" justify="center" align="center">
          <v-col v-for="(image, i) in frames.items" :key="image" cols="auto">
            <v-card
              variant="tonal"
              :key="i"
              :width="250"
              :class="{ active: i === index }"
              :color="partiallyLabelled(image) ? 'amber' : undefined"
              @click="
                index = i;
                dialog = false;
              "
            >
              <v-img
                :src="createCachedUrl(frames.framesUrl, image)"
                class="rounded-t"
              >
                <template #placeholder>
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

              <v-card-title class="d-flex justify-space-between text-body-1">
                <span class="ellipsis">{{ image }}</span>

                <span class="text-no-wrap ml-2">
                  {{ getLabelledCount(image) }} / {{ labelsCount }}
                </span>
              </v-card-title>
            </v-card>
          </v-col>
        </v-row>
      </v-card-content>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.ellipsis {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
.v-card.active {
  outline: 2px
    rgba(
      var(--v-theme-success),
      calc(0.7 * var(--v-theme-success-overlay-multiplier))
    )
    solid;
  outline-offset: 2px;
}

.v-card.parent {
  min-width: 800px;
  height: calc(100vh - 48px);
}
@media screen and (max-width: 800px) {
  .v-card.parent {
    min-width: initial;
    max-width: calc(100vw - 24px);
  }
}
</style>
