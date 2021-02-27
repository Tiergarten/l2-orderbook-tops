import logging
import os
import unittest
import pandas as pd
import numpy as np
from numpy.testing import assert_array_equal

from helper import *
from l2_orderbook_tops import l2_orderbook_tops

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


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
