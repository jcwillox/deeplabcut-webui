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
  colors: string[];
}>();

const emit = defineEmits<{
  (e: "panzoomchange", detail: PanzoomEventDetail): void;
  (e: "update:labels", labels: LabelsModel): void;
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

const calcFixedFromCorner = (
  x: number,
  y: number,
  offsetX = 0,
  offsetY = 0
) => {
  if (
    parentEl.value &&
    imgEl.value?.image?.naturalWidth &&
    imgEl.value?.image?.naturalHeight
  ) {
    const scale = panzoom.value?.getScale() || 1;
    const rect = parentEl.value.getBoundingClientRect();
    const naturalWidth = imgEl.value.image.naturalWidth;
    const naturalHeight = imgEl.value.image.naturalHeight;

    const tX = ((x / scale - offsetX) / rect.width) * naturalWidth;
    const tY = ((y / scale - offsetY) / rect.height) * naturalHeight;

    return { x: tX, y: tY };
  }
};

const calcPointFromCorner = (clientX: number, clientY: number) => {
  if (imgEl.value && parentEl.value && panzoom.value) {
    const parentRect = parentEl.value.getBoundingClientRect();
    const rect: DOMRect = imgEl.value.$el.getBoundingClientRect();

    let tX = clientX - parentRect.left;
    let tY = clientY - parentRect.top;
    tX -= rect.left - parentRect.left;
    tY -= rect.top - parentRect.top;

    return { x: tX, y: tY };
  }
};

const frames = useFrames();
const panzoom = ref<PanzoomObject | null>(null);

const imgEl = ref<InstanceType<typeof VImg> | null>(null);
const parentEl: Ref<HTMLDivElement | null> = ref(null);
const labelMarkerEls = ref<InstanceType<typeof LabelMarker>[] | null>(null);

function* bodyparts(image?: string, labels?: LabelsModel | null) {
  if (labels && image) {
    const individuals = labels[image];
    for (const individual in individuals) {
      const bodyparts = individuals[individual];
      let index = 0;
      for (const bodypart in bodyparts) {
        const coords = bodyparts[bodypart];
        yield { individual, bodypart, coords, index };
        index++;
      }
    }
  }
}

const labelItems = ref<[string, string, LabelsCoords, string][]>([]);
const updateLabelItems = () => {
  const items: [string, string, LabelsCoords, string][] = [];
  const iterBodyparts = bodyparts(props.image, props.labels);
  for (const { individual, bodypart, coords, index } of iterBodyparts) {
    const newCoords = calcRelativeToOrigin(coords.x, coords.y, -6, -6);
    if (newCoords) {
      items.push([individual, bodypart, newCoords, props.colors[index]]);
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

const handlePanzoomChange = (
  individual: string,
  bodypart: string,
  detail: PanzoomEventDetail
) => {
  // only trigger when initiated by a user
  if (detail.originalEvent?.isTrusted) {
    const coords = calcFixedFromCorner(detail.x, detail.y, -6, -6);
    if (coords) {
      emit("update:labels", {
        [props.image!]: {
          [individual]: {
            [bodypart]: coords
          }
        }
      });
    }
  }
};

const handleClick = (ev: MouseEvent) => {
  if (props.selected) {
    const iterBodyparts = bodyparts(props.image, props.labels);
    for (const { individual, bodypart, coords } of iterBodyparts) {
      if (`${individual}-${bodypart}` == props.selected) {
        if (!(coords.x && coords.y)) {
          const relativeCoords = calcPointFromCorner(ev.clientX, ev.clientY);
          const trueCoords = calcFixedFromCorner(
            relativeCoords!.x,
            relativeCoords!.y
          );
          if (trueCoords) {
            emit("update:labels", {
              [props.image!]: {
                [individual]: {
                  [bodypart]: trueCoords
                }
              }
            });
          }
        }
      }
    }
  }
};

const resetZoom = () => {
  panzoom.value?.reset({ animate: false });
  if (labelMarkerEls.value) {
    for (const labelMarkerEl of labelMarkerEls.value) {
      labelMarkerEl.resetPosition();
    }
  }
};

onMounted(() => {
  panzoom.value = Panzoom(imgEl.value!.$el, {
    maxScale: 32,
    contain: "outside"
  });

  imgEl.value!.$el.addEventListener(
    "panzoomchange",
    (e: CustomEvent<PanzoomEventDetail>) => emit("panzoomchange", e.detail)
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

// handle changing aspect ratio
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
  aspectRatioString,
  resetZoom
});
</script>

<template>
  <div ref="parentEl">
    <v-img
      ref="imgEl"
      :src="createCachedUrl(frames.framesUrl, image)"
      :aspect-ratio="aspectRatio"
      @load="handleImgLoad"
      @click="handleClick"
    >
      <template #placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
      <LabelMarker
        ref="labelMarkerEls"
        v-for="[individual, bodypart, coords, color] in labelItems"
        :key="`${individual}-${bodypart}`"
        :coords="coords"
        :color="color"
        :parent="panzoom"
        :selected="`${individual}-${bodypart}` === props.selected"
        @panzoomchange="
          detail => handlePanzoomChange(individual, bodypart, detail)
        "
      />
    </v-img>
  </div>
</template>
