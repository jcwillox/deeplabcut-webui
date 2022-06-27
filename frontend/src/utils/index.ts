import { isDefined } from "@vueuse/core";

export * from "./fetch";
export * from "./use-exact-click";
export * from "./use-hotkeys";

export function toTimecode(seconds: number) {
  const hh = String(~~(seconds / 3600)).padStart(2, "0");
  const mm = String(~~((seconds % 3600) / 60)).padStart(2, "0");
  const ss = String(~~seconds % 60).padStart(2, "0");
  const ms = String(~~((seconds - ~~seconds) * 1000)).padStart(3, "0");
  return `${hh}:${mm}:${ss}.${ms}`;
}

export function isArrayDefined<T>(
  arr: T[]
): arr is Exclude<T, null | undefined>[] {
  return arr.every(v => isDefined(v));
}

/**
 * Returns `true` if the object is `null`, `undefined`, or has no keys or items,
 * otherwise, returns `false`.
 */
export function isEmpty(obj?: object | null) {
  for (const i in obj) return false;
  return true;
}

export function humanizeBytes(bytes: number): string {
  if (bytes < 1000) {
    return `${bytes} B`;
  }
  const units = ["K", "M", "G", "T"];
  for (const unit of units) {
    bytes /= 1024;
    if (bytes < 1) {
      return `${bytes.toPrecision(2)} ${unit}iB`;
    }
    if (bytes < 100) {
      return `${bytes.toPrecision(3)} ${unit}iB`;
    }
  }
  return `${bytes} T`;
}
