"""
bmi_gipl.py

Python 2 code to run the f2py-created gipl 'library'

Note: all names are converted to lower case for f2py

"""

from __future__ import print_function

import sys
import numpy as np
import f2py_gipl


# Unset the default of printing numpy arrays in scientific notation
np.set_printoptions(suppress=True)


def print_usage():
    print('Usage:')
    print('  python {} <config_file>'.format(sys.argv[0]))
    print('e.g.:')
    print('  python {} gipl_config.cfg'.format(sys.argv[0]))
    print(' ')


def initialize_f2py_gipl():
    if len(sys.argv) == 1:
        # Default case is to run the short 3-year monthly run
        f2py_gipl.initialize('gipl_config_3yr.cfg')
    else:
        # Note: Fortran error just stops the code, so can't trap an Exception
        f2py_gipl.initialize(sys.argv[1])


def get_gipl_array(array_name):
    # Not sure how to generically send info to f2py
    # without manually editing a signature file, so this stands between
    if array_name == 'zdepth':
        # zdepth is a 1-D array in depth
        n_levels = f2py_gipl.get_int_val('n_grd')
        returned_array = f2py_gipl.get_float_array1d('zdepth', n_levels)
    elif array_name == 'temp':
        # temp is a 2-D array in depth
        xdim = f2py_gipl.get_int_val('n_site')
        ydim = f2py_gipl.get_int_val('n_grd')
        returned_array = f2py_gipl.get_float_array2d('temp', xdim, ydim)
    elif array_name == 'utemp_i':
        # temp is a 2-D array in depth
        xdim = f2py_gipl.get_int_val('n_time') + 2
        ydim = f2py_gipl.get_int_val('n_site')
        returned_array = f2py_gipl.get_float_array2d('utemp_i', xdim, ydim)
    elif array_name == 'snd_i':
        # temp is a 2-D array in depth
        xdim = f2py_gipl.get_int_val('n_time') + 2
        ydim = f2py_gipl.get_int_val('n_site')
        returned_array = f2py_gipl.get_float_array2d('snd_i', xdim, ydim)
    elif array_name == 'stcon_i':
        # temp is a 2-D array in depth
        xdim = f2py_gipl.get_int_val('n_time') + 2
        ydim = f2py_gipl.get_int_val('n_site')
        returned_array = f2py_gipl.get_float_array2d('stcon_i', xdim, ydim)
    else:
        print('in get_float_val(), array_name not recognized: {}'.format(
            array_name))
        raise ValueError('unrecognized array_name in get_gipl_array()')

    return returned_array


def set_gipl_array(array_name, array_values):
    # Not sure how to generically send info to f2py
    # without manually editing a signature file, so this stands between
    if array_name == 'zdepth':
        # zdepth is a 1-D array in depth
        assert array_values.ndim == 1
        n_levels = f2py_gipl.get_int_val('n_grd')
        assert array_values.size == n_levels
        f2py_gipl.set_float_array1d(array_name, array_values)
    elif array_name == 'temp':
        # temp is a 2-D array in location, value
        assert array_values.ndim == 2
        f2py_gipl.set_float_array2d(array_name, array_values)
    elif array_name == 'utemp_i':
        # utemp_i is a 2-D array in time, value
        assert array_values.ndim == 2
        f2py_gipl.set_float_array2d(array_name, array_values)
    elif array_name == 'snd_i':
        # snd_i is a 2-D array in time, value
        assert array_values.ndim == 2
        f2py_gipl.set_float_array2d(array_name, array_values)
    elif array_name == 'stcon_i':
        # stcon_i is a 2-D array in time, value
        assert array_values.ndim == 2
        f2py_gipl.set_float_array2d(array_name, array_values)
    else:
        print('in set_gipl_array(), array_name not recognized: {}'.format(
            array_name))
        raise ValueError('unrecognized array_name in set_gipl_array()')


if __name__ == '__main__':
    # Initialize the GIPL model in the Fortran code
    initialize_f2py_gipl()

    python_time_loop = f2py_gipl.get_float_val('time_loop')
    python_time_step = f2py_gipl.get_float_val('time_step')
    python_time_e = f2py_gipl.get_float_val('time_e')
    python_n_time = f2py_gipl.get_int_val('n_time')

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
