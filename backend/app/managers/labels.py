import os
from functools import lru_cache
from typing import Dict, Literal, cast

import pandas as pd

from ..utils import get_project_path

LabelsModel = Dict[str, Dict[str, Dict[Literal["x", "y"], float]]]


class LabelManager:
    def __init__(self):
        pass

    @staticmethod
    def get_labels(project, video) -> LabelsModel:
        """Retrieve labelled points of each frame for a given video."""
        name = os.path.splitext(video)[0]
        path = get_project_path(project, "labeled-data", name, "CollectedData_TM.h5")

        if not os.path.exists(path):
            return {}

        df: pd.DataFrame = cast(pd.DataFrame, pd.read_hdf(path))
        output = {}

        for image in df.index:
            image_name = os.path.basename(image)

            output[image_name] = {
                df.columns[i][1]: {
                    "x": df.loc[image][df.columns[i]],
                    "y": df.loc[image][df.columns[i + 1]],
                }
                # iterate by 2's, so we can grab x,y pairs
                for i in range(0, len(df.columns), 2)
            }

        return output


@lru_cache()
def get_label_manager():
    return LabelManager()
