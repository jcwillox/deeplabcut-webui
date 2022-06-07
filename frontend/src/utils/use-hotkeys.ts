import hotkeys, { type KeyHandler } from "hotkeys-js";
import { onActivated, onDeactivated } from "vue";

export const useHotkeys = (keys: string, callback: KeyHandler) => {
  onActivated(() => {
    hotkeys(keys, callback);
  });

  onDeactivated(() => {
    hotkeys.unbind(keys, callback);
  });
};
