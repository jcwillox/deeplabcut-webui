import os
from functools import lru_cache
from typing import Dict, Literal, Tuple, cast, Optional

import numpy as np
import pandas as pd

from ..utils import get_project_path

# frame -> individual -> bodypart -> coords
LabelsModel = Dict[str, Dict[str, Dict[str, Dict[Literal["x", "y"], Optional[float]]]]]
LabelsGroups = Dict[Tuple[str, str], LabelsModel]


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


@lru_cache()
def get_label_manager():
    return LabelManager()
