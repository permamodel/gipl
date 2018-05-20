# -*- coding: utf-8 -*-
"""
bmi_gipl.py

Python 2 code providing the BMI interface to GIPL

See also example usage code in bmi_gipl_examples.py

TODO:
    write get_gipl_val() and set_gipl_val() which wrap get_float_val() etc
    Write BmiVariable and BmiGrid classes to better organize variable and
      grid information
    Generate code below to run entirely using BMI function calls
    Probably put new variables in Fortran code to properly store outputs
      to arrays, rather than to temporary arrays and files
    First pass: use n_time loop and write_output() to get exact output match
    Second pass: Use mod(timestep, n_time) to bmi_output from outputvar arrays
    Try to structure files as python package
    Move docs, examples, around.  Generate license file

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




class BmiGiplMethod(object):
    """ Implement a BMI interface to Fortran-90 based GIPL model via f2py """

    def __init__(self):
        self._model = None
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
        # NOTE: Some of these don't yet exist in the Fortran code, except
        #       as temporary entries in "save" arrays
        self._var_name_map = {
            'atmosphere_bottom_air__temperature':    'utemp_i',
            'surface__snow_depth':                   'snd_i',
            'surface__snow_thermal_conductivity':    'stcon_i',
            'soil__temperature':                     'temp',
            'freeze_up__temperature':                'fu_temp',
            'snow_level':                            'snow_level',
            'freezing_front__depth':                 'cfrz_frn',
            'freeze_up__time_current':               'frz_up_time_cur',
            'freeze_up__time_total':                 'frz_up_time_tot',
            'model_current__timestep':               'time_loop',
            'model_timesteps_per_year':              'n_time',
            'model_num_levels__depth':               'n_grd',
            'model_num_levels__depth_selected':      'm_grd',
            'model_sites__number':                   'n_site',
            'model_start__time':                     'time_beg',
            'model_end__time':                       'time_end',
            'model_start__timestep':                 'time_s',
            'model_end__timestep':                   'time_e',
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
        self._model = f2py_gipl
        if cfg_filename:
            self._model.initialize(cfg_filename)
        else:
            self._model.initialize(self.default_config_filename)


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
        # Close any input files
        self._model.finalize()


    def get_start_time(self):
        return 0.0


    def get_end_time(self):
        return self._model.get_float_val('time_e')


    def get_time_step(self):
        return self._model.get_float_val('time_step')


    def get_current_time(self):
        return self._model.get_float_val('time_loop')


    def get_value(self, var_name):
        return get_gipl_var(self, self._var_name_map[var_name])


''' BMI functions to implement: (copied from bmi_frost_number_Geo.py

    def get_grid_type(self, grid_number):
        return self._grid_type[grid_number]

    def get_value_ref(self, var_name):
        return self._values[var_name]

    def set_value(self, var_name, new_var_values):
        val = self.get_value_ref(var_name)
        val.flat = new_var_values

    def set_value_at_indices(self, var_name, indices, new_var_values):
        self.get_value_ref(var_name).flat[indices] = new_var_values

    def get_var_itemsize(self, var_name):
        return np.asarray(self.get_value_ref(var_name)).flatten()[0].nbytes

    def get_value_at_indices(self, var_name, indices):
        return self.get_value_ref(var_name).take(indices)

    def get_var_nbytes(self, var_name):
        return np.asarray(self.get_value_ref(var_name)).nbytes

    def get_var_type(self, var_name):
        return str(self.get_value_ref(var_name).dtype)

    def get_component_name(self):
        return self._name

    def get_var_grid(self, var_name):
        for grid_id, var_name_list in self._grids.items():
            if var_name in var_name_list:
                return grid_id

    def get_grid_shape(self, grid_id):
        var_name = self._grids[grid_id]
        value = np.array(self.get_value_ref(var_name)).shape
        return value

    def get_grid_size(self, grid_id):
        grid_size = self.get_grid_shape(grid_id)
        if grid_size == ():
            return 1
        else:
            return int(np.prod(grid_size))

    def get_grid_spacing(self, grid_id):
        assert_true(grid_id < self.ngrids)
        return np.array([1, 1], dtype='float32')

    def get_grid_origin(self, grid_id):
        return np.array([0.0, 0.0], dtype='float32')

    def get_grid_rank(self, var_id):
        return len(self.get_grid_shape(var_id))
'''


if __name__ == '__main__':
    # Note: this currently just runs the code, rather than running via BMI

    # Initialize the GIPL model in the Fortran code
    #initialize_f2py_gipl()

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
        bmigipl.update()
        bmigipl.update()
        bmigipl._model.write_output()
        bmigipl.update()
        bmigipl._model.write_output()

        python_time_loop += python_n_time

    bmigipl.finalize()
