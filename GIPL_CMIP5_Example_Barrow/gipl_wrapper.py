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
