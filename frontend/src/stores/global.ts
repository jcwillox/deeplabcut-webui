import { useFrames } from "@/stores";
import { defineStore } from "pinia";

export const useStore = defineStore("global", {
  state: () => ({
    project: "",
    video: "",
    cVideo: "",
    backend: "http://127.0.0.1:8000",
    token: "",
    autoSelect: true
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
