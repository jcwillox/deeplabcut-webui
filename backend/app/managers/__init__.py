from fastapi import FastAPI

from .labels import get_label_manager, LabelManager, LabelsModel


def register_events(app: FastAPI):
    get_label_manager().register_events(app)
