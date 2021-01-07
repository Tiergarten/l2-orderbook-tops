from libcpp.set cimport set
from libcpp.vector cimport vector

cdef extern from "price_level_book.cpp":
    pass

cdef extern from "price_level_book.h":
    cdef cppclass Book:
        Book() except +
        void add_ask(double price, double qty)
        void add_bid(double price, double qty)
        vector[double] get_tops(int top_n)
