<script setup lang="ts">
import { useStore } from "@/stores/global";
import { createUrl } from "@/utils/fetch";
import Panzoom, { type PanzoomObject } from "@panzoom/panzoom";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { computed, onMounted, ref, watch } from "vue";
import type { VImg } from "vuetify/components";

defineProps<{
  image: string;
}>();

const emit = defineEmits<{
  (e: "panzoomchange", detail: PanzoomEventDetail): void;
}>();

const store = useStore();
const imgEl = ref<InstanceType<typeof VImg> | null>(null);
let instance: PanzoomObject | undefined;
let url = ref("");

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
</script>

<template>
  <div>
    <v-img
      ref="imgEl"
      :src="createUrl(framesUrl, image)"
      :aspect-ratio="16 / 9"
      :eager="true"
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
