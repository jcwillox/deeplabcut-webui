<script lang="ts">
export default {
  name: "LabelsList"
};
</script>

<script setup lang="ts">
import { useConfig, useLabels } from "@/stores";
import { isEmpty, useHotkeys } from "@/utils";
import { syncRef, useVModel } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";

const props = defineProps<{
  opened?: string[];
  selected?: string[];
}>();

const emit = defineEmits<{
  (e: "update:opened", opened: string[]): void;
  (e: "update:selected", selected: string[]): void;
}>();

const labelsStore = useLabels();
const { individuals } = storeToRefs(labelsStore);
const { bodyparts, hasCoords, updateLabel } = labelsStore;
const { config, colors, colorsIndividuals } = storeToRefs(useConfig());

const selected = useVModel(props, "selected", emit);
const opened = ref<string[] | undefined>(undefined);
syncRef(opened, useVModel(props, "opened", emit));

// ensure exactly one individual is open
watch(opened, (value, oldValue) => {
  if (value?.length === 0) {
    opened.value = oldValue;
  }
});

// set first individual as open when loaded
watch(
  config,
  (value, oldValue) => {
    if (value && isEmpty(oldValue)) {
      opened.value = config.value?.individuals.slice(0, 1);
    }
  },
  { immediate: true }
);

const createSubtitle = (coords?: LabelsCoords) => {
  let output = "";
  if (coords) {
    if (coords.x) {
      output += "x: " + Math.round(coords.x);
      if (coords.y) {
        output += " • ";
      }
    }
    if (coords.y) {
      output += "y: " + Math.round(coords.y);
    }
  }
  return output;
};

const getLabelledCount = (bodyparts?: LabelsBodyparts) => {
  let count = 0;
  for (const bodypart in bodyparts) {
    if (hasCoords(bodyparts[bodypart])) {
      count++;
    }
  }
  return count;
};

const selectNextBodypart = () => {
  let foundFirst = false;
  for (const { individual, bodypart, coords } of bodyparts()) {
    if (selected.value?.length) {
      if (selected.value[0] === `${individual}-${bodypart}`) {
        foundFirst = true;
        continue;
      } else if (!foundFirst) {
        continue;
      }
    }
    if (!hasCoords(coords)) {
      opened.value = [individual];
      selected.value = [`${individual}-${bodypart}`];
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
      return;
    }
  }
  // clear selection as there is no next individual or bodypart
  selected.value = undefined;
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur();
  }
};

useHotkeys("esc", () => {
  // deselect current label
  selected.value = [];
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur();
  }
});

useHotkeys("n", () => {
  selectNextBodypart();
});
</script>

<template>
  <v-list
    v-if="config"
    v-model:selected="selected"
    v-model:opened="opened"
    open-strategy="single"
    class="overflow-y-auto"
  >
    <v-list-group
      v-for="(individual, index) in config.individuals"
      :key="individual"
      :value="individual"
    >
      <template #activator="{ props }">
        <v-list-item v-bind="props" active-color="blue">
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
            {{ getLabelledCount(individuals?.[individual]) }} /
            {{ config.bodyparts.length }}
          </template>
        </v-list-item>
      </template>

      <v-list-item
        v-for="(bodypart, index) in config.bodyparts"
        :key="`${individual}-${bodypart}`"
        :value="`${individual}-${bodypart}`"
      >
        <template #prepend>
          <v-list-item-avatar start>
            <v-icon :style="colors.length > index && { color: colors[index] }">
              mdi-circle
            </v-icon>
          </v-list-item-avatar>
        </template>
        <template #title>
          {{ bodypart }}
        </template>
        <template #subtitle>
          {{ createSubtitle(individuals?.[individual]?.[bodypart]) }}
        </template>
        <template
          v-if="hasCoords(individuals?.[individual]?.[bodypart])"
          #append
        >
          <v-list-item-avatar end>
            <v-btn
              size="small"
              variant="plain"
              @click.stop="updateLabel(individual, bodypart)"
              icon
            >
              <v-icon size="small">mdi-restore</v-icon>
              <v-tooltip activator="parent" location="bottom" text="Reset" />
            </v-btn>
          </v-list-item-avatar>
        </template>
      </v-list-item>
    </v-list-group>
  </v-list>
</template>

<style scoped>
.v-list-group__items .v-list-item {
  --indent-padding: 16px;
}
</style>
