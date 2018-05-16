#!/bin/bash
echo "removing files in output directory..."
rm dump/start.txt
rm dump/result.txt
rm dump/mean.txt

echo ". ./compile_f2p"
. ./compile_f2p

echo "python gipl_wrapper.py"
python gipl_wrapper.py $1

echo ". ./check_noopt_3yr "
. ./check_noopt_3yr 
