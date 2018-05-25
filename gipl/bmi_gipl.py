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
    add BMI grid functions

    change Fortran code to use a single array of input values,
        e.g. don't overwrite with interpolated values if a value has already
            been specified, and  use setattr/getattr to pass arrays
        and move snd, stcon, etc arrays back to their original modules

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


class BmiGiplMethod(object):
    """ Implement a BMI interface to Fortran-90 based GIPL model via f2py """

    def __init__(self):
        self._model = f2py_gipl

        # For now, all variables of interest in Python will be defined
        #   in the gipl_bmi module.
        self._fortran_module_ref = self._model.gipl_bmi

        self._grids = {}
        self.ngrids = 0

        self.default_config_filename = '../examples/gipl_config_3yr.cfg'

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
            'model__timestep':
                'time_step',
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
            'model_first__timestep':
                'time_s',
            'model_last__timestep':
                'time_e',
        }

        # Each variable name should have an associated unit
        self._var_units_map = {
            'atmosphere_bottom_air__temperature':    'deg_c',
            'surface__snow_depth':                   'm',
            'surface__snow_thermal_conductivity':    'W m^-1 K^-1',
            'soil__temperature':                     'deg_c',
            'freeze_up__time__monthly':              'years',
            'freeze_up__temperature_monthly':        'deg C',
            'snow_level__monthly':                   'm',
            'freeze_up__time__annual':               'years',
            'freeze_up__temperature_annual':         'deg C',
            'snow_level__annual':                    'm',
            'freezing_front__depth':                 'm',
            'freeze_up__time_current':               'years',
            'freeze_up__time_total':                 'years',
            'model__timestep':                       'months',
            'model_current__timestep':               '1',
            'model_timesteps_per_year':              '1',
            'model_num_levels__depth':               '1',
            'model_num_levels__depth_selected':      '1',
            'model_sites__number':                   '1',
            'model_start__time':                     '1',
            'model_end__time':                       '1',
            'model_first__timestep':                 '1',
            'model_last__timestep':                  '1',
        }

        # Each variable is associated with a grid
        self._var_grid_map = {
            'atmosphere_bottom_air__temperature':    'grid_float_everyts',
            'surface__snow_depth':                   'grid_float_everyts',
            'surface__snow_thermal_conductivity':    'grid_float_everyts',

            'soil__temperature':                     'grid_float_site_z',

            'freeze_up__time__monthly':              'grid_float_month_site',
            'freeze_up__temperature_monthly':        'grid_float_month_site',
            'snow_level__monthly':                   'grid_float_month_site',

            'freeze_up__time__annual':               'grid_float_site',
            'freeze_up__temperature_annual':         'grid_float_site',
            'snow_level__annual':                    'grid_float_site',

            'freezing_front__depth':                 'grid_float_site',
            'freeze_up__time_current':               'grid_float_site',
            'freeze_up__time_total':                 'grid_float_site',

            'model__timestep':                       'point_float',
            'model_current__timestep':               'point_float',
            'model_timesteps_per_year':              'point_int',
            'model_num_levels__depth':               'point_int',
            'model_num_levels__depth_selected':      'point_int',

            'model_sites__number':                   'point_int',
            'model_start__time':                     'point_float',
            'model_end__time':                       'point_float',
            'model_first__timestep':                 'point_float',
            'model_last__timestep':                  'point_float',
        }

        self._grid_numbers = {
            'point_int':              0,
            'point_float':            1,
            'grid_float_site':        2,
            'grid_float_site_z':      3,
            'grid_float_everyts':     4,
            'grid_float_month_site':  5,
        }

        self._grid_types = {
            0:              'point',
            1:              'point',
            2:              'uniform_rectilinear',
            3:              'rectilinear',
            4:              'uniform_rectilinear',
            5:              'uniform_rectilinear',
        }


    def initialize(self, cfg_filename=None):
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
        # Currently, need to call write_output() as part of update
        # so that output values are identical
        self._model.write_output()


    def update_until(self, target_time):
        self._model.update_model_until(target_time)


    def finalize(self):
        self._model.finalize()


    def get_start_time(self):
        return 0.0


    def get_end_time(self):
        return self.get_value('model_last__timestep')


    def get_time_step(self):
        return self.get_value('model__timestep')


    def get_current_time(self):
        return self.get_value('model_current__timestep')


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


    def set_value_at_indices(self, var_name, indices, new_var_values):
        self.get_value_ref(var_name).flat[indices] = new_var_values


    def get_var_type(self, var_name):
        return str(self.get_value_ref(var_name).dtype)


    def get_var_nbytes(self, var_name):
        return np.asarray(self.get_value_ref(var_name)).nbytes


    def get_component_name(self):
        return self._name


    def get_var_itemsize(self, var_name):
        return np.asarray(self.get_value_ref(var_name)).flatten()[0].nbytes


    def get_var_grid(self, var_name):
        grid_name = self._var_grid_map[var_name]
        return self._grid_numbers[grid_name]


    def get_grid_type(self, grid_id):
        return self._grid_types[grid_id]


    def get_grid_shape(self, grid_id):
        """ find a variable with this grid id, and return its shape """
        for var in self._var_grid_map.keys():
            if self._grid_numbers[self._var_grid_map[var]] == grid_id:
                return self.get_value_ref(var).shape


    def get_grid_rank(self, grid_id):
        """ find a variable with this grid id, and return its shape """
        for var in self._var_grid_map.keys():
            if self._grid_numbers[self._var_grid_map[var]] == grid_id:
                return self.get_value_ref(var).ndim


    def get_grid_size(self, grid_id):
        grid_size = self.get_grid_shape(grid_id)
        if grid_size == ():
            return 1
        else:
            return int(np.prod(grid_size))


if __name__ == '__main__':

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
        #bmigipl._model.write_output()
        bmigipl.update()
        #bmigipl._model.write_output()

        python_time_loop += python_n_time

    bmigipl.finalize()
