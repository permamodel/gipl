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
