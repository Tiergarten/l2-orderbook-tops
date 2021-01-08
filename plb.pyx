# distutils: language = c++

from price_level_book cimport Book
import numpy as np
cimport numpy as np
from cpython cimport array
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def l2_walk(long[:] _ts, long[:] _side, double[:] _price, double[:] _qty):
    cdef int TOP_LEN = 10 
    cdef Book *book = new Book(TOP_LEN)
   
    cdef Py_ssize_t alloc_len = len(_ts)*TOP_LEN*2*2
    cdef Py_ssize_t T = len(_ts)
    cdef Py_ssize_t y = TOP_LEN*2*2

    _out_tops = np.full((T,y), np.nan, dtype=np.dtype('d'))
    cdef double[:,::1] out_tops_view = _out_tops

    _out_ts = np.full((T,), np.nan, dtype=np.dtype('long'))
    cdef long[:] out_ts_view = _out_ts

    cdef int i, out_ix

    cdef double ret[10*2*2]
    cdef double prev_ret[10*2*2]

    out_ix = 0
    for i in range(len(_ts)):
        if _side[i] == 1:
            book.add_bid(_price[i], _qty[i])
        else:
            book.add_ask(_price[i], _qty[i])
           
        ret[:] = book.get_tops()

        # Only append if we dont already have this row
        if i == 0:
            out_tops_view[out_ix,:] = ret 
            out_ts_view[out_ix] = _ts[i]
        else:
            for x in range(y):
                if ret[x] != prev_ret[x]:
                    out_tops_view[out_ix,:] = ret
                    out_ts_view[out_ix] = _ts[i]
                    break


        prev_ret = ret
        out_ix = out_ix + 1

    del book

    ret_np = np.hstack((_out_ts.reshape((T,1)), _out_tops))
    ret_np = ret_np[~np.isnan(ret_np).any(axis=1)]
    return ret_np            
