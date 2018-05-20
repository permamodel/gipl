!
! gipl_bmi.f90
!
! Routines permitting access to gipl variables from python
!
! Note: All names are converted to lower case for f2py

!subroutine get_time_vars(new_time_loop)
!  use gipl_bmi
!
!  real*8 :: new_time_loop
!
!!f2py intent(out) :: new_time_loop
!
!  new_time_loop = time_loop
!
!end subroutine get_time_vars

subroutine get_time_vars(in_time_loop)
  use gipl_bmi

  implicit none

  real*8 :: in_time_loop

!f2py intent(out) :: in_time_loop

  in_time_loop = time_loop

  print*, 'in get_time_vars(), in_time_loop = ', in_time_loop

end subroutine get_time_vars


subroutine get_float_val(var_name, var_val)
  use gipl_bmi

  implicit none

  character(64) :: var_name
  real*8 :: var_val

!f2py intent(in) :: var_name
!f2py intent(out) :: var_val

  if (var_name .eq. 'time_loop') then
    var_val = time_loop
  elseif (var_name .eq. 'time_step') then
    var_val = time_step
  elseif (var_name .eq. 'time_e') then
    var_val = time_e
  else
    print*,'Fortran BMI error: get_float_var not recognized: ', var_name
    stop
  endif

end subroutine get_float_val


subroutine set_float_val(var_name, var_val)
  use gipl_bmi

  implicit none

  character(64) :: var_name
  real*8 :: var_val

!f2py intent(in) :: var_name
!f2py intent(in) :: var_val

  if (var_name .eq. 'time_loop') then
    time_loop = var_val
  elseif (var_name .eq. 'time_step') then
    time_step = var_val
  elseif (var_name .eq. 'time_e') then
    time_e = var_val
  else
    print*,'Fortran BMI error: set_float_var not recognized: ', var_name
    stop
  endif

end subroutine set_float_val


subroutine get_int_val(var_name, var_val)
  use gipl_bmi
  use grd

  implicit none

  character(64) :: var_name
  integer :: var_val

!f2py intent(in) :: var_name
!f2py intent(out) :: var_val

  if (var_name .eq. 'n_time') then
    var_val = n_time
  elseif (var_name .eq. 'n_grd') then
    var_val = n_grd
  elseif (var_name .eq. 'm_grd') then
    var_val = m_grd
  elseif (var_name .eq. 'n_site') then
    var_val = n_site
  else
    print*,'Fortran BMI error: get_int_var not recognized: ', var_name
    stop
  endif

end subroutine get_int_val


subroutine set_int_val(var_name, var_val)
  use gipl_bmi

  implicit none

  character(64) :: var_name
  integer :: var_val

!f2py intent(in) :: var_name
!f2py intent(in) :: var_val

  if (var_name .eq. 'n_time') then
    n_time = var_val
  else
    print*,'Fortran BMI error: set_int_var not recognized: ', var_name
    stop
  endif

end subroutine set_int_val


subroutine get_string_val(var_name, var_val)
  use gipl_bmi

  implicit none

  character(64) :: var_name
  character(64) :: var_val

!f2py intent(in) :: var_name
!f2py intent(out) :: var_val

  if (var_name .eq. 'fconfig') then
    var_val = fconfig
  else
    print*,'Fortran BMI error: get_string_var not recognized: ', var_name
    stop
  endif

end subroutine get_string_val


subroutine set_string_val(var_name, var_val)
  use gipl_bmi

  implicit none

  character(64) :: var_name
  character(64) :: var_val

!f2py intent(in) :: var_name
!f2py intent(in) :: var_val

  if (var_name .eq. 'fconfig') then
    fconfig = var_val
  else
    print*,'Fortran BMI error: set_string_var not recognized: ', var_name
    stop
  endif

end subroutine set_string_val


subroutine get_float_array1d(array_name, array_dim, return_array)
  use gipl_bmi
  use grd

  implicit none

  character(64) :: array_name
  integer :: array_dim
  real*8, dimension(array_dim) :: return_array

!f2py intent(in) :: array_name
!f2py intent(in) :: array_dim
!f2py intent(out) :: return_array

  if (array_name .eq. 'zdepth') then
    return_array = zdepth
  else
    print*,'Fortran BMI error: get_float_array1d name not recognized: ', array_name
    stop
  endif

end subroutine get_float_array1d


subroutine set_float_array1d(array_name, array_values, array_dim)
  use gipl_bmi
  use grd

  implicit none

  real*8, dimension(array_dim) :: array_values
  integer :: array_dim
  character(64) :: array_name

!f2py intent(in) :: array_values
!f2py intent(in, hide) :: array_dim
!f2py intent(in) :: array_name

  if (array_name .eq. 'zdepth') then
    print*, 'Assigning zdepth...'
    zdepth = array_values
  else
    print*,'Fortran BMI error: set_float_array1d array_name not recognized: ',&
      array_name
    stop
  endif

end subroutine set_float_array1d


subroutine get_float_array2d(array_name, xdim, ydim, return_array)
  use gipl_bmi
  use grd
  use thermo  ! provides temp
  use bnd     ! provides utemp_i, snd_i, stcon_i

  implicit none

  character(64) :: array_name
  integer :: xdim, ydim
  real*8, dimension(xdim, ydim) :: return_array

!f2py intent(in) :: array_name
!f2py intent(in) :: xdim, ydim
!f2py intent(out) :: return_array

  if (array_name .eq. 'temp') then
    return_array = temp
  elseif (array_name .eq. 'utemp_i') then
    return_array = utemp_i
  elseif (array_name .eq. 'snd_i') then
    return_array = snd_i
  elseif (array_name .eq. 'stcon_i') then
    return_array = stcon_i
  else
    print*,'Fortran BMI error: get_float_array2d name not recognized: ', array_name
    stop
  endif

end subroutine get_float_array2d


subroutine set_float_array2d(array_name, array_values, xdim, ydim)
  use gipl_bmi
  use grd
  use thermo  ! provides temp
  use bnd     ! provides utemp_i, snd_i, stcon_i

  implicit none

  character(64) :: array_name
  real*8, dimension(xdim, ydim) :: array_values
  integer :: xdim, ydim

!f2py intent(in) :: array_name
!f2py intent(in) :: array_values
!f2py intent(in, hide) :: xdim, ydim

  if (array_name .eq. 'temp') then
    temp = array_values
  elseif (array_name .eq. 'utemp_i') then
    utemp_i = array_values
  elseif (array_name .eq. 'snd_i') then
    snd_i = array_values
  elseif (array_name .eq. 'stcon_i') then
    stcon_i = array_values
  else
    print*,'Fortran BMI error: set_float_array1d array_name not recognized: ',&
      array_name
    stop
  endif

end subroutine set_float_array2d


subroutine get_int_array1d_element(array_name, array_index, array_val)
  use gipl_bmi
  use grd

  implicit none

  character(64) :: array_name
  integer :: array_index
  integer :: array_val

!f2py intent(in) :: array_name
!f2py intent(in) :: array_index
!f2py intent(out) :: array_val

  if (array_name .eq. 'zdepth_id') then
    array_val = zdepth_id(array_index)
  else
    print*,'Fortran BMI error: get_int_array1d_element name not recognized: ', array_name
    stop
  endif

end subroutine get_int_array1d_element


subroutine set_int_array1d_element(array_name, array_index, array_val)
  use gipl_bmi
  use grd

  implicit none

  character(64) :: array_name
  integer :: array_index
  integer :: array_val

!f2py intent(in) :: array_name
!f2py intent(in) :: array_index
!f2py intent(in) :: array_val

  if (array_name .eq. 'zdepth_id') then
    zdepth_id(array_index) = array_val
  else
    print*,'Fortran BMI error: set_int_array1d_element array_name not recognized: ',&
      array_name
    stop
  endif

end subroutine set_int_array1d_element

subroutine get_float_array1d_element(array_name, array_index, array_val)
  use gipl_bmi
  use grd

  implicit none

  character(64) :: array_name
  integer :: array_index
  real*8 :: array_val

!f2py intent(in) :: array_name
!f2py intent(in) :: array_index
!f2py intent(out) :: array_val

  if (array_name .eq. 'zdepth') then
    array_val = zdepth(array_index)
  else
    print*,'Fortran BMI error: get_float_array1d_element name not recognized: ', array_name
    stop
  endif

end subroutine get_float_array1d_element


subroutine set_float_array1d_element(array_name, array_index, array_val)
  use gipl_bmi
  use grd

  implicit none

  character(64) :: array_name
  integer :: array_index
  real*8 :: array_val

!f2py intent(in) :: array_name
!f2py intent(in) :: array_index
!f2py intent(in) :: array_val

  if (array_name .eq. 'zdepth') then
    zdepth(array_index) = array_val
  else
    print*,'Fortran BMI error: set_float_array1d_element array_name not recognized: ',&
      array_name
    stop
  endif

end subroutine set_float_array1d_element

subroutine get_int_array2d_element(array_name, x_index, y_index, array_val)
  use gipl_bmi
  use grd
  use alt  ! provides n_frz_frn

  implicit none

  character(64) :: array_name
  integer :: x_index, y_index
  integer :: array_val

!f2py intent(in) :: array_name
!f2py intent(in) :: x_index, y_index
!f2py intent(out) :: array_val

  if (array_name .eq. 'n_frz_frn') then
    array_val = n_frz_frn(x_index, y_index)
  else
    print*,'Fortran BMI error: get_int_array2d_element name not recognized: ', array_name
    stop
  endif

end subroutine get_int_array2d_element


subroutine set_int_array2d_element(array_name, x_index, y_index, array_val)
  use gipl_bmi
  use grd
  use alt  ! provides n_frz_frn

  implicit none

  character(64) :: array_name
  integer :: x_index, y_index
  integer :: array_val

!f2py intent(in) :: array_name
!f2py intent(in) :: x_index, y_index
!f2py intent(in) :: array_val

  if (array_name .eq. 'n_frz_frn') then
    n_frz_frn(x_index, y_index) = array_val
  else
    print*,'Fortran BMI error: set_int_array2d_element array_name not recognized: ',&
      array_name
    stop
  endif

end subroutine set_int_array2d_element

subroutine get_float_array2d_element(array_name, x_index, y_index, array_val)
  use gipl_bmi
  use grd
  use thermo  ! provides temp
  use bnd     ! provides utemp_i, snd_i, stcon_i

  implicit none

  character(64) :: array_name
  integer :: x_index, y_index
  real*8 :: array_val

!f2py intent(in) :: array_name
!f2py intent(in) :: x_index, y_index
!f2py intent(out) :: array_val

  if (array_name .eq. 'temp') then
    array_val = temp(x_index, y_index)
  elseif (array_name .eq. 'utemp_i') then
    array_val = utemp_i(x_index, y_index)
  elseif (array_name .eq. 'snd_i') then
    array_val = snd_i(x_index, y_index)
  elseif (array_name .eq. 'stcon_i') then
    array_val = stcon_i(x_index, y_index)
  elseif (array_name .eq. 'monthly_time') then
    array_val = monthly_time(x_index, y_index)
  elseif (array_name .eq. 'monthly_freeze_up_temp') then
    array_val = monthly_freeze_up_temp(x_index, y_index)
  elseif (array_name .eq. 'monthly_snow_level') then
    array_val = monthly_snow_level(x_index, y_index)
  !elseif (array_name .eq. 'monthly_temperature') then
  !  array_val = monthly_temperature(x_index, y_index)
  else
    print*,'Fortran BMI error: get_float_array2d_element name not recognized: ', array_name
    stop
  endif

end subroutine get_float_array2d_element


subroutine set_float_array2d_element(array_name, x_index, y_index, array_val)
  use gipl_bmi
  use grd
  use thermo  ! provides temp
  use bnd     ! provides utemp_i, snd_i, stcon_i

  implicit none

  character(64) :: array_name
  integer :: x_index, y_index
  real*8 :: array_val

!f2py intent(in) :: array_name
!f2py intent(in) :: x_index, y_index
!f2py intent(in) :: array_val

  if (array_name .eq. 'temp') then
    temp(x_index, y_index) = array_val
  elseif (array_name .eq. 'utemp_i') then
    utemp_i(x_index, y_index) = array_val
  elseif (array_name .eq. 'snd_i') then
    snd_i(x_index, y_index) = array_val
  elseif (array_name .eq. 'stcon_i') then
    stcon_i(x_index, y_index) = array_val
  elseif (array_name .eq. 'monthly_time') then
    monthly_time(x_index, y_index) = array_val
  elseif (array_name .eq. 'monthly_freeze_up_temp') then
    monthly_freeze_up_temp(x_index, y_index) = array_val
  elseif (array_name .eq. 'monthly_snow_level') then
    monthly_snow_level(x_index, y_index) = array_val
  !elseif (array_name .eq. 'monthly_temperature') then
  !  monthly_temperature(x_index, y_index) = array_val
  else
    print*,'Fortran BMI error: set_float_array2d_element array_name not recognized: ',&
      array_name
    stop
  endif

end subroutine set_float_array2d_element
