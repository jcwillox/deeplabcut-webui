import { useStore } from "@/stores";
import { useFetch } from "@/utils";
import { defineStore } from "pinia";
import { computed, ref, watch } from "vue";
import { useRoute, type RouteRecordName } from "vue-router";

export const useFrames = defineStore("frames", () => {
  const items = ref<string[]>([]);
  const isFetching = ref(false);

  const store = useStore();
  const route = useRoute();
  const framesUrl = computed(() => "/videos/" + store.video + "/frames");

  const update = async () => {
    isFetching.value = true;
    const resp = await useFetch(framesUrl).get().json<string[]>();
    isFetching.value = false;
    if (Array.isArray(resp.data.value)) {
      items.value = resp.data.value;
    }
    return resp;
  };

  const extract = (frame: number) => {
    return useFetch(framesUrl)
      .post({ frames: [frame] })
      .json();
  };

  const handleRouteChange = (route: RouteRecordName) => {
    if (route == "extract" || route == "label") {
      if (items.value.length == 0 && !isFetching.value) {
        update();
      }
    }
  };

  // track video changes
  watch(
    () => store.video,
    () => {
      // refetch frames
      if (route && (route.name == "extract" || route.name == "label")) {
        update();
      }
    }
  );

  return {
    items,
    isFetching,
    framesUrl,
    handleRouteChange,
    update,
    extract
  };
});
