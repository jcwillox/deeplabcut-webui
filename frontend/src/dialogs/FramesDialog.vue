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
  <v-dialog
    v-model="dialog"
    width="auto"
    height="calc(100% - 48px)"
    min-width="800px"
  >
    <template #activator="props">
      <slot name="activator" v-bind="props" />
    </template>
    <v-card class="parent h-100">
      <v-toolbar color="primary" density="comfortable">
        <v-toolbar-title>Frames</v-toolbar-title>
        <v-btn icon="mdi-close" @click="dialog = false" />
      </v-toolbar>
      <div class="overflow-y-auto pa-4">
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
      </div>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.ellipsis {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
@media screen and (max-width: 1000px) {
  .v-card.parent {
    width: 100%;
    max-width: calc(100vw - 16px);
    align-self: center;
  }
}
/* outline active card */
.v-card.active {
  outline: 2px
    rgba(
      var(--v-theme-success),
      calc(0.7 * var(--v-theme-success-overlay-multiplier))
    )
    solid;
  outline-offset: 2px;
}
/* fix the tonal card color covering image */
.v-card.v-card--variant-tonal > :deep(.v-card__underlay) {
  height: 48px;
  top: auto;
}
</style>
