#!/bin/bash

mkdir Connectors_JST.pretty

# create Through-hole type shrouded header, Top entry type
for i in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do

    if [ $i -lt 10 ]
    then
        PIN_NUMBER="0${i}"
    else
        PIN_NUMBER=${i}
    fi

   ./connectors_jst_ph_tht_top.py $i > "Connectors_JST.pretty/JST_PH_B${i}B-PH-K_${PIN_NUMBER}x2.00mm_Straight.kicad_mod"
done

# create Through-hole type shrouded header, Side entry type
for i in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do
    if [ $i -lt 10 ]
    then
        PIN_NUMBER="0${i}"
    else
        PIN_NUMBER=${i}
    fi

   ./connectors_jst_ph_tht_side.py $i > "Connectors_JST.pretty/JST_PH_S${i}B-PH-K_${PIN_NUMBER}x2.00mm_Angled.kicad_mod"
done

# SMT type shrouded header, Top entry type
for i in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do
    if [ $i -lt 10 ]
    then
        PIN_NUMBER="0${i}"
    else
        PIN_NUMBER=${i}
    fi

   ./connectors_jst_ph_smd_top.py $i > "Connectors_JST.pretty/JST_PH_B${i}B-PH-SM4-TB_${PIN_NUMBER}x2.00mm_Straight.kicad_mod"
done

# SMT type shrouded header, Side entry type
for i in 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
    if [ $i -lt 10 ]
    then
        PIN_NUMBER="0${i}"
    else
        PIN_NUMBER=${i}
    fi

   ./connectors_jst_ph_smd_side.py $i > "Connectors_JST.pretty/JST_PH_S${i}B-PH-SM4-TB_${PIN_NUMBER}x2.00mm_Angled.kicad_mod"
done

