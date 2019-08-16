from typing import Tuple
import typing
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from typing import List

class TrainData(typing.NamedTuple):
    feats: np.ndarray
    targs: np.ndarray
      
    
def format_data(dat, targ_column:List[str]) -> Tuple[TrainData, StandardScaler]:
    scale = StandardScaler().fit(dat)
    proc_dat = dat.as_matrix()
    mask = np.ones(proc_dat.shape[1], dtype=bool)
    dat_cols = list(dat.columns)
    for col_name in targ_column:
        mask[dat_cols.index(col_name)] = False
    feats = proc_dat[:, mask].astype(float)
    targs = proc_dat[:, ~mask].astype(float)
    return TrainData(feats, targs)

def make_data(csv_path:str, target_col:str)->TrainData:
    final_df = pd.read_csv(csv_path)
    final_df = final_df[:6087]
    height_df = final_df[[target_col, 'precip', 'temp']]
    height_df.columns = [target_col, 'precip', 'temp']
    preprocessed_data2, s = format_data(height_df, [target_col])
    return preprocessed_data2

