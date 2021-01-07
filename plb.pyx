# distutils: language = c++

from price_level_book cimport Book
import numpy as np
cimport numpy as np
from cpython cimport array
cimport cython

cdef class PyBook:
    cdef Book *book

    def __cinit__(self):
        self.book = new Book()

    def add_bid(self, double price, double qty):
        self.book.add_bid(price, qty)

    def add_ask(self, double price, double qty):
        self.book.add_ask(price, qty)

    def get_top10(self):
        cdef double ret[10*2*2]
        ret[:] = self.book.get_tops(10)
        return ret


cdef class L2Walk:
    def __cinit__(self, int top_n):
        pass

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def l2_walk(self, long[:] _ts, long[:] _side, double[:] _price, double[:] _qty):
        cdef int T = len(_ts)
        cdef Book *book = new Book()
        
        _out = np.full(T*10*2*2, 0, dtype=np.dtype('d')).reshape((T, 10*2*2))
        cdef double[:,::1] out_view = _out

        cdef int i
        cdef double ret[40]

        for i in range(len(_ts)):
            if _side[i] == 1:
                book.add_bid(_price[i], _qty[i])
            else:
                book.add_ask(_price[i], _qty[i])
		
            ret[:] = book.get_tops(10)
            out_view[i] = ret
            
        return _out
		    
