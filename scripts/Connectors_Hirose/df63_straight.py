#!/usr/bin/env python

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

"""
footprint specific details to go here

Hirose DF63

URL:
https://www.hirose.com/product/en/products/DF63/

Datasheet:
https://www.hirose.com/product/en/download_file/key_name/DF63/category/Catalog/doc_file_id/51104/?file_category_id=4&item_id=47&is_series=1
"""

import sys
import os
#sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
from math import sqrt
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = ""
series_long = 'DF63 through hole'
manufacturer = 'Hirose'
orientation = 'H'
number_of_rows = 1
datasheet = 'https://www.hirose.com/product/en/products/DF63/'

#pins_per_row per row
pins_per_row_range = [1,2,3,4,5,6]

#Molex part number
#n = number of circuits per row
part_code = "DF63-{n:d}P-3.96DSA"

pitch = 3.96
drill = 1.8

pad_to_pad_clearance = 1.5
max_annular_ring = 0.5
min_annular_ring = 0.15



pad_size = [pitch - pad_to_pad_clearance, drill + 2*max_annular_ring]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

pad_shape=Pad.SHAPE_OVAL
if pad_size[1] == pad_size[0]:
    pad_shape=Pad.SHAPE_CIRCLE



def generate_one_footprint(pins, configuration):
    mpn = part_code.format(n=pins)
    pad_silk_off = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']
    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins,
        pitch=pitch, orientation=orientation_str)

    footprint_name = footprint_name.replace("__",'_')

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pins_per_row, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))



    #vertical center of connector
    y2 = 3.25 + mount_size / 2
    y1 = y2 - 7.05
    yt = y2 - 8

    #Major dimensions
    B = ( pincount - 1 ) * pitch
    A = B + 4.7

    #calculate major dimensions
    x1 = (B - A) / 2
    x2 = x1 + A

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()

    #pins
    fp.append(
        PadArray(
                pincount=pincount,
                initial = 1,
                start = [0, 0],
                x_spacing = pitch,
                type = Pad.TYPE_THT,
                layers = Pad.LAYERS_THT,
                shape = pad_shape,
                size = pad_size,
                drill = drill,
                )
    )

    #mounting hole
    if pincount > 1:
        fp.append(Pad(at=[-1.5,3.25],type=Pad.TYPE_NPTH,layers=Pad.LAYERS_NPTH,shape=Pad.SHAPE_CIRCLE,size=mount_size,drill=mount_size))

    #connector outline

    #tab thickness
    t = 1.2

    def outline(offset=0):
        outline = [
        {'x': B/2, 'y': y2 + offset},
        {'x': x1 - offset, 'y': y2 + offset},
        {'x': x1 - offset, 'y': yt - offset},
        {'x': x1 + t + offset, 'y': yt - offset},
        {'x': x1 + t + offset, 'y': y1 - offset},
        {'x': B/2, 'y': y1 - offset},
        ]

        return outline

    fp.append(PolygoneLine(polygone=outline(),layer='F.Fab'))
    fp.append(PolygoneLine(polygone=outline(),layer='F.Fab',x_mirror=B/2))

    fp.append(PolygoneLine(polygone=outline(offset=0.15)))
    fp.append(PolygoneLine(polygone=outline(offset=0.15),x_mirror=B/2))

    #draw lines between pads on F.Fab
    for i in range(pincount - 1):
        x = (i + 0.5) * pitch

        fp.append(Line(start=[x,y1],end=[x,y2],layer='F.Fab'))

    #pin-1 indicator
    fp.append(Circle(center=[0,-3.75],radius=0.25, width=0.15))
    fp.append(Circle(center=[0,-3.75],radius=0.25, width=0.15,layer='F.Fab'))

    #add a 3D model reference
    fp.append(Model(filename="Connectors_Hirose.3dshapes/" + footprint_name + ".wrl"))

    #filename
    filename = output_dir + footprint_name + ".kicad_mod"

    file_handler = KicadFileHandler(fp)
    file_handler.writeFile(filename)
