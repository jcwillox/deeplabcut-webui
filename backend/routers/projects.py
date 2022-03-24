import os

from fastapi import APIRouter

from ..const import PROJECTS_DIR

router = APIRouter()


class ProjectType(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value) -> str:
        if value not in os.listdir(PROJECTS_DIR):
            raise ValueError("this project does not exist")
        return value


@router.get("")
def list_projects():
    return os.listdir(PROJECTS_DIR)
