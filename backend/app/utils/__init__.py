import os
from typing import List, Optional

import yaml
from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError, Field, root_validator

from .deepmerge import deepmerge
from ..config import get_settings


def is_safe_path(base, path, follow_symlinks=True):
    if follow_symlinks:
        path = os.path.realpath(path)
    else:
        path = os.path.abspath(path)
    base = os.path.abspath(base)
    return base == os.path.commonpath((base, path))


def ensure_safe_path(base, path, follow_symlinks=True):
    if is_safe_path(base, path, follow_symlinks):
        return path
    raise HTTPException(status.HTTP_403_FORBIDDEN)


def get_project_path(path, *paths):
    """Returns a path relative to the project directory, raises `HTTPException` for unsafe paths"""
    base = get_settings().projects
    return ensure_safe_path(base, os.path.join(base, path, *paths))


class ProjectConfig(BaseModel):
    bodyparts: List[str]
    colormap: str = "rainbow"
    individuals: Optional[List[str]]
    multi_animal: bool = Field(alias="multianimalproject", default=False)
    scorer: str

    @root_validator(pre=True)
    def handle_aliases(cls, values):
        if bodyparts := values.get("multianimalbodyparts"):
            values["bodyparts"] = bodyparts
        return values


def get_project_config(project: str) -> Optional[ProjectConfig]:
    path = get_project_path(project, "config.yaml")
    if os.path.exists(path):
        with open(path) as file:
            data = yaml.safe_load(file)
        return ProjectConfig.parse_obj(data)


class QueryModel(BaseModel):
    """Special model which allows creating a pydantic model that works with query parameters"""

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
        except ValidationError as e:
            errors = e.errors()
            for error in errors:
                error["loc"] = ("query",) + error["loc"]
            raise HTTPException(422, detail=errors)
