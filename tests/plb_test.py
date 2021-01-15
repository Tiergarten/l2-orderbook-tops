import logging
import os
import unittest
import pandas as pd
import numpy as np

from l2_orderbook_tops import l2_orderbook_tops 

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def get_sample_input(self):
        input_data = (
            (pd.Timestamp('2019-01-01 00:15:54'), 100.00, 0.01, 1),
            (pd.Timestamp('2019-01-01 00:16:54'), 100.05, 0.02, 1),
            (pd.Timestamp('2019-01-01 00:16.55'), 100.05, 0.00, 1),
            (pd.Timestamp('2019-01-01 00:17:54'), 100.06, 0.03, 1),
            (pd.Timestamp('2019-01-01 00:18:54'), 100.07, 0.03, 0),
            (pd.Timestamp('2019-01-01 00:19:54'), 100.08, 0.02, 0),
            (pd.Timestamp('2019-01-01 01:19:54'), 100.08, 0.04, 0)
        )

        df = pd.DataFrame(input_data) \
            .rename(columns={0: 'dt', 1: 'price', 2: 'qty', 3: 'side'})

        df['timestamp'] = (df['dt'].astype(np.int64) / int(1e6)).astype(np.uint64)
        df['side'] = df['side'].astype('uint32')
        df['price'] = (df['price']*100).astype('uint32')
        df['qty'] = (df['qty']*1000).astype('uint32')

        return df

    def test_bids(self):
        df = self.get_sample_input()

        """
        ret = plb.l2_walk(df['dt'].values, df['side'].values, df['price'].values, 
                df['qty'].values, total_dollar_depth=100).values
        """

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
        np.testing.assert_array_equal(ret[1][5:col_sz - 2], np.zeros(ret.shape[1] - 5 - 2))
        self.assertEqual(ret[1][-2], 30)
        self.assertEqual(ret[1][-1], 0)


if __name__ == '__main__':
    unittest.main()
