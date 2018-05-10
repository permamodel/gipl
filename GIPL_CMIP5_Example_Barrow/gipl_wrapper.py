"""
gipl_wrapper.py

Python 2 code to run the f2py-created gipl 'library'
"""

from __future__ import print_function

import numpy
import f2py_gipl

print(dir(f2py_gipl))

f2py_gipl.run_gipl2()


