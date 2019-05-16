#!/usr/bin/env python3

'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
'''

import sys
import os

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
from math import sqrt
import argparse
import yaml
from KicadModTree import *

output_dir = "Connector_Stocko.pretty"

if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
    os.makedirs(output_dir)

#connector constraints
pad_span = 2.5
pad_size_x = 1.5
pad_size_y = 2
drill = 1
fab_outline_x = 3.6
fab_outline_y = 3.75
fab_cut_depth = 2
fab_cut_width = 2
fab_arc_r = 0.5
fab_first_pin = 0.5

silks_outline_x = fab_outline_x + 0.11
silks_outline_y = fab_outline_y + 0.11
silks_cut_depth = 2
silks_cut_width = 2 + 0.22
silks_arc_r = fab_arc_r + 0.11

courtyard_outline = 0.5

for itr in range (1, 20 + 1):

    # for special case, details: https://www.stocko-contact.com/en/products-connector-system-pitch-2.5-mm-rfk-2-mks-1650.php
    if itr == 1:
        pin_count = 2
    elif itr == 2:
        pin_count = 2
        fab_outline_x = 2.7
        silks_outline_x = fab_outline_x + 0.11
    else:
        pin_count = itr
        fab_outline_x = 3.6
        silks_outline_x = fab_outline_x + 0.11

    #init kicad footprint
    footprint_name = "Stocko_MKS_16{}-6-0-{}{:02d}_1x{}_P2.50mm_Vertical".format(50 + itr, pin_count, pin_count, pin_count)
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Stocko MKS 16xx series connector, (https://www.stocko-contact.com/downloads/steckverbindersystem-raster-2,5-mm.pdf#page=15), generated with kicad-footprint-generator")
    kicad_mod.setTags("Stocko RFK MKS 16xx")

    #CREATE PIN

    #first rectangle pin
    kicad_mod.append(Pad(number = 1, type = Pad.TYPE_THT, shape = Pad.SHAPE_ROUNDRECT,
                        at=[0, 0], size=[pad_size_x, pad_size_y], drill=drill, layers=Pad.LAYERS_THT,
                        radius_ratio=0.25))
    #circle pin
    for pin_cnt in range (2, pin_count + 1):
        kicad_mod.append(Pad(number = pin_cnt, type = Pad.TYPE_THT, shape = Pad.SHAPE_OVAL,
                        at=[(pin_cnt - 1) * pad_span, 0], size=[pad_size_x, pad_size_y], drill=drill, layers = Pad.LAYERS_THT))

    #CREATE SILKSCREEN
    #name
    kicad_mod.append(Text(type = 'reference', text='REF**', at=[(pin_count - 1) * (pad_span / 2), -4.5], layer='F.SilkS'))
    #top
    kicad_mod.append(Line(start = [-silks_outline_x + silks_arc_r, -silks_outline_y],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_arc_r, -silks_outline_y], layer = 'F.SilkS'))
    #left
    kicad_mod.append(Line(start = [-silks_outline_x, -silks_outline_y + silks_arc_r],
                          end = [-silks_outline_x, silks_outline_y - silks_arc_r], layer = 'F.SilkS'))
    #right
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x, -silks_outline_y + silks_arc_r],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x, silks_outline_y - silks_arc_r], layer = 'F.SilkS'))
    #bottom left
    kicad_mod.append(Line(start = [-silks_outline_x + silks_arc_r, silks_outline_y],
                          end = [-silks_outline_x + silks_cut_width, silks_outline_y], layer = 'F.SilkS'))
    kicad_mod.append(Line(start = [-silks_outline_x + silks_cut_width, silks_outline_y],
                          end = [-silks_outline_x + silks_cut_width, silks_outline_y - silks_cut_depth], layer = 'F.SilkS'))
    #bottom right
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_arc_r, silks_outline_y],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_cut_width, silks_outline_y], layer = 'F.SilkS'))
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_cut_width, silks_outline_y],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_cut_width, silks_outline_y - silks_cut_depth], layer = 'F.SilkS'))
    #bottom center
    kicad_mod.append(Line(start = [-silks_outline_x + silks_cut_width, silks_outline_y - silks_cut_depth],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_cut_width, silks_outline_y - silks_cut_depth], layer = 'F.SilkS'))
    #arc left top
    kicad_mod.append(Arc(center = [-silks_outline_x + silks_arc_r, -silks_outline_y + silks_arc_r],
                         start = [-silks_outline_x, -silks_outline_y + silks_arc_r], angle = 90, layer = 'F.SilkS'))
    #arc right top
    kicad_mod.append(Arc(center = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_arc_r, -silks_outline_y + silks_arc_r],
                         start = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_arc_r, -silks_outline_y], angle = 90, layer = 'F.SilkS'))
    #arc left bottom
    kicad_mod.append(Arc(center = [-silks_outline_x + silks_arc_r, silks_outline_y - silks_arc_r],
                         start = [-silks_outline_x + silks_arc_r, silks_outline_y], angle = 90, layer = 'F.SilkS'))
    #arc right bottom
    kicad_mod.append(Arc(center = [(pin_cnt - 1) * pad_span + silks_outline_x - silks_arc_r, silks_outline_y - silks_arc_r],
                         start = [(pin_cnt - 1) * pad_span + silks_outline_x, silks_outline_y - silks_arc_r], angle = 90, layer = 'F.SilkS'))
    #first pin indicator
    kicad_mod.append(Line(start = [0.3, 2.9], end = [0, 2.4], layer = 'F.SilkS'))
    kicad_mod.append(Line(start = [0, 2.4], end = [-0.3, 2.9], layer = 'F.SilkS'))
    kicad_mod.append(Line(start = [-0.3, 2.9], end = [0.3, 2.9], layer = 'F.SilkS'))


    #CREATE FABRICATION
    #name
    kicad_mod.append(Text(type = 'user', text = '%R', at = [(pin_count - 1) * (pad_span / 2), -2], layer = 'F.Fab'))
    kicad_mod.append(Text(type = 'value', text = footprint_name, at = [(pin_count - 1) * (pad_span / 2), silks_outline_y + 2], layer = 'F.Fab'))
    #top
    kicad_mod.append(Line(start = [-fab_outline_x + fab_arc_r, -fab_outline_y],
                          end = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_arc_r, -fab_outline_y], layer = 'F.Fab'))
    #left
    kicad_mod.append(Line(start = [-fab_outline_x, -fab_outline_y + fab_arc_r],
                          end = [-fab_outline_x, fab_outline_y - fab_arc_r], layer = 'F.Fab'))
    #right
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + fab_outline_x, -fab_outline_y + fab_arc_r],
                          end = [(pin_cnt - 1) * pad_span + fab_outline_x, fab_outline_y - fab_arc_r], layer = 'F.Fab'))
    #bottom left
    kicad_mod.append(Line(start = [-fab_outline_x + fab_arc_r, fab_outline_y],
                          end = [-fab_outline_x + fab_cut_width, fab_outline_y], layer = 'F.Fab'))
    kicad_mod.append(Line(start = [-fab_outline_x + fab_cut_width, fab_outline_y],
                          end = [-fab_outline_x + fab_cut_width, fab_outline_y - fab_cut_depth], layer = 'F.Fab'))
    #bottom right
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_arc_r, fab_outline_y],
                          end = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_cut_width, fab_outline_y], layer = 'F.Fab'))
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_cut_width, fab_outline_y],
                          end = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_cut_width, fab_outline_y - fab_cut_depth], layer = 'F.Fab'))
    #bottom center and first pin indicator
    kicad_mod.append(Line(start = [-fab_outline_x + fab_cut_width, fab_outline_y - fab_cut_depth],
                          end = [-fab_first_pin, fab_outline_y - fab_cut_depth], layer = 'F.Fab'))

    kicad_mod.append(Line(start = [fab_first_pin, fab_outline_y - fab_cut_depth],
                          end = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_cut_width, fab_outline_y - fab_cut_depth], layer = 'F.Fab'))

    kicad_mod.append(Line(start = [-fab_first_pin, fab_outline_y - fab_cut_depth],
                          end = [0, fab_outline_y - fab_cut_depth - fab_first_pin], layer = 'F.Fab'))

    kicad_mod.append(Line(start = [0, fab_outline_y - fab_cut_depth - fab_first_pin],
                          end = [fab_first_pin, fab_outline_y - fab_cut_depth], layer = 'F.Fab'))

    #arc left top
    kicad_mod.append(Arc(center = [-fab_outline_x + fab_arc_r, -fab_outline_y + fab_arc_r],
                         start = [-fab_outline_x, -fab_outline_y + fab_arc_r], angle = 90, layer = 'F.Fab'))
    #arc right top
    kicad_mod.append(Arc(center = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_arc_r, -fab_outline_y + fab_arc_r],
                         start = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_arc_r, -fab_outline_y], angle = 90, layer = 'F.Fab'))
    #arc left bottom
    kicad_mod.append(Arc(center = [-fab_outline_x + fab_arc_r, fab_outline_y - fab_arc_r],
                         start = [-fab_outline_x + fab_arc_r, fab_outline_y], angle = 90, layer = 'F.Fab'))
    #arc right bottom
    kicad_mod.append(Arc(center = [(pin_cnt - 1) * pad_span + fab_outline_x - fab_arc_r, fab_outline_y - fab_arc_r],
                         start = [(pin_cnt - 1) * pad_span + fab_outline_x, fab_outline_y - fab_arc_r], angle = 90, layer = 'F.Fab'))

    #CREATE COURTYARD
    kicad_mod.append(RectLine(start = [-fab_outline_x - courtyard_outline, -fab_outline_y - courtyard_outline],
                              end = [(pin_cnt - 1) * pad_span + fab_outline_x + courtyard_outline, fab_outline_y + courtyard_outline],
                              layer = 'F.CrtYd'))
    #add 3D model
    kicad_mod.append(Model(filename="${{KISYS3DMOD}}/Connector_Stocko.3dshapes/{}.wrl".format(footprint_name),
                        at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
    #output kicad model
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(output_dir + '/' + footprint_name + '.kicad_mod')