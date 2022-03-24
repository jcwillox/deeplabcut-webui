import os
from typing import List

import cv2
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from pydantic import validator, BaseModel

from .projects import ProjectType
from ..responses.video import VideoResponse
from ..utils import QueryModel, get_project_path

router = APIRouter()


class VideoItemResponse(BaseModel):
    name: str
    accessed: float
    created: float
    size: int


@router.get("", response_model=List[VideoItemResponse])
def list_videos(project: ProjectType):
    path = get_project_path(project, "videos")
    for entry in os.scandir(path):
        entry: os.DirEntry
        info = entry.stat()
        yield {
            "name": entry.name,
            "accessed": info.st_atime,
            "created": info.st_ctime,
            "size": info.st_size,
        }


class VideoCommonQuery(QueryModel):
    project: ProjectType
    video: str

    @validator("video")
    def valid_video(cls, value: str, values) -> str:
        if "project" in values and value not in os.listdir(
            get_project_path(values["project"], "videos")
        ):
            raise ValueError("this video does not exist")
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
    return VideoResponse(request, file_path=path, content_type="video/mp4")
