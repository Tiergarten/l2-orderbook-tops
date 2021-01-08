import logging
import os
import unittest
import pandas as pd
import numpy as np
import plb

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_bids(self):
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
                .rename(columns={0:'dt', 1:'price', 2:'qty', 3:'side'}) 

        ret = plb.l2_walk(df.dt.astype(int).values, df.side.astype(int).values, df.price.values, df.qty.values)

        self.assertEqual(ret.shape[0], len(input_data))

        # First iteration
        self.assertEqual(ret[0][0], df.dt.astype(int).values[0])
        self.assertEqual(ret[0][1], 100)
        self.assertEqual(ret[0][2], 0.01)
        np.testing.assert_array_equal(ret[0][3:], np.zeros(ret.shape[1]-3))

        # Second iteration
        self.assertEqual(ret[1][0], df.dt.astype(int).values[1])
        self.assertEqual(ret[1][1], 100.05)
        self.assertEqual(ret[1][2], 0.02)

        self.assertEqual(ret[1][3], 100.0)
        self.assertEqual(ret[1][4], 0.01)

        # Third iteration
        self.assertEqual(ret[2][0], df.dt.astype(int).values[2])
        self.assertEqual(ret[2][1], 100)
        self.assertEqual(ret[2][2], 0.01)
        np.testing.assert_array_equal(ret[2][3:], np.zeros(ret.shape[1]-3))

        print('done')

if __name__ == '__main__':
    unittest.main()
