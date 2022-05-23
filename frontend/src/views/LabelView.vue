<script lang="ts">
export default {
  name: "LabelView"
};
</script>

<script setup lang="ts">
import LabelEditor from "@/components/LabelEditor.vue";
import { useFrames, useStore } from "@/stores";
import { createCachedUrl, useFetch } from "@/utils/fetch";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { computed, ref, watch } from "vue";

const store = useStore();
const frames = useFrames();
const framesUrl = computed(() => "/videos/" + store.video + "/frames");

const labelEditorEl = ref<InstanceType<typeof LabelEditor> | null>(null);

const labelsUrl = computed(() => "/videos/" + store.video + "/labels");
const { data: labels } = useFetch(labelsUrl, { refetch: true }).get().json();

const imgIndex = ref(0);
const updateIndex = (n: number) => {
  if (frames.items.length == 0) {
    imgIndex.value = 0;
  } else {
    const length = frames.items.length;
    imgIndex.value = (((imgIndex.value + n) % length) + length) % length;
  }
};

// reset selected frame when changing video
watch(
  () => frames.items,
  () => {
    if (frames.items.length == 0) {
      imgIndex.value = 0;
    }
  }
);

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
        @click="updateIndex(-1)"
      ></v-btn>
      <LabelEditor
        class="flex-grow-1"
        :image="frames.items[imgIndex]"
        ref="labelEditorEl"
        @panzoomchange="panZoomChange"
      />
      <v-btn
        class="h-100 rounded-0"
        icon="mdi-chevron-right"
        variant="plain"
        size="small"
        @click="updateIndex(1)"
      ></v-btn>
    </div>
    <div style="flex-grow: 1" class="ml-1">
      <v-img
        v-if="store.video"
        :src="createCachedUrl(framesUrl, frames.items[imgIndex])"
        :aspect-ratio="16 / 9"
        :eager="true"
      >
        <div id="zoomBox"></div>
      </v-img>

      <v-list v-if="labels">
        <v-list-group
          v-for="(label, key) in labels[frames.items[imgIndex]]"
          :key="key"
        >
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              :title="(key as unknown as string)"
              :value="key"
            ></v-list-item>
          </template>

          <v-list-item
            v-for="(coord, bodypart) in labels[frames.items[imgIndex]][key]"
            :key="bodypart"
            :value="bodypart"
            :title="(bodypart as unknown as string)"
            :subtitle="`x: ${
              labels[frames.items[imgIndex]][key][bodypart]['x']
            },  y: ${labels[frames.items[imgIndex]][key][bodypart]['y']}`"
            prepend-icon="mdi-circle"
          ></v-list-item>
        </v-list-group>
      </v-list>
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
