## GIPL

# Initial README.md file for permamodel/gipl repository

This project consists of a version of the GIPL model that can be wrapped
with a BMI interface.

Included here are:

  - Fortran source code that can be compiled:
    - In standalone mode by gfortran using the include Makefile
    - As a shared object library (f2py_gipl.so) using the included Makefile
  - Sample configuration files:
    - ./examples/gipl_config.cfg
    - ./examples/gipl_config_3yr.cfg
    - ./examples/gipl_config_5yr.cfg
  - Sample input files in ./gipl/in/
  - Current output directory ./gipl/output/
  - Directories with sample outputs:
    - ./examples/original_output/     # a 135 year monthly run, run with optimized code
    - ./examples/original_output/     # a 135 year monthly run, run with optimized code
    - ./examples/output_no_opt_3yr/   # the first 3 years' output of ./original_output/
    - ./examples/output_no_opt_5yr/   # the first 5 years' output of ./original_output/
  - bmi_gipl.py
    - Python code to run the model via an import of a shared object library
    - shared object library is the result of "make f2py_gipl.so"
    - uses Numpy's "f2py" compiler, which comes with Python2 and Python3

Quick usage:

  - . Script mrc3, performs the following actions:
    - make clean
    - make
    - runs the code for the short -- 3-year -- sample run
    - compares the output of the code -- in ./output/ -- to the expected results
    - Run from the ./gipl/ directory as ". ../examples/mrc3"
    

  - ./run_python2.sh, performs the following actions:
    - compiles the code via f2py
    - runs the code by running 'python bmi_gipl.py'
      - by default, this runs the same 3-year configuration as the Fortran code
    - compares the results to the values in the expected directory
    - Run from the ./gipl/ directory as ". ../examples/run_python2.sh"

Example scripts:
  - Note: most of these scripts were developed and tested while in the ./gipl/ directory
  - Scripts that start with "mr" are "make; run" scripts the build the executable from Fortran source code
  - "mrc" is short for "make; run; compare", so the output is compared with a sample output directory
  - "check_..." scripts compare the current output directory with example outputs
  - "make f2py_gipl.so" compiles the shared object library that Python can import
    - and generates a Python-importable shared library named "f2py_gipl.so"
    - can be imported by Python with "import f2py_gipl"
  - "run_python2.sh" is equivalent to "mrc3" and uses Python-compatible process to:
    - make, run, compare the code results when it is run from Python
   
