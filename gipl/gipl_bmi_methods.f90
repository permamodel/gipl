! gipl_bmi_methods.f90
!
! Only BMI methods are defined here.  These serve as the interface between
! the GIPL code via BMI

subroutine initialize(initial_config_file)
  implicit none

  character(64) :: initial_config_file

  call initialize_f90(initial_config_file)
end subroutine initialize



