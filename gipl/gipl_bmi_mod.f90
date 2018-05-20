module gipl_bmi

  integer, save :: n_site
  integer, save :: n_time
  character(64), save :: fconfig = ""
  real*8, save :: time_loop
  real*8, save :: time_step
  real*8, save :: time_beg,time_end
  real*8 :: time_s, time_e

  !! Test arrays to see how f2py passes arrays to python/numpy
  integer, allocatable, dimension(:, :, :), save :: intarray3d
  real*8, allocatable, dimension(:, :, :), save :: doublearray3d


  ! Input arrays

  ! upper boundary snow time and snow depth (input)
  real*8 ,allocatable,dimension(:,:):: snd

  ! time and upper boundary temprature (interpolated)
  real*8,allocatable,dimension(:,:)::  utemp

  ! snow thermal conductivity time and itself (input)
  real*8 ,allocatable,dimension(:,:):: stcon

  !! these variables would be added to make coupling simpler
  !real*8, allocatable, dimension(:,:) :: surface_temp
  !real*8, allocatable, dimension(:,:) :: snow_depth
  !real*8, allocatable, dimension(:,:) :: snow_thermal_conductivity


  !!! these variables are added to make output simpler

  ! Written to file 1, result_file: 'result.txt'
  ! Effectively printed every timestep
  real*8,allocatable,dimension(:,:) :: monthly_time           ! site,month
  real*8,allocatable,dimension(:,:) :: monthly_freeze_up_temp ! site,month
  real*8,allocatable,dimension(:,:) :: monthly_snow_level     ! site,month
  real*8,allocatable,dimension(:,:,:) :: monthly_temperature  ! site,month,depth

  ! Written to file 2, aver_res_file: 'mean.txt'
  ! Annual averages, so written  at end of each year
  ! Compute average of "file 1" values, and:
  real*8, allocatable, dimension(:) :: annual_average_time    ! site
  real*8, allocatable, dimension(:) :: annual_freeze_up_temp  ! site
  real*8, allocatable, dimension(:) :: annual_snow_level      ! site
  real*8, allocatable, dimension(:,:) :: annual_temperature   ! site
  real*8, allocatable, dimension(:) :: freeze_up_depth        ! site
  real*8, allocatable, dimension(:) :: freeze_up_time_current ! site
  real*8, allocatable, dimension(:) :: freeze_up_time_total   ! site

  ! Written to file 3, restart_file: 'start.txt'
  ! This is the temperature at depths, array 'temp'

end module gipl_bmi
