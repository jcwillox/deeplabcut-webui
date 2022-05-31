<script setup lang="ts">
import Panzoom, { type PanzoomObject } from "@panzoom/panzoom";
import type { MiscOptions } from "@panzoom/panzoom/dist/src/types";
import { onBeforeUnmount, onMounted, ref, watch, type Ref } from "vue";

const props = defineProps<{
  coords: LabelsCoords;
  selected?: boolean;
  parent: PanzoomObject | null;
  color: string;
}>();

const panzoom = ref<PanzoomObject | null>(null);
const labelEl: Ref<HTMLDivElement | null> = ref(null);

const resetPosition = () => {
  if (panzoom.value) {
    // coords must contain non-null values for this component to be rendered
    panzoom.value.reset({
      startX: props.coords.x!,
      startY: props.coords.y!,
      animate: false
    });
  } else {
    console.error("instance was not defined when updating coords");
  }
};

watch(() => props.coords, resetPosition);

const setTransform: MiscOptions["setTransform"] = (elem, { x, y, scale }) => {
  // adjust the panning according to the parents scale
  if (props.parent) {
    const parentScale = props.parent.getScale();
    panzoom.value?.setStyle(
      "transform",
      `scale(${scale / parentScale}) translate(${x}px, ${y}px)`
    );
  }
};

onMounted(() => {
  panzoom.value = Panzoom(labelEl.value!, {
    contain: "inside",
    startX: props.coords.x,
    startY: props.coords.y,
    setTransform
  });
});

onBeforeUnmount(() => {
  panzoom.value?.destroy();
});

defineExpose({
  panzoom: panzoom,
  resetPosition
});
</script>

<template>
  <div ref="labelEl" :class="{ selected }" />
</template>

<style scoped>
div {
  top: 0;
  left: 0;
  position: absolute;
  border-radius: 50%;
  border: 2px solid v-bind("props.color");
  width: 12px;
  height: 12px;
}
div.selected {
  box-shadow: 0 0 0 2px white;
}
</style>
