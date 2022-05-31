<script lang="ts">
export default {
  name: "LabelView"
};
</script>

<script setup lang="ts">
import FramesDialog from "@/components/FramesDialog.vue";
import LabelEditor from "@/components/LabelEditor.vue";
import { useFrames, useStore } from "@/stores";
import { createCachedUrl, useFetch } from "@/utils";
import { evaluate_cmap } from "@/utils/colormap";
import type { PanzoomEventDetail } from "@panzoom/panzoom/dist/src/types";
import { computed, ref, watch } from "vue";

const store = useStore();
const frames = useFrames();
const framesUrl = computed(() => "/videos/" + store.video + "/frames");

const labelEditorEl = ref<InstanceType<typeof LabelEditor> | null>(null);

const labelsUrl = computed(() => "/videos/" + store.video + "/labels");
const { data: labels } = useFetch<string>(labelsUrl, { refetch: true })
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

const image = computed<string>(() => frames.items[imgIndex.value]);
const individuals = computed<LabelsIndividuals>(() =>
  labels.value ? labels.value[image.value] : {}
);

// reset selected frame when changing video
watch(
  () => frames.items,
  () => {
    if (frames.items.length == 0) {
      imgIndex.value = 0;
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

const opened = ref<string[] | undefined>(undefined);
const selected = ref<string[] | undefined>(undefined);

const { data: configProject } = useFetch("/projects/" + store.project)
  .get()
  .json();

// extract and cache bodypart colors
const colors = computed(() => {
  const individual =
    individuals.value && Object.keys(individuals.value).shift();
  if (individual && configProject.value.colormap) {
    const bodyparts = Object.keys(individuals.value[individual]);
    return bodyparts.map((_, i) => {
      const rgb = evaluate_cmap(
        i / bodyparts.length,
        configProject.value.colormap
      );
      return `rgb(${rgb.join(",")})`;
    });
  }
  return [];
});

// extract and cache individual colors
const colorsIndividuals = computed(() => {
  const names = individuals.value && Object.keys(individuals.value);
  if (names) {
    return names.map((_, i) => {
      const rgb = evaluate_cmap(i / names.length, "Set1");
      return `rgb(${rgb.join(",")})`;
    });
  }
  return [];
});

// ensure exactly one individual is open
watch(opened, (value, oldValue) => {
  if (opened.value?.length == 2) {
    opened.value.shift();
  } else if (value?.length == 0) {
    opened.value = oldValue;
  }
});

// set first individual as open when loaded
watch(individuals, (value, oldValue) => {
  if (value && (!oldValue || Object.keys(oldValue).length == 0)) {
    const individual = Object.keys(value).shift();
    opened.value = individual ? [individual] : undefined;
  }
});

const createSubtitle = (coords: LabelsCoords) => {
  let output = "";
  if (coords.x) {
    output += "x: " + Math.round(coords.x);
    if (coords.y) {
      output += " • ";
    }
  }
  if (coords.y) {
    output += "y: " + Math.round(coords.y);
  }
  return output;
};

const getLabelledCount = (bodyparts: LabelsBodyparts) => {
  let count = 0;
  for (const bodypart in bodyparts) {
    if (bodyparts[bodypart].x && bodyparts[bodypart].y) {
      count++;
    }
  }
  return count;
};
</script>

<template>
  <v-container
    class="d-flex flex-wrap flex-sm-nowrap justify-center pa-1"
    style="max-height: calc(100vh - 80px)"
    fluid
  >
    <div
      class="flex-grow-1"
      :style="{
        maxWidth: `calc((100vh - 80px) * ${labelEditorEl?.aspectRatioString} + 80px)`
      }"
    >
      <div class="d-flex button-surface">
        <div class="d-flex flex-column">
          <v-btn
            class="rounded-0 rounded-s flex-grow-1"
            icon="mdi-chevron-left"
            variant="plain"
            size="small"
            @click="updateIndex(-1)"
          />
        </div>
        <LabelEditor
          ref="labelEditorEl"
          :image="frames.items[imgIndex]"
          :labels="labels"
          :selected="selected && selected[0]"
          :colors="colors"
          class="flex-grow-1 h-100"
          @panzoomchange="panZoomChange"
        >
        </LabelEditor>
        <div class="d-flex flex-column">
          <FramesDialog v-model="imgIndex">
            <template #activator="props1">
              <v-tooltip bottom>
                <template v-slot:activator="props2">
                  <v-btn
                    v-bind="{ ...props2.props, ...props1.props }"
                    class="rounded-0 rounded-te"
                    icon="mdi-expand-all"
                    variant="plain"
                    size="small"
                  />
                </template>
                <span>Show all frames</span>
              </v-tooltip>
            </template>
          </FramesDialog>
          <v-divider />
          <v-btn
            class="rounded-0 rounded-be flex-grow-1"
            icon="mdi-chevron-right"
            variant="plain"
            size="small"
            @click="updateIndex(1)"
          />
        </div>
      </div>
    </div>
    <div class="d-flex flex-column pl-1 w-25" style="max-width: 280px">
      <v-img
        v-if="store.video"
        :src="createCachedUrl(framesUrl, frames.items[imgIndex])"
        :aspect-ratio="labelEditorEl?.aspectRatio"
        class="flex-grow-0"
      >
        <div id="zoomBox" />
        <div class="panel top" />
        <div class="panel left" />
        <div class="panel right" />
        <div class="panel bottom" />
      </v-img>

      <v-list
        v-if="labels"
        v-model:opened="opened"
        v-model:selected="selected"
        class="overflow-y-auto"
      >
        <v-list-group
          v-for="(bodyparts, individual, index) in individuals"
          :key="individual"
          :value="individual"
        >
          <template v-slot:activator="{ props }">
            <v-list-item v-bind="props" active-color="blue" :value="individual">
              <template #prepend>
                <v-list-item-avatar start>
                  <v-icon :style="{ color: colorsIndividuals[index] }">
                    mdi-circle
                  </v-icon>
                </v-list-item-avatar>
              </template>
              <template #title>
                <span class="text-capitalize">{{ individual }}</span>
              </template>
              <template #subtitle>
                {{ getLabelledCount(individuals[individual]) }} /
                {{ Object.keys(individuals[individual]).length }}
              </template>
            </v-list-item>
          </template>

          <v-list-item
            v-for="(coords, bodypart, index) in bodyparts"
            :key="`${individual}-${bodypart}`"
            :value="`${individual}-${bodypart}`"
          >
            <template #prepend>
              <v-list-item-avatar start>
                <v-icon :style="{ color: colors[index] }">mdi-circle</v-icon>
              </v-list-item-avatar>
            </template>
            <template #title>
              {{ bodypart }}
            </template>
            <template #subtitle>
              {{ createSubtitle(coords) }}
            </template>
          </v-list-item>
        </v-list-group>
      </v-list>
    </div>
  </v-container>
</template>

<style scoped>
#zoomBox {
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

.v-list-group__items .v-list-item {
  --indent-padding: 16px;
}

.button-surface .v-btn {
  background-color: rgb(var(--v-theme-on-surface-variant));
}
</style>
