<script setup lang="ts">
import LabelMarker from "@/components/LabelMarker.vue";
import { useFrames } from "@/stores";
import { createCachedUrl } from "@/utils/fetch";
import Panzoom, { type PanzoomObject } from "@panzoom/panzoom";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { useResizeObserver } from "@vueuse/core";
import { onMounted, ref, watch, type Ref } from "vue";
import type { VImg } from "vuetify/components";

const props = defineProps<{
  image?: string;
  labels: LabelsModel | null;
  selected?: string;
}>();

const emit = defineEmits<{
  (e: "panzoomchange", detail: PanzoomEventDetail): void;
}>();

// the pan x/y calculations are relative to the origin which is the center of
// the element. This means the axes flip based on what quadrant the image is
// panned into;
//   top-left     +x +y
//   bottom-left  +x -y
//   bottom-right -x -y
//   top-right    -x +y
// additionally, pixels are effectively removed / added to the bottom-right
// when resizing, meaning that the origin moves towards the bottom-right
// when resizing the image.
const calcRelativeToOrigin = (
  x?: number | null,
  y?: number | null,
  offsetX = 0,
  offsetY = 0
) => {
  if (
    x &&
    y &&
    parentEl.value &&
    imgEl.value?.image?.naturalWidth &&
    imgEl.value?.image?.naturalHeight
  ) {
    const width = parentEl.value.getBoundingClientRect().width;
    const height = parentEl.value.getBoundingClientRect().height;
    const naturalWidth = imgEl.value.image.naturalWidth;
    const naturalHeight = imgEl.value.image.naturalHeight;

    const scale = panzoom.value?.getScale() || 1;

    const tX = ((x / naturalWidth) * width + offsetX) * scale;
    const tY = ((y / naturalHeight) * height + offsetY) * scale;

    return { x: tX, y: tY };
  }
};

const frames = useFrames();
const panzoom = ref<PanzoomObject | null>(null);

const imgEl = ref<InstanceType<typeof VImg> | null>(null);
const parentEl: Ref<HTMLDivElement | null> = ref(null);
const labelMarkerEls = ref<InstanceType<typeof LabelMarker>[] | null>(null);

const labelItems = ref<[string, string, LabelsCoords][]>([]);
const updateLabelItems = () => {
  const items: [string, string, LabelsCoords][] = [];
  if (props.image && props.labels) {
    const individuals = props.labels[props.image];
    for (const individual in individuals) {
      const bodyparts = individuals[individual];
      for (const bodypart in bodyparts) {
        const coords = bodyparts[bodypart];
        const newCoords = calcRelativeToOrigin(coords.x, coords.y, -6, -6);
        if (newCoords) {
          items.push([individual, bodypart, newCoords]);
        }
      }
    }
  }
  labelItems.value = items;
};

watch([() => props.image, () => props.labels], updateLabelItems);

// when the element is resized we need to update the minimap
// as well as account for the new dimensions when making calculations
useResizeObserver(parentEl, () => {
  updateLabelItems();
});

onMounted(() => {
  panzoom.value = Panzoom(imgEl.value!.$el, {
    maxScale: 32,
    contain: "outside"
  });

  imgEl.value!.$el.addEventListener("panzoomchange", (e: CustomEvent) =>
    emit("panzoomchange", e.detail)
  );

  // link all label markers to the images zooming
  parentEl.value!.addEventListener("wheel", (event: WheelEvent) => {
    const oldScale = panzoom.value!.getScale();
    panzoom.value!.zoomWithWheel(event);

    if (labelMarkerEls.value) {
      const newScale = panzoom.value!.getScale();
      for (const labelMarkerEl of labelMarkerEls.value) {
        if (labelMarkerEl.panzoom) {
          const pan = labelMarkerEl.panzoom.getPan();
          labelMarkerEl.panzoom.pan(
            (pan.x / oldScale) * newScale,
            (pan.y / oldScale) * newScale
          );
        } else {
          console.error("panzoom was null on labelMarkerEl");
        }
      }
    }
  });
});

const aspectRatio = ref<number | undefined>(undefined);
const aspectRatioString = ref<string | undefined>(undefined);

const handleImgLoad = () => {
  if (imgEl.value && imgEl.value.image) {
    aspectRatio.value =
      imgEl.value.image.naturalWidth / imgEl.value.image.naturalHeight;
    aspectRatioString.value = `${imgEl.value.image.naturalWidth}/${imgEl.value.image.naturalHeight}`;
  }
};

defineExpose({
  aspectRatio,
  aspectRatioString
});
</script>

<template>
  <div ref="parentEl">
    <v-img
      ref="imgEl"
      :src="createCachedUrl(frames.framesUrl, image)"
      :aspect-ratio="aspectRatio"
      @load="handleImgLoad"
    >
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
      <LabelMarker
        ref="labelMarkerEls"
        v-for="[individual, bodypart, coords] in labelItems"
        :key="`${individual}-${bodypart}`"
        :coords="coords"
        :parent="panzoom"
        :selected="`${individual}-${bodypart}` === props.selected"
      />
    </v-img>
  </div>
</template>
