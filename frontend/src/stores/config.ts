import { useStore } from "@/stores";
import { useFetch } from "@/utils";
import { evaluate_cmap } from "js-colormaps";
import { defineStore } from "pinia";
import { computed, watch } from "vue";

export const useConfig = defineStore("config", () => {
  const store = useStore();
  const configUrl = computed(() => "/projects/" + store.project);

  const { data: config, execute } = useFetch(configUrl, { immediate: false })
    .get()
    .json<ProjectConfig>();

  watch(
    () => store.project,
    () => {
      if (store.project) {
        execute();
      } else {
        config.value = null;
      }
    },
    { immediate: true }
  );

  const colors = computed(() => {
    const bodyparts = config.value?.bodyparts || [];
    return bodyparts.map((_, i) => {
      const rgb = evaluate_cmap(i / bodyparts.length, config.value!.colormap);
      return `rgb(${rgb.join(",")})`;
    });
  });

  const colorsIndividuals = computed(() => {
    const individuals = config.value?.individuals || [];
    return individuals.map((_, i) => {
      const rgb = evaluate_cmap(i / individuals.length, "Set1");
      return `rgb(${rgb.join(",")})`;
    });
  });

  const labelsCount = computed(
    () =>
      (config.value?.individuals.length || 0) *
      (config.value?.bodyparts.length || 0)
  );

  const labelKeyMap = computed(() => {
    const keyMap = new Map<string, [string, string]>();
    if (config.value) {
      for (const individual of config.value.individuals) {
        for (const bodypart of config.value.bodyparts) {
          keyMap.set(`${individual}-${bodypart}`, [individual, bodypart]);
        }
      }
    }
    return keyMap;
  });

  return { config, colors, colorsIndividuals, labelsCount, labelKeyMap };
});
