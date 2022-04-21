<script setup lang="ts">
import { useStore } from "@/stores/global";
import { createUrl, useFetch, useUrl } from "@/utils/fetch";
import type { VideoJsPlayer } from "video.js";
import { computed, ref, watch, type Ref } from "vue";
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
  </v-container>
</template>
