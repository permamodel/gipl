#CC=ifort
CC=gfortran

#CFLAGS=-c -Ofast #-Wall
CFLAGS=-c  -Wall

all: gipl

gipl: gipl.o
	$(CC) gipl_bmi.o gipl_bmi_mod.o gipl_mods.o gipl.o -o gipl

#gipl_bmi.mod: gipl_bmi_mod.o gipl_bmi_mod.f90
#	$(CC) $(CFLAGS) gipl_bmi_mod.f90

gipl_bmi.o: gipl_bmi.f90
	$(CC) $(CFLAGS) gipl_bmi.f90

gipl_bmi_mod.o: gipl_bmi_mod.f90
	$(CC) $(CFLAGS) gipl_bmi_mod.f90

gipl_mods.o: gipl_mods.f90
	$(CC) $(CFLAGS) gipl_mods.f90

gipl.o: gipl.f90 gipl_mods.o gipl_bmi_mod.o gipl_bmi.o
	$(CC) $(CFLAGS) gipl.f90

clean:
	rm *o *.mod

clean_all:

	rm *.o *.mod gipl

