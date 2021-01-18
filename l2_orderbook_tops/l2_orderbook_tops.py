from l2_orderbook_tops import py_price_level_book
import pandas as pd
import logging

def get_tops(df, tops_len=8, watch_dollar_dist_depth=50):
    logging.info('Calculating top({}, watch_depth={})'.format(tops_len, watch_dollar_dist_depth))
    ts, tops = py_price_level_book.l2_walk(df['timestamp'].values, df['side'].values, df['price'].values, 
            df['qty'].values, tops_len, watch_dollar_dist_depth)

    df = to_dataframe(ts, tops, tops_len)
    return df


def to_dataframe(ts, tops_data, tops_n):
    '''ts (64bit) and tops (32bit) has to be built into seperate dataframes and
    joined to avoid everything being upcasted to 64bit'''
    ts_df = pd.DataFrame(ts, columns=['ts'])
    data_df = pd.DataFrame(tops_data)
    
    data_df.columns = get_columns(tops_n)

    return pd.merge(ts_df, data_df, left_index=True, right_index=True)


def get_columns(tops_n):
    col_pairs = [('b_'+str(n), 'bq_'+str(n)) for n in range(tops_n)]
    col_pairs +=  [('a_'+str(n), 'aq_'+str(n)) for n in range(tops_n)]

    flattened_cols = [item for sublist in col_pairs for item in sublist]
    return flattened_cols + ['b_total', 'a_total']
