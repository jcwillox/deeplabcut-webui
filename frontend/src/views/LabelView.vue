<script lang="ts">
export default {
  name: "LabelView"
};
</script>

<script setup lang="ts">
import AdvImg from "@/components/AdvImg.vue";
import LabelEditor from "@/components/LabelEditor.vue";
import LabelsList from "@/components/LabelsList.vue";
import FrameInfoDialog from "@/dialogs/FrameInfoDialog.vue";
import FramesDialog from "@/dialogs/FramesDialog.vue";
import { useFrames, useLabels } from "@/stores";
import { createCachedUrl, useHotkeys } from "@/utils";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import type { VBtn } from "vuetify/components";

const route = useRoute();
const frames = useFrames();
const dialog = ref(false);
const { index, image, pending } = storeToRefs(useLabels());

const labelEditorEl = ref<InstanceType<typeof LabelEditor> | null>(null);
const minimapEl = ref<InstanceType<typeof AdvImg> | null>(null);
const videoBtnEl = ref<InstanceType<typeof VBtn> | null>(null);

const mapWidth = ref("0%");
const mapHeight = ref("0%");
const mapScale = ref(1);

const panZoomChange = (detail: PanzoomEventDetail) => {
  const width = labelEditorEl.value!.$el.getBoundingClientRect().width;
  const height = labelEditorEl.value!.$el.getBoundingClientRect().height;
  mapScale.value = detail.scale;
  mapWidth.value = ((width / 2 - detail.x) / width) * 100 + "%";
  mapHeight.value = ((height / 2 - detail.y) / height) * 100 + "%";
};

// bind route hash to frame
watch(
  () => route.hash,
  value => {
    if (route.name === "label" && value) {
      index.value = frames.items.indexOf(value.slice(1));
    }
  },
  { immediate: true }
);

// make sure we do not display an image that no longer exists
watch(
  () => frames.items,
  () => {
    const newIdx = frames.items.indexOf(image.value);
    if (newIdx >= 0) {
      index.value = newIdx;
    } else if (index.value == frames.items.length - 1) {
      index.value--;
    }
  }
);

// define hotkeys
useHotkeys("a", () => {
  index.value--;
});
useHotkeys("d", () => {
  index.value++;
});
useHotkeys("g", () => {
  dialog.value = !dialog.value;
});
useHotkeys("r", () => {
  labelEditorEl.value?.resetZoom();
});
useHotkeys("v", () => {
  videoBtnEl.value?.$el.click();
});
</script>

<template>
  <v-container
    class="d-flex flex-wrap flex-sm-nowrap justify-center pa-1"
    style="max-height: calc(100vh - 72px)"
    fluid
  >
    <div
      class="flex-grow-1"
      :style="{
        maxWidth: `calc((100vh - 80px - 15px) * ${
          minimapEl?.aspectRatio || '16/9'
        } + 80px)`
      }"
    >
      <div>
        <div class="d-flex button-surface">
          <div class="d-flex flex-column">
            <v-btn
              class="rounded-0 rounded-s flex-grow-1"
              variant="plain"
              size="small"
              @click="index--"
              icon
            >
              <v-icon>mdi-chevron-left</v-icon>
              <v-tooltip activator="parent" location="end">
                Previous frame <kbd>A</kbd>
              </v-tooltip>
            </v-btn>
          </div>
          <LabelEditor
            ref="labelEditorEl"
            v-if="image"
            class="flex-grow-1 h-100"
            @panzoomchange="panZoomChange"
          />
          <div
            v-else
            class="d-flex justify-center align-center flex-grow-1 text-center"
            style="
              height: 4500px;
              max-width: 8000px;
              max-height: calc(100vh - 80px - 15px);
            "
          >
            <span>No frames have been extracted.</span>
          </div>
          <div class="d-flex flex-column">
            <FramesDialog v-model="dialog">
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  class="rounded-0 rounded-te"
                  variant="plain"
                  size="small"
                  icon
                >
                  <v-icon>mdi-expand-all</v-icon>
                  <v-tooltip activator="parent" location="end">
                    Show all frames <kbd>G</kbd>
                  </v-tooltip>
                </v-btn>
              </template>
            </FramesDialog>
            <v-divider />
            <v-btn
              class="rounded-0"
              variant="plain"
              size="small"
              @click="labelEditorEl?.resetZoom()"
              icon
            >
              <v-icon>mdi-restore</v-icon>
              <v-tooltip activator="parent" location="end">
                Reset zoom <kbd>R</kbd>
              </v-tooltip>
            </v-btn>
            <v-divider />
            <FrameInfoDialog :image="image" hide-label-btn>
              <template #activator="{ showInVideo, props }">
                <v-btn
                  ref="videoBtnEl"
                  class="rounded-0"
                  variant="plain"
                  size="small"
                  @click.stop="showInVideo"
                  icon
                >
                  <v-icon>mdi-movie</v-icon>
                  <v-tooltip activator="parent" location="end">
                    Show in Video <kbd>V</kbd>
                  </v-tooltip>
                </v-btn>
                <v-divider />
                <v-btn
                  v-bind="props"
                  class="rounded-0"
                  variant="plain"
                  size="small"
                  icon
                >
                  <v-icon>mdi-information-outline</v-icon>
                  <v-tooltip activator="parent" location="end">
                    Image Info
                  </v-tooltip>
                </v-btn>
              </template>
            </FrameInfoDialog>
            <v-divider />
            <v-btn
              class="rounded-0 rounded-be flex-grow-1"
              variant="plain"
              size="small"
              @click="index++"
              icon
            >
              <v-icon>mdi-chevron-right</v-icon>
              <v-tooltip activator="parent" location="end">
                Next frame <kbd>D</kbd>
              </v-tooltip>
            </v-btn>
          </div>
        </div>
        <div class="d-flex justify-space-between text-body-2">
          <span>{{ image }}</span>
          <span>{{ pending ? "saving..." : "" }}</span>
          <span>
            {{ Math.min(index + 1, frames.items.length) }} /
            {{ frames.items.length }}
          </span>
        </div>
      </div>
    </div>
    <div class="d-flex flex-column pl-1 w-25" style="max-width: 280px">
      <AdvImg
        ref="minimapEl"
        v-if="image"
        :src="createCachedUrl(frames.framesUrl, image)"
        class="flex-shrink-0"
      >
        <div class="zoom-box"></div>
        <div class="panel top"></div>
        <div class="panel left"></div>
        <div class="panel right"></div>
        <div class="panel bottom"></div>
      </AdvImg>

      <LabelsList />
    </div>
  </v-container>
</template>

<style scoped>
.zoom-box {
  border: 1px solid #d8dee9;
  position: relative;
  left: calc(v-bind("mapWidth") - 50% / v-bind("mapScale"));
  top: calc(v-bind("mapHeight") - 50% / v-bind("mapScale"));
  width: calc(100% / v-bind("mapScale"));
  height: calc(100% / v-bind("mapScale"));
}

.panel {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: black;
  opacity: 0.6;
}
.panel.top {
  height: calc(v-bind("mapHeight") - 50% / v-bind("mapScale"));
}
.panel.left {
  top: calc(v-bind("mapHeight") - 50% / v-bind("mapScale"));
  height: calc(100% / v-bind("mapScale"));
  width: calc(v-bind("mapWidth") - 50% / v-bind("mapScale"));
}
.panel.right {
  top: calc(v-bind("mapHeight") - 50% / v-bind("mapScale"));
  height: calc(100% / v-bind("mapScale"));
  left: calc(50% / v-bind("mapScale") + v-bind("mapWidth"));
}
.panel.bottom {
  top: calc(v-bind("mapHeight") + 50% / v-bind("mapScale"));
}

.button-surface .v-btn {
  background-color: rgb(var(--v-theme-on-surface-variant));
}
.button-surface .v-btn.v-theme--dark {
  background-color: rgb(var(--v-theme-surface));
}
</style>
