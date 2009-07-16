#!/bin/bash 
COUNTER=$1
while [  $COUNTER -le $2 ]; do
     python solver.py $COUNTER --silent --var-order $3 --val-order $4
     let COUNTER=COUNTER+1 
done

# python solver.py 1