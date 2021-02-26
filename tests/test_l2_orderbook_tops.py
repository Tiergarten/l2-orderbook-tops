import logging
import os
import unittest
import pandas as pd
import numpy as np
from numpy.testing import assert_array_equal

from helper import *
from l2_orderbook_tops import l2_orderbook_tops

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


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
            (pd.Timestamp('2019-01-01 01:19:55'), 100.16, 0.04, 0),  # 3
            (pd.Timestamp('2019-01-01 01:19:56'), 100.17, 0.04, 0),  # 4
            (pd.Timestamp('2019-01-01 01:19:57'), 100.18, 0.04, 0),  # 5
            (pd.Timestamp('2019-01-01 01:19:58'), 100.19, 0.04, 0),  # 6
            (pd.Timestamp('2019-01-01 01:19:59'), 100.20, 0.04, 0),  # 7
            (pd.Timestamp('2019-01-01 01:20:00'), 100.21, 0.04, 0),  # 8
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
