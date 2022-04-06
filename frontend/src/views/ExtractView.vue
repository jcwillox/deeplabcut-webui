<script setup lang="ts">
import type { VideoJsPlayer } from "video.js";
import { computed } from "vue";
import VideoJS from "../components/VideoJS.vue";

let player = $ref<InstanceType<typeof VideoJS> | null>(null);

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
      :fps="23.976"
      @player-ready="playerReady"
      @keydown.space="toggleVideo"
      @keydown.left="() => player?.seekBackward()"
      @keydown.right="() => player?.seekForward()"
    >
      <source
        src="https://daiz.github.io/frame-accurate-ish/time.mp4"
        type="video/mp4"
      />
    </VideoJS>
  </v-container>
</template>
