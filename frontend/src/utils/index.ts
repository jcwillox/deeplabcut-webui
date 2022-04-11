export * from "./fetch";

export function toTimecode(seconds: number) {
  const hh = String(~~(seconds / 3600)).padStart(2, "0");
  const mm = String(~~((seconds % 3600) / 60)).padStart(2, "0");
  const ss = String(~~seconds % 60).padStart(2, "0");
  const ms = String(~~((seconds - ~~seconds) * 1000)).padStart(3, "0");
  return `${hh}:${mm}:${ss}.${ms}`;
}
