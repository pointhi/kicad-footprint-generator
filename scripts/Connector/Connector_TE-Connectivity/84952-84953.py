#!/usr/bin/env python

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

"""

This family of parts is spread over 2 datasheets, depending on the contact side:

Bottom contact:
http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=84952&DocType=Customer+Drawing&DocLang=English&DocFormat=pdf&PartCntxt=1-84952-5

Top contact:
http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=84953&DocType=Customer+Drawing&DocLang=English&DocFormat=pdf&PartCntxt=1-84953-5

"""

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

partnumbers = ["84952","84953"]
pincounts = range(4, 31)

def generate_one_footprint(partnumber, pincount, configuration):
    # only double digit pincount parts have leading chars on the PN
    if pincount >= 10:
        pn_prefix = str(pincount)[0] + "-"
    else:
        pn_prefix = ""

    footprint_name = 'TE_{pnp}{pn:s}-{pns}_1x{pc:02g}_P1.0mm_Horizontal'.format(pnp=pn_prefix, pn=partnumber, pns=str(pincount)[-1], pc=pincount)

    print('Building {:s}'.format(footprint_name))

    # calculate working values
    pitch = 1
    pad_y = -1.8
    pad_width = 0.61
    pad_height = 2
    pad_x_span = pitch * (pincount - 1)
    pad1_x = pad_x_span / 2.0

    tab_width = 4.33 - 1.65
    tab_height = 3.6
    tab_x = pad_x_span / 2.0 + 1.65 + tab_width / 2.0
    tab_y = pad_y + pad_height / 2.0 + tab_height / 2.0

    body_y1 = pad_y + pad_height / 2.0
    half_body_width = pad_x_span / 2.0 + 3.435
    actuator_y1 = body_y1 + 5.4
    actuator_y2 = body_y1 + 7.3
    half_actuator_width = pad_x_span / 2.0 + 4.46
    ear_height = 0.89

    silk_clearance = 0.36
    marker_y = 1.8
    nudge = 0.12

    courtyard_precision = 0.01
    courtyard_clearance = 0.5
    courtyard_x = round_to(half_actuator_width + courtyard_clearance, courtyard_precision)
    courtyard_y1 = round_to(pad_y - pad_height / 2.0 - courtyard_clearance, courtyard_precision)
    courtyard_y2 = round_to(actuator_y2 + courtyard_clearance, courtyard_precision)

    label_y_offset = 0.7

    # select correct datasheet URL depending on part number
    if partnumber == "84952":
        datasheet = "http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=84952&DocType=Customer+Drawing&DocLang=English&DocFormat=pdf&PartCntxt=84952-4"
        side = "bottom"
    elif partnumber == "84953":
        datasheet = "http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=84953&DocType=Customer+Drawing&DocLang=English&DocFormat=pdf&PartCntxt=84953-4"
        side = "top"

    # initialise footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription('TE FPC connector, {pc:02g} {side}-side contacts, 1.0mm pitch, 1.0mm height, SMT, {ds}'.format(pc=pincount, side=side, ds=datasheet))
    kicad_mod.setTags('te fpc {:s}'.format(partnumber))
    kicad_mod.setAttribute('smd')

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', size=[1,1], at=[0, courtyard_y1 - label_y_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='%R', size=[1,1], at=[0, tab_y], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[0, courtyard_y2 + label_y_offset], layer='F.Fab'))

    # create pads
    kicad_mod.append(PadArray(pincount=pincount, x_spacing=pitch, center=[0,pad_y], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height], layers=Pad.LAYERS_SMT))

    # create tab (smt mounting) pads
    kicad_mod.append(Pad(at=[-tab_x, tab_y], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[tab_width, tab_height], layers=Pad.LAYERS_SMT))
    kicad_mod.append(Pad(at=[tab_x, tab_y], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[tab_width, tab_height], layers=Pad.LAYERS_SMT))

    # create fab outline and pin 1 marker
    kicad_mod.append(PolygoneLine(polygone=[[-half_body_width, body_y1],[half_body_width, body_y1],[half_body_width, actuator_y1-ear_height],\
            [half_actuator_width, actuator_y1-ear_height],[half_actuator_width, actuator_y1],[-half_actuator_width, actuator_y1],\
            [-half_actuator_width, actuator_y1-ear_height],[-half_body_width, actuator_y1-ear_height],[-half_body_width, body_y1]], layer='F.Fab'))
    kicad_mod.append(PolygoneLine(polygone=[[-pad1_x-0.5, body_y1],[-pad1_x, body_y1+1],[-pad1_x+0.5, body_y1]], layer='F.Fab'))

    # create open actuator outline
    kicad_mod.append(PolygoneLine(polygone=[[half_body_width, actuator_y1],[half_body_width, actuator_y2-ear_height],\
            [half_actuator_width, actuator_y2-ear_height],[half_actuator_width, actuator_y2],[-half_actuator_width, actuator_y2],\
            [-half_actuator_width, actuator_y2-ear_height],[-half_body_width, actuator_y2-ear_height],[-half_body_width, actuator_y1]], layer='F.Fab', width=0.1))

    # create silkscreen outline and pin 1 marker
    kicad_mod.append(PolygoneLine(polygone=[[half_body_width+nudge, tab_y+tab_height/2.0+silk_clearance],[half_body_width+nudge, actuator_y1-ear_height-nudge],\
            [half_actuator_width+nudge, actuator_y1-ear_height-nudge],[half_actuator_width+nudge, actuator_y1+nudge],[-half_actuator_width-nudge, actuator_y1+nudge],\
            [-half_actuator_width-nudge, actuator_y1-ear_height-nudge],[-half_body_width-nudge, actuator_y1-ear_height-nudge],\
            [-half_body_width-nudge, tab_y+tab_height/2.0+silk_clearance]], layer='F.SilkS'))
    kicad_mod.append(PolygoneLine(polygone=[[-tab_x+tab_width/2.0+silk_clearance, body_y1-nudge],[-pad1_x-pad_width/2.0-silk_clearance, body_y1-nudge],\
            [-pad1_x-pad_width/2.0-silk_clearance, body_y1-nudge-marker_y]], layer='F.SilkS'))
    kicad_mod.append(Line(start=[pad1_x+pad_width/2.0+silk_clearance, body_y1-nudge], end=[tab_x-tab_width/2.0-silk_clearance, body_y1-nudge], layer='F.SilkS'))

    # create courtyard
    kicad_mod.append(RectLine(start=[-courtyard_x, courtyard_y1], end=[courtyard_x, courtyard_y2], layer='F.CrtYd'))

    # add model
    kicad_mod.append(Model(filename="${{KISYS3DMOD}}/Connectors_TE-Connectivity.3dshapes/{:s}.wrl".format(footprint_name), at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    # print render tree
    if args.verbose:
        print(kicad_mod.getRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{:s}.kicad_mod'.format(footprint_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../conn_config_KLCv3.yaml')
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    # with pincount(s) and partnumber(s) to be generated, build them all in a nested loop
    for partnumber in partnumbers:
        for pincount in pincounts:
            generate_one_footprint(partnumber, pincount, configuration)
