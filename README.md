# l2-orderbook

Extract top N best bid & best ask prices and sizes from L2 orderbook data. 

Optionally sum total bid and ask sizes within specified dollar amount of the mid price at each tick (incurs a significant performance hit, ~21x on 44 million input rows & top_n = 8). 

See example.ipynb for usage.

## Technology

Python, Cython, C++
