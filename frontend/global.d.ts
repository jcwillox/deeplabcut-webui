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
