import os
import pandas as pd
import numpy as np
import logging

from l2_orderbook_tops import l2_orderbook_tops


def _set_types(df):
    """Pre-process input, convert decimals to unsigned ints"""

    df['timestamp'] = df['timestamp'].astype('uint64')

    df['side'] = np.where(df['side'] == 'b', 1, 0)
    df['side'] = df['side'].astype('uint32')

    df['price'] = (df['price']*100).astype('uint32')
    df['qty'] = (df['qty']*1000).astype('uint32')

    return df


def _get_binance_orderbook_snap_delta(input_dir, dt, symbol='BTCUSDT'):
    """Load Binance L2 orderbook snapshot and delta files"""
    
    fn_template = os.path.join(input_dir, '{}_T_DEPTH_{}_depth_'.format(symbol, dt))
    snap_fn = fn_template + 'snap.csv'
    update_fn = fn_template + 'update.csv'
    
    needed_cols = ['timestamp', 'side', 'price', 'qty', 'symbol']

    snap_df = pd.read_csv(snap_fn, usecols=needed_cols)
    delta_df = pd.read_csv(update_fn, usecols=needed_cols)

    return snap_df[snap_df['symbol'] == symbol], delta_df[delta_df['symbol'] == symbol]


def get_binance_tops(input_dir, input_date, symbol):
    """
    Helper to get TOPS from raw Binance order book data files

    Parameters
    ----------
    input_dir : string
        Directory which contains Binance orderbook snap and delta files

    input_date : string
        Date of Binance order book data to parse

    watch_dollar_dist_depth : int
        Dollar amount of order size to track from mid_price and store in a_total/b_total columns

    Returns
    -------
    out : pd.DataFrame
        Dataframe containing order book data parsed into TOPS view

    """
    snap, delta = _get_binance_orderbook_snap_delta(input_dir, input_date, symbol)

    snap = _set_types(snap)
    delta = _set_types(delta)

    snap_times = snap['timestamp'].drop_duplicates()
    logging.info(f'Got {len(snap_times)} snapshots...')

    output = []
    for prev, curr in zip(snap_times, snap_times[1:]):
        s = snap[
            snap['timestamp'] == prev
            ]

        c = delta[
            (delta['timestamp'] >= prev)
            & (delta['timestamp'] < curr)
            ]

        snap_and_updates = pd.concat([s, c])
        logging.info(f'Starting snap chunk starting {prev}')
        tops = l2_orderbook_tops.get_tops(snap_and_updates)
        output.append(tops)

    out_concat = pd.concat(output)
    logging.info(f'got {out_concat} output rows')

    # TODO: These columns are useless without prices, remove it completely from C too
    out_concat = out_concat.drop(columns=['a_total', 'b_total'])

    out_concat['bid_quotes'] = [np.array(row) for row in out_concat[[c for c in out_concat.columns if c.startswith('b_')]].to_numpy()]
    out_concat['bid_sizes'] = [np.array(row) for row in out_concat[[c for c in out_concat.columns if c.startswith('bq_')]].to_numpy()]

    out_concat['ask_quotes'] = [np.array(row) for row in out_concat[[c for c in out_concat.columns if c.startswith('a_')]].to_numpy()]
    out_concat['ask_sizes'] = [np.array(row) for row in out_concat[[c for c in out_concat.columns if c.startswith('aq_')]].to_numpy()]

    drop_col_nms = [c for c in out_concat.columns if
                    c.startswith('b_') or c.startswith('bq_') or c.startswith('a_') or c.startswith('aq_')]

    out_concat = out_concat.drop(columns=drop_col_nms)
    return out_concat

