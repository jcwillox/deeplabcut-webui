import os
import threading
import time
from functools import lru_cache
from queue import SimpleQueue
from typing import Dict, Literal, Tuple, cast, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI

from ..utils import get_project_path, deepmerge

# frame -> individual -> bodypart -> coords
LabelsModel = Dict[str, Dict[str, Dict[str, Dict[Literal["x", "y"], Optional[float]]]]]
LabelsGroups = Dict[Tuple[str, str], LabelsModel]


class LabelManager:
    def __init__(self):
        self.queue: "SimpleQueue[LabelsGroups]" = SimpleQueue()
        self.shutdown_event = threading.Event()

    def add(self, project: str, video: str, labels: LabelsModel):
        self.queue.put({(project, video): labels})

    def _worker(self):
        while not self.shutdown_event.is_set():
            groups: LabelsGroups = {}

            for _ in range(self.queue.qsize()):
                item = self.queue.get()
                deepmerge(item, groups)

            for (project, video), item in groups.items():
                self.write_labels(project, video, item)

            # write at most once per second
            time.sleep(1)

    @staticmethod
    def get_labels(project, video) -> LabelsModel:
        """Retrieve labelled points of each frame for a given video."""
        name = os.path.splitext(video)[0]
        path = get_project_path(project, "labeled-data", name, "CollectedData_TM.h5")

        if not os.path.exists(path):
            return {}

        df: pd.DataFrame = cast(pd.DataFrame, pd.read_hdf(path)).replace({np.nan: None})
        output = {}

        multi_animal = "individuals" in df.columns.names

        for image in df.index:
            image_name = os.path.basename(image)
            output.setdefault(image_name, {})

            if multi_animal:
                for i in range(0, len(df.columns), 2):
                    individual = df.columns[i][1]
                    bodypart = df.columns[i][2]
                    output[image_name].setdefault(individual, {})
                    output[image_name][individual][bodypart] = {
                        "x": df.loc[image][df.columns[i]],
                        "y": df.loc[image][df.columns[i + 1]],
                    }
            else:
                output[image_name]["individual1"] = {
                    df.columns[i][1]: {
                        "x": df.loc[image][df.columns[i]],
                        "y": df.loc[image][df.columns[i + 1]],
                    }
                    # iterate by 2's, so we can grab x,y pairs
                    for i in range(0, len(df.columns), 2)
                }

        return output

    @staticmethod
    def get_labelled_count(labels: LabelsModel) -> int:
        """Returns the number of frames which have at least one point labelled."""

        def has_labels(frame_: str) -> bool:
            for bodyparts in labels[frame_].values():
                if any(c["x"] or c["y"] for c in bodyparts.values()):
                    return True

        count = 0
        for frame in labels:
            if has_labels(frame):
                count += 1
        return count

    @staticmethod
    def write_labels(project, video, labels: LabelsModel):
        name = os.path.splitext(video)[0]
        path = get_project_path(project, "labeled-data", name, "CollectedData_TM")
        path_hdf = path + ".h5"
        path_csv = path + ".csv"

        df: pd.DataFrame = cast(pd.DataFrame, pd.read_hdf(path_hdf))

        for image, parts in labels.items():
            for bodypart, coords in parts.items():
                image_path = os.path.join("labeled-data", name, image)
                for coord, value in coords.items():
                    df.loc[image_path][("TM", bodypart, coord)] = value

        # create backups before writing the files
        os.replace(path_hdf, path_hdf + ".bak")
        os.replace(path_csv, path_csv + ".bak")

        # save to disk
        df.to_csv(path_csv)
        df.to_hdf(path_hdf, "df_with_missing")

    def _start(self):
        threading.Thread(target=self._worker).start()

    def _close(self):
        self.shutdown_event.set()

    def register_events(self, app: FastAPI):
        app.add_event_handler("startup", self._start)
        app.add_event_handler("shutdown", self._close)


@lru_cache()
def get_label_manager():
    return LabelManager()
