!
! gipl_bmi.f90
!
! Routines permitting access to gipl variables from python
!

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
  endif

end subroutine


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
  endif

end subroutine


subroutine get_int_val(var_name, var_val)
  use gipl_bmi

  implicit none

  character(64) :: var_name
  integer :: var_val

!f2py intent(in) :: var_name
!f2py intent(out) :: var_val

  if (var_name .eq. 'n_time') then
    var_val = n_time
  else
    print*,'Fortran BMI error: get_int_var not recognized: ', var_name
  endif

end subroutine


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
  endif

end subroutine


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
  endif

end subroutine


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
    print*,'Fortran BMI error: get_string_var not recognized: ', var_name
  endif

end subroutine
