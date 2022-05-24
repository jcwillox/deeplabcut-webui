import { useStore } from "@/stores";
import { createFetch } from "@vueuse/core";
import { isArrayDefined } from "@/utils/index";

const cache: Map<string, string> = new Map();
export const clearUrlCache = () => cache.clear();

export function createCachedUrl(...parts: string[]): string;
export function createCachedUrl(
  ...parts: (string | undefined | null)[]
): undefined;
export function createCachedUrl(
  ...parts: (string | undefined | null)[]
): string | undefined {
  if (isArrayDefined(parts)) {
    const key = parts.join("/");
    if (cache.has(key)) {
      return cache.get(key);
    }
    const newUrl = createUrl(...parts);
    cache.set(key, newUrl);
    return newUrl;
  } else {
    return undefined;
  }
}

export const createUrl = (...parts: string[]): string => {
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
