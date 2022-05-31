import os

from fastapi import APIRouter, Depends, HTTPException, status
from natsort import os_sorted

from ..config import get_settings, Settings
from ..utils import get_project_config, ProjectConfig

router = APIRouter()


class ProjectType(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value) -> str:
        if value not in os.listdir(get_settings().projects):
            raise ValueError("this project does not exist")
        return value


@router.get("")
def list_projects(settings: Settings = Depends(get_settings)):
    for entry in os_sorted(os.scandir(settings.projects), key=lambda x: x.name):
        entry: os.DirEntry
        if not entry.is_dir():
            continue

        info = entry.stat()
        config = get_project_config(entry.name)
        if not config:
            continue

        yield {
            "name": entry.name,
            "accessed": info.st_atime,
            "created": info.st_ctime,
            "multi_animal": config.multi_animal,
            "colormap": config.colormap,
        }


@router.get("/{project}", response_model=ProjectConfig)
def get_project(project: ProjectType):
    config = get_project_config(project)
    if config:
        return config
    raise HTTPException(status.HTTP_404_NOT_FOUND)
