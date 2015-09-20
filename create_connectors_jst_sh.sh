#!/bin/bash

mkdir Connectors_JST_SH.pretty

# SMT type shrouded header, Top entry type
for i in "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15"
do
   ./connectors_jst_sh_smd_top.py $i > "Connectors_JST_SH.pretty/Connectors_JST_BM${i}B-SRSS-TB.kicad_mod"
done

