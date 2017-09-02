#!/bin/bash
cd ../content/rush/
for day in 01 02 03 04 05 06 07 08 09 10 11 12 13 14
do
    mv *-${day}T* Sep$day
done
