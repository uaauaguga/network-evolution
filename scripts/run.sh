#!/bin/bash
echo -e "connect-probability\tdelete-probability\tadd-probability\tn-node\tslope\tr\tp"

for n in 100 200 400 800;do
for cp in 0.001 0.01 0.1 0.9;do
 for dp in 0.001 0.01 0.1 0.9;do
  for ap in 0.001 0.01 0.1 0.9;do
   scripts/simulate.py -dp $dp -ap $ap -cp $cp -n $n 
   done 
  done
 done
done
