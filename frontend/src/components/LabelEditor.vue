<script setup lang="ts">
import { useStore } from "@/stores";
import { createCachedUrl } from "@/utils/fetch";
import Panzoom, { type PanzoomObject } from "@panzoom/panzoom";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { computed, onMounted, ref } from "vue";
import type { VImg } from "vuetify/components";

defineProps<{
  image?: string;
}>();

const emit = defineEmits<{
  (e: "panzoomchange", detail: PanzoomEventDetail): void;
}>();

const store = useStore();
const imgEl = ref<InstanceType<typeof VImg> | null>(null);
const framesUrl = computed(() => "/videos/" + store.video + "/frames");

let instance: PanzoomObject | undefined;

onMounted(() => {
  instance = Panzoom(imgEl.value!.$el, {
    maxScale: 32,
    contain: "outside"
  });
  imgEl.value!.$el.addEventListener("panzoomchange", (e: CustomEvent) =>
    emit("panzoomchange", e.detail)
  );
  imgEl.value!.$el.parentElement.addEventListener(
    "wheel",
    instance.zoomWithWheel
  );
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
  <div>
    <v-img
      ref="imgEl"
      :src="createCachedUrl(framesUrl, image)"
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
    </v-img>
  </div>
</template>
