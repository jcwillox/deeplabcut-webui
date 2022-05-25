import { defineStore } from "pinia";

interface State {
  error?: ErrorState;
  updatedAt?: Date;
}

interface ErrorState {
  status?: number;
  message?: string;
  stack?: string;
}

export const useErrors = defineStore("errors", {
  state: (): State => ({
    error: undefined,
    updatedAt: undefined
  }),
  actions: {
    set(state: ErrorState) {
      this.error = state;
      this.updatedAt = new Date();
    },
    reset() {
      this.error = undefined;
      this.updatedAt = new Date();
    }
  }
});
