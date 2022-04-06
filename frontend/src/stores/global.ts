import { defineStore } from "pinia";

export const useStore = defineStore({
  id: "global",
  state: () => ({
    project: "",
    video: "",
    backend: "http://127.0.0.1:8000"
  }),
  actions: {
    resetProject() {
      this.project = "";
      this.video = "";
    }
  }
});
