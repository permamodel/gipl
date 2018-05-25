! Geophysical Institute Permafrost Laboratory model version 2 GIPLv2
! version 2 is a numerical transient model that employs phase changes
! and the effect of the unfrozen volumetric water content in the
! non-homogeneuos soil texture
! Original version of the model developed by Romanovsky and Tipenko 2004
! and described in Marchenko et al., (2008)
! Current version been significantly modified from its predecessor
! and uses IRF coding design
! This version is maintained by E. Jafarov at INSTAAR, CU Boulder
! Please cite Jafarov et al., (2012) work when using it.

program gipl2
  use gipl_bmi

  implicit none

  ! Note: this code could be rewritten to accept a filename from the cmd line
  character(64) :: filename_passed = ''

  real*8 :: time_reference_counter
  character(64) :: passed_config_filename

  if (iargc() .eq. 1) then
    call getarg(1, fconfig)
  else
    !fconfig = 'gipl_config_3yr.cfg'
    fconfig = '../examples/gipl_config_3yr.cfg'
  endif

  if (filename_passed .ne. '') then
    fconfig = filename_passed
  endif

  ! if configuration file is defined elsewhere, use that
  ! otherwise, set a default here
  if (fconfig .eq. '') then
    fconfig='gipl_config_3yr.cfg'
    print *, 'No config file specified.  Using: ', fconfig
  ! Full 135 year config file:
  !   fconfig='gipl_config.cfg'
  endif

  passed_config_filename = fconfig

  print*,'Running from Fortran with config file: ', fconfig

  call initialize(passed_config_filename)

  ! Because we want to test both update() and update_until(), and because
  ! there are write()s both the time of a year's timestep and the timestep
  ! prior, we need two calls to write_output() at different points in
  ! the annual cycle
  do while (time_loop .lt. time_e)
    print*, 'run_gipl time_loop: ', time_loop
    time_reference_counter = time_loop

    ! Note: if an adjustment to surface temperature, snow depth, or stcon
    !    is to be made, it should be made before a call to update()
    !    and to the internal-interpolated grids:
    !       utemp_i(i_time(i_site)))
    !       snd_i(i_time(i_site)))
    !       stcon_i(i_time(i_site)))
    !    These values were interpolated for the following year at the end
    !      of the previous year in update() (or initialize() for 1st yr
    call update()
    call update_until(time_reference_counter + (n_time - 3) * time_step)
    call update()
    call update()
    !call write_output()
    call update()
    !call write_output()
  enddo

  call finalize()

end program gipl2
