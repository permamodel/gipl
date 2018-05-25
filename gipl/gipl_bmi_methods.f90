! gipl_bmi_methods.f90
!
! Only BMI methods are defined here.  These serve as the interface between
! the GIPL code via BMI

subroutine initialize(initial_config_file)
  implicit none

  character(64) :: initial_config_file

  call initialize_f90(initial_config_file)

end subroutine initialize


subroutine update()
  call update_model()
  call write_output()

end subroutine update


subroutine update_until(target_time)
  implicit none

  real*8 :: target_time

  call update_model_until(target_time)

end subroutine update_until


subroutine finalize()
  call finalize_f90()

end subroutine finalize


subroutine get_time_step(time_step_value)
  use gipl_bmi

  implicit none

  real*8, intent(out) :: time_step_value

  time_step_value = time_step

end subroutine get_time_step


subroutine get_end_time(end_time_value)
  use gipl_bmi

  implicit none

  real*8, intent(out) :: end_time_value

  end_time_value = time_e

end subroutine get_end_time


subroutine get_var_ref(var_name, dest)
  use gipl_bmi

  implicit none

  character(64) :: var_name

  !real*8, target :: time_loop_val
  real*8, pointer, intent(inout) :: dest

  select case (var_name)
  case ('model_current__timestep')
    dest = time_loop
  end select
end subroutine get_var_ref


subroutine get_value(var_name, dest)
  use gipl_bmi

  implicit none

  character(64) :: var_name
  real*8 :: temporary_float
  integer :: temporary_int
  real*8, intent(out) :: dest

  select case (var_name)
  case ('model_current__timestep')
    temporary_float = time_loop
    dest = temporary_float
  case ('model_timesteps_per_year')
    temporary_int = n_time
    print*, 'temporary_int: ', temporary_int
    dest = temporary_int
  case default
    print*, 'Default case, fail:', var_name
    print*, 'model_current__timestep', 'xxx'
    print*, var_name, 'xxx'
    stop
  end select

end subroutine get_value
