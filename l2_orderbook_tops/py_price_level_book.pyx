# distutils: language = c++

import numpy as np
import pandas as pd
import logging

from cpython cimport array
cimport cython
cimport numpy as np

from price_level_book cimport Book

cdef int array_cmp(unsigned int *left, unsigned int *right, unsigned int size):
    for i in range(size):
        if left[i] != right[i]:
            return 1

    return 0

@cython.boundscheck(False)
@cython.wraparound(False)
def l2_walk(unsigned long long[:] _ts, unsigned int[:] _side, unsigned int[:] _price, unsigned int[:] _qty, 
        unsigned int tops_n=8, unsigned int watch_dollar_dist_depth=0):

    cdef Book *book = new Book(tops_n)
    cdef int row_sz = book.out_len()

    # TODO: For large orderbooks we won't use the full len in output as we're only interested in tops
    # Can I use a heuristic to allocate a fraction of the initial array and re-alloc if needed?
    cdef Py_ssize_t T = len(_ts)

    _out_tops = np.full((T,row_sz), 0, dtype=np.uint32)
    cdef unsigned int[:,::1] out_tops_view = _out_tops

    _out_ts = np.full((T,), 0, dtype=np.uint64)
    cdef unsigned long[:] out_ts_view = _out_ts

    cdef unsigned int i, out_ix

    # TODO: This array size information needs to be set dynamically
    cdef unsigned int ret[(8*2*2)+2]
    cdef unsigned int prev_ret[(8*2*2)+2]

    out_ix = 0
    i = 0
    while i < T:
        # Updates from the same timestamp should be applied in bulk
        # before writing an output row
        while True:
            if _side[i] == 1:
                book.add_bid(_price[i], _qty[i])
            else:
                book.add_ask(_price[i], _qty[i])

            if _ts[i+1] ==  _ts[i]:
                i = i + 1
            else:
                break

        ret[:] = book.get_tops(watch_dollar_dist_depth)
        #print('raw: ' + str(ret))

        # Only append row if TOPS change (or initial row)
        if out_ix == 0 or array_cmp(ret, prev_ret, row_sz-2) != 0:
            out_tops_view[out_ix,:] = ret 
            out_ts_view[out_ix] = _ts[i]
            #print('adding: ' + str(ret))

            prev_ret = ret
            out_ix = out_ix + 1

        i = i + 1

    del book

    logging.info(f'Wrote {out_ix} rows')

    _out_ts = _out_ts.reshape((T,1))
    return _out_ts[:out_ix], _out_tops[:out_ix]