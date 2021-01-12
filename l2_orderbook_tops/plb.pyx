# distutils: language = c++

from price_level_book cimport Book
import numpy as np
cimport numpy as np
import pandas as pd
from cpython cimport array
cimport cython


def set_types(df):
    '''Pre-process input'''

    df['timestamp'] = df['timestamp'].astype('uint64')

    df['side'] = np.where(df['side'] == 'b', 1, 0)
    df['side'] = df['side'].astype('uint32')

    df['price'] = (df['price']*100).astype('uint32')
    df['qty'] = (df['qty']*1000).astype('uint32')

    return df


@cython.boundscheck(False)
@cython.wraparound(False)
def l2_walk(unsigned long long[:] _ts, unsigned int[:] _side, unsigned int[:] _price, unsigned int[:] _qty, int TOP_LEN=8, int total_dollar_depth=0):
    cdef Book *book = new Book(TOP_LEN)
    cdef int row_sz = book.out_len()

    # TODO: For large orderbooks we won't use the full len in output as we're only interested in tops
    # Can I use a heuristic to allocate a fraction of the initial array and re-alloc if needed?
    cdef Py_ssize_t T = len(_ts)

    _out_tops = np.full((T,row_sz), 0, dtype=np.uint32)
    cdef unsigned int[:,::1] out_tops_view = _out_tops

    _out_ts = np.full((T,), 0, dtype=np.uint64)
    cdef unsigned long[:] out_ts_view = _out_ts

    cdef int i, out_ix

    # TODO: This array size information needs to be set dynamically
    cdef unsigned int ret[(8*2*2)+2]
    cdef unsigned int prev_ret[(8*2*2)+2]

    out_ix = 0
    for i in range(T):
        if _side[i] == 1:
            book.add_bid(_price[i], _qty[i])
        else:
            book.add_ask(_price[i], _qty[i])
           
        ret[:] = book.get_tops(total_dollar_depth)

        if i == 0:
            out_tops_view[out_ix,:] = ret 
            out_ts_view[out_ix] = _ts[i]
        # Only append if there is a change in tops(n)
        # Do not include total_bid, total_ask in check as they'll always change (hence -2)
        else:
            for x in range(row_sz-2):
                if ret[x] != prev_ret[x]:
                    out_tops_view[out_ix,:] = ret
                    out_ts_view[out_ix] = _ts[i]
                    break


        prev_ret = ret
        out_ix = out_ix + 1

    del book

    _out_ts = _out_ts.reshape((T,1))
    return to_dataframe(_out_ts[_out_ts.any(axis=1)], _out_tops[_out_tops.any(axis=1)], TOP_LEN)


def to_dataframe(ts, tops_data, tops_n):
    '''ts (64bit) and tops (32bit) has to be built into seperate dataframes and
    joined to avoid everything being upcasted to 64bit'''
    ts_df = pd.DataFrame(ts, columns=['ts'])
    data_df = pd.DataFrame(tops_data)
    data_df.columns = get_columns(tops_n)

    return pd.merge(ts_df, data_df, left_index=True, right_index=True)


def get_tops(df, tops_n=8, total_dollar_depth=50):
        return l2_walk(df['timestamp'].values, df['side'].values, df['price'].values, df['qty'].values)


def get_columns(tops_n):
    cols = []
    side = 'b'

    num = 0
    for i in range(tops_n*2):
        if i == tops_n:
            side ='a'
            num = 0

        col_nm = '{}_{}'.format(side, num)
        cols.append(col_nm)
        
        col_nm = '{}q_{}'.format(side, num)
        cols.append(col_nm)

        num = num + 1

    cols.append('b_total')
    cols.append('a_total')

    return cols
