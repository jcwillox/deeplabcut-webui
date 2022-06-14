<script lang="ts">
export default {
  name: "ExtractView"
};
</script>

<script setup lang="ts">
import { useFrames, useStore } from "@/stores";
import { useHotkeys } from "@/utils";
import { createCachedUrl, useFetch } from "@/utils/fetch";
import { computed, ref, watch } from "vue";
import { VSlideGroup, VSlideGroupItem } from "vuetify/components";
import VideoJS from "../components/VideoJS.vue";

const store = useStore();
const frames = useFrames();
const player = ref<InstanceType<typeof VideoJS> | null>(null);

const videoUrl = computed(() => "/videos/" + store.video);
const framesUrl = computed(() => videoUrl.value + "/frames");

const timecode = computed(() => player.value?.timecode || 0);
const frame = computed({
  get: () => player.value?.frame || 0,
  set: value => {
    player.value?.seekTo(Number(value));
  }
});

const toggleVideo = () => {
  if (player.value?.videojs?.paused()) {
    player.value.videojs.play();
  } else {
    player.value?.videojs?.pause();
  }
};

// fetch the videos' fps from backend
const { data: details } = useFetch(videoUrl, { refetch: true }).get().json();
const fps = computed(() => (details.value ? details.value.fps : -1));
const selectedFrame = ref<number | undefined>(undefined);

// reset selected frame changing video
watch(
  () => frames.items,
  () => {
    if (frames.items.length == 0) {
      selectedFrame.value = 0;
    }
  }
);

// extract frame logic
const extractFrame = async () => {
  player.value?.videojs?.pause();
  const { data, statusCode } = await frames.extract(frame.value);
  if (statusCode.value == 200) {
    await frames.update();
    selectedFrame.value = frames.items.indexOf(data.value[0]);
  }
};

// change the player to the frame extracted from the images name
const clickFrame = (frameName: string) => {
  const frameNumber = /\d+/.exec(frameName);
  player.value?.seekTo(Number(frameNumber));
};

// define hotkeys
useHotkeys("a", () => {
  player.value?.seekBackward(1);
});
useHotkeys("shift+a", () => {
  player.value?.seekBackward(10);
});
useHotkeys("d", () => {
  player.value?.seekForward(1);
});
useHotkeys("shift+d", () => {
  player.value?.seekForward(10);
});
useHotkeys("shift+e", () => {
  extractFrame();
});
useHotkeys("space", () => {
  toggleVideo();
  return false;
});
</script>

<template>
  <v-container class="pa-0 fill-height" fluid>
    <VideoJS
      ref="player"
      :fps="fps"
      :src="createCachedUrl(videoUrl, 'stream')"
      max-height-offset="136px"
    ></VideoJS>

    <div class="d-flex px-2 py-1 align-center justify-center">
      <v-text-field
        label="Frame"
        v-model="frame"
        color="primary"
        variant="outlined"
        density="compact"
        style="max-width: 164px"
        type="number"
        hide-details
        persistent-placeholder
      ></v-text-field>
      <div
        class="d-flex align-center justify-center my-2 mx-2 mx-sm-6"
        style="gap: 4px"
      >
        <v-btn
          size="small"
          color="primary-darken-2"
          @click="player?.seekBackward(10)"
          icon
        >
          <v-icon size="small">mdi-chevron-double-left</v-icon>
          <v-tooltip activator="parent" location="top">
            Back 10 frames <kbd>Shift</kbd><kbd>A</kbd>
          </v-tooltip>
        </v-btn>
        <v-btn
          size="small"
          color="primary-darken-1"
          @click="player?.seekBackward()"
          icon
        >
          <v-icon size="small">mdi-chevron-left</v-icon>
          <v-tooltip activator="parent" location="top">
            Back 1 frame <kbd>A</kbd>
          </v-tooltip>
        </v-btn>
        <v-btn height="40" color="primary" @click="extractFrame" rounded>
          Extract
          <v-tooltip activator="parent" location="top">
            <kbd>Shift</kbd><kbd>E</kbd>
          </v-tooltip>
        </v-btn>
        <v-btn
          size="small"
          color="primary-darken-1"
          @click="player?.seekForward()"
          icon
        >
          <v-icon size="small">mdi-chevron-right</v-icon>
          <v-tooltip activator="parent" location="top">
            Forward 1 frame <kbd>D</kbd>
          </v-tooltip>
        </v-btn>
        <v-btn
          size="small"
          color="primary-darken-2"
          @click="player?.seekForward(10)"
          icon
        >
          <v-icon size="small">mdi-chevron-double-right</v-icon>
          <v-tooltip activator="parent" location="top">
            Forward 10 frames <kbd>Shift</kbd><kbd>D</kbd>
          </v-tooltip>
        </v-btn>
      </div>
      <v-text-field
        label="Timecode"
        v-model="timecode"
        color="primary"
        variant="outlined"
        density="compact"
        style="max-width: 164px"
        readonly
        hide-details
        persistent-placeholder
      ></v-text-field>
    </div>

    <v-slide-group
      v-if="store.video"
      v-model="selectedFrame"
      class="mb-3 mt-1 elevation-1"
      center-active
      show-arrows
    >
      <v-slide-group-item
        v-for="image in frames.items"
        :key="image"
        v-slot="{ toggle }"
      >
        <v-card class="ma-4" width="100" @click="toggle">
          <div class="d-flex fill-height align-center justify-center">
            <v-img
              :src="createCachedUrl(framesUrl, image)"
              @click="clickFrame(image)"
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
        </v-card>
      </v-slide-group-item>
    </v-slide-group>
  </v-container>
</template>
