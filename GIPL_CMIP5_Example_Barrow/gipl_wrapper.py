"""
gipl_wrapper.py

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


def list_so_routines(so_library):
    # This will print a list of all the routines in the Fortran shared library
    print(dir(so_library))


def run_as_fortran(so_library, cfg_file=None):
    # this assumes the internal routine is 'run_gipl'
    #
    # Usage examples:
    #      run_as_fortran(f2py_gipl)
    #      run_as_fortran(f2py_gipl, cfg_file='gipl_config_3yr.cfg')
    #      run_as_fortran(f2py_gipl, cfg_file='gipl_config.cfg')

    if not cfg_file:
        try:
            cfg_file = sys.argv[1]
            print('from python cmdlin, cfg_file is: {}'.format(cfg_file))
        except IndexError:
            cfg_file = ''
            print('no cmdline arg, cfg_file is set to <none>')
    else:
        print('cfg_file passed from Python as: {}'.format(cfg_file))

    so_library.run_gipl(cfg_file)


def run_from_python_asif_fortran():
    # Sample usage:
    #    run_from_python_asif_fortran()

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


def modify_time_e():
    # Example of using get_float_val() and set_float_val()
    # Modify the end time for this loop
    python_time_e = f2py_gipl.get_float_val('time_e')
    print('After initialization, time_e is: {}'.format(python_time_e))

    time_e_newval = 21.0
    f2py_gipl.set_float_val('time_e', time_e_newval)
    python_time_e = f2py_gipl.get_float_val('time_e')
    print('After setting time_e to {}, time_e is: {}'.format(
        time_e_newval, python_time_e))


def initialize_f2py_gipl():
    if len(sys.argv) == 1:
        # Default case is to run the short 3-year monthly run
        f2py_gipl.initialize('gipl_config_3yr.cfg')
    else:
        # Note: Fortran error just stops the code, so can't trap an Exception
        f2py_gipl.initialize(sys.argv[1])


def modify_gipl_strings():
    # Test string routines between fortran and python
    python_fconfig = f2py_gipl.get_string_val('fconfig')
    print('After setting from fortran, python_fconfig is: {}'.format(
        python_fconfig))

    new_string_val = 'gipl_config.cfg'
    f2py_gipl.set_string_val('fconfig', new_string_val)

    python_fconfig = f2py_gipl.get_string_val('fconfig')
    print('After setting fron python and getting from fortran,')
    print('  python_fconfig is: {}'.format(python_fconfig))


def get_gipl_array(array_name):
    # Not sure how to generically send info to f2py
    # without manually editing a signature file, so this stands between
    if array_name == 'zdepth':
        # zdepth is a 1-D array in depth
        n_levels = f2py_gipl.get_int_val('n_grd')
        print('n_levels of zdepth grid: {}'.format(n_levels))
        returned_array = f2py_gipl.get_array1d('zdepth', n_levels)
        #returned_array = f2py_gipl.get_array1d('zdepth')
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
        f2py_gipl.set_array1d(array_name, array_values)
    else:
        print('in set_gipl_array(), array_name not recognized: {}'.format(
            array_name))
        raise ValueError('unrecognized array_name in get_gipl_array()')


def array1d_assignment_example():
    # Show an example of using get_gipl_array() and set_gipl_array()
    depth_array = get_gipl_array('zdepth')
    print('depth_array as originally set:')
    print(depth_array)
    print('\n')


    new_depth_array = np.subtract(depth_array, 1.0)
    print('depth_array as modified in python:')
    print('new_depth_array:')
    print(new_depth_array)
    print('\n')

    set_gipl_array('zdepth', new_depth_array)

    depth_array = get_gipl_array('zdepth')
    print('depth_array retrieved from fortran after editing:')
    print(depth_array)


if __name__ == '__main__':
    # Initialize the GIPL model in the Fortran code
    initialize_f2py_gipl()

    # Get the time parameters from the Fortran code
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

    # End of __main__
