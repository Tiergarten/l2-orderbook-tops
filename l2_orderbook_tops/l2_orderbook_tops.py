from l2_orderbook_tops import py_price_level_book
import pandas as pd
import logging


def get_tops(df, tops_len=500, watch_dollar_dist_depth=50):
    """
    Get tops from binance orderbook data and skip over the start-of-day snapshot data

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe which requires the following columns: timestamp, side, price, qty

    tops_len : int
        Number of TOP N bid/asks to track

    watch_dollar_dist_depth : int
        Dollar amount of order size to track from mid_price and store in a_total/b_total columns

    Returns
    -------
    out : pd.DataFrame
        Dataframe containing order book data parsed into TOPS view

    """
    logging.info('Calculating top({}, watch_depth={})'.format(tops_len, watch_dollar_dist_depth))
    ts, tops = py_price_level_book.l2_walk(df['timestamp'].values, df['side'].values, df['price'].values,
                                           df['qty'].values, tops_len, watch_dollar_dist_depth)

    df = _to_dataframe(ts, tops, tops_len)
    return df


def _to_dataframe(ts, tops_data, tops_n):
    """
    Merge timestamp and data dataframes, set column names

    Notes
    -----
    ts (64bit) and tops (32bit) has to be built into seperate dataframes and
    joined to avoid everything being upcasted to 64bit
    """
    ts_df = pd.DataFrame(ts, columns=['ts'])
    data_df = pd.DataFrame(tops_data)
    
    data_df.columns = _get_columns(tops_n)

    return pd.merge(ts_df, data_df, left_index=True, right_index=True)


def _get_columns(tops_n):
    """
    Create column names for dataframe schema based on number of TOPS required
    """
    col_pairs = [('b_'+str(n), 'bq_'+str(n)) for n in range(tops_n)]
    col_pairs += [('a_'+str(n), 'aq_'+str(n)) for n in range(tops_n)]

    flattened_cols = [item for sublist in col_pairs for item in sublist]
    return flattened_cols + ['b_total', 'a_total']
