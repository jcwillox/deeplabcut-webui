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
const url = ref("");

const labelEditorEl = ref<InstanceType<typeof LabelEditor> | null>(null);

const imgCounter = ref(0);
const imgIndex = computed({
  get: () => imgCounter.value,
  set: value => {
    if (value < 0) {
      if (framesList.value.length > 0) {
        imgCounter.value = framesList.value.length - 1;
      } else {
        imgCounter.value = 0;
      }
    } else if (value >= framesList.value.length) {
      imgCounter.value = 0;
    } else {
      imgCounter.value = value;
    }
  }
});

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

const mapWidth = ref("0%");
const mapHeight = ref("0%");
const mapScale = ref(8);

const panZoomChange = (detail: PanzoomEventDetail) => {
  const width = labelEditorEl.value!.$el.getBoundingClientRect().width;
  const height = labelEditorEl.value!.$el.getBoundingClientRect().height;
  mapScale.value = detail.scale;
  mapWidth.value = ((width / 2 - detail.x) / width) * 100 + "%";
  mapHeight.value = ((height / 2 - detail.y) / height) * 100 + "%";
};
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
      >
        <div id="zoomBox"></div>
      </v-img>
    </div>
  </v-container>
</template>

<style scoped>
#zoomBox {
  border: 1px solid #d8dee9;
  position: relative;
  left: calc(v-bind("mapWidth") - 50% / v-bind("mapScale"));
  top: calc(v-bind("mapHeight") - 50% / v-bind("mapScale"));
  width: calc(100% / v-bind("mapScale"));
  height: calc(100% / v-bind("mapScale"));
}
</style>
