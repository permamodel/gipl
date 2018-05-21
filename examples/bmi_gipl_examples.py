"""
bmi_gipl_examples.py

These are sample codes for running routines in bmi_gipl.py
"""

from __future__ import print_function

import sys
import numpy as np
import f2py_gipl
import bmi_gipl


# Unset the default of printing numpy arrays in scientific notation
np.set_printoptions(suppress=True)


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


def example_get_set_float_array1d():
    # Show an example of using get_gipl_array() and set_gipl_array()
    # with 1D arrays
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


def example_get_set_float_array2d():
    # Show an example of using get_gipl_array() and set_gipl_array()
    # with 2D arrays
    temp_array = get_gipl_array('temp')
    print('temp_array as originally set:')
    print(temp_array)
    print('\n')

    new_temp_array = np.subtract(temp_array, 1.0)
    print('temp_array as modified in python:')
    print('new_temp_array:')
    print(new_temp_array)
    print('\n')

    set_gipl_array('temp', new_temp_array)

    temp_array = get_gipl_array('temp')
    print('temp_array retrieved from fortran after editing:')
    print(temp_array)


def example2_get_set_float_array2d():
    # Example of setting surface temperature
    # which should be done just before an update_model() call
    surf_temp_thisyear = get_gipl_array('utemp_i')
    print('surf_temp_thisyear as originally set:')
    print(surf_temp_thisyear)
    print('\n')

    new_surf_temp_thisyear = np.subtract(surf_temp_thisyear, 1.0)
    print('new_surf_temp_thisyear as modified in python:')
    print('new_surf_temp_thisyear:')
    print(new_surf_temp_thisyear)
    print('\n')

    set_gipl_array('utemp_i', new_surf_temp_thisyear)

    surf_temp_thisyear = get_gipl_array('utemp_i')
    print('surf_temp_thisyear retrieved from fortran after editing:')
    print(surf_temp_thisyear)

    #print('Stopping utemp_i example')
    #exit(0)


def example_get_set_int_array1d_value():
    # Example of accessing single element of a 1D array
    sample_level = 5
    depth_index = f2py_gipl.get_int_array1d_element('zdepth_id', sample_level)
    print('depth id of sample level {} is: {}'.format(sample_level,
                                                      depth_index))

    new_depth_index = depth_index + 1
    print('Will set depth index to {}'.format(new_depth_index))
    f2py_gipl.set_int_array1d_element(
        'zdepth_id', sample_level, new_depth_index)

    depth_index = f2py_gipl.get_int_array1d_element('zdepth_id', sample_level)
    print('after resetting, current depth id of sample level {} is: {}'.format(
        sample_level, depth_index))


def example_get_set_float_array1d_value():
    # Example of accessing single element of a 1D array
    sample_level = 5
    depth_index = f2py_gipl.get_float_array1d_element('zdepth', sample_level)
    print('depth id of sample level {} is: {}'.format(sample_level,
                                                      depth_index))

    new_depth_index = depth_index + 1
    print('Will set depth index to {}'.format(new_depth_index))
    f2py_gipl.set_float_array1d_element(
        'zdepth', sample_level, new_depth_index)

    depth_index = f2py_gipl.get_float_array1d_element('zdepth', sample_level)
    print('after resetting, current depth id of sample level {} is: {}'.format(
        sample_level, depth_index))


def example_get_set_float_array2d_value():
    # Example of accessing single element of a 2D array

    # The following example works when placed just before the time_loop
    # increment in the main python_time_loop
    #   example_get_set_float_array2d_value()

    sample_i = 1
    sample_j = 3
    depth_index = f2py_gipl.get_float_array2d_element(
        'res', sample_i, sample_j)
    print('snow level in res of sample level ({}, {}) is: {}'.format(
        sample_i, sample_j, depth_index))

    new_depth_index = depth_index + 1
    print('Will set snow level to {}'.format(new_depth_index))
    f2py_gipl.set_float_array2d_element(
        'res', sample_i, sample_j, new_depth_index)

    depth_index = f2py_gipl.get_float_array2d_element(
        'res', sample_i, sample_j)
    print('after resetting,')
    print('  current snow level of res at sample level ({}, {}) is: {}'
          .format(sample_i, sample_j, depth_index))
