#!/bin/bash

mkdir Connectors_JST_PH.pretty

# create Through-hole type shrouded header, Top entry type
for i in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do
   ./connectors_jst_ph_tht_top.py $i > "Connectors_JST_PH.pretty/Connectors_JST_B${i}B-PH-K.kicad_mod"
done

# create Through-hole type shrouded header, Side entry type
for i in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do
   ./connectors_jst_ph_tht_side.py $i > "Connectors_JST_PH.pretty/Connectors_JST_S${i}B-PH-K.kicad_mod"
done
