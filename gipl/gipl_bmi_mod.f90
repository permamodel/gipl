module gipl_bmi

  integer, save :: n_site
  integer, save :: n_time
  character(64), save :: fconfig = ""
  real*8, save :: time_loop
  real*8, save :: time_step
  real*8, save :: time_beg,time_end
  real*8, save :: time_s, time_e

  ! Input arrays

  ! upper boundary snow time and snow depth (input)
  real*8 ,allocatable,dimension(:,:):: snd(:,:)

  ! time and upper boundary temprature (interpolated)
  real*8,allocatable,dimension(:,:)::  utemp(:,:)

  ! snow thermal conductivity time and itself (input)
  real*8 ,allocatable,dimension(:,:):: stcon(:,:)

end module gipl_bmi
