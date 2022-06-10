import os
import shutil
import threading
import time
from functools import lru_cache
from glob import glob
from queue import SimpleQueue
from typing import Dict, Literal, Tuple, cast, Optional, List

import numpy as np
import pandas as pd
from fastapi import FastAPI

from ..utils import get_project_path, deepmerge, get_project_config, ProjectConfig
from ..utils.conversion import ensure_multi_index

# frame -> individual -> bodypart -> coords
LabelsCoords = Dict[Literal["x", "y"], Optional[float]]
LabelsBodyparts = Dict[str, LabelsCoords]
LabelsIndividuals = Dict[str, LabelsBodyparts]
LabelsModel = Dict[str, LabelsIndividuals]

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
        paths = glob(
            get_project_path(project, "labeled-data", name, f"CollectedData_*.h5")
        )
        if len(paths) == 0:
            return {}
        if len(paths) == 1:
            path = paths[0]
        else:
            print("using config to get labels")
            config = get_project_config(project)
            if not config:
                return {}
            path = get_project_path(
                project, "labeled-data", name, f"CollectedData_{config.scorer}.h5"
            )
            if not os.path.exists(path):
                return {}

        df: pd.DataFrame = cast(pd.DataFrame, pd.read_hdf(path)).replace({np.nan: None})
        output = {}

        multi_animal = "individuals" in df.columns.names

        for image in df.index:
            # support old data format
            if not isinstance(df.index, pd.MultiIndex):
                image_name = os.path.basename(image)
            else:
                image_name = image[-1]
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
    def _reindex_dataframe(
        labels: LabelsModel,
        config: ProjectConfig,
        name: str,
        df: Optional[pd.DataFrame] = None,
    ):
        images = [("labeled-data", name, image) for image in labels]
        if df is not None:
            images = list(set(images) - set(df.index))
        if not images:
            return df
        new_df: Optional[pd.DataFrame] = None
        a = np.empty((len(images), 2))
        a[:] = np.nan
        for individual in config.individuals or ["individual1"]:
            for bodypart in config.bodyparts:
                if config.multi_animal:
                    cols = pd.MultiIndex.from_product(
                        [[config.scorer], [individual], [bodypart], ["x", "y"]],
                        names=["scorer", "individuals", "bodyparts", "coords"],
                    )
                else:
                    cols = pd.MultiIndex.from_product(
                        [[config.scorer], [bodypart], ["x", "y"]],
                        names=["scorer", "bodyparts", "coords"],
                    )
                index = pd.MultiIndex.from_tuples(images)
                frame = pd.DataFrame(a, columns=cols, index=index)
                new_df = pd.concat([new_df, frame], axis=1)
        if df is not None:
            new_df = pd.concat([df, new_df], axis=0)
        new_df.sort_index(inplace=True)
        return new_df

    def write_labels(self, project, video, labels: LabelsModel):
        name = os.path.splitext(video)[0]
        base_path = get_project_path(project, "labeled-data", name)
        backup_path = os.path.join(base_path, "backups")

        config = get_project_config(project)
        if not config:
            raise Exception(f"config file missing for project: '{project}'")
        scorer = config.scorer

        path_hdf = os.path.join(base_path, f"CollectedData_{scorer}.h5")
        path_csv = os.path.join(base_path, f"CollectedData_{scorer}.csv")
        os.makedirs(backup_path, exist_ok=True)

        df: Optional[pd.DataFrame]
        if os.path.exists(path_hdf):
            # load dataframe from disk
            df = cast(pd.DataFrame, pd.read_hdf(path_hdf))
            ensure_multi_index(df)
            # add new images to dataframe
            df = self._reindex_dataframe(labels, config, name, df)
        else:
            # create new data frame
            df = self._reindex_dataframe(labels, config, name)

        if df is None:
            return

        for image, individuals in labels.items():
            image_path = ("labeled-data", name, image)
            for individual, bodyparts in individuals.items():
                for bodypart, coords in bodyparts.items():
                    for coord, value in coords.items():
                        if config.multi_animal:
                            key = (scorer, individual, bodypart, coord)
                        else:
                            key = (scorer, bodypart, coord)
                        df.loc[image_path][key] = value

        # create backups before writing the files
        def create_backup(path, suffix, overwrite=False):
            if not os.path.exists(path):
                return
            backup_target = os.path.join(backup_path, os.path.basename(path) + suffix)
            if overwrite or not os.path.exists(backup_target):
                shutil.copy2(path, backup_target)

        create_backup(path_hdf, ".original")
        create_backup(path_csv, ".original")
        create_backup(path_hdf, ".bak", overwrite=True)
        create_backup(path_csv, ".bak", overwrite=True)

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
