CC=gfortran

CFLAGS=-c  -Wall

gipl: gipl.o
	$(CC) gipl_bmi_mod.o gipl_mods.o gipl.o gipl_main.o -o gipl

all: gipl f2py_gipl.so

gipl_bmi_mod.o: gipl_bmi_mod.f90
	$(CC) $(CFLAGS) gipl_bmi_mod.f90

gipl_mods.o: gipl_mods.f90
	$(CC) $(CFLAGS) gipl_mods.f90

gipl_main.o: gipl_main.f90
	$(CC) $(CFLAGS) gipl_main.f90

gipl.o: gipl.f90 gipl_mods.o gipl_bmi_mod.o gipl_main.o
	$(CC) $(CFLAGS) gipl.f90

f2py_gipl.so: gipl.f90 gipl_mods.f90 gipl_bmi_mod.f90
	f2py -m f2py_gipl gipl.f90 gipl_mods.f90 gipl_bmi_mod.f90 -c > f2py_gipl_and_mods.out 2>&1

clean:
	rm *.o *.so *.mod f2py_gipl_and_mods.out gipl 

clean_fortran:
	rm *.o *.mod gipl 

clean_python:
	rm f2py_gipl_and_mods.out *.so
