<script setup lang="ts">
import { useStore } from "@/stores/global";
import { useFetch } from "@/utils/fetch";
import type { VideoJsPlayer } from "video.js";
import { computed } from "vue";
import VideoJS from "../components/VideoJS.vue";

let player = $ref<InstanceType<typeof VideoJS> | null>(null);

const store = useStore();
const url = computed(() => "/videos/" + store.video);

// construct the url to stream the selected video
const urlStream = computed(() => {
  const newUrl = new URL(url.value + "/stream", store.backend);
  newUrl.searchParams.append("project", store.project);
  return newUrl.toString();
});

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

// fetch the videos fps from backend
const { data } = useFetch(url, { refetch: true }).get().json();
const fps = computed(() => (data.value ? data.value.fps : -1));
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
      :src="urlStream"
      @player-ready="playerReady"
      @keydown.space="toggleVideo"
      @keydown.left="() => player?.seekBackward()"
      @keydown.right="() => player?.seekForward()"
    ></VideoJS>
  </v-container>
</template>
