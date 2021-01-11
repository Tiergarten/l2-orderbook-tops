from libcpp.set cimport set

cdef extern from "price_level_book.cpp":
    pass

cdef extern from "price_level_book.h":
    cdef cppclass PriceLevel:
        double price, qty
        PriceLevel(double p, double q) except +

    cdef cppclass Book:
        Book(int tops_n) except +
        int out_len()
        void add_ask(double price, double qty)
        void add_bid(double price, double qty)
        double *get_tops(int total_dollar_depth)
