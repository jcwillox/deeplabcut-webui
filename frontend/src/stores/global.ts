import { defineStore } from "pinia";
import { useFrames } from "@/stores";

export const useStore = defineStore("global", {
  state: () => ({
    project: "",
    video: "",
    cVideo: "",
    backend: "http://127.0.0.1:8000"
  }),
  actions: {
    resetProject() {
      this.project = "";
      this.cVideo = "";
    },
    setVideo(video: string) {
      this.video = video;
      this.cVideo = video;
      useFrames().items = [];
    }
  },
  persist: true
});
