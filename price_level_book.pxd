from libcpp.set cimport set

cdef extern from "price_level_book.cpp":
    pass

cdef extern from "price_level_book.h":
    cdef cppclass Book:
        Book(int tops_n) except +
        int out_len()
        void add_ask(unsigned int price, unsigned int qty)
        void add_bid(unsigned int price, unsigned int qty)
        unsigned *get_tops(unsigned int total_dollar_depth)
