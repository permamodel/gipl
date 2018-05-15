"""
gipl_wrapper.py

Python 2 code to run the f2py-created gipl 'library'
"""

from __future__ import print_function

#import numpy
import f2py_gipl

# This will print a list of all the routines in the Fortran shared library
#print(dir(f2py_gipl))

f2py_gipl.run_gipl2()


