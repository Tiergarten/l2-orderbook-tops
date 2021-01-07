# distutils: language = c++

from price_level_book cimport Book
import numpy as np
cimport numpy as np
from cpython cimport array
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def l2_walk(self, long[:] _ts, long[:] _side, double[:] _price, double[:] _qty):
    cdef Book *book = new Book()
   
    cdef Py_ssize_t alloc_len = len(_ts)*5*2*2
    cdef Py_ssize_t T = len(_ts)
    cdef Py_ssize_t y = 5*2*2

    _out_tops = np.full((T,y), np.nan, dtype=np.dtype('d'))
    cdef double[:,::1] out_tops_view = _out_tops

    _out_ts = np.full((T,), np.nan, dtype=np.dtype('long'))
    cdef long[:] out_ts_view = _out_ts

    cdef int i, out_ix
    cdef double ret[5*2*2]
    cdef double prev_ret[5*2*2]

    out_ix = 0
    for i in range(len(_ts)):
        if _side[i] == 1:
            book.add_bid(_price[i], _qty[i])
        else:
            book.add_ask(_price[i], _qty[i])
            
        ret[:] = book.get_tops(5)

        # Only append if we dont already have this row
        if i == 0:
            out_tops_view[out_ix,:] = ret 
            out_ts_view[out_ix] = _ts[i]

            prev_ret = ret
            out_ix = out_ix + 1
        else:
            for x in range(y):
                if ret[x] != prev_ret[x]:
                    out_tops_view[out_ix,:] = ret
                    out_ts_view[out_ix] = _ts[i]

                    out_ix = out_ix + 1
                    break
        prev_ret = ret

    del book
    return np.hstack((_out_ts.reshape((T,1)), _out_tops))
                
