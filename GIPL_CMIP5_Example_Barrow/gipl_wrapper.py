"""
gipl_wrapper.py

Python 2 code to run the f2py-created gipl 'library'
"""

from __future__ import print_function

#import numpy
import f2py_gipl

# This will print a list of all the routines in the Fortran shared library
#print(dir(f2py_gipl))

# The following just runs the single-call in the Fortran code
#f2py_gipl.run_gipl2()

#f2py_gipl.initialize('gipl_config_3yr.cfg')
f2py_gipl.initialize('gipl_config.cfg')

# Doesn't work...
#print('f2py_gipl.time_loop: {}'.format(f2py_gipl.time_loop))

python_time_loop = 0.0
python_time_e = 36.0
python_time_step = 1.0
python_n_time = 12.0
while python_time_loop < python_time_e:
    print('in python, time_loop: {}'.format(python_time_loop))

    f2py_gipl.update_model()
    f2py_gipl.update_model_until(
        python_time_loop + (python_n_time - 3) * python_time_step)
    f2py_gipl.update_model()
    f2py_gipl.update_model()
    f2py_gipl.write_output()
    f2py_gipl.update_model()
    f2py_gipl.write_output()

    python_time_loop += python_n_time

f2py_gipl.finalize()
