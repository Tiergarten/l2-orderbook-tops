import os
import pandas as pd
from l2_orderbook_tops import plb

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

    df = plb.set_types(df)
    tops = plb.get_tops(df)
    
    return tops.iloc[snap.shape[0]:]

