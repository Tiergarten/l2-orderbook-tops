from distutils.core import setup
from Cython.Build import cythonize
import numpy
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(ext_modules = cythonize(
           "plb.pyx"                 # our Cython source
      ), include_dirs=[numpy.get_include()])
