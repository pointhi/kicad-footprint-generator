#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools

from footprint_text_fields import addTextFields
import argparse
import yaml
from KicadModTree import *

series = 'M20-890'
series_long = 'Male Horizontal Surface Mount Single Row 2.54mm (0.1 inch) Pitch PCB Connector'
manufacturer = 'Harwin'
pitch = 2.54
datasheet = 'https://cdn.harwin.com/pdfs/M20-890.pdf'
pin_min = 3
pin_max = 20
mpn = 'M20-890{pincount:02g}xx'
padsize = [2.5, 1]

def roundToBase(value, base):
    if base == 0:
        return value
    return round(value/base) * base

def gen_fab_pins(origx, origy, kicad_mod, configuration):
    poly_f_back = [
        {'x': origx+3.8, 'y': origy-0.64/2},
        {'x': origx-0.9, 'y': origy-0.64/2},
        {'x': origx-0.9, 'y': origy+0.64/2},
        {'x': origx+3.8, 'y': origy+0.64/2},
    ]
    poly_f_front = [
        {'x': origx+6.3, 'y': origy-0.64/2},
        {'x': origx+12.3, 'y': origy-0.64/2},
        {'x': origx+12.3, 'y': origy+0.64/2},
        {'x': origx+6.3, 'y': origy+0.64/2},
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_f_back,
        width=configuration['fab_line_width'], layer="F.Fab"))
    kicad_mod.append(PolygoneLine(polygone=poly_f_front,
       width=configuration['fab_line_width'], layer="F.Fab"))

def gen_silk_pins(origx, origy, kicad_mod, configuration, fill):
    poly_s_back1 = [
        {'x': origx+2.5/2+configuration['silk_pad_clearance']+configuration['silk_line_width'], 'y': origy-0.64/2-configuration['silk_line_width']},
        {'x': origx+3.8-configuration['silk_line_width'], 'y': origy-0.64/2-configuration['silk_line_width']},
    ]
    poly_s_back2 = [
        {'x': origx+2.5/2+configuration['silk_pad_clearance']+configuration['silk_line_width'], 'y': origy+0.64/2+configuration['silk_line_width']},
        {'x': origx+3.8-configuration['silk_line_width'], 'y': origy+0.64/2+configuration['silk_line_width']},
    ]
    poly_s_front = [
        {'x': origx+6.3+configuration['silk_line_width'], 'y': origy-0.64/2-configuration['silk_line_width']},
        {'x': origx+12.3+configuration['silk_line_width'], 'y': origy-0.64/2-configuration['silk_line_width']},
        {'x': origx+12.3+configuration['silk_line_width'], 'y': origy+0.64/2+configuration['silk_line_width']},
        {'x': origx+6.3+configuration['silk_line_width'], 'y': origy+0.64/2+configuration['silk_line_width']},
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_s_back1,
        width=configuration['silk_line_width'], layer="F.SilkS"))
    kicad_mod.append(PolygoneLine(polygone=poly_s_back2,
        width=configuration['silk_line_width'], layer="F.SilkS"))
    kicad_mod.append(PolygoneLine(polygone=poly_s_front,
        width=configuration['silk_line_width'], layer="F.SilkS"))
    if fill:
        kicad_mod.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[origx+configuration['silk_line_width']+(6.3+12.3)/2, origy], size=[6, 0.64+configuration['silk_line_width']], layers=["F.SilkS"]))

def gen_footprint(pinnum, manpart, configuration):
    orientation_str = configuration['orientation_options']['H']
    footprint_name = configuration['fp_name_format_string'].format(
        man=manufacturer,
        series='',
        mpn=manpart,
        num_rows=1,
        pins_per_row=pinnum,
        mounting_pad="",
        pitch=pitch,
        orientation=orientation_str)
    footprint_name = footprint_name.replace('__','_')

    print(footprint_name)
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("{manufacturer} {series}, {mpn}{alt_mpn}, {pins_per_row} Pins per row ({datasheet}), generated with kicad-footprint-generator".format(
        manufacturer = manufacturer,
        series = series_long,
        mpn = manpart, 
        alt_mpn = '', 
        pins_per_row = pinnum,
        datasheet = datasheet))
        
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry='horizontal'))

    kicad_mod.setAttribute('smd')
    
    # Pads
    kicad_mod.append(PadArray(start=[-6.775+padsize[0]/2, -(pitch*(pinnum-1))/2], initial=1,
        pincount=pinnum, increment=1,  y_spacing=pitch, size=padsize,
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT, drill=None))

    # Fab
    for y in range(0, pinnum):
        gen_fab_pins(-6.775+padsize[0]/2, -(pitch*(pinnum-1))/2+pitch+(y-1)*2.54, kicad_mod, configuration)
    poly_f_body = [
        {'x': -6.775+padsize[0]/2+3.8, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2+0.4+2.54},
        {'x': -6.775+padsize[0]/2+3.8+0.4, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54},
        {'x': -6.775+padsize[0]/2+6.3, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54},
        {'x': -6.775+padsize[0]/2+6.3, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54*pinnum+2.54},
        {'x': -6.775+padsize[0]/2+3.8, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54*pinnum+2.54},
        {'x': -6.775+padsize[0]/2+3.8, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2+0.4+2.54},
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_f_body,
        width=configuration['fab_line_width'], layer="F.Fab"))

    # SilkS
    silkslw = configuration['silk_line_width']
    s_body = [
        {'x': -6.775+padsize[0]/2+3.8-silkslw, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2-silkslw+2.54},
        {'x': -6.775+padsize[0]/2+6.3+silkslw, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2-silkslw+2.54},
        {'x': -6.775+padsize[0]/2+6.3+silkslw, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54*pinnum+silkslw+2.54},
        {'x': -6.775+padsize[0]/2+3.8-silkslw, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54*pinnum+silkslw+2.54},
        {'x': -6.775+padsize[0]/2+3.8-silkslw, 'y': -(pitch*(pinnum-1))/2-pitch-2.54/2-silkslw+2.54},
    ]
    kicad_mod.append(PolygoneLine(polygone=s_body,
            width=configuration['silk_line_width'], layer="F.SilkS"))
    for y in range(0, pinnum):
        gen_silk_pins(-6.775+padsize[0]/2, -(pitch*(pinnum-1))/2+pitch+(y-1)*2.54, kicad_mod, configuration, y==0)
    s_pin1 = [
        {'x': -6.775+padsize[0]/2-(2.5/2+configuration['silk_pad_clearance']+configuration['silk_line_width']), 'y': -(pitch*(pinnum-1))/2},
        {'x': -6.775+padsize[0]/2-(2.5/2+configuration['silk_pad_clearance']+configuration['silk_line_width']), 'y': -(pitch*(pinnum-1))/2-1/2-configuration['silk_line_width']-configuration['silk_pad_clearance']},
        {'x': -6.775+padsize[0]/2, 'y': -(pitch*(pinnum-1))/2-1/2-configuration['silk_line_width']-configuration['silk_pad_clearance']},
    ]
    kicad_mod.append(PolygoneLine(polygone=s_pin1,
            width=configuration['silk_line_width'], layer="F.SilkS"))
    
    
    # CrtYd
    cy_offset = configuration['courtyard_offset']['connector']
    cy_grid = configuration['courtyard_grid']
    bounding_box={
        'left': -6.775+padsize[0]/2-2.5/2,
        'right': -6.775+padsize[0]/2+12.3,
        'top': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54,
        'bottom': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54*pinnum+2.54,
    }
    cy_top = roundToBase(bounding_box['top'] - cy_offset, cy_grid)
    cy_bottom = roundToBase(bounding_box['bottom'] + cy_offset, cy_grid)
    cy_left = roundToBase(bounding_box['left'] - cy_offset, cy_grid)
    cy_right = roundToBase(bounding_box['right'] + cy_offset, cy_grid)
    poly_cy = [
        {'x': cy_left, 'y': cy_top},
        {'x': cy_right, 'y': cy_top},
        {'x': cy_right, 'y': cy_bottom},
        {'x': cy_left, 'y': cy_bottom},
        {'x': cy_left, 'y': cy_top},
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_cy,
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    # Text Fields
    body_edge={
        'left': -6.775+padsize[0]/2+3.8,
        'right': -6.775+padsize[0]/2+6.3,
        'top': -(pitch*(pinnum-1))/2-pitch-2.54/2-silkslw+2.54,
        'bottom': -(pitch*(pinnum-1))/2-pitch-2.54/2+2.54*pinnum+silkslw+2.54,
    }
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy_top, 'bottom':cy_bottom}, fp_name=footprint_name, text_y_inside_position='center', allow_rotation=True)

    # 3D model
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')
    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))
    
    # Output
    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

def gen_family(configuration):
    for x in range(pin_min, pin_max+1):
        gen_footprint(x, mpn.format(pincount=x), configuration)

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

	gen_family(configuration)