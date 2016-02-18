#!/bin/bash

mkdir Connectors_Molex.pretty

# SMT type shrouded header, Top entry type
for i in "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "16"
do
   ./connectors_molex_kk_6410_top.py $i > "Connectors_Molex.pretty/Molex_KK_6410-${i}.kicad_mod"
done
