<script lang="ts">
export default {
  name: "LabelsList"
};
</script>

<script setup lang="ts">
import { useVModel } from "@vueuse/core";
import { evaluate_cmap } from "js-colormaps";
import { computed, ref, watch } from "vue";

const props = defineProps<{
  config: ProjectConfig | null;
  individuals: LabelsIndividuals | null;
  colors: string[];
  selected?: string[];
}>();

const opened = ref<string[] | undefined>(undefined);
const selected = useVModel(props, "selected");

// ensure exactly one individual is open
watch(opened, (value, oldValue) => {
  if (value?.length === 0) {
    opened.value = oldValue;
  }
});

// set first individual as open when loaded
watch(
  () => props.config,
  (value, oldValue) => {
    if (value && (!oldValue || Object.keys(oldValue).length == 0)) {
      opened.value = props.config?.individuals.slice(0, 1);
    }
  }
);

// extract and cache individual colors
const colorsIndividuals = computed(() => {
  const individuals = props.config?.individuals;
  if (individuals) {
    return individuals.map((_, i) => {
      const rgb = evaluate_cmap(i / individuals.length, "Set1");
      return `rgb(${rgb.join(",")})`;
    });
  }
  return [];
});

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
    if (bodyparts[bodypart].x && bodyparts[bodypart].y) {
      count++;
    }
  }
  return count;
};
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
      </v-list-item>
    </v-list-group>
  </v-list>
</template>

<style scoped>
.v-list-group__items .v-list-item {
  --indent-padding: 16px;
}
</style>
