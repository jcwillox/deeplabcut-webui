type LabelsCoords = Record<"x" | "y", number | null | undefined>;
type LabelsBodyparts = Record<string, LabelsCoords>;
type LabelsIndividuals = Record<string, LabelsBodyparts>;
type LabelsModel = Record<string, LabelsIndividuals>;

type VideoFrameRequestCallbackId = number;

interface VideoFrameMetadata {
  presentationTime: DOMHighResTimeStamp;
  expectedDisplayTime: DOMHighResTimeStamp;
  width: number;
  height: number;
  mediaTime: number;
  presentedFrames: number;
  processingDuration?: number;
  captureTime?: DOMHighResTimeStamp;
  receiveTime?: DOMHighResTimeStamp;
  rtpTimestamp?: number;
}

interface HTMLVideoElement extends HTMLMediaElement {
  requestVideoFrameCallback(
    callback: (now: DOMHighResTimeStamp, metadata: VideoFrameMetadata) => void
  ): VideoFrameRequestCallbackId;
  cancelVideoFrameCallback(handle: VideoFrameRequestCallbackId): void;
}

declare module "virtual:pwa-register/vue" {
  import type { Ref } from "vue";

  export interface RegisterSWOptions {
    immediate?: boolean;
    onNeedRefresh?: () => void;
    onOfflineReady?: () => void;
    onRegistered?: (
      registration: ServiceWorkerRegistration | undefined
    ) => void;
    onRegisterError?: (error: unknown) => void;
  }

  export function useRegisterSW(options?: RegisterSWOptions): {
    needRefresh: Ref<boolean>;
    offlineReady: Ref<boolean>;
    updateServiceWorker: (reloadPage?: boolean) => Promise<void>;
  };
}
