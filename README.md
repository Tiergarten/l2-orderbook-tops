# l2-orderbook-tops

Extract TOPS (top N best bid & best ask prices and sizes) from L2 orderbook data. 

Optionally sum total bid and ask sizes within specified dollar amount of the mid price at each tick.

See [Example Usage Notebook](docs/example_usage.ipynb) for usage.

## Technology

Python, Numpy, Cython, C++

Makes use of libstdc::set to order L2 price levels on insertion for efficient querying.

## Benchmarks

The basic l2-orderbook-tops implementation runs ~114x faster then the naive Python implementation on a sample of 100,000 L2 price level updates. When tracking the qty of the closest $50 and $100 worth of orders from the mid, this improvement decreases to 15x and 8x respectively.

![alt text](docs/benchmarks.png)

See [Benchmark Notebook](docs/benchmarks.ipynb) for details.
