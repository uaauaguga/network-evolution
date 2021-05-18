#!/bin/bash
echo -e "connect-probability\tdelete-probability\tadd-probability\tslope\tr"
for cp in 0.001 0.01 0.1;do
 for dp in 0.001 0.01 0.1 0.2 0.4 0.9;do
  for ap in 0.001 0.01 0.1 0.2 0.4 0.9;do
   scripts/simulate.py -dp $dp -ap $ap -cp $cp 
  done 
 done
done
