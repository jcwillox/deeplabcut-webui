<script lang="ts">
export default {
  name: "LabelView"
};
</script>

<script setup lang="ts">
import { useStore } from "@/stores/global";
import { createUrl, useFetch } from "@/utils/fetch";
import panzoom, { type PanZoom } from "panzoom";
import { computed, ref, watch, watchEffect } from "vue";
import type { VCarouselItem } from "vuetify/components";

const store = useStore();
const imgIndex = ref(0);
const carouselEl = ref<InstanceType<typeof VCarouselItem>[] | null>(null);
const url = ref("");

watch(
  () => store.video,
  () => {
    if (store.video) {
      url.value = "/videos/" + store.video;
    }
  },
  { immediate: true }
);

const framesUrl = computed(() => url.value + "/frames");

const { data: frames } = useFetch(framesUrl, {
  refetch: true
})
  .get()
  .json();
const framesList = computed<string[]>(() => (frames.value ? frames.value : []));

let instance: PanZoom | undefined;

watchEffect(() => {
  if (carouselEl.value) {
    if (instance) {
      instance.dispose();
    }
    instance = panzoom(carouselEl.value[imgIndex.value].$el);
  }
});
</script>

<template>
  <v-container fluid class="d-flex pa-1">
    <div style="flex-grow: 4">
      <v-carousel
        v-if="frames"
        hide-delimiters
        progress="primary"
        class="fill-height"
        v-model="imgIndex"
      >
        <v-carousel-item v-for="(frame, i) in frames" :key="i" ref="carouselEl">
          <v-img :src="createUrl(framesUrl, frame)" :aspect-ratio="16 / 9">
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular
                  indeterminate
                  color="grey lighten-5"
                ></v-progress-circular>
              </v-row>
            </template>
          </v-img>
        </v-carousel-item>
      </v-carousel>
    </div>
    <div style="flex-grow: 1" class="ml-1">
      <v-img
        :src="createUrl(framesUrl, framesList[imgIndex])"
        :aspect-ratio="16 / 9"
        :eager="true"
      />
    </div>
  </v-container>
</template>
