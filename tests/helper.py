import unittest
import pandas as pd
import numpy as np
from numpy.testing import assert_array_equal


def pre_process_input(input_data):
    """
    Turn input data into a dataframe with the correct column names
    Scale & convert price and qtys into unsigned ints
    """
    df = pd.DataFrame(input_data) \
        .rename(columns={0: 'dt', 1: 'price', 2: 'qty', 3: 'side'})

    df['timestamp'] = (df['dt'].astype(np.int64) / int(1e6)).astype(np.uint64)
    df['side'] = df['side'].astype('uint32')
    df['price'] = (df['price'] * 100).astype('uint32')
    df['qty'] = (df['qty'] * 1000).astype('uint32')

    return df


def assert_tops_output_equal(output, expected_ts=None, expected_bids_in=None, expected_asks_in=None,
                             side_struct_size=(8*2)+1):
    # TODO: If input len doesn't match top N then pad with zeros

    if expected_ts is not None:
        assert_array_equal(output[0], expected_ts, 'timestamps do not match')

    if expected_bids_in is not None:
        expected_bids_in = np.array(expected_bids_in)
        expected_bid_sz = np.array([sum(expected_bids_in[1::2])])

        assert_array_equal(output[1:17], expected_bids_in, 'bids do not match')
        assert_array_equal(output[-2], expected_bid_sz, 'total bid watch size does not match')

    if expected_asks_in is not None:
        expected_asks_in = np.array(expected_asks_in)
        expected_ask_sz = np.array([sum(expected_asks_in[1::2])])

        assert_array_equal(output[17:-2], expected_asks_in, 'asks do not match')
        assert_array_equal(output[-1], expected_ask_sz, 'total ask watch size does not match')