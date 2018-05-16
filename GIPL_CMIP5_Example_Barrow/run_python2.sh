#!/bin/bash
echo "removing files in output directory..."
echo "rm dump/start.txt"
rm dump/start.txt
echo "rm dump/result.txt"
rm dump/result.txt
echo "rm dump/mean.txt"
rm dump/mean.txt

echo ". ./compile_f2p"
. ./compile_f2p

echo "python gipl_wrapper.py"
python gipl_wrapper.py $1

echo ". ./check_noopt_3yr "
. ./check_noopt_3yr 
