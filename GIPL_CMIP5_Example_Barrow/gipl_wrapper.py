"""
gipl_wrapper.py

Python 2 code to run the f2py-created gipl 'library'
"""

from __future__ import print_function

#import numpy
import sys
import f2py_gipl


def print_usage():
    print('Usage:')
    print('  python {} <config_file>'.format(sys.argv[0]))
    print('e.g.:')
    print('  python {} gipl_config.cfg'.format(sys.argv[0]))
    print(' ')


if __name__ == '__main__':
    # This will print a list of all the routines in the Fortran shared library
    #print(dir(f2py_gipl))

    # The following just runs the single-call in the Fortran code
    #f2py_gipl.run_gipl2()

    if len(sys.argv) == 1:
        # Default case is to run the short 3-year monthly run
        f2py_gipl.initialize('gipl_config_3yr.cfg')
    else:
        # Note: Fortran error just stops the code, so can't trap an Exception
        f2py_gipl.initialize(sys.argv[1])

    # Set up parameters to run the python loop...
    #python_time_loop = 0.0
    #python_time_e = 36.0
    #python_time_step = 1.0
    #python_n_time = 12.0

    # Get the time parameters from the Fortran code
    python_time_loop = f2py_gipl.get_float_val('time_loop')
    python_time_step = f2py_gipl.get_float_val('time_step')
    python_time_e = f2py_gipl.get_float_val('time_e')
    python_n_time = f2py_gipl.get_float_val('n_time')

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

    # End of __main__
