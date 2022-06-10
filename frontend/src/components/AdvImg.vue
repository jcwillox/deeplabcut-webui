<script setup lang="ts">
import { ref, type Ref } from "vue";

defineProps<{
  src?: string;
  alt?: string;
}>();

const emit = defineEmits<{
  (e: "load", imgEl: HTMLImageElement): void;
}>();

const imgEl: Ref<HTMLImageElement | null> = ref(null);

const aspectRatio = ref<string | undefined>(undefined);
const naturalWidth = ref<number | null>(null);
const naturalHeight = ref<number | null>(null);

const onLoad = () => {
  if (imgEl.value) {
    aspectRatio.value = `${imgEl.value.naturalWidth}/${imgEl.value.naturalHeight}`;
    naturalWidth.value = imgEl.value.naturalWidth;
    naturalHeight.value = imgEl.value.naturalHeight;
    emit("load", imgEl.value);
  }
};

defineExpose({
  aspectRatio,
  image: imgEl,
  naturalWidth,
  naturalHeight
});
</script>

<template>
  <div>
    <img ref="imgEl" :src="src" :alt="alt" @load="onLoad" />
    <slot></slot>
  </div>
</template>

<style scoped>
div {
  aspect-ratio: v-bind("aspectRatio");
  position: relative;
  overflow: hidden;
}
img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
