# distutils: language = c++

from price_level_book cimport Book
import numpy as np
cimport numpy as np
import pandas as pd
from cpython cimport array
cimport cython


@cython.boundscheck(False)
@cython.wraparound(False)
def l2_walk(long[:] _ts, long[:] _side, double[:] _price, double[:] _qty, int TOP_LEN=8, int total_dollar_depth=0):
    cdef Book *book = new Book(TOP_LEN)
    cdef int row_sz = book.out_len()

    # TODO: For large orderbooks we won't use the full len in output as we're only interested in tops
    # Can I use a heuristic to allocate a fraction of the initial array and re-alloc if needed?
    cdef Py_ssize_t T = len(_ts)

    _out_tops = np.full((T,row_sz), np.nan, dtype=np.dtype('d'))
    cdef double[:,::1] out_tops_view = _out_tops

    _out_ts = np.full((T,), np.nan, dtype=np.dtype('long'))
    cdef long[:] out_ts_view = _out_ts

    cdef int i, out_ix

    # TODO: This return double* size information needs to be set dynamically
    cdef double ret[(8*2*2)+2]
    cdef double prev_ret[(8*2*2)+2]

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
    ret_np = np.hstack((_out_ts, _out_tops))
    ret_np = ret_np[~np.isnan(ret_np).any(axis=1)]

    ret_df = pd.DataFrame(ret_np)
    ret_df.columns = get_columns(TOP_LEN)

    return ret_df


def get_columns(tops_n):
    cols = []
    side = 'b'

    num = 0
    for i in range(tops_n*2):
        if i == tops_n:
            side ='a'
            num = 0

        cols.append('{}_{}'.format(side, num))
        cols.append('{}q_{}'.format(side, num))

        num = num + 1

    cols.append('b_total')
    cols.append('a_total')

    return ['ts'] + cols

