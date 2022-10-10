<script setup lang="ts">
import { useFrames } from "@/stores";
import { createCachedUrl } from "@/utils";
import { ref } from "vue";
import { useRouter } from "vue-router";

const props = defineProps<{
  image?: string;
  onShowInVideo?: (frameNum: number) => void;
  onShowInLabel?: (image: string) => void;
  hideLabelBtn?: boolean;
}>();

const router = useRouter();
const frames = useFrames();
const dialog = ref(false);
const isDeleting = ref(false);

const deleteFrame = async () => {
  isDeleting.value = true;
  const { statusCode } = await frames.remove(props.image!);
  if (statusCode.value == 200) {
    await frames.update();
  }
  isDeleting.value = false;
  dialog.value = false;
};

const showInLabels = () => {
  if (props.onShowInLabel) {
    props.onShowInLabel(props.image!);
  } else {
    router.push({ name: "label", hash: "#" + props.image });
  }
  dialog.value = false;
};

const showInVideo = () => {
  const frameNumber = /\d+/.exec(props.image!)?.[0];
  if (frameNumber && props.onShowInVideo) {
    props.onShowInVideo(Number(frameNumber));
  } else {
    router.push({ name: "extract", hash: "#" + frameNumber });
  }
  dialog.value = false;
};
</script>

<template>
  <v-dialog v-model="dialog" width="1000px" max-width="calc(100% - 8px)">
    <template #activator="props">
      <slot name="activator" v-bind="{ ...props, showInVideo, showInLabels }" />
    </template>
    <v-card v-if="image">
      <v-toolbar color="primary" density="comfortable">
        <v-toolbar-title>{{ image }}</v-toolbar-title>
        <v-btn icon="mdi-close" @click="dialog = false" />
      </v-toolbar>
      <v-img
        :src="createCachedUrl(frames.framesUrl, image)"
        class="rounded ma-2"
        max-height="calc(100vh - 189px)"
      >
        <template #placeholder>
          <v-row class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular
              indeterminate
              color="grey-lighten-5"
            ></v-progress-circular>
          </v-row>
        </template>
      </v-img>
      <v-divider />
      <v-card-actions>
        <v-btn :loading="isDeleting" color="red" @click="deleteFrame">
          Delete
        </v-btn>
        <v-spacer />
        <v-btn :color="hideLabelBtn ? 'blue' : 'default'" @click="showInVideo">
          Show in Video
        </v-btn>
        <v-btn v-if="!hideLabelBtn" color="blue" @click="showInLabels">
          Show in Labels
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
