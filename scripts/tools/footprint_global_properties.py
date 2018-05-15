#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path

from KicadModTree import *  # NOQA
from drawing_tools import *

crt_offset = 0.25
lw_fab = 0.1
lw_crt = 0.05
lw_slk = 0.12
slk_offset = lw_slk/2
slk_pad_offset = lw_slk/2+0.2
txt_offset = 1
grid_crt=0.01
min_pad_distance=0.2
fab_text_size_min=0.25
fab_text_size_max=2.00
