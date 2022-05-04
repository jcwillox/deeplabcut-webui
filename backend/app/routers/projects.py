import os

from fastapi import APIRouter, Depends
from natsort import os_sorted

from ..config import get_settings, Settings

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
    return os_sorted(os.listdir(settings.projects))
