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

  character(64) :: empty_filename = ''

  if (iargc() .eq. 1) then
    call getarg(1, fconfig)
  else
    !fconfig = 'gipl_config_3yr.cfg'
    fconfig = '../examples/gipl_config_3yr.cfg'
  endif

  print*,'Running from Fortran with config file: ', fconfig

  call run_gipl(empty_filename)
end
