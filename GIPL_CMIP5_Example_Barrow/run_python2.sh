#!/bin/bash
echo "removing files in output directory..."
echo "rm output/start.txt"
rm output/start.txt
echo "rm output/result.txt"
rm output/result.txt
echo "rm output/mean.txt"
rm output/mean.txt

echo ". ./compile_f2p"
. ./compile_f2p

echo "python gipl_wrapper.py"
python gipl_wrapper.py $1

echo ". ./check_noopt_3yr "
. ./check_noopt_3yr 
