import os
from typing import List

import cv2
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import FileResponse
from natsort import os_sorted
from pydantic import BaseModel, validator

from .projects import ProjectType
from ..config import Settings, get_settings
from ..managers import get_label_manager, LabelManager, LabelsModel
from ..responses import VideoResponse
from ..utils import QueryModel, get_project_path

router = APIRouter()


class VideoItemResponse(BaseModel):
    name: str
    accessed: float
    created: float
    size: int
    extracted: int
    labelled: int


@router.get("", response_model=List[VideoItemResponse])
def list_videos(
    project: ProjectType, manager: LabelManager = Depends(get_label_manager)
):
    path = get_project_path(project, "videos")

    for entry in os_sorted(os.scandir(path), key=lambda x: x.name):
        entry: os.DirEntry
        info = entry.stat()
        labels = manager.get_labels(project, entry.name)

        yield {
            "name": entry.name,
            "accessed": info.st_atime,
            "created": info.st_ctime,
            "size": info.st_size,
            "extracted": len(labels),
            "labelled": manager.get_labelled_count(labels),
        }


class VideoCommonQuery(QueryModel):
    project: ProjectType
    video: str

    @validator("video")
    def valid_video(cls, value: str, values) -> str:
        if "project" in values and value not in os.listdir(
            get_project_path(values["project"], "videos")
        ):
            raise ValueError(f"The video '{value}' does not exist")
        return value


class VideoDetailResponse(BaseModel):
    fps: float


@router.get("/{video}", response_model=VideoDetailResponse)
def get_video(params: VideoCommonQuery = Depends(VideoCommonQuery)):
    path = get_project_path(params.project, "videos", params.video)
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return {"fps": fps}


@router.get("/{video}/stream")
def stream_video(
    request: Request, params: VideoCommonQuery = Depends(VideoCommonQuery)
):
    path = get_project_path(params.project, "videos", params.video)
    try:
        path = os.path.realpath(path, strict=True)
    except OSError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err)
    return VideoResponse(request, file_path=path, content_type="video/mp4")


@router.get("/{video}/frames")
def get_frames(params: VideoCommonQuery = Depends(VideoCommonQuery)):
    name = os.path.splitext(params.video)[0]
    path = get_project_path(params.project, "labeled-data", name)

    if not os.path.exists(path):
        return []
    for file in os_sorted(os.listdir(path)):
        if file.endswith(".png"):
            yield file


@router.get("/{video}/frames/{frame}")
def get_frame(frame: str, params: VideoCommonQuery = Depends(VideoCommonQuery)):
    name = os.path.splitext(params.video)[0]
    path = get_project_path(params.project, "labeled-data", name, frame)
    if not os.path.exists(path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="frame does not exist"
        )
    return FileResponse(path)


@router.delete("/{video}/frames/{frame}")
def remove_frame(frame: str, params: VideoCommonQuery = Depends(VideoCommonQuery)):
    name = os.path.splitext(params.video)[0]
    path = get_project_path(params.project, "labeled-data", name, frame)
    if os.path.exists(path):
        os.remove(path)


class ExtractRequestBody(BaseModel):
    frames: List[int]


@router.post("/{video}/frames", response_model=List[str])
def extract_frames(
    body: ExtractRequestBody,
    params: VideoCommonQuery = Depends(VideoCommonQuery),
    manager: LabelManager = Depends(get_label_manager),
    settings: Settings = Depends(get_settings),
):
    path = get_project_path(params.project, "videos", params.video)
    video = cv2.VideoCapture(path)

    name = os.path.splitext(params.video)[0]
    destination = get_project_path(params.project, "labeled-data", name)
    os.makedirs(destination, exist_ok=True)

    for frame in body.frames:
        image_name = settings.frame_format.format(frame)
        image_path = os.path.join(destination, image_name)
        if not os.path.exists(image_path):
            video.set(cv2.CAP_PROP_POS_FRAMES, frame)
            success, image = video.read()
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed reading frame '{frame}' from video",
                )
            cv2.imwrite(image_path, image)
        # add new frame to collected data file
        manager.add(params.project, params.video, {image_name: {}})
        yield image_name

    video.release()


@router.get("/{video}/labels", response_model=LabelsModel)
def get_labels(
    params: VideoCommonQuery = Depends(VideoCommonQuery),
    manager: LabelManager = Depends(get_label_manager),
):
    return manager.get_labels(params.project, params.video)


@router.put("/{video}/labels")
def update_labels(
    labels: LabelsModel,
    params: VideoCommonQuery = Depends(VideoCommonQuery),
    manager: LabelManager = Depends(get_label_manager),
):
    manager.add(params.project, params.video, labels)
