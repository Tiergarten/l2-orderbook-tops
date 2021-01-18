import logging
import os
import unittest
import pandas as pd
import numpy as np
from numpy.testing import assert_array_equal
from l2_orderbook_tops import l2_orderbook_tops

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


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


def assert_tops_output_equal(output, expected_ts, expected_bids, expected_asks):
    # TODO: If input len doesn't match top N then pad with zeros
    expected_bids = np.array(expected_bids)
    expected_asks = np.array(expected_asks)

    expected_bid_sz = np.array([sum(expected_bids[1::2])])
    expected_ask_sz = np.array([sum(expected_asks[1::2])])

    assert_array_equal(output[0], expected_ts, 'timestamps do not match')
    assert_array_equal(output[1:17], expected_bids, 'bids do not match')
    assert_array_equal(output[17:-2], expected_asks, 'asks do not match')
    assert_array_equal(output[-2], expected_bid_sz, 'total bid watch size does not match')
    assert_array_equal(output[-1], expected_ask_sz, 'total ask watch size does not match')


class TestWatch(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestWatch, self).__init__(*args, **kwargs)

    def test_bid_watch(self):
        input_data = (
            (pd.Timestamp('2019-01-01 00:15:54'), 100.00, 0.01, 1),
            (pd.Timestamp('2019-01-01 00:16:54'), 50.05, 0.02, 1),
            (pd.Timestamp('2019-01-01 00:16:54'), 45.05, 0.02, 1)
        )

        df = pre_process_input(input_data)
        ret = l2_orderbook_tops.get_tops(df, watch_dollar_dist_depth=5000).values

        final_iteration = ret[-1]
        self.assertEqual(final_iteration[-2], 30)

    def test_ask_watch(self):
        input_data = (
            (pd.Timestamp('2019-01-01 00:15:54'), 100.00, 0.01, 0),
            (pd.Timestamp('2019-01-01 00:16:54'), 149.00, 0.02, 0),
            (pd.Timestamp('2019-01-01 00:16:54'), 151.00, 0.02, 0)
        )

        df = pre_process_input(input_data)
        ret = l2_orderbook_tops.get_tops(df, watch_dollar_dist_depth=5000).values

        final_iteration = ret[-1]
        self.assertEqual(final_iteration[-1], 30)


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_bids(self):
        input_data = (
            (pd.Timestamp('2019-01-01 00:15:54'), 100.00, 0.01, 1),
            (pd.Timestamp('2019-01-01 00:16:54'), 100.05, 0.02, 1)
        )
        df = pre_process_input(input_data)
        ret = l2_orderbook_tops.get_tops(df, watch_dollar_dist_depth=100).values

        self.assertEqual(ret.shape[0], df.shape[0])
        col_sz = ret.shape[1]

        # First iteration
        #self.assertEqual(ret[0][0], df.dt.astype(np.int64).values[0])
        self.assertEqual(ret[0][1], 10000)
        self.assertEqual(ret[0][2], 10)
        np.testing.assert_array_equal(ret[0][3:col_sz-2], np.zeros(ret.shape[1]-3-2))
        self.assertEqual(ret[0][-2], 10)
        self.assertEqual(ret[0][-1], 0)

        # Second iteration
        #self.assertEqual(ret[1][0], df.dt.astype(np.int64).values[1])
        self.assertEqual(ret[1][1], 10005)
        self.assertEqual(ret[1][2], 20)
        self.assertEqual(ret[1][3], 10000)
        self.assertEqual(ret[1][4], 10)
        assert_array_equal(ret[1][5:col_sz - 2], np.zeros(ret.shape[1] - 5 - 2))
        self.assertEqual(ret[1][-2], 30)
        self.assertEqual(ret[1][-1], 0)

    def test_bid_asks(self):
        input_data = (
            (pd.Timestamp('2019-01-01 00:15:54'), 100.00, 0.01, 1),  # 8
            (pd.Timestamp('2019-01-01 00:16:54'), 100.05, 0.02, 1),
            (pd.Timestamp('2019-01-01 00:16.55'), 100.05, 0.00, 1),
            (pd.Timestamp('2019-01-01 00:17:54'), 100.06, 0.03, 1),  # 7
            (pd.Timestamp('2019-01-01 00:18:54'), 100.07, 0.03, 1),  # 6
            (pd.Timestamp('2019-01-01 00:19:54'), 100.08, 0.03, 1),  # 5
            (pd.Timestamp('2019-01-01 00:20:54'), 100.09, 0.03, 1),  # 4
            (pd.Timestamp('2019-01-01 00:21:54'), 100.10, 0.03, 1),  # 3
            (pd.Timestamp('2019-01-01 00:22:54'), 100.11, 0.03, 1),  # 2
            (pd.Timestamp('2019-01-01 00:23:54'), 100.12, 0.03, 1),  # 1

            (pd.Timestamp('2019-01-01 00:18:54'), 100.14, 0.03, 0),  # 1
            (pd.Timestamp('2019-01-01 00:19:54'), 100.15, 0.02, 0),  # 2
            (pd.Timestamp('2019-01-01 01:19:54'), 100.16, 0.04, 0),  # 3
            (pd.Timestamp('2019-01-01 01:19:54'), 100.17, 0.04, 0),  # 4
            (pd.Timestamp('2019-01-01 01:19:54'), 100.18, 0.04, 0),  # 5
            (pd.Timestamp('2019-01-01 01:19:54'), 100.19, 0.04, 0),  # 6
            (pd.Timestamp('2019-01-01 01:19:54'), 100.20, 0.04, 0),  # 7
            (pd.Timestamp('2019-01-01 01:19:54'), 100.21, 0.04, 0),  # 8
        )

        df = pre_process_input(input_data)
        ret = l2_orderbook_tops.get_tops(df, watch_dollar_dist_depth=100).values

        self.assertEqual(ret.shape[0], df.shape[0])
        col_sz = ret.shape[1]
        final_iteration = ret[-1]

        # TODO: ts to epoch millis conversion hacky
        expected_ts = (df.dt.astype(np.int64).astype(np.uint64).values[-1]/1000000).astype(np.uint64)
        expected_bids = [10012, 30, 10011, 30, 10010, 30, 10009, 30, 10008, 30,
                         10007, 30, 10006, 30, 10000, 10]
        expected_asks = [10014, 30, 10015, 20, 10016, 40, 10017, 40, 10018, 40,
                         10019, 40, 10020, 40, 10021, 40]

        assert_tops_output_equal(final_iteration, expected_ts, expected_bids, expected_asks)


if __name__ == '__main__':
    unittest.main()
