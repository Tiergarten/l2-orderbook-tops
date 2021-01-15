import os
import pandas as pd
import numpy as np
from l2_orderbook_tops import l2_orderbook_tops


def set_types(df):
    '''Pre-process input, convert decimals to unsigned ints'''

    df['timestamp'] = df['timestamp'].astype('uint64')

    df['side'] = np.where(df['side'] == 'b', 1, 0)
    df['side'] = df['side'].astype('uint32')

    df['price'] = (df['price']*100).astype('uint32')
    df['qty'] = (df['qty']*1000).astype('uint32')

    return df


def get_binance_orderbook_snap_delta(input_dir, dt):
    '''Load Binance L2 orderbook snapshot and delta files'''
    
    fn_template = os.path.join(input_dir, 'BTCUSDT_T_DEPTH_{}_depth_'.format(dt))
    snap_fn = fn_template + 'snap.csv'
    update_fn = fn_template + 'update.csv'
    
    needed_cols = ['timestamp', 'side', 'price', 'qty'] 
    
    return pd.read_csv(snap_fn, usecols=needed_cols), pd.read_csv(update_fn, usecols=needed_cols)


def get_binance_tops(input_dir, input_date):
    '''Get tops from binance orderbook data and skip over the start-of-day snapshot data'''
    snap, delta = get_binance_orderbook_snap_delta(input_dir, input_date)
    df = pd.concat([snap, delta])

    df = set_types(df)
    tops = l2_orderbook_tops.get_tops(df)
    
    return tops.iloc[snap.shape[0]:]

