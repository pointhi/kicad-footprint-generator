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

for itr in range (1, 20 + 1):

    #connector constraints
    pad_span = 2.5
    pad_size = 2
    drill = 1
    silks_outline_x = 3.6
    silks_outline_y = 3.75
    cut_depth = 2
    cut_width = 2
    arc_r = 1.3
    courtyard_outline = 0.25

    # for special case, details: https://www.stocko-contact.com/en/products-connector-system-pitch-2.5-mm-rfk-2-mks-1650.php
    if itr == 1:
        pin_count = 2
    elif itr == 2:
        pin_count = 2
        silks_outline_x = 2.7
    else:
        pin_count = itr

    #init kicad footprint
    footprint_name = "Stocko_MKS_16{}-6-0-{}{:02d}_1x{}_P2.50mm_Vertical".format(50 + itr, pin_count, pin_count, pin_count)
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Stocko MKS 16xx series connector, (https://www.stocko-contact.com/downloads/steckverbindersystem-raster-2,5-mm.pdf), generated with kicad-footprint-generator")
    kicad_mod.setTags("Stocko RFK MKS 16xx")

    #CREATE PIN
    #first square pin
    kicad_mod.append(Pad(number = 1, type = Pad.TYPE_THT, shape = Pad.SHAPE_RECT,
                        at=[0, 0], size=[pad_size, pad_size], drill=drill, layers=Pad.LAYERS_THT))
    #circle pin
    for pin_cnt in range (2, pin_count + 1):
        kicad_mod.append(Pad(number = pin_cnt, type = Pad.TYPE_THT, shape = Pad.SHAPE_CIRCLE,
                        at=[(pin_cnt - 1) * pad_span, 0], size=[pad_size, pad_size], drill = drill, layers = Pad.LAYERS_THT))

    #CREATE SILKSCREEN
    #name
    kicad_mod.append(Text(type = 'reference', text='REF**', at=[(pin_count - 1) * (pad_span / 2), -4.5], layer='F.SilkS'))
    #top
    kicad_mod.append(Line(start = [-silks_outline_x + arc_r, -silks_outline_y],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - arc_r, -silks_outline_y], layer = 'F.SilkS'))
    #left
    kicad_mod.append(Line(start = [-silks_outline_x, -silks_outline_y + arc_r],
                          end = [-silks_outline_x, silks_outline_y - arc_r], layer = 'F.SilkS'))
    #right
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x, -silks_outline_y + arc_r],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x, silks_outline_y - arc_r], layer = 'F.SilkS'))
    #bottom left
    kicad_mod.append(Line(start = [-silks_outline_x + arc_r, silks_outline_y],
                          end = [-silks_outline_x + cut_width, silks_outline_y], layer = 'F.SilkS'))
    kicad_mod.append(Line(start = [-silks_outline_x + cut_width, silks_outline_y],
                          end = [-silks_outline_x + cut_width, silks_outline_y - cut_depth], layer = 'F.SilkS'))
    #bottom right
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x - arc_r, silks_outline_y],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - cut_width, silks_outline_y], layer = 'F.SilkS'))
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x - cut_width, silks_outline_y],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - cut_width, silks_outline_y - cut_depth], layer = 'F.SilkS'))
    #bottom center
    kicad_mod.append(Line(start = [-silks_outline_x + cut_width, silks_outline_y - cut_depth],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - cut_width, silks_outline_y - cut_depth], layer = 'F.SilkS'))
    #arc left top
    kicad_mod.append(Arc(center = [-silks_outline_x + arc_r, -silks_outline_y + arc_r],
                         start = [-silks_outline_x, -silks_outline_y + arc_r], angle = 90, layer = 'F.SilkS'))
    #arc right top
    kicad_mod.append(Arc(center = [(pin_cnt - 1) * pad_span + silks_outline_x - arc_r, -silks_outline_y + arc_r],
                         start = [(pin_cnt - 1) * pad_span + silks_outline_x - arc_r, -silks_outline_y], angle = 90, layer = 'F.SilkS'))
    #arc left bottom
    kicad_mod.append(Arc(center = [-silks_outline_x + arc_r, silks_outline_y - arc_r],
                         start = [-silks_outline_x + arc_r, silks_outline_y], angle = 90, layer = 'F.SilkS'))
    #arc right bottom
    kicad_mod.append(Arc(center = [(pin_cnt - 1) * pad_span + silks_outline_x - arc_r, silks_outline_y - arc_r],
                         start = [(pin_cnt - 1) * pad_span + silks_outline_x, silks_outline_y - arc_r], angle = 90, layer = 'F.SilkS'))
    #first pin indicator
    kicad_mod.append(Line(start = [0.3, 2.1], end = [0, 1.5], layer = 'F.SilkS'))
    kicad_mod.append(Line(start = [0, 1.5], end = [-0.3, 2.1], layer = 'F.SilkS'))
    kicad_mod.append(Line(start = [-0.3, 2.1], end = [0.3, 2.1], layer = 'F.SilkS'))

    #CREATE FABRICATION
    silks_outline_x_fab = silks_outline_x - 0.11
    silks_outline_y_fab = silks_outline_y - 0.11
    cut_depth = 2 + 0.11
    cut_width = 2 - 0.11
    arc_r = arc_r - 0.11

    #name
    kicad_mod.append(Text(type = 'user', text = '%R', at = [(pin_count - 1) * (pad_span / 2), -2], layer = 'F.Fab'))
    kicad_mod.append(Text(type = 'value', text = footprint_name, at = [(pin_count - 1) * (pad_span / 2), silks_outline_y + 2], layer = 'F.Fab'))
    #top
    kicad_mod.append(Line(start = [-silks_outline_x_fab + arc_r, -silks_outline_y_fab],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x_fab - arc_r, -silks_outline_y_fab], layer = 'F.Fab'))
    #left
    kicad_mod.append(Line(start = [-silks_outline_x_fab, -silks_outline_y_fab + arc_r],
                          end = [-silks_outline_x_fab, silks_outline_y_fab - arc_r], layer = 'F.Fab'))
    #right
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x_fab, -silks_outline_y_fab + arc_r],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x_fab, silks_outline_y_fab - arc_r], layer = 'F.Fab'))
    #bottom left
    kicad_mod.append(Line(start = [-silks_outline_x_fab + arc_r, silks_outline_y_fab],
                          end = [-silks_outline_x + cut_width, silks_outline_y_fab], layer = 'F.Fab'))
    kicad_mod.append(Line(start = [-silks_outline_x + cut_width, silks_outline_y_fab],
                          end = [-silks_outline_x + cut_width, silks_outline_y - cut_depth], layer = 'F.Fab'))
    #bottom right
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x_fab - arc_r, silks_outline_y_fab],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - cut_width, silks_outline_y_fab], layer = 'F.Fab'))
    kicad_mod.append(Line(start = [(pin_cnt - 1) * pad_span + silks_outline_x - cut_width, silks_outline_y_fab],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - cut_width, silks_outline_y - cut_depth], layer = 'F.Fab'))
    #bottom center
    kicad_mod.append(Line(start = [-silks_outline_x + cut_width, silks_outline_y - cut_depth],
                          end = [(pin_cnt - 1) * pad_span + silks_outline_x - cut_width, silks_outline_y - cut_depth], layer = 'F.Fab'))
    #arc left top
    kicad_mod.append(Arc(center = [-silks_outline_x_fab + arc_r, -silks_outline_y_fab + arc_r],
                         start = [-silks_outline_x_fab, -silks_outline_y_fab + arc_r], angle = 90, layer = 'F.Fab'))
    #arc right top
    kicad_mod.append(Arc(center = [(pin_cnt - 1) * pad_span + silks_outline_x_fab - arc_r, -silks_outline_y_fab + arc_r],
                         start = [(pin_cnt - 1) * pad_span + silks_outline_x_fab - arc_r, -silks_outline_y_fab], angle = 90, layer = 'F.Fab'))
    #arc left bottom
    kicad_mod.append(Arc(center = [-silks_outline_x_fab + arc_r, silks_outline_y_fab - arc_r],
                         start = [-silks_outline_x_fab + arc_r, silks_outline_y_fab], angle = 90, layer = 'F.Fab'))
    #arc right bottom
    kicad_mod.append(Arc(center = [(pin_cnt - 1) * pad_span + silks_outline_x_fab - arc_r, silks_outline_y_fab - arc_r],
                         start = [(pin_cnt - 1) * pad_span + silks_outline_x_fab, silks_outline_y_fab - arc_r], angle = 90, layer = 'F.Fab'))

    kicad_mod.append(Line(start = [0.3, 2.1], end = [0, 1.5], layer = 'F.Fab'))
    kicad_mod.append(Line(start = [0, 1.5], end = [-0.3, 2.1], layer = 'F.Fab'))
    kicad_mod.append(Line(start = [-0.3, 2.1], end = [0.3, 2.1], layer = 'F.Fab'))

    #CREATE COURTYARD
    kicad_mod.append(RectLine(start = [-silks_outline_x - courtyard_outline, -silks_outline_y - courtyard_outline],
                              end = [(pin_cnt - 1) * pad_span + silks_outline_x + courtyard_outline, silks_outline_y + courtyard_outline],
                              layer = 'F.CrtYd'))
    #add 3D model
    kicad_mod.append(Model(filename="${{KISYS3DMOD}}/Connector_Stocko.3dshapes/{}.wrl".format(footprint_name),
                        at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
    #output kicad model
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(output_dir + '/' + footprint_name + '.kicad_mod')