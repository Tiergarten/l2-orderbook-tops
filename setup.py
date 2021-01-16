import numpy as np
from setuptools import setup, Extension, find_packages
import Cython.Build

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(
    name='l2_orderbook_tops',
    version='0.0.1',
    cmdclass={'build_ext': Cython.Build.build_ext},
    package_dir={'l2_orderbook_tops': 'l2_orderbook_tops'},
    packages = find_packages(),
    ext_modules=[Extension(
        'l2_orderbook_tops.py_price_level_book',
        sources=['l2_orderbook_tops/py_price_level_book.pyx'],
        language='c++',
        include_dirs=[np.get_include()],
    )],
    zip_safe=False
)
