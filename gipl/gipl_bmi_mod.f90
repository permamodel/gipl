module gipl_bmi

  character(64), save :: fconfig = ""

  integer, save :: n_site
  integer, save :: n_time
  integer, save :: n_grd
  integer, save :: m_grd
  integer, save :: n_total_timesteps

  real*8, save :: time_loop
  real*8, save :: time_step
  real*8, save :: time_beg
  real*8, save :: time_end
  real*8, save :: time_s
  real*8, save :: time_e

  ! Input arrays, added to make coupling simpler
  real*8, allocatable, dimension(:) :: surface_temp               ! timestep
  real*8, allocatable, dimension(:) :: snow_depth                 ! timestep
  real*8, allocatable, dimension(:) :: snow_thermal_conductivity  ! timestep

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
  ! soil temperature 
  real*8, allocatable,dimension(:,:) :: temp

end module gipl_bmi
