<script setup lang="ts">
import AdvImg from "@/components/AdvImg.vue";
import LabelMarker from "@/components/LabelMarker.vue";
import { useConfig, useFrames, useLabels } from "@/stores";
import { createCachedUrl } from "@/utils/fetch";
import Panzoom, { type PanzoomObject } from "@panzoom/panzoom";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { useResizeObserver } from "@vueuse/core";
import { storeToRefs } from "pinia";
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
  type Ref
} from "vue";

const props = defineProps<{
  opened?: string[];
  selected?: string[];
}>();

const emit = defineEmits<{
  (e: "panzoomchange", detail: PanzoomEventDetail): void;
  (e: "update:opened", opened: string[]): void;
  (e: "update:selected", selected: string[]): void;
}>();

const opened = computed({
  get: () => props.opened?.[0],
  set: value => {
    emit("update:opened", value ? [value] : []);
  }
});

const selected = computed({
  get: () => props.selected?.[0],
  set: value => {
    emit("update:selected", value ? [value] : []);
  }
});

const frames = useFrames();
const labelsStore = useLabels();
const { config, colors, colorsIndividuals } = storeToRefs(useConfig());
const { bodyparts, hasCoords, updateLabel } = labelsStore;
const { image, individuals } = storeToRefs(labelsStore);

const panzoom = ref<PanzoomObject | null>(null);

const imgEl = ref<InstanceType<typeof AdvImg> | null>(null);
const parentEl: Ref<HTMLDivElement | null> = ref(null);
const labelMarkerEls = ref<InstanceType<typeof LabelMarker>[] | null>(null);

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
    imgEl.value?.naturalWidth &&
    imgEl.value?.naturalHeight
  ) {
    const width = parentEl.value.getBoundingClientRect().width;
    const height = parentEl.value.getBoundingClientRect().height;
    const naturalWidth = imgEl.value.naturalWidth;
    const naturalHeight = imgEl.value.naturalHeight;

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
    imgEl.value?.naturalWidth &&
    imgEl.value?.naturalHeight
  ) {
    const scale = panzoom.value?.getScale() || 1;
    const rect = parentEl.value.getBoundingClientRect();
    const naturalWidth = imgEl.value.naturalWidth;
    const naturalHeight = imgEl.value.naturalHeight;

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

const labelItems = ref<[string, string, LabelsCoords, string[]][]>([]);
const updateLabelItems = () => {
  const items: [string, string, LabelsCoords, string[]][] = [];
  if (parentEl.value?.clientHeight) {
    for (const { i, j, individual, bodypart, coords } of bodyparts()) {
      const newCoords = calcRelativeToOrigin(coords?.x, coords?.y, -6, -6);
      if (newCoords) {
        const colors_ = [colors.value[j] || "white"];
        if (config.value?.multi_animal) {
          colors_.push(colorsIndividuals.value[i]);
        }
        items.push([individual, bodypart, newCoords, colors_]);
      }
    }
  }
  labelItems.value = items;
};

watch([individuals, config], updateLabelItems);

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
      updateLabel(individual, bodypart, coords);
    }
  }
};

const handleClick = (ev: MouseEvent) => {
  if (!selected.value || !config.value) {
    return;
  }
  for (const { i, j, individual, bodypart, coords } of bodyparts()) {
    if (`${individual}-${bodypart}` == selected.value) {
      if (!hasCoords(coords)) {
        const relativeCoords = calcPointFromCorner(ev.clientX, ev.clientY);
        const trueCoords = calcFixedFromCorner(
          relativeCoords!.x,
          relativeCoords!.y
        );
        if (trueCoords) {
          updateLabel(individual, bodypart, trueCoords);

          const { individuals, bodyparts } = config.value;
          if (bodyparts.length > j + 1) {
            // select next bodypart
            selected.value = `${individual}-${bodyparts[j + 1]}`;
          } else if (individuals.length > i + 1) {
            // select next individual
            opened.value = individuals[i + 1];
            selected.value = `${individuals[i + 1]}-${bodyparts[0]}`;
          } else {
            // clear selection as there is no next individual or bodypart
            selected.value = undefined;
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
    contain: "outside",
    cursor: "auto"
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

onBeforeUnmount(() => {
  panzoom.value?.destroy();
  panzoom.value = null;
});

defineExpose({
  resetZoom
});
</script>

<template>
  <div ref="parentEl">
    <AdvImg
      ref="imgEl"
      :src="createCachedUrl(frames.framesUrl, image)"
      @load="updateLabelItems"
      @click="handleClick"
    >
      <LabelMarker
        ref="labelMarkerEls"
        v-for="[individual, bodypart, coords, colors] in labelItems"
        :key="`${individual}-${bodypart}`"
        :coords="coords"
        :colors="colors"
        :parent="panzoom"
        :selected="`${individual}-${bodypart}` === selected"
        @panzoomchange="
          detail => handlePanzoomChange(individual, bodypart, detail)
        "
      />
    </AdvImg>
  </div>
</template>
