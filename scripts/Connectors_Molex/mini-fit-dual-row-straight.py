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

draw_inner_details = False

series = "Mega-Fit"
series_long = 'Mega-Fit Power Connectors'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 2


#pins_per_row_per_row per row
pins_per_row_range = range(1,13)

#Molex part number
#n = number of circuits per row
variant_params = {
    'peg':{
        'mount_pins': 'plastic_peg',
        'descriptive_name': 'Snap-in Plastic Peg PCB Lock',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/039289068_sd.pdf',
        'part_code': {'mpn':"39-28-9{n:02d}x",'eng_num':"5566-{n:02}A2"},
        },
    'no-peg':{
        'mount_pins': '',
        'descriptive_name': '',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/039281043_sd.pdf',
        'part_code': {'mpn':"39-28-x{n:02d}x",'eng_num':"5566-{n:02}A"},
        }
}

pitch = 4.2
drill = 1.4
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 1.5
max_annular_ring = 0.95
min_annular_ring = 0.15


row = 5.5

pad_size = [pitch - pad_to_pad_clearance, row - pad_to_pad_clearance]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

if pad_size[1] - drill < 2*min_annular_ring:
    pad_size[1] = drill + 2*min_annular_ring
if pad_size[1] - drill > max_annular_ring:
    pad_size[1] = drill + 2*max_annular_ring

pad_shape = Pad.SHAPE_OVAL
if pad_size[0] == pad_size[1]:
    pad_shape = Pad.SHAPE_CIRCLE


def generate_one_footprint(pins_per_row, variant, configuration):
    silk_pad_off = configuration['silk_pad_clearance']+configuration['silk_line_width']/2

    mpn = variant_params[variant]['part_code']['mpn'].format(n=pins_per_row*2)
    old_mpn = variant_params[variant]['part_code']['eng_num'].format(n=pins_per_row*2)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row,
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    descr_format_str = "Molex {:s}, {:s} (old mpn/engineering number: {:s}), {:d} Pins per row, Mounting: {:s} ({:s}), generated with kicad-footprint-generator"
    kicad_mod.setDescription(descr_format_str.format(
        series_long, mpn, old_mpn, pins_per_row,
        variant_params[variant]['descriptive_name'], variant_params[variant]['datasheet']))
    tags = configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation])
    tags += variant_params[variant]['mount_pins']
    kicad_mod.setTags(tags)


    #calculate fp dimensions

    #connector length
    A = pins * pitch + 1.2

    #pin centers
    B = (pins - 1) * pitch

    #plasic pin-lock
    C = A + 4

    #connector width
    W = 9.6

    #corner positions
    x1 = -(A-B)/2
    x2 = x1 + A

    y1 = -(W-row) / 2 - 0.2
    y2 = y1 + W + 0.1

    #tab length
    tab_l = 3.4
    #tab width
    tab_w = 1.4

    # set general values
    footprint.append(Text(type='reference', text='REF**', at=[B/2,10], layer='F.SilkS'))
    footprint.append(Text(type='user', text='%R', at=[B/2,3], layer='F.Fab'))
    footprint.append(Text(type='value', text=fp_name, at=[B/2,-4], layer='F.Fab'))

    #generate the pads
    footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT))
    footprint.append(PadArray(pincount=pins, initial=pins+1, start=[0, row], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT))

    #add PCB locators if needed
    if peg:
        loc = 3.00
        footprint.append(Pad(at=[B/2-C/2, row - 0.46],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))
        footprint.append(Pad(at=[B/2+C/2, row - 0.46],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))

        footprint.append(Circle(center=[B/2-C/2, row-0.46],radius=loc/2+0.25,width=0.12))
        footprint.append(Circle(center=[B/2+C/2, row-0.46],radius=loc/2+0.25,width=0.12))

    #draw the outline of the shape
    footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab',width=0.1))

    #draw the outline of the tab
    footprint.append(PolygoneLine(polygone=[
        {'x': B/2 - tab_l/2,'y': y2},
        {'x': B/2 - tab_l/2,'y': y2 + tab_w},
        {'x': B/2 + tab_l/2,'y': y2 + tab_w},
        {'x': B/2 + tab_l/2,'y': y2},
    ], layer='F.Fab', width=0.1))

    #draw the outline of each pin slot (alternating shapes)
    #slot size
    S = 3.5

    def square_slot(x,y):
        footprint.append(RectLine(start=[x-S/2,y-S/2],end=[x+S/2,y+S/2],layer='F.Fab'))

    def notch_slot(x,y):
        footprint.append(PolygoneLine(polygone=[
        {'x': x-S/2, 'y': y+S/2},
        {'x': x-S/2, 'y': y-S/4},
        {'x': x-S/4, 'y': y-S/2},
        {'x': x+S/4, 'y': y-S/2},
        {'x': x+S/2, 'y': y-S/4},
        {'x': x+S/2, 'y': y+S/2},
        {'x': x-S/2, 'y': y+S/2},
        ], layer='F.Fab', width=0.1))

    q = 1
    notch = True
    for i in range(pins):
        if notch:
            y_square = 0
            y_notch = row
        else:
            y_square = row
            y_notch = 0

        square_slot(i * pitch, y_square)
        notch_slot(i*pitch, y_notch)

        q -= 1

        if (q == 0):
            q = 2
            notch = not notch


    #draw the outline of the connector on the silkscreen
    off = 0.1
    outline = [
    {'x': B/2,'y': y1-off},
    {'x': x1-off,'y': y1-off},
    {'x': x1-off,'y': y2+off},
    {'x': B/2 - tab_l/2 - off,'y': y2+off},
    {'x': B/2 - tab_l/2 - off,'y': y2 + off + tab_w},
    {'x': B/2, 'y': y2 + off + tab_w},
    ]

    footprint.append(PolygoneLine(polygone=outline, width=0.12))
    footprint.append(PolygoneLine(polygone=outline, x_mirror=B/2, width=0.12))

    #pin-1 marker

    L = 2.5
    O = 0.35

    pin = [
        {'x': x1 + L,'y': y1 - O},
        {'x': x1 - O,'y': y1 - O},
        {'x': x1 - O,'y': y1 + L},
    ]

    footprint.append(PolygoneLine(polygone=pin, width=0.12))
    footprint.append(PolygoneLine(polygone=pin, width=0.1, layer='F.Fab'))

    #draw the courtyard
    if peg:
        W = C + 3
    else:
        W = A

    footprint.append(RectLine(start=[B/2-W/2,y1],end=[B/2+W/2,y2 + tab_w], width=0.05, layer='F.CrtYd', offset=0.5, grid=0.05))

    #Add a model
    footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))

    #filename
    filename = output_dir + fp_name + ".kicad_mod"

    file_handler = KicadFileHandler(footprint)
    file_handler.writeFile(filename)
