<script setup lang="ts">
import Panzoom, { type PanzoomObject } from "@panzoom/panzoom";
import type {
  MiscOptions,
  PanzoomEventDetail
} from "@panzoom/panzoom/dist/src/types";
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
  type Ref
} from "vue";

const props = defineProps<{
  coords: LabelsCoords;
  selected?: boolean;
  parent: PanzoomObject | null;
  colors: string[];
}>();

const emit = defineEmits<{
  (e: "panzoomchange", detail: PanzoomEventDetail): void;
}>();

const color = computed(() => props.colors[0]);
const boxShadow = computed(() => {
  const colors = [];
  if (props.colors.length > 1) {
    colors.push(props.colors[1]);
  }
  if (props.selected) {
    colors.push("white");
  }
  return colors
    .map((color, index) => {
      return `0 0 0 ${(index + 1) * 2}px ${color}`;
    })
    .join(", ");
});

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

// update position if coords change
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
    cursor: "auto",
    startX: props.coords.x,
    startY: props.coords.y,
    setTransform
  });

  labelEl.value!.addEventListener("panzoomchange", e => {
    emit("panzoomchange", (e as CustomEvent<PanzoomEventDetail>).detail);
  });
});

onBeforeUnmount(() => {
  panzoom.value?.destroy();
});

defineExpose({
  panzoom,
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
  border: 2px solid v-bind("color");
  box-shadow: v-bind("boxShadow");
  width: 12px;
  height: 12px;
}
</style>
