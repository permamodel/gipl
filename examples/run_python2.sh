#!/bin/bash
echo "removing files in output directory..."
echo "rm output/start.txt"
rm output/start.txt
echo "rm output/result.txt"
rm output/result.txt
echo "rm output/mean.txt"
rm output/mean.txt

echo "make f2py_gipl.so"
make f2py_gipl.so

echo "python bmi_gipl.py"
python bmi_gipl.py $1

echo ". ./check_noopt_3yr "
. ../examples/check_noopt_3yr 
