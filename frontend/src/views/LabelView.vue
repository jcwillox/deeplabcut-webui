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
const dialog = ref(false);

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
  <v-container fluid class="d-flex align-center justify-center my-2">
    <v-row justify="center">
      <v-dialog v-model="dialog">
        <template v-slot:activator="{ props }">
          <v-btn color="primary" rounded v-bind="props">
            Frame: {{ imgIndex + 1 }} of {{ framesList.length }}
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="text-h5"> Select Frame </span>
          </v-card-title>
          <v-card-content>
            <v-row class="text-center" justify="center">
              <v-col v-for="(frame, i) in frames" :key="i" cols="auto">
                <div>
                  <v-img
                    :style="
                      i === imgIndex && { border: '5px solid yellowgreen' }
                    "
                    :src="createUrl(framesUrl, frame)"
                    :aspect-ratio="16 / 9"
                    :width="400"
                    @click="
                      imgIndex = i;
                      dialog = false;
                    "
                    cover
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
    </v-row>
  </v-container>
</template>
