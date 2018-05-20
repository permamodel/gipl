# -*- coding: utf-8 -*-
"""
bmi_gipl.py

Python 2 code providing the BMI interface to GIPL

See also example usage code in bmi_gipl_examples.py

NOTES:
    Regarding namespace independence:
        Tested instantiating two different BmiGiplMethods at once.
            If they use the same shared object library via 'import',
            for instance both use f2py_gipl, then the namespaces of
            the two Methods collide.
        If two different shared object libraries are used, e.g. by
            compiling the same code to f2py_gipl2.so, then the namespaces
            are independent.
        If two different python calls are made to the same shared object
            library, then the two namespaces are independent: e.g. by
            running make and creating a different .so file.

    Regarding direct access to Fortran variables from Python:
        Variables in Fortran modeles are accessible from Python
        However, if the variables are allocatable, they do *not* show
            up in the vars() or dir() lists.  (The are still accessible.)
        A three dimension array allocated in Fortran as:
                array3d(xdim, ydim, zdim)
            is referenced in Python as:
                array3d[0:xdim-1, 0:ydim-1, 0:zdim-1]

CONVENTIONS:
    When referencing arrays in Python, it will be assumed tha 0-based indexing
        will be used in the Python code.  Therefore:
                array(1)    (in Fortran)
            is the same as
                array[0]    (in Python)


TODO:
    change Fortran code to use a single array of input values,
        e.g. don't overwrite with interpolated values if a value has already
            been specified, and  use setattr/getattr to pass arrays
        and move snd, stcon, etc arrays back to their original modules

    rewrite access routines to use getattr() and setattr()

    Use mod(timestep, n_time) to bmi_output from outputvar arrays

    Try to structure files as python package
        e.g.: Move docs, examples, around.  Generate license file
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


def get_gipl_var(bmimethod, var_name):
    """ return the value of this gipl_variable """
    if var_name in ('time_loop', 'time_step', 'time_b', 'time_e'):
        result = bmimethod._model.get_float_val(var_name)
    elif var_name in ('n_time', 'n_grd', 'm_grd', 'n_site'):
        result = bmimethod._model.get_int_val(var_name)
    else:
        raise ValueError('gipl variable not recognized: {}'.format(var_name))

    return result


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




class BmiFortranVariable(object):
    """ Class to describe variables in the Fortran code accessible via BMI """
    def __init__(self, fortran_name, fortran_module,
                 dtype=float, rank=0, isInput=False, isOutput=False,
                 dim1_var_name=None, dim2_var_name=None, dim3_var_name=None):
        """ Set the attributes at initialization """
        self.fortran_name = fortran_name
        self.fortran_module = fortran_module
        self.dtype = dtype
        self.rank = rank
        self.isInput = isInput
        self.isOutput = isOutput
        self.dim1_var_name = dim1_var_name
        self.dim2_var_name = dim2_var_name
        self.dim3_var_name = dim3_var_name


    def get_val(self):
        return getattr(self.fortran_module, self.fortran_name)


    def set_val(self, var_value):
        setattr(self.fortran_module, self.fortran_name, var_value)



class BmiGiplMethod(object):
    """ Implement a BMI interface to Fortran-90 based GIPL model via f2py """

    def __init__(self):
        self._model = f2py_gipl

        # For now, all variables of interest in Python will be defined
        #   in the gipl_bmi module.
        self._fortran_module_ref = self._model.gipl_bmi

        self._grids = {}
        self.ngrids = 0
        self.default_config_filename = './gipl_config_3yr.cfg'

        self._name = 'GIPL model, f2py version'
        self._attributes = {
            'model_name':      'GIPL BMI via f2py method',
            'version':         '0.1',
            'author_name':     'J. Scott Stewart',
            'grid_type':       'rectilinear',
            'time_step_type':  'fixed',
            'step_method':     'explicit',
            'component_name':  'gipl',
            'model_family':    'PermaModel',
            'time_units':      'years'
        }

        self.variables = ()

        # Input and output names should be CSDMS standard names
        self._input_var_names = (
            'atmosphere_bottom_air__temperature',
            'surface__snow_depth',
            'surface__snow_thermal_conductivity',
        )

        self._output_var_names = (
            'soil__temperature',
            'freeze_up__temperature',
            'snow_level',
            'freeze_up__depth',
            'freeze_up__time_current',
            'freeze_up__time_total',
        )

        # Standard names should correspond to variables in the model code
        # Note: Currently, all variables here are assumed to be defined
        #       in the module 'gipl_bmi' in the fortran code.
        self._var_name_map = {
            'atmosphere_bottom_air__temperature':
                'surface_temp',
            'surface__snow_depth':
                'snow_depth',
            'surface__snow_thermal_conductivity':
                'snow_thermal_conductivity',
            'soil__temperature':
                'temp',
            'freeze_up__time__monthly':
                'monthly_time',
            'freeze_up__temperature__monthly':
                'monthly_freeze_up_temp',
            'snow_level__monthly':
                'monthly_snow_level',
            'freeze_up__time__annual':
                'annual_average_time',
            'freeze_up__temperature__annual':
                'annual_freeze_up_temp',
            'snow_level__annual':
                'annual_snow_level',
            'freezing_front__depth':
                'freeze_up_depth',
            'freeze_up__time_current':
                'freeze_up_time_current',
            'freeze_up__time_total':
                'freeze_up_time_total',
            'model_current__timestep':
                'time_loop',
            'model_timesteps_per_year':
                'n_time',
            'model_num_levels__depth':
                'n_grd',
            'model_num_levels__depth_selected':
                'm_grd',
            'model_sites__number':
                'n_site',
            'model_start__time':
                'time_beg',
            'model_end__time':
                'time_end',
            'model_start__timestep':
                'time_s',
            'model_end__timestep':
                'time_e',
        }

        # Each variable name should have an associated unit
        self._var_units_map = {
            'atmosphere_bottom_air__temperature':    'deg_c',
            'surface__snow_depth':                   'meters',
            'surface__snow_thermal_conductivity':    '1',
            'soil__temperature':                     'deg_c',
            'freeze_up__temperature':                'deg_c',
            'snow_level':                            'meters',
            'freezing_front__depth':                 'meters',
            'freeze_up__time_current':               'years',
            'freeze_up__time_total':                 'years',
            'model_current__timestep':               '1',
            'model_timesteps_per_year':              '1',
            'model_num_levels__depth':               '1',
            'model_num_levels__depth_selected':      '1',
            'model_sites__number':                   '1',
            'model_start__time':                     '1',
            'model_end__time':                       '1',
            'model_start__timestep':                 '1',
            'model_end__timestep':                   '1',
        }

        # Each variable is associated with a grid
        self._var_grid_map = {
            'atmosphere_bottom_air__temperature':    'grid_everyts_float',
            'surface__snow_depth':                   'grid_everyts_float',
            'surface__snow_thermal_conductivity':    'grid_everyts_float',
            'soil__temperature':                     'grid_z_float',
            'freeze_up__temperature':                'grid_everyts_float',
            'snow_level':                            'grid_everyts_float',
            'freezing_front__depth':                 'grid_annualts_float',
            'freeze_up__time_current':               'grid_annualts_float',
            'freeze_up__time_total':                 'grid_annualts_float',
        }

        self._grid_numbers = {
            'grid_everyts_float':  0,
            'grid_annualts_float': 1,
            'grid_z_float':        2,
        }

        self._grid_types = {
            'grid_everyts_float':  'uniform_rectilinear',
            'grid_annualts_float': 'uniform_rectilinear',
            'grid_z_float':        'rectilinear',
        }


    def initialize(self, cfg_filename=None):
        if cfg_filename:
            self._model.initialize(cfg_filename)
        else:
            self._model.initialize(self.default_config_filename)

        model_current__timestep = BmiFortranVariable(
            'time_loop', self._model)
        model_timesteps_per_year = BmiFortranVariable(
            'n_time', self._model, dtype=np.int32)
        self.variables = (
            model_current__timestep,
            model_timesteps_per_year,
        )


    def get_attribute(self, attribute_name):
        try:
            return self._attributes[attribute_name.lower()]
        except KeyError:
            raise ValueError('Not attribute named: {}'.format(attribute_name))


    def get_input_var_names(self):
        return self._input_var_names


    def get_output_var_names(self):
        return self._output_var_names


    def get_var_name(self, long_var_name):
        return self._var_name_map[long_var_name]


    def get_var_units(self, long_var_name):
        return self._var_units_map[long_var_name]


    def update(self):
        self._model.update_model()


    def update_until(self, target_time):
        self._model.update_model_until(target_time)


    def finalize(self):
        self._model.finalize()


    def get_start_time(self):
        return 0.0


    def get_end_time(self):
        return self._model.get_float_val('time_e')


    def get_time_step(self):
        return self._model.get_float_val('time_step')


    def get_current_time(self):
        return self._model.get_float_val('time_loop')


    def get_value_ref(self, var_name):
        return getattr(self._fortran_module_ref,
                       self._var_name_map[var_name])


    def get_value(self, var_name):
        return self.get_value_ref(var_name).copy()


    def set_value(self, var_name, src):
        setattr(self._fortran_module_ref,
                self._var_name_map[var_name],
                src)


    def get_value_at_indices(self, var_name, indices):
        return self.get_value_ref(var_name).take(indices)
        #self.get_value_ref(var_name).flat[indices] = new_var_values
        #return self.get_value_ref(var_name).copy()[indices]

    def set_value_at_indices(self, var_name, indices, new_var_values):
        self.get_value_ref(var_name).flat[indices] = new_var_values


if __name__ == '__main__':
    # Note: this currently just runs the code, rather than running via BMI

    bmigipl = BmiGiplMethod()

    if len(sys.argv) == 1:
        bmigipl.initialize()
    else:
        bmigipl.initialize(sys.argv[1])

    python_time_loop = bmigipl.get_value('model_current__timestep')
    python_time_step = bmigipl.get_time_step()
    python_time_e = bmigipl.get_end_time()
    python_n_time = bmigipl.get_value('model_timesteps_per_year')

    while python_time_loop < python_time_e:
        print('in python, time_loop: {}'.format(python_time_loop))

        bmigipl.update()
        bmigipl.update_until(
            python_time_loop + (python_n_time - 3) * python_time_step)
        time_loop_in_loop = bmigipl.get_value('model_current__timestep')
        bmigipl.update()
        bmigipl.update()
        bmigipl._model.write_output()
        bmigipl.update()
        bmigipl._model.write_output()

        python_time_loop += python_n_time

    bmigipl.finalize()
