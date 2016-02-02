#!/bin/bash

mkdir Connectors_JST.pretty

# SMT type shrouded header, Top entry type
for i in "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15"
do
   ./connectors_jst_sh_smd_top.py $i > "Connectors_JST.pretty/JST_SH_BM${i}B-SRSS-TB_${i}x1.00mm_Straight.kicad_mod"
done

# SMT type shrouded header, Side entry type
for i in "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "20"
do
   ./connectors_jst_sh_smd_side.py $i > "Connectors_JST.pretty/JST_SH_SM${i}B-SRSS-TB_${i}x1.00mm_Angled.kicad_mod"
done
