<script lang="ts">
export default {
  name: "LabelView"
};
</script>

<script setup lang="ts">
import AdvImg from "@/components/AdvImg.vue";
import FramesDialog from "@/components/FramesDialog.vue";
import LabelEditor from "@/components/LabelEditor.vue";
import LabelsList from "@/components/LabelsList.vue";
import { useFrames, useStore } from "@/stores";
import { createCachedUrl, useFetch, useHotkeys } from "@/utils";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { useDebounceFn } from "@vueuse/core";
import { deepmerge } from "deepmerge-ts";
import { computed, ref, watch } from "vue";

const store = useStore();
const frames = useFrames();
const dialog = ref(false);
const opened = ref<string[] | undefined>(undefined);
const selected = ref<string[] | undefined>(undefined);

const labelEditorEl = ref<InstanceType<typeof LabelEditor> | null>(null);
const minimapEl = ref<InstanceType<typeof AdvImg> | null>(null);

const labelsUrl = computed(() => "/videos/" + store.video + "/labels");
const { data: labels, execute } = useFetch(labelsUrl, { refetch: true })
  .get()
  .json<LabelsModel>();

const imgIndex = ref(0);
const updateIndex = (n: number) => {
  if (frames.items.length == 0) {
    imgIndex.value = 0;
  } else {
    const length = frames.items.length;
    imgIndex.value = (((imgIndex.value + n) % length) + length) % length;
  }
};

const image = computed(() => frames.items[imgIndex.value]);
const individuals = computed<LabelsIndividuals | null>(() =>
  labels.value ? labels.value[image.value] : null
);

watch(
  () => frames.items,
  () => {
    if (frames.items.length == 0) {
      // reset selected frame when changing video
      imgIndex.value = 0;
    } else {
      // refetch labels when a new frame is extracted
      execute();
    }
  }
);

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

const pending = ref<LabelsModel | null>(null);
const isSyncing = ref(false);

const syncBackend = useDebounceFn(
  async () => {
    // ensure we are only sending 1 request at a time
    if (!isSyncing.value) {
      if (pending.value === null) {
        console.error("pending changes was null while syncing backend");
        return;
      }

      isSyncing.value = true;
      let payload: LabelsModel | null = pending.value;
      pending.value = null;

      try {
        console.debug("SyncBackend: Starting", payload);
        const { statusCode } = await useFetch(labelsUrl).put(payload);

        if (statusCode.value == 200) {
          payload = null;
          console.debug("SyncBackend: Finished");
        } else {
          console.debug("SyncBackend: Failed", statusCode.value, pending.value);
        }
      } finally {
        // ensure we always reset syncing status
        isSyncing.value = false;

        // merge back any changes we were trying to send
        if (payload) {
          pending.value = pending.value
            ? deepmerge(payload, pending.value)
            : payload;
        }

        // reschedule update if there are pending changes
        if (pending.value) {
          syncBackend()?.then();
          console.debug("SyncBackend: Rescheduled", pending.value);
        }
      }
    }
  },
  500,
  { maxWait: 2000 }
);

const updateLabels = (newLabels: LabelsModel) => {
  pending.value = deepmerge(pending.value, newLabels);
  labels.value = deepmerge(labels.value, newLabels);
  syncBackend();
};

const resetLabel = (individual: string, bodypart: string) => {
  updateLabels({
    [image.value]: {
      [individual]: {
        [bodypart]: { x: null, y: null }
      }
    }
  });
};

// define hotkeys
useHotkeys("a", () => {
  updateIndex(-1);
});
useHotkeys("d", () => {
  updateIndex(1);
});
useHotkeys("g", () => {
  dialog.value = !dialog.value;
});
useHotkeys("r", () => {
  labelEditorEl.value?.resetZoom();
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
        maxWidth: `calc((100vh - 80px - 15px) * ${minimapEl?.aspectRatio} + 80px)`
      }"
    >
      <div>
        <div class="d-flex button-surface">
          <div class="d-flex flex-column">
            <v-btn
              class="rounded-0 rounded-s flex-grow-1"
              variant="plain"
              size="small"
              @click="updateIndex(-1)"
              icon
            >
              <v-icon size="small">mdi-chevron-left</v-icon>
              <v-tooltip activator="parent" location="end">
                Previous frame <kbd>A</kbd>
              </v-tooltip>
            </v-btn>
          </div>
          <LabelEditor
            ref="labelEditorEl"
            v-model:opened="opened"
            v-model:selected="selected"
            :image="frames.items[imgIndex]"
            :labels="labels"
            class="flex-grow-1 h-100"
            @panzoomchange="panZoomChange"
            @update:labels="updateLabels"
          >
          </LabelEditor>
          <div class="d-flex flex-column">
            <FramesDialog
              v-model="dialog"
              v-model:index="imgIndex"
              :labels="labels"
            >
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  class="rounded-0 rounded-te"
                  variant="plain"
                  size="small"
                  icon
                >
                  <v-icon size="small">mdi-expand-all</v-icon>
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
              <v-icon size="small">mdi-restore</v-icon>
              <v-tooltip activator="parent" location="end">
                Reset zoom <kbd>R</kbd>
              </v-tooltip>
            </v-btn>
            <v-divider />
            <v-btn
              class="rounded-0 rounded-be flex-grow-1"
              variant="plain"
              size="small"
              @click="updateIndex(1)"
              icon
            >
              <v-icon size="small">mdi-chevron-right</v-icon>
              <v-tooltip activator="parent" location="end">
                Next frame <kbd>D</kbd>
              </v-tooltip>
            </v-btn>
          </div>
        </div>
        <div class="d-flex justify-space-between text-body-2">
          <span>{{ image }}</span>
          <span>{{ pending ? "saving..." : "" }}</span>
          <span>{{ imgIndex + 1 }} / {{ frames.items.length }}</span>
        </div>
      </div>
    </div>
    <div class="d-flex flex-column pl-1 w-25" style="max-width: 280px">
      <AdvImg ref="minimapEl" :src="createCachedUrl(frames.framesUrl, image)">
        <div class="zoom-box"></div>
        <div class="panel top"></div>
        <div class="panel left"></div>
        <div class="panel right"></div>
        <div class="panel bottom"></div>
      </AdvImg>

      <LabelsList
        v-model:opened="opened"
        v-model:selected="selected"
        :individuals="individuals"
        @reset:label="resetLabel"
      />
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
