import pandas as pd
import numpy as np
from scipy.stats import hmean
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--subs', nargs='+', type=str)
parser.add_argument('--output', nargs=1, type=str)
args = parser.parse_args()
subs = [pd.read_csv(x) for x in args.subs]
preds = subs[0]
preds.iloc[:, 1:] = hmean(np.stack(subs)+1e-40, axis=0)
preds.to_csv(args.output, index=False)