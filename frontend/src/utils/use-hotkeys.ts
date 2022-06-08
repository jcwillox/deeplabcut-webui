import hotkeys, { type KeyHandler } from "hotkeys-js";
import { onActivated, onDeactivated, onMounted, onUnmounted } from "vue";

export const useHotkeys = (keys: string, callback: KeyHandler) => {
  let unbind: (() => void) | undefined;

  const bind = () => {
    if (unbind == null) {
      hotkeys(keys, callback);
      unbind = () => {
        hotkeys.unbind(keys, callback);
        unbind = undefined;
      };
    }
  };

  onMounted(bind);
  onUnmounted(() => unbind?.());

  onActivated(bind);
  onDeactivated(() => unbind?.());
};
