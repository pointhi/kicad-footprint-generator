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
#sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
from math import sqrt
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "Picoflex"
series_long = 'Picoflex Ribbon-Cable Connectors'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 2
datasheet = 'http://www.molex.com/pdm_docs/sd/908140004_sd.pdf'

#pins_per_row per row
pins_range = (4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26)

#Molex part number
#n = number of circuits per row
part_code = "90814-00{n:02}"

pitch = 1.27
pitch_row = 2.54

def generate_one_footprint(pins, configuration):
    mpn = part_code.format(n=pins)

    CrtYd_off = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']
    body_edge = {}
    bounding_box = {}

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins//2, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Pins ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pins, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    kicad_mod.setAttribute('smd')

    #
    # Draw all graphical objects
    #
    BodyWidth = 4.1
    BodyHeight = ((pins - 1) * pitch) + (2 * 2.525)
    #
    HalfBodyWidth = BodyWidth / 2
    HalfBodyHeight = BodyHeight / 2

    PadWidth = 2
    PadHeight = 1.2
	#
    AllPadsWidth = 6
    AllPadsHeight = ((pins - 1) * pitch)
    #
    HalfAllPadsWidth = AllPadsWidth / 2
    HalfAllPadsHeight = AllPadsHeight / 2

    GuideHoleDrillSize = 1.9

    GuideHoleX1 = 1.1 - HalfAllPadsWidth
    GuideHoleY1 = -1.925 - HalfAllPadsHeight

    GuideHoleX1 = 1.1 - HalfAllPadsWidth
    GuideHoleY2 = 1.925 + HalfAllPadsHeight

    KeepOutAreaWidth = 7.9
    KeepOutAreaHeight = BodyHeight

    body_edge['right'] = HalfBodyWidth
    body_edge['left'] = -HalfBodyWidth
    body_edge['top'] = -HalfBodyHeight
    body_edge['bottom'] = HalfBodyHeight

    bounding_box['right'] = HalfAllPadsWidth + PadWidth/2
    bounding_box['left'] = -bounding_box['right']
    bounding_box['bottom'] = GuideHoleY2 + GuideHoleDrillSize/2 + 0.175
    bounding_box['top'] = -bounding_box['bottom']
    #
    # Generate the pads
    #
    tpc = int(pins / 2)
    kicad_mod.append(PadArray(
        start=[round(0 - HalfAllPadsWidth, 2), round(0 - HalfAllPadsHeight, 2)],
        pincount=tpc, initial=1, increment=2, x_spacing=0, y_spacing=2*pitch,
        size=[PadWidth, PadHeight], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
        layers=Pad.LAYERS_SMT))
    kicad_mod.append(PadArray(
        start=[round(HalfAllPadsWidth, 2), round(pitch - HalfAllPadsHeight, 2)],
        pincount=tpc, initial=2, increment=2, x_spacing=0,  y_spacing=2*pitch,
        size=[PadWidth, PadHeight], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
        layers=Pad.LAYERS_SMT))

    #
    # Generate the drill holes
    #
    kicad_mod.append(Pad(at=[GuideHoleX1, GuideHoleY1],type=Pad.TYPE_NPTH,
        shape=Pad.SHAPE_CIRCLE, size=GuideHoleDrillSize,
        drill=GuideHoleDrillSize, layers=Pad.LAYERS_NPTH))
    kicad_mod.append(Pad(at=[GuideHoleX1, GuideHoleY2],type=Pad.TYPE_NPTH,
        shape=Pad.SHAPE_CIRCLE, size=GuideHoleDrillSize,
        drill=GuideHoleDrillSize, layers=Pad.LAYERS_NPTH))

    #
    # Add the Fab line
    #
    # Start in upper right corner
    x1 = HalfBodyWidth
    y1 = 0 - HalfBodyHeight
    x2 = x1
    y2 = y1 + BodyHeight
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.Fab', width=configuration['fab_line_width']))
    #
    # Bottom line to bottom drill hole
    x1 = x2
    y1 = y2
    x2 = GuideHoleX1 + (GuideHoleDrillSize / 2)
    y2 = y2
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.Fab', width=configuration['fab_line_width']))
    # Arc around bottom drill hole
    ccx = GuideHoleX1
    ccy = GuideHoleY2
    csx = x2
    csy = HalfAllPadsHeight + 2.525
    kicad_mod.append(Arc(
        center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)],
        angle=230.0, layer='F.Fab', width=configuration['fab_line_width']))
    # Left line from bottom drill hole to top drill hole including the Fab Pin 1 marker
    x1 = -HalfBodyWidth
    y1 = GuideHoleY2 - (GuideHoleDrillSize / 2) - 0.17
    x2 = x1
    y2 = 0 - (HalfAllPadsHeight - (PadHeight / 2))
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.Fab', width=configuration['fab_line_width']))
    x1 = x2
    y1 = y2
    x2 = x1 + (PadHeight / 2)
    y2 = y2 - (PadHeight / 2)
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.Fab', width=configuration['fab_line_width']))
    x1 = x2
    y1 = y2
    x2 = x1 - (PadHeight / 2)
    y2 = y2 - (PadHeight / 2)
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.Fab', width=configuration['fab_line_width']))
    x1 = x2
    y1 = y2
    x2 = x1
    y2 = GuideHoleY1 + (GuideHoleDrillSize / 2) + 0.17
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.Fab', width=configuration['fab_line_width']))

    # Arc around top drill hole
    ccx = GuideHoleX1
    ccy = GuideHoleY1
    csx = x1
    csy = y2
    kicad_mod.append(Arc(
        center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)],
        angle=230.0, layer='F.Fab', width=configuration['fab_line_width']))
    # Top line to top drill hole
    x1 = HalfBodyWidth
    y1 = 0 - HalfBodyHeight
    x2 = GuideHoleX1 + (GuideHoleDrillSize / 2) + 0.02
    y2 = y1
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.Fab', width=configuration['fab_line_width']))

    #
    # Add the Silk line
    #
    # Start in upper right corner
    x1 = HalfBodyWidth + 0.13
    y1 = 0 - HalfBodyHeight - 0.13
    x2 = x1
    y2 = 0 - ((HalfAllPadsHeight - pitch) + (PadHeight / 2) + 0.3)
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    y1 = 0 - ((HalfAllPadsHeight - pitch) - (PadHeight / 2) - 0.4)
    y2 = 0 - ((HalfAllPadsHeight - (3 *pitch)) + (PadHeight / 2) + 0.4)
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    if (pins > 3):
        for halfpins in range(int((pins / 2)) - 2):
            y1 = y1 + (2 * pitch)
            y2 = y2 + (2 * pitch)
            kicad_mod.append(PolygoneLine(
                polygone=[[round(x1, 2), round(y1 + 0.06, 2)],
                    [round(x2, 2), round(y2 - 0.06, 2)]],
                layer='F.SilkS', width=configuration['silk_line_width']))

    x1 = x1
    y1 = HalfAllPadsHeight + (PadHeight / 2) + 0.3
    x2 = HalfBodyWidth + 0.13
    y2 = HalfBodyHeight + 0.13
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    #
    # Bottom line to bottom drill hole
    x1 = x2
    y1 = y2
    x2 = GuideHoleX1 + (GuideHoleDrillSize / 2) + 0.1
    y2 = y2
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    # Arc around bottom drill hole
    ccx = GuideHoleX1
    ccy = GuideHoleY2
    csx = x2
    csy = y2
    kicad_mod.append(Arc(
        center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)],
        angle=222.8, layer='F.SilkS', width=configuration['silk_line_width']))
    # Left line from bottom drill hole to top drill hole
    x1 = -HalfBodyWidth - 0.13
    y1 = GuideHoleY2 - (GuideHoleDrillSize / 2) - 0.3
    x2 = x1
    y2 = y1 - 0.5
    y2 = HalfAllPadsHeight - pitch + (PadHeight / 2) + 0.3
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    y1 = ((HalfAllPadsHeight - pitch) - (PadHeight / 2) - 0.4)
    y2 = ((HalfAllPadsHeight - (3 *pitch)) + (PadHeight / 2) + 0.4)
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    # Add small lines between pads
    if (pins > 3):
        for halfpins in range(int((pins / 2)) - 2):
            y1 = y1 - (2 * pitch)
            y2 = y2 - (2 * pitch)
            kicad_mod.append(PolygoneLine(
                polygone=[[round(x1, 2), round(y1 + 0.06, 2)],
                    [round(x2, 2), round(y2 - 0.06, 2)]],
                layer='F.SilkS', width=configuration['silk_line_width']))


    # Arc around top drill hole
    y2 = GuideHoleY1 + (GuideHoleDrillSize / 2) + 0.3
    ccx = GuideHoleX1
    ccy = GuideHoleY1
    csx = x1 - 0.63
    csy = y2 -0.35
    #
    # xxx, yyy is the new pin 1 marker
    #
    xxx1 = csx
    yyy1 = csy
    xxx2 = xxx1
    yyy2 = 0 - (HalfAllPadsHeight + (PadHeight / 2) + 0.3)
    kicad_mod.append(PolygoneLine(
        polygone=[[round(xxx1, 2), round(yyy1, 2)], [round(xxx2, 2), round(yyy2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    xxx1 = xxx2
    yyy1 = yyy2
    xxx2 = 0 - (HalfAllPadsWidth + (PadWidth / 2))
    yyy2 = yyy1
    kicad_mod.append(PolygoneLine(
        polygone=[[round(xxx1, 2), round(yyy1, 2)], [round(xxx2, 2), round(yyy2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    #
    kicad_mod.append(Arc(
        center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)],
        angle=191.0, layer='F.SilkS', width=configuration['silk_line_width']))
    # Top line to top drill hole
    x1 = HalfBodyWidth + 0.13
    y1 = 0 - HalfBodyHeight - 0.13
    x2 = GuideHoleX1 + (GuideHoleDrillSize / 2) + 0.13
    y2 = y1
    kicad_mod.append(PolygoneLine(
        polygone=[[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
        layer='F.SilkS', width=configuration['silk_line_width']))

    #
    # Add the pin 1 marker
    #
    # Start in upper right corner
#        x1 = 0 - (HalfAllPadsWidth + (PadWidth / 2) + 0.25 + 0.25)
#        y1 = 0 - HalfAllPadsHeight - 1
#        x2 = x1
#        y2 = round(y1 + 3, 0)
#        kicad_mod.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS', width=configuration['silk_line_width']))

    #
    # Add the keep out area
    #
    x1 = 0 - (KeepOutAreaWidth / 2)
    y1 = 0 - (KeepOutAreaHeight / 2)
    x2 = x1 + KeepOutAreaWidth
    y2 = y1 + KeepOutAreaHeight
    kicad_mod.append(RectLine(start=[round(x1, 2), round(y1, 2)],
        end=[round(x2, 2), round(y2, 2)], layer='Dwgs.User', width=0.1))
    kicad_mod.append(Text(type='user', text='KEEPOUT',
        at=[0,0], rotation=90,
        layer='Cmts.User'))
    x1 = 0 - (KeepOutAreaWidth / 2)
    y1 = 0 - (KeepOutAreaHeight / 2)
    x2 = 0 - (KeepOutAreaWidth / 2)
    y2 = 0 - (KeepOutAreaHeight / 2)
    GridDelta = 2 * pitch
    dx1 = 0
    dy1 = GridDelta
    yy1 = y1;
    while (x1 < (KeepOutAreaWidth / 2)):
        y1 = y1 + GridDelta
        yy1 = yy1 + dy1
        if (y1 > ((KeepOutAreaHeight / 2))):
            yy1 = (KeepOutAreaHeight / 2)
            dy1 = 0
            dx1 = y1 - (KeepOutAreaHeight / 2)
            x1 = (0 - (KeepOutAreaWidth / 2)) + dx1
        x2 = x2 + GridDelta
        if (x2 >= ((KeepOutAreaWidth / 2))):
            x2 = (KeepOutAreaWidth / 2)
            y2 = y1 - KeepOutAreaWidth
        if (x1 < (KeepOutAreaWidth / 2)):
            kicad_mod.append(PolygoneLine(
                polygone=[[round(x1, 2), round(yy1, 2)],
                    [round(x2, 2), round(y2, 2)]],
                layer='Dwgs.User',width=0.1))

    ########################### CrtYd #################################
    cx1 = roundToBase(bounding_box['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(bounding_box['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(bounding_box['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box['bottom'] + configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2},
        fp_name=footprint_name, text_y_inside_position='left')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../conn_config_KLCv3.yaml')
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.safe_load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    for pins in pins_range:
        generate_one_footprint(pins, configuration)
