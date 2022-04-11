<script setup lang="ts">
import { toTimecode } from "@/utils";
import type { VideoJsPlayer, VideoJsPlayerOptions } from "video.js";
import videojs from "video.js";
import { onMounted, watch } from "vue";

const props = defineProps<{
  options?: VideoJsPlayerOptions;
  src: string | videojs.Tech.SourceObject;
  fps: number;
}>();

const emit = defineEmits<{
  (e: "playerReady", videojs: VideoJsPlayer): void;
}>();

let videoEl = $ref<HTMLVideoElement | null>(null);
let player = $ref<VideoJsPlayer | null>(null);

let cFrame = $ref(0);
let cTimecode = $ref(toTimecode(0));
let drift = 0;

const setSource = (url: string, type = "video/mp4") => {
  if (!player) return;
  if (!player.paused()) {
    player.pause();
  }
  player.src({ src: url, type });
  player.load();
  player.currentTime(0);
};

const _setFromSource = () => {
  if (props.src) {
    if (typeof props.src === "string") {
      console.log("setting string source");
      setSource(props.src);
    } else {
      setSource(props.src.src, props.src.type);
    }
  }
};

watch(() => props.src, _setFromSource);

onMounted(() => {
  player = videojs(
    videoEl!,
    { fluid: true, muted: true, ...props.options },
    () => {
      _setFromSource();
      emit("playerReady", player!);
    }
  );

  videoEl?.requestVideoFrameCallback(onFrameCallback);
});

const onFrameCallback = (
  now: DOMHighResTimeStamp,
  metadata: VideoFrameMetadata
) => {
  if (metadata.presentedFrames == 1) {
    console.debug("first frame", now, metadata);
    if (metadata.mediaTime > 0) {
      console.log("accounting for video start drift of", metadata.mediaTime);
      drift = metadata.mediaTime;
    } else {
      drift = 0;
    }
  }

  cFrame = Math.round((metadata.mediaTime - drift) * props.fps);
  cTimecode = toTimecode(metadata.mediaTime - drift);

  videoEl?.requestVideoFrameCallback(onFrameCallback);
};

/* Seeking Functions */
const seek = (frames: number) => {
  if (player && !player.paused()) {
    player.pause();
  }
  seekTo(cFrame + frames);
};

const seekForward = (frames = 1) => {
  seek(frames);
};

const seekBackward = (frames = 1) => {
  seek(-frames);
};

const seekTo = (frame: number) => {
  const time = frame / props.fps + drift;
  console.log(`seeking to: ${frame} (${toTimecode(time)})`, time);
  if (drift) {
    console.log(
      `actual    : ${frame} (${toTimecode(time - drift)})`,
      time - drift
    );
  }
  player?.currentTime(time + 0.00001);
};

defineExpose({
  frame: $$(cFrame),
  timecode: $$(cTimecode),
  videojs: $$(player),
  videoEl: $$(videoEl),
  setSource,
  seek,
  seekTo,
  seekForward,
  seekBackward
});
</script>

<template>
  <video
    ref="videoEl"
    class="video-js vjs-big-play-centered"
    preload="metadata"
    controls
  >
    <slot></slot>
  </video>
</template>

<style>
@import "video.js/dist/video-js.min.css";
</style>
