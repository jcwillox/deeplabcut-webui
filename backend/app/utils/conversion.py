import pandas as pd


def ensure_multi_index(df: pd.DataFrame):
    # make paths platform-agnostic if they are not already
    if not isinstance(df.index, pd.MultiIndex):
        path = df.index[0]
        try:
            sep = "/" if "/" in path else "\\"
            splits = tuple(df.index.str.split(sep))
            df.index = pd.MultiIndex.from_tuples(splits)
        except TypeError:  # ignore numerical index of frame indices
            pass
