<script setup lang="ts">
import { toTimecode } from "@/utils";
import type { VideoJsPlayer, VideoJsPlayerOptions } from "video.js";
import videojs from "video.js";
import { onMounted, ref, watch, type Ref } from "vue";

const props = defineProps<{
  options?: VideoJsPlayerOptions;
  src: string | videojs.Tech.SourceObject;
  fps: number;
  maxHeightOffset: string;
}>();

const emit = defineEmits<{
  (e: "playerReady", videojs: VideoJsPlayer): void;
}>();

const videoEl: Ref<HTMLVideoElement | null> = ref(null);
const player: Ref<VideoJsPlayer | null> = ref(null);

const cFrame = ref(0);
const cTimecode = ref(toTimecode(0));
let drift = 0;

const setSource = (url: string, type = "video/mp4") => {
  if (!player.value) return;
  if (!player.value.paused()) {
    player.value.pause();
  }
  player.value.src({ src: url, type });
  player.value.load();
  player.value.currentTime(0);
};

const _setFromSource = () => {
  if (props.src) {
    if (typeof props.src === "string") {
      setSource(props.src);
    } else {
      setSource(props.src.src, props.src.type);
    }
  }
};

watch(() => props.src, _setFromSource);

onMounted(() => {
  player.value = videojs(
    videoEl.value!,
    { fluid: true, muted: true, ...props.options },
    () => {
      _setFromSource();
      emit("playerReady", player.value!);
    }
  );

  videoEl.value?.requestVideoFrameCallback(onFrameCallback);
});

const onFrameCallback = (
  now: DOMHighResTimeStamp,
  metadata: VideoFrameMetadata
) => {
  if (metadata.presentedFrames == 1) {
    console.debug("first frame", now, metadata);
    if (metadata.mediaTime > 0) {
      console.debug("accounting for video start drift of", metadata.mediaTime);
      drift = metadata.mediaTime;
    } else {
      drift = 0;
    }
  }

  cFrame.value = Math.round((metadata.mediaTime - drift) * props.fps);
  cTimecode.value = toTimecode(metadata.mediaTime - drift);

  videoEl.value?.requestVideoFrameCallback(onFrameCallback);
};

/* Seeking Functions */
const seek = (frames: number) => {
  if (player.value && !player.value.paused()) {
    player.value.pause();
  }
  seekTo(cFrame.value + frames);
};

const seekForward = (frames = 1) => {
  seek(frames);
};

const seekBackward = (frames = 1) => {
  seek(-frames);
};

const seekTo = (frame: number) => {
  const time = frame / props.fps + drift;
  console.debug(`seeking to: ${frame} (${toTimecode(time)})`, time);
  if (drift) {
    console.debug(
      `actual    : ${frame} (${toTimecode(time - drift)})`,
      time - drift
    );
  }
  player.value?.currentTime(time + 0.00001);
};

defineExpose({
  frame: cFrame,
  timecode: cTimecode,
  videojs: player,
  videoEl: videoEl,
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

.video-js.vjs-fluid,
.video-js.vjs-16-9,
.video-js.vjs-4-3,
video.video-js,
video.vjs-tech {
  max-height: calc(100vh - v-bind("maxHeightOffset")) !important;
  position: relative !important;
  width: 100%;
  height: auto !important;
  max-width: 100% !important;
  padding-top: 0 !important;
  line-height: 0;
}

.vjs-control-bar {
  line-height: 1;
}
</style>
