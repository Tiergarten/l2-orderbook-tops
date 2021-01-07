from libcpp.set cimport set

cdef extern from "price_level_book.cpp":
    pass

cdef extern from "price_level_book.h":
    cdef cppclass PriceLevel:
        double price, qty
        PriceLevel(double p, double q) except +

    cdef cppclass Book:
        set[PriceLevel] bids, asks
        Book() except +
        void add_item(double price, double qty, set[PriceLevel] *side)
        void add_ask(double price, double qty)
        void add_bid(double price, double qty)
        double *get_tops(int top_n)
