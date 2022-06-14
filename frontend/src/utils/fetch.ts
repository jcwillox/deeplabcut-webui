import { useErrors, useStore } from "@/stores";
import { isArrayDefined } from "@/utils/index";
import { createFetch } from "@vueuse/core";

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
  if (store.token != "") {
    url.searchParams.append("token", store.token);
  }
  return url.toString();
};

export const useFetch = createFetch({
  options: {
    async beforeFetch({ url, options }) {
      return { url: createUrl(url), options };
    },
    afterFetch(ctx) {
      // clear error state after successful request
      useErrors().reset();
      return ctx;
    },
    onFetchError(ctx) {
      const errors = useErrors();
      if (ctx.response && ctx.response.status >= 400) {
        if (ctx.response.status >= 500 || ctx.response.status == 401) {
          errors.set({
            status: ctx.response.status,
            message: ctx.error.message,
            stack: ctx.error.stack
          });
        }
      } else if (ctx.error) {
        // no response has been received
        errors.set({
          message: ctx.error.message,
          stack: ctx.error.stack
        });
      }
      ctx.data = null;
      return ctx;
    }
  },
  fetchOptions: {
    mode: "cors"
  }
});
