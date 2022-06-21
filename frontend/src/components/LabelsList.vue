<script lang="ts">
export default {
  name: "LabelsList"
};
</script>

<script setup lang="ts">
import { useConfig, useLabels } from "@/stores";
import { isEmpty, useHotkeys } from "@/utils";
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";

const labelsStore = useLabels();
const { individuals, selected } = storeToRefs(labelsStore);
const { hasCoords, updateLabel, getLabelledCount, selectNextLabel } =
  labelsStore;
const { config, colors, colorsIndividuals, labelKeyMap } = storeToRefs(
  useConfig()
);

const opened = ref<string[] | undefined>(undefined);

// ensure exactly one individual is open
watch(opened, (value, oldValue) => {
  if (value?.length === 0) {
    opened.value = oldValue;
  }
});

watch(selected, value => {
  if (value?.length) {
    const individual = labelKeyMap.value.get(value[0])?.[0];
    if (individual && !opened.value?.includes(individual)) {
      opened.value = [individual];
    }
  }
});

// set first individual as open when loaded
watch(
  config,
  (value, oldValue) => {
    if (value && isEmpty(oldValue)) {
      opened.value = config.value?.individuals.slice(0, 1) || [];
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

useHotkeys("n", () => selectNextLabel());
useHotkeys("shift+n", () => selectNextLabel(false));
useHotkeys("esc", () => {
  // deselect current label
  selected.value = [];
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur();
  }
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
            {{ getLabelledCount(undefined, individual) }} /
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
