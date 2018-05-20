module gipl_const

  real*8, parameter  :: hcap_snow=840000.0                ! heat capacity of snow (constant)
  real*8, parameter  :: Lf=333.2*1.D+6                    ! Latent of water fusion
  integer, parameter :: lbound=2                          ! 1 const temp, 2 heat flux condition at the bottom boundary
  integer, parameter :: n_lay=10                          ! total allowed number of soil layer

end module gipl_const

module bnd
  integer :: n_temp                                       ! number of upper boundary points for temperature (input)
  real*8,allocatable,dimension(:):: utemp_time         ! upper boundary time and temperature (input)
  real*8,allocatable,dimension(:,:):: utemp         ! upper boundary time and temperature (input)
  real*8,allocatable,dimension(:):: utemp_time_i(:)     ! time and upper boundary temprature (interpolated)
  real*8,allocatable,dimension(:,:):: utemp_i(:,:)     ! time and upper boundary temprature (interpolated)
  integer :: n_snow                                       ! number of upper boundary points for snow (input)
  real*8 ,allocatable,dimension(:):: snd_time(:)              ! upper boundary snow time and snow depth (input)
  real*8 ,allocatable,dimension(:,:):: snd(:,:)              ! upper boundary snow time and snow depth (input)
  integer :: n_stcon
  real*8 ,allocatable,dimension(:):: stcon_time(:)          ! snow thermal conductivity time and itself (input)
  real*8 ,allocatable,dimension(:,:):: stcon(:,:)          ! snow thermal conductivity time and itself (input)
  real*8 ,allocatable,dimension(:,:):: snd_i (:,:)        ! snow depth and thermal conductivity (interpolated)
  real*8 ,allocatable,dimension(:,:):: stcon_i (:,:)        ! snow depth and thermal conductivity (interpolated)
  real*8 :: TINIR
  real*8 :: time_restart                                  ! restart time in restart file


! Parameter read from cmd file
  integer :: restart                                     ! 0/1 start from previous time step / start from the begining
  ! time_step is now in the gipl_bmi module
  !real*8 :: time_step                                    ! step is the timestep in the example it is 1 yr
  real*8 :: TAUM                                         ! taum is the convergence parameter used by the stefan subroutine
  real*8 :: TMIN                                         ! tmin minimal timestep used in the Stefan subroutine
  ! time_beg and time_end are not in gipl_bmi module
  !real*8 :: time_beg,time_end                            ! inbegin time, end time
  integer :: itmax                                       ! maximum number of iterations in Stefan subroutine
  !integer :: n_time                                      ! number of time steps that temp will be averaged over
  integer :: n_frz_max                                   ! maximum number of freezing fronts
  real*8 :: smooth_coef                                  ! smoothing factor
  real*8 :: unf_water_coef                               ! unfrozen water coefficient
  real*8 :: n_sec_day                                    ! number of second in a day
  real*8 :: frz_frn_max,frz_frn_min                      ! freezing front min and max depth [meters]
  real*8 :: sat_coef                                     ! saturation coefficient [dimensionless, fraction of 1]
! output file names
  character(64) :: restart_file,result_file,aver_res_file

  type site_gipl
    real*8 :: time
  end type site_gipl

end module bnd

module thermo
  real*8 L_fus                                            ! Latent heat of fusion [W/mK]
  real*8 sea_level                                        ! how many meter above the sea level the borehole is

! thermo physical parameters of soil for each soil layer
  real*8,allocatable,dimension(:,:):: vwc                           ! volumetric water content
  real*8,allocatable,dimension(:,:):: a_coef,b_coef            ! a and b unfrozen water curve coefficients
  real*8,allocatable,dimension(:,:):: temp_frz                      ! temperature freezing depression
  real*8,allocatable,dimension(:,:):: EE
  real*8,allocatable,dimension(:,:):: hcap_frz,hcap_thw        ! soil layer heat capacity thawed/frozen
  real*8,allocatable,dimension(:,:):: tcon_frz,tcon_thw        ! soil layer thermal conductivity thawed/frozen


  real*8 :: hcap_s                                         ! heat capacity of snow (constant) nondimentional

  ! temp is now defined in gipl_bmi_mod.f90
  !real*8, allocatable,dimension(:,:) :: temp                        ! soil temperature
  real, allocatable,dimension(:,:):: n_bnd_lay                      ! number of boundaries between layer in soil
  integer k0


  integer, allocatable ,dimension(:):: snow_code,veg_code        ! (not necccessary) required for runing in parallel
  integer, allocatable ,dimension(:):: geo_code,gt_zone_code     ! (not necccessary) required for runing in parallel
  real*8, allocatable  ,dimension(:):: temp_grd                     ! temprature gradient at the lower boundary

  !real*8 ,allocatable,dimension(:,:):: RES                          ! unified variable for the writing results into the file

end module thermo

module grd

  integer,allocatable,dimension(:):: n_lay_cur                      ! current number of soil layers <= n_lay
! calclulated as a sum of organic and mineral soil layers
  !integer :: n_site                                       ! number of sites
  ! n_grd now defined in bmi_bmi_mod.f90
  !integer :: n_grd                                        ! total number of grid points with depth (grid.txt)
  real*8,allocatable,dimension(:):: zdepth,dz                    ! vertical grid and distance between grid point 'zdepth(n_grd)'
  integer,allocatable,dimension(:,:):: lay_id                      ! layer index
  ! m_grd now defined in bmi_bmi_mod.f90
  !integer :: m_grd                                        ! number of grid points to store in res file
  integer,allocatable,dimension(:):: zdepth_id                      ! index vector of stored grid points 'zdepth_id(m_grid)'
  integer :: n_ini                                        ! number of vertical grid cells in init file
  real*8, allocatable,dimension(:) :: zdepth_ini     ! depth and correspoding initial temperature (time=0) 'zdepth_ini(n_ini)'
  real*8, allocatable,dimension(:,:) :: ztemp_ini     ! depth and correspoding initial temperature (time=0) 'zdepth_ini(n_ini)'
  character(210) :: FMT1,FMT2                             ! results formating type

end module grd

module alt
  integer,allocatable,dimension(:,:)::n_frz_frn                     ! number of freezing front (e.g. when freezup is about to happened)
  integer,allocatable,dimension(:)::i_time                          ! internal time step with the the main loop
  real*8 ,allocatable,dimension(:,:,:)::z_frz_frn                   ! depth of the freezing front
end module alt

