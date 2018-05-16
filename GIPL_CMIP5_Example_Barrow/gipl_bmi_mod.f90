module gipl_bmi

  integer, save :: n_site
  integer, save :: n_time
  character(64), save :: fconfig = ""
  real*8, save :: time_loop
  real*8, save :: time_step
  real*8, save :: time_beg,time_end
  real*8, save :: time_s, time_e

!  subroutine bmi_initialize(config_filename)
!    use gipl_const
!    use bnd
!    use thermo
!    use grd
!    use alt
!
!    implicit none
!
!    fconfig = config_filename
!    initialize(n_site, n_time)
!  end subroutine bmi_initialize

end module gipl_bmi
