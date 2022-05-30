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
const dialog = ref(false);
const frames = useFrames();
const framesUrl = computed(() => "/videos/" + store.video + "/frames");

const labelEditorEl = ref<InstanceType<typeof LabelEditor> | null>(null);

const labelsUrl = computed(() => "/videos/" + store.video + "/labels");
const { data: labels } = useFetch<string>(labelsUrl, { refetch: true })
  .get()
  .json<LabelsModel>();

const imgIndex = ref(0);
const updateIndex = (n: number) => {
  if (frames.items.length == 0) {
    imgIndex.value = 0;
  } else {
    const length = frames.items.length;
    imgIndex.value = (((imgIndex.value + n) % length) + length) % length;
  }
};

const image = computed<string>(() => frames.items[imgIndex.value]);
const individuals = computed<LabelsIndividuals>(() =>
  labels.value ? labels.value[image.value] : {}
);

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
const mapScale = ref(1);

const panZoomChange = (detail: PanzoomEventDetail) => {
  const width = labelEditorEl.value!.$el.getBoundingClientRect().width;
  const height = labelEditorEl.value!.$el.getBoundingClientRect().height;
  mapScale.value = detail.scale;
  mapWidth.value = ((width / 2 - detail.x) / width) * 100 + "%";
  mapHeight.value = ((height / 2 - detail.y) / height) * 100 + "%";
};

const opened = ref();
const selected = ref();

// ensure exactly one individual is open
watch(opened, (value: string[], oldValue: string[]) => {
  if (opened.value.length == 2) {
    opened.value.shift();
  } else if (value.length == 0) {
    opened.value = oldValue;
  }
});

// set first individual as open when loaded
watch(individuals, (value, oldValue) => {
  if (value && (!oldValue || Object.keys(oldValue).length == 0)) {
    opened.value = [Object.keys(value).shift()];
  }
});

const createSubtitle = (coords: LabelsCoords) => {
  let output = "";
  if (coords.x) {
    output += "x: " + Math.round(coords.x);
    if (coords.y) {
      output += " • ";
    }
  }
  if (coords.y) {
    output += "y: " + Math.round(coords.y);
  }
  return output;
};
</script>

<template>
  <v-container
    class="d-flex flex-wrap flex-sm-nowrap justify-center pa-1"
    style="max-height: calc(100vh - 80px)"
    fluid
  >
    <div
      class="flex-grow-1"
      :style="{
        maxWidth: `calc((100vh - 80px) * ${labelEditorEl?.aspectRatioString} + 80px)`
      }"
    >
      <div class="d-flex">
        <v-btn
          class="rounded-0 rounded-s h-auto"
          icon="mdi-chevron-left"
          size="small"
          style="background-color: rgb(var(--v-theme-on-surface-variant))"
          variant="plain"
          @click="updateIndex(-1)"
        ></v-btn>
        <LabelEditor
          ref="labelEditorEl"
          :image="frames.items[imgIndex]"
          :labels="labels"
          class="flex-grow-1"
          @panzoomchange="panZoomChange"
        >
        </LabelEditor>
        <v-btn
          class="rounded-0 rounded-e h-auto"
          icon="mdi-chevron-right"
          variant="plain"
          size="small"
          style="background-color: rgb(var(--v-theme-on-surface-variant))"
          @click="updateIndex(1)"
        ></v-btn>
      </div>
    </div>
    <div class="d-flex flex-column pl-1 w-25" style="max-width: 280px">
      <v-img
        v-if="store.video"
        :src="createCachedUrl(framesUrl, frames.items[imgIndex])"
        :aspect-ratio="labelEditorEl?.aspectRatio"
        class="flex-grow-0"
      >
        <div id="zoomBox" />
      </v-img>

      <v-list
        v-if="labels"
        v-model:opened="opened"
        v-model:selected="selected"
        class="overflow-y-auto"
      >
        <v-list-group
          v-for="(bodyparts, individual) in individuals"
          :key="individual"
          :value="individual"
        >
          <template v-slot:activator="{ props }">
            <v-list-item v-bind="props" active-color="blue" :value="individual">
              <v-list-item-header>
                <v-list-item-title class="text-capitalize">
                  {{ individual }}
                </v-list-item-title>
              </v-list-item-header>
            </v-list-item>
          </template>

          <v-list-item
            v-for="(coords, bodypart) in bodyparts"
            :key="`${individual}-${bodypart}`"
            :value="`${individual}-${bodypart}`"
          >
            <v-list-item-avatar start>
              <v-icon>mdi-circle</v-icon>
            </v-list-item-avatar>
            <v-list-item-header>
              <v-list-item-title>{{ bodypart }}</v-list-item-title>
              <v-list-item-subtitle>{{
                createSubtitle(coords)
              }}</v-list-item-subtitle>
            </v-list-item-header>
          </v-list-item>
        </v-list-group>
      </v-list>
    </div>
  </v-container>
  <v-container fluid class="d-flex align-center justify-center my-2">
    <v-row justify="center">
      <v-dialog v-model="dialog">
        <template v-slot:activator="{ props }">
          <v-btn color="primary" rounded v-bind="props">
            Frame: {{ imgIndex + 1 }} of {{ frames.items.length }}
          </v-btn>
        </template>
        <v-toolbar color="primary" class="rounded-t">
          <v-toolbar-title>Select Frame</v-toolbar-title>
          <v-spacer />
          <v-btn icon="mdi-close" @click="dialog = false" />
        </v-toolbar>
        <v-card style="height: calc(100vh - 104px)" class="rounded-t-0">
          <v-card-content>
            <v-row class="text-center" justify="center">
              <v-col v-for="(frame, i) in frames.items" :key="i" cols="auto">
                <div>
                  <v-img
                    :style="
                      i === imgIndex && { border: '5px solid yellowgreen' }
                    "
                    :src="createCachedUrl(framesUrl, frame)"
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
    </v-row>
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

.v-list-group__items .v-list-item {
  padding-inline-start: calc(8px + var(--indent-padding)) !important;
}
</style>
