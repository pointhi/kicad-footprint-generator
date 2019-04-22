#!/usr/bin/env python3

import sys
import os
#sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path


# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "SF"
manufacturer = 'XP_POWER'
#Designed to support SF_IA, SF_IH, SF_ITX, SF_ITQ series, and potentially more

fab_pin1_marker_type = 1
pin1_marker_offset = 0.3
pin1_marker_linelen = 1.25

drill_size = 0.85#0.5 pin diameter, 0.35 pin pitch tolerance
pad_to_pad_clearance = 0.69
pad_copper_y_solder_length = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15

xpitch = 7.62
ypitch = 2.54

def generate_one_footprint(fpid, rows, datasheet, configuration):
    pins = []
    if fpid == "IAxxxxS" and rows == "SIP" :
        casetolerance = 0.5
        casemaxwidth = 6.09
        casemaxlength = 19.30
        x_max = 1.40
        x_min = x_max - (casemaxwidth - casetolerance)
        y_min = -1.53
        y_max = y_min + (casemaxlength - casetolerance)
        pins = [1, 2, 4, 5, 6]
        xpos = [1, 1, 1, 1, 1]
        ypos = [1, 2, 4, 5, 6]
    elif fpid == "IA48xxS" and rows == "SIP" :
        casetolerance = 0.5
        casemaxwidth = 7.20
        casemaxlength = 19.30
        x_max = 1.40
        x_min = x_max - (casemaxwidth - casetolerance)
        y_min = -1.53
        y_max = y_min + (casemaxlength - casetolerance)
        pins = [1, 2, 4, 5, 6]
        xpos = [1, 1, 1, 1, 1]
        ypos = [1, 2, 4, 5, 6]
    elif fpid == "IAxxxxD" and rows == "DIP" :
        casetolerance = 0.5
        casemaxwidth = 10.16
        casemaxlength = 20.32
        x_min = -(casemaxwidth-casetolerance-xpitch)/2
        x_max = x_min + (casemaxwidth - casetolerance)
        y_min = -(casemaxlength-casetolerance-15.24)/2
        y_max = y_min + (casemaxlength - casetolerance)
        pins = [1, 2, 3, 4, 5, 6]
        xpos = [1, 1, 2, 2, 2, 2]
        ypos = [1, 7, 1, 4, 6, 7]
    elif fpid == "IA48xxD" and rows == "DIP" :
        casetolerance = 0.5
        casemaxwidth = 10.16
        casemaxlength = 20.32
        x_min = -(casemaxwidth-casetolerance-xpitch)/2
        x_max = x_min + (casemaxwidth - casetolerance)
        y_min = -(casemaxlength-casetolerance-15.24)/2
        y_max = y_min + (casemaxlength - casetolerance)
        pins = [1, 2, 3, 4, 5, 6]
        xpos = [1, 1, 2, 2, 2, 2]
        ypos = [1, 7, 1, 4, 6, 7]
    elif fpid == "IHxxxxS" and rows == "SIP" :
        casetolerance = 0.5
        casemaxwidth = 7.20
        casemaxlength = 19.5
        x_max = 1.25
        x_min = x_max - (casemaxwidth - casetolerance)
        y_min = -2.29
        y_max = y_min + (casemaxlength - casetolerance)
        pins = [1, 2, 4, 5, 6]
        xpos = [1, 1, 1, 1, 1]
        ypos = [1, 2, 4, 5, 6]
    elif fpid == "IHxxxxSH" and rows == "SIP" :
        casetolerance = 0.5
        casemaxwidth = 7.62
        casemaxlength = 19.5
        x_max = 1.25
        x_min = x_max - (casemaxwidth - casetolerance)
        y_min = -2.29
        y_max = y_min + (casemaxlength - casetolerance)
        pins = [1, 2, 4, 5, 6]
        xpos = [1, 1, 1, 1, 1]
        ypos = [1, 2, 5, 6, 7]
    elif fpid == "IHxxxxD" and rows == "DIP" :
        casetolerance = 0.5
        casemaxwidth = 10.16
        casemaxlength = 20.32
        x_min = -(casemaxwidth-casetolerance-xpitch)/2
        x_max = x_min + (casemaxwidth - casetolerance)
        y_min = -(casemaxlength-casetolerance-15.24)/2
        y_max = y_min + (casemaxlength - casetolerance)
        pins = [1, 2, 3, 4, 5, 6]
        xpos = [1, 1, 2, 2, 2, 2]
        ypos = [1, 7, 1, 4, 6, 7]
    elif fpid == "IHxxxxDH" and rows == "DIP" :
        casetolerance = 0.5
        casemaxwidth = 10.16
        casemaxlength = 20.32
        x_min = -(casemaxwidth-casetolerance-xpitch)/2
        x_max = x_min + (casemaxwidth - casetolerance)
        y_min = -(casemaxlength-casetolerance-15.24)/2
        y_max = y_min + (casemaxlength - casetolerance)
        pins = [1, 2, 3, 4, 5, 6]
        xpos = [1, 1, 2, 2, 2, 2]
        ypos = [1, 7, 1, 5, 7, 6]
    elif fpid == "ITQxxxxS-H" and rows == "SIP" :
        casetolerance = 0.5
        casewidth = 9.20
        caselength = 21.85
        x_max = 3.20
        x_min = x_max - casewidth
        y_min = -(caselength - 17.78)/2
        y_max = y_min + caselength
        pins = [1, 2, 3, 6, 7, 8]
        xpos = [1, 1, 1, 1, 1, 1]
        ypos = [1, 2, 3, 6, 7, 8]
    elif fpid == "ITxxxxxS" and rows == "SIP" :
        casetolerance = 0.5
        casewidth = 9.20
        caselength = 21.85
        x_max = 3.20
        x_min = x_max - casewidth
        y_min = -(caselength - 17.78)/2
        y_max = y_min + caselength
        pins = [1, 2, 3, 6, 7]
        xpos = [1, 1, 1, 1, 1]
        ypos = [1, 2, 3, 6, 7]
    elif fpid == "ITXxxxxSA" and rows == "SIP" :
        casetolerance = 0.5
        casewidth = 9.20
        caselength = 21.85
        x_max = 3.20
        x_min = x_max - casewidth
        y_min = -(caselength - 17.78)/2
        y_max = y_min + caselength
        pins = [1, 2, 6, 7, 8]
        xpos = [1, 1, 1, 1, 1]
        ypos = [1, 2, 6, 7, 8]

    silk_x_min = x_min - configuration['silk_fab_offset']
    silk_x_max = x_max + configuration['silk_fab_offset']
    silk_y_min = y_min - configuration['silk_fab_offset']
    silk_y_max = y_max + configuration['silk_fab_offset']

    footprint_name = "Converter_DCDC_XP_POWER-{:s}_THT".format(fpid)
    ser = ""
    if fpid.startswith("IA_"):
        ser="SF_IA"
    elif fpid.startswith("IH_"):
        ser="SF_IH"
    elif fpid.startswith("ITX_"):
        ser="SF_ITX"
    elif fpid.startswith("ITQ_"):
        ser="SF_ITQ"

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("XP_POWER {:s} {:s}, {:s}, ({:s}), generated with kicad-footprint-generator".format(ser,fpid, rows, datasheet))
    kicad_mod.setTags("XP_POWER {:s} {:s} {:s} DCDC-Converter".format(ser,fpid,rows))

    # create Silkscreen
    kicad_mod.append(RectLine(start=[silk_x_min,silk_y_min], end=[silk_x_max,silk_y_max],
        layer='F.SilkS', width=configuration['silk_line_width']))

    ########################### Pin 1 marker ################################
    poly_pin1_marker = [
        {'x':silk_x_min-pin1_marker_offset+pin1_marker_linelen, 'y':silk_y_min-pin1_marker_offset},
        {'x':silk_x_min-pin1_marker_offset, 'y':silk_y_min-pin1_marker_offset},
        {'x':silk_x_min-pin1_marker_offset, 'y':silk_y_min-pin1_marker_offset+pin1_marker_linelen}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker, layer='F.SilkS', width=configuration['silk_line_width']))
    if fab_pin1_marker_type == 1:
        kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker, layer='F.Fab', width=configuration['fab_line_width']))

    if fab_pin1_marker_type == 2:
        poly_pin1_marker_type2 = [
            {'x':-1, 'y':y_min},
            {'x':0, 'y':y_min+1},
            {'x':1, 'y':y_min}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker_type2, layer='F.Fab', width=configuration['fab_line_width']))

    ########################## Fab Outline ###############################
    kicad_mod.append(RectLine(start=[x_min,y_min], end=[x_max,y_max],
        layer='F.Fab', width=configuration['fab_line_width']))
    ############################# CrtYd ##################################
    part_x_min = x_min
    part_x_max = x_max
    part_y_min = y_min
    part_y_max = y_max

    #Note, we use the connector courtyard clearance of 0.5 mm because the unusually large case tolerance of 0.5mm of XP Powers DC DC converters
    cx1 = roundToBase(part_x_min-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(part_y_min-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(part_x_max+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(part_y_max+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))


    ############################# Pads ##################################
    pad_size = [ypitch - pad_to_pad_clearance, drill_size + 2*pad_copper_y_solder_length]

    if pad_size[0] - drill_size < 2*min_annular_ring:
        pad_size[0] = drill_size + 2*min_annular_ring

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    for i in range(len(pins)):
        pshape = Pad.SHAPE_OVAL
        if pins[i] == 1:
            pshape = Pad.SHAPE_RECT
        kicad_mod.append(Pad(number=pins[i], type=Pad.TYPE_THT, shape=pshape, at=[(xpos[i]-1)*xpitch, (ypos[i]-1)*ypitch], size=pad_size, drill=drill_size, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    ######################### Text Fields ###############################
    text_center_y = 1.5
    body_edge={'left':part_x_min, 'right':part_x_max, 'top':part_y_min, 'bottom':part_y_max}
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position=text_center_y)

    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(series=ser)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)
    print(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='conv_config_KLCv3.yaml')
    parser.add_argument('--kicad4_compatible', action='store_true', help='Create footprints kicad 4 compatible')
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

    configuration['kicad4_compatible'] = args.kicad4_compatible

    generate_one_footprint("IA48xxS"   ,"SIP","https://www.xppower.com/pdfs/SF_IA.pdf", configuration)
    generate_one_footprint("IAxxxxS"   ,"SIP","https://www.xppower.com/pdfs/SF_IA.pdf", configuration)
    generate_one_footprint("IA48xxD"   ,"DIP","https://www.xppower.com/pdfs/SF_IA.pdf", configuration)
    generate_one_footprint("IAxxxxD"   ,"DIP","https://www.xppower.com/pdfs/SF_IA.pdf", configuration)
    generate_one_footprint("IHxxxxS"   ,"SIP","https://www.xppower.com/pdfs/SF_IH.pdf", configuration)
    generate_one_footprint("IHxxxxSH"  ,"SIP","https://www.xppower.com/pdfs/SF_IH.pdf", configuration)
    generate_one_footprint("IHxxxxD"   ,"DIP","https://www.xppower.com/pdfs/SF_IH.pdf", configuration)
    generate_one_footprint("IHxxxxDH"  ,"DIP","https://www.xppower.com/pdfs/SF_IH.pdf", configuration)
    generate_one_footprint("ITQxxxxS-H","SIP","https://www.xppower.com/pdfs/SF_ITQ.pdf", configuration)
    generate_one_footprint("ITxxxxxS"  ,"SIP","https://www.xppower.com/pdfs/SF_ITX.pdf https://www.xppower.com/pdfs/SF_ITQ.pdf", configuration)
    generate_one_footprint("ITXxxxxSA", "SIP","https://www.xppower.com/pdfs/SF_ITX.pdf", configuration)

