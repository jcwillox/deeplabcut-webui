import { useStore } from "@/stores/global";
import { createFetch } from "@vueuse/core";

export const useFetch = createFetch({
  options: {
    async beforeFetch({ url, options }) {
      const store = useStore();
      const newUrl = new URL(url, store.backend);
      if (store.project != "")
        newUrl.searchParams.append("project", store.project);
      url = newUrl.toString();
      return { url, options };
    }
  },
  fetchOptions: {
    mode: "cors"
  }
});
