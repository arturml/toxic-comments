import pandas as pd
import numpy as np
from scipy.stats import hmean
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--subs', nargs='+', type=str)
parser.add_argument('--output', nargs=1, type=str)
args = parser.parse_args()
preds = pd.read_csv(args.subs[0])
subs = np.stack([pd.read_csv(x).set_index('id').values for x in args.subs])
preds.iloc[:, 1:] = hmean(subs+1e-40, axis=0)
preds.to_csv(args.output[0], index=False)