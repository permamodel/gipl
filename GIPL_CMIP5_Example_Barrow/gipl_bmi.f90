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

  if (var_name .eq. 'time_loop') var_val = time_loop
  if (var_name .eq. 'time_step') var_val = time_step
  if (var_name .eq. 'time_e') var_val = time_e
  if (var_name .eq. 'n_time') var_val = n_time

end subroutine
