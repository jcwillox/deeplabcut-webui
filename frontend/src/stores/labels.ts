import { useConfig, useFrames, useStore } from "@/stores";
import { useFetch } from "@/utils";
import { useDebounceFn } from "@vueuse/core";
import { deepmerge } from "deepmerge-ts";
import { defineStore, storeToRefs } from "pinia";
import { computed, ref, watch } from "vue";

export const useLabels = defineStore("labels", () => {
  const store = useStore();
  const frames = useFrames();
  const { config } = storeToRefs(useConfig());

  /* LABEL FETCHING */
  const labelsUrl = computed(() => "/videos/" + store.video + "/labels");
  const indexVal = ref(0);
  const index = computed({
    get: () => indexVal.value,
    set: value => {
      const length = frames.items.length;
      indexVal.value = length ? ((value % length) + length) % length : 0;
    }
  });

  const { data: labels, execute } = useFetch(labelsUrl, { refetch: true })
    .get()
    .json<LabelsModel>();

  const image = computed(() => frames.items[index.value]);
  const individuals = computed<LabelsIndividuals | null>(() =>
    labels.value ? labels.value[image.value] : null
  );

  watch(
    () => frames.items,
    () => {
      if (frames.items.length == 0) {
        // reset selected frame when changing video
        index.value = 0;
      } else {
        // refetch labels when a new frame is extracted
        execute();
      }
    }
  );

  /* SYNCING LOGIC */
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
            console.debug(
              "SyncBackend: Failed",
              statusCode.value,
              pending.value
            );
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

  const updateLabel = (
    individual: string,
    bodypart: string,
    coords: LabelsCoords = { x: null, y: null }
  ) => {
    const patch = {
      [image.value]: {
        [individual]: {
          [bodypart]: coords
        }
      }
    };

    pending.value = deepmerge(pending.value, patch);
    labels.value = deepmerge(labels.value, patch);
    syncBackend();
  };

  /* UTILITY FUNCTIONS */
  function* bodyparts(image_: string = image.value) {
    // we iterate using the individuals and bodyparts from the config
    // as they are not all guaranteed to be in the labels object
    if (config.value) {
      for (const [i, individual] of config.value.individuals.entries()) {
        for (const [j, bodypart] of config.value.bodyparts.entries()) {
          const coords = labels.value?.[image_]?.[individual]?.[bodypart];
          yield { i, j, individual, bodypart, coords };
        }
      }
    }
  }

  const hasCoords = (coords?: LabelsCoords) => {
    return coords && (coords.x || coords.y);
  };

  /** Returns the number of bodyparts that have been labelled for a given image */
  const getLabelledCount = (image_: string = image.value) => {
    let count = 0;
    for (const { coords } of bodyparts(image_)) {
      if (hasCoords(coords)) {
        count++;
      }
    }
    return count;
  };

  return {
    index,
    image,
    labels,
    individuals,
    pending,
    updateLabel,
    bodyparts,
    hasCoords,
    getLabelledCount
  };
});
