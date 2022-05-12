<script lang="ts">
export default {
  name: "ExtractView"
};
</script>

<script setup lang="ts">
import { useStore } from "@/stores/global";
import { createUrl, useFetch, useUrl } from "@/utils/fetch";
import type { VideoJsPlayer } from "video.js";
import { computed, ref, watch } from "vue";
import { VSlideGroup, VSlideGroupItem } from "vuetify/components";
import VideoJS from "../components/VideoJS.vue";

let player = $ref<InstanceType<typeof VideoJS> | null>(null);

const store = useStore();
const url = ref("");

// only update url when there is a video to prevent requesting broken urls
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
const streamUrl = useUrl(url, "stream");

const timecode = computed(() => player?.timecode || 0);
const frame = computed({
  get: () => player?.frame || 0,
  set: value => {
    player?.seekTo(Number(value));
  }
});

const playerReady = (videojs: VideoJsPlayer) => {
  console.log("player-ready", videojs);
};

const toggleVideo = () => {
  if (player?.videojs?.paused()) {
    player.videojs.play();
  } else {
    player?.videojs?.pause();
  }
};

// fetch the videos' fps from backend
const { data: details } = useFetch(url, { refetch: true }).get().json();
const fps = computed(() => (details.value ? details.value.fps : -1));

// fetch the list of currently extracted frames
const { data: frames, execute: refetchFrames } = useFetch(framesUrl, {
  refetch: true
})
  .get()
  .json();

const selectedFrame = ref<number | undefined>(undefined);
const framesList = computed<string[]>(() => (frames.value ? frames.value : []));

// reset the frames list and index when changing video
watch(framesUrl, () => {
  frames.value = null;
  selectedFrame.value = 0;
});

// extract frame logic
const extractFrame = async () => {
  player?.videojs?.pause();
  const { data, statusCode } = await useFetch(url.value + "/frames")
    .post({ frames: [frame.value] })
    .json();
  if (statusCode.value == 200) {
    await refetchFrames();
    selectedFrame.value = framesList.value.indexOf(data.value[0]);
  }
};

// change the player to the frame extracted from the images name
const clickFrame = (frameName: string) => {
  const frameNumber = /\d+/.exec(frameName);
  player?.seekTo(Number(frameNumber));
};
</script>

<template>
  <v-container fluid class="pa-0 fill-height">
    <div class="d-flex pa-2">
      <v-text-field
        label="Frame"
        variant="outlined"
        density="compact"
        v-model="frame"
        hide-details
        persistent-placeholder
      ></v-text-field>
      <v-text-field
        class="pl-2"
        label="Timecode"
        variant="outlined"
        density="compact"
        v-model="timecode"
        readonly
        hide-details
        persistent-placeholder
      ></v-text-field>
    </div>

    <VideoJS
      ref="player"
      :fps="fps"
      :src="streamUrl"
      @player-ready="playerReady"
      @keydown.space="toggleVideo"
      @keydown.left="() => player?.seekBackward()"
      @keydown.right="() => player?.seekForward()"
    ></VideoJS>

    <div class="d-flex align-center justify-center my-2" style="gap: 4px">
      <v-btn
        size="small"
        color="primary-darken-2"
        icon="mdi-chevron-double-left"
        @click="() => player?.seekBackward(10)"
      />
      <v-btn
        size="small"
        color="primary-darken-1"
        icon="mdi-chevron-left"
        @click="() => player?.seekBackward()"
      />
      <v-btn height="40" color="primary" @click="extractFrame" rounded>
        Extract
      </v-btn>
      <v-btn
        size="small"
        color="primary-darken-1"
        icon="mdi-chevron-right"
        @click="() => player?.seekForward()"
      />
      <v-btn
        size="small"
        color="primary-darken-2"
        icon="mdi-chevron-double-right"
        @click="() => player?.seekForward(10)"
      />
    </div>

    <VSlideGroup
      v-if="store.video"
      v-model="selectedFrame"
      class="my-3 mt-4 elevation-1"
      center-active
      show-arrows
    >
      <VSlideGroupItem
        v-for="image in framesList"
        :key="image"
        v-slot="{ toggle }"
      >
        <v-card class="ma-4" width="100" @click="toggle">
          <div class="d-flex fill-height align-center justify-center">
            <v-img
              :src="createUrl(framesUrl, image)"
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
      </VSlideGroupItem>
    </VSlideGroup>
  </v-container>
</template>
