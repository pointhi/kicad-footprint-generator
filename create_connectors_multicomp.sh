#!/bin/bash

mkdir Connectors_Multicomp.pretty

# Wire-To-Board-Steckverbinder, Straight
for i in "10" "14" "16" "20" "26" "34" "40" "50" "60" "64"
do
   ./connectors_multicomp_mc9a12.py $i > "Connectors_Multicomp.pretty/Connectors_Multicomp_MC9A12-${i}34.kicad_mod"
done

# Wire-To-Board-Steckverbinder, Right Angle
for i in "10" "14" "16" "20" "26" "34" "40" "50" "60"
do
   ./connectors_multicomp_mc9a22.py $i > "Connectors_Multicomp.pretty/Connectors_Multicomp_MC9A22-${i}34.kicad_mod"
done
