<script lang="ts">
export default {
  name: "LabelView"
};
</script>

<script setup lang="ts">
import LabelEditor from "@/components/LabelEditor.vue";
import { useStore } from "@/stores/global";
import { createUrl, useFetch } from "@/utils/fetch";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { computed, ref, watch } from "vue";

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
    <div class="d-flex flex-row align-center" style="flex-grow: 4">
      <v-btn
        class="h-100 rounded-0"
        icon="mdi-chevron-left"
        variant="plain"
        size="small"
        @click="imgIndex--"
      ></v-btn>
      <LabelEditor
        class="flex-grow-1"
        :image="framesList[imgIndex]"
        ref="labelEditorEl"
        @panzoomchange="panZoomChange"
      />
      <v-btn
        class="h-100 rounded-0"
        icon="mdi-chevron-right"
        variant="plain"
        size="small"
        @click="imgIndex++"
      ></v-btn>
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
