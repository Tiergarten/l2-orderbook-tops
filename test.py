import pandas as pd
import plb 
import numpy as np

snapshot = pd.read_csv('../order_imbalance/BTCUSDT_T_DEPTH_2020-11-01_depth_snap.csv')
deltas = pd.read_csv('../order_imbalance/BTCUSDT_T_DEPTH_2020-11-01_depth_update.csv')
df = pd.concat([snapshot,deltas])

df['side'] = np.where(df['side'] == 'b', 1, 0)

data = df[['timestamp', 'side', 'price', 'qty']] \
        .head(10000) \
        .values
    
ret = plb.l2_walk(data[:,0].astype(int), data[:,1].astype(int), data[:,2], data[:,3])

ret_df = pd.DataFrame(ret)

print(ret_df.head())
