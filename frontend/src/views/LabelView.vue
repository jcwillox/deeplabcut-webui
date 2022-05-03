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

const { data: frames, execute: refetchFrames } = useFetch(framesUrl, {
  refetch: true
})
  .get()
  .json();

let instance: PanZoom | undefined;

watchEffect(() => {
  if (carouselEl.value) {
    if (instance) {
      instance.dispose();
    }
    instance = panzoom(carouselEl.value[imgIndex.value].$el);
    //console.log(carouselEl.value[imgIndex.value].$el.firstElementChild);
  }
});
/*
const carouselChangeHandler = (index: number) => {
  console.log(`index ${index} `);
  if (carouselEl.value) {
    if (instance) {
      instance.dispose();
    }
    instance = panzoom(carouselEl.value[index].$el);
    //console.log(carouselEl.value[imgIndex.value].$el.firstElementChild);
  }
};
*/
</script>

<template>
  <div id="labeller" style="display: flex">
    <div id="main" style="border-style: solid; width: 80%; height: 1000px">
      <div id="carousel" style="border-style: dotted">
        <v-carousel
          hide-delimiters
          progress="primary"
          v-if="frames"
          class="fill-height"
          v-model="imgIndex"
        >
          <v-carousel-item
            v-for="(frame, i) in frames"
            :key="i"
            ref="carouselEl"
          >
            <v-img :src="createUrl(framesUrl, frame)">
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
    </div>

    <div id="sidebar" style="border-style: solid; width: 20%">
      <div id="miniview" style="border-style: solid">
        <v-img :src="createUrl(framesUrl, frames[imgIndex])" :eager="true" />
      </div>
    </div>
  </div>
</template>
