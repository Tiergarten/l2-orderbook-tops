import logging
import os
import unittest
import pandas as pd
import numpy as np
from numpy.testing import assert_array_equal

from helper import *
from l2_orderbook_tops import l2_orderbook_tops

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class TestSameMillis(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSameMillis, self).__init__(*args, **kwargs)

    def test_bids(self):
        input_data = (
            (pd.Timestamp('2019-01-01 00:15:54'), 100.00, 0.01, 1),
            (pd.Timestamp('2019-01-01 00:15:54'), 100.05, 0.02, 1),
            (pd.Timestamp('2019-01-01 00:15:54'), 100.06, 0.02, 1)
        )

        df = pre_process_input(input_data)
        ret = l2_orderbook_tops.get_tops(df, watch_dollar_dist_depth=100).values

        # All for same millisecond, we should get one output row
        self.assertEqual(ret.shape[0], 1)

        expected_bids = [10006, 20, 10005, 20, 10000, 10] + [0] * 10
        assert_tops_output_equal(ret[0], expected_bids_in=expected_bids)
