import { useStore } from "@/stores";
import { useFetch } from "@/utils";
import { defineStore } from "pinia";

interface State {
  items: string[];
  isFetching: boolean;
}

export const useFrames = defineStore("frames", {
  state: (): State => ({
    items: [],
    isFetching: false
  }),
  getters: {
    framesUrl() {
      return "/videos/" + useStore().video + "/frames";
    }
  },
  actions: {
    async update() {
      this.isFetching = true;
      const resp = await useFetch(this.framesUrl).get().json();
      this.isFetching = false;
      if (Array.isArray(resp.data.value)) {
        this.items = resp.data.value;
      }
      return resp;
    },
    extract(frame: number) {
      return useFetch(this.framesUrl)
        .post({ frames: [frame] })
        .json();
    }
  }
});
