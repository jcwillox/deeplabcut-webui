import { useStore } from "@/stores/global";
import { createFetch, type MaybeRef } from "@vueuse/core";
import { readonly, ref, unref, watch } from "vue";

export const useUrl = (...parts: MaybeRef<string>[]) => {
  const url = ref("");
  const store = useStore();
  watch(
    [
      () => store.backend,
      () => store.project,
      ...parts.filter(part => typeof part != "string")
    ],
    () => {
      // we skip update if there is no project selected
      // to avoid setting the url to a broken link
      if (store.project) {
        url.value = createUrl(...parts.map(part => unref(part)));
      }
    },
    { immediate: true }
  );
  return readonly(url);
};

export const createUrl = (...parts: string[]) => {
  const store = useStore();
  const url = new URL(parts.join("/"), store.backend);
  if (store.project != "") {
    url.searchParams.append("project", store.project);
  }
  return url.toString();
};

export const useFetch = createFetch({
  options: {
    async beforeFetch({ url, options }) {
      return { url: createUrl(url), options };
    }
  },
  fetchOptions: {
    mode: "cors"
  }
});
