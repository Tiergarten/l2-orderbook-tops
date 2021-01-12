import numpy as np
from setuptools import setup, Extension
import Cython.Build

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(
    name='l2_orderbook_tops',
    cmdclass={'build_ext': Cython.Build.build_ext},
    package_dir={'l2_orderbook_tops': 'l2_orderbook_tops'},
    packages=['l2_orderbook_tops'],
    ext_modules=[Extension(
        'l2_orderbook_tops.extension',
        sources=['l2_orderbook_tops/plb.pyx'],
        language='c++',
        include_dirs=[np.get_include()],
    )],
    test_suite='tests',
    zip_safe=False
)
