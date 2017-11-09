#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

#import argparse
sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from helpers import *
from KicadModTree import *
from math import sqrt

series = "SHL"
orientation = 'Horizontal'
number_of_rows = 1
datasheet = 'http://www.jst-mfg.com/product/pdf/eng/eSHL.pdf'

# http://www.jst-mfg.com/product/pdf/eng/eSHL.pdf

#pincount = int(args.pincount[0])

def generate_one_footprint(pincount, configuration):
    pad_edge_silk_center_offset = configuration['silk_pad_clearence'] + configuration['silk_line_width']/2

    pad_spacing = 1
    start_pos_x = -(pincount-1)*pad_spacing/2
    end_pos_x = (pincount-1)*pad_spacing/2

    pad_y_outside_distance = 4.6
    body_edge_to_mount_pad_edge = 0.7
    pad_size = [0.6, pad_y_outside_distance - 3.35]
    pad_y = -pad_y_outside_distance/2 + pad_size[1]/2


    A = (pincount - 1) * pad_spacing
    B = A + 3.8
    b_size_y = 4.3

    mounting_pad_size = [0.9, 1.7]
    mpad_x = -(A/2) - 1 - (mounting_pad_size[0]/2)
    mpad_y = pad_y_outside_distance/2 - mounting_pad_size[1]/2

    # body outline coordinates
    oyb = pad_y_outside_distance/2 + body_edge_to_mount_pad_edge
    oyt = oyb - b_size_y
    oxl = -B/2
    oxr = B/2

    jst_name = "SM{pincount:02}B-SHLS-TF".format(pincount=pincount)

    # SMT type shrouded header, Side entry type (normal type)
    footprint_name = configuration['fp_name_format_string'].format(series=series, mpn=jst_name, num_rows=number_of_rows,
        pins_per_row=pincount, pitch=pad_spacing, orientation=orientation)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("JST SHL series connector, {:s} ({:s})".format(jst_name, datasheet))
    kicad_mod.setAttribute('smd')
    kicad_mod.setTags('connector jst SHL SMT side')

    #create outline
    # create Courtyard
    # output kicad model

    #create pads
    createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, pad_size, pad_y)

    #add mounting pads (no number)

    kicad_mod.append(Pad(number='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
        at={'x':mpad_x, 'y':mpad_y}, size=mounting_pad_size, layers=Pad.LAYERS_SMT))
    kicad_mod.append(Pad(number='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
        at={'x':-mpad_x, 'y':mpad_y}, size=mounting_pad_size, layers=Pad.LAYERS_SMT))

    #add bottom line
    silk_x = -B/2 - configuration['silk_fab_offset']
    silk_y_b = oyb + configuration['silk_fab_offset']
    silk_mp_y_b = mpad_y + mounting_pad_size[1]/2 + pad_edge_silk_center_offset
    silk_mp_y_t = mpad_y - mounting_pad_size[1]/2 - pad_edge_silk_center_offset
    silk_y_t = oyt - configuration['silk_fab_offset']
    kicad_mod.append(PolygoneLine(polygone=[{'x':silk_x, 'y': silk_mp_y_b},
         {'x':silk_x, 'y':silk_y_b},
         {'x':-silk_x, 'y':silk_y_b},
         {'x':-silk_x, 'y':silk_mp_y_b}],
         layer="F.SilkS", width=configuration['silk_line_width']))

    #add left line (including pin 1 mark)
    kicad_mod.append(PolygoneLine(polygone=[{'x':silk_x,'y':silk_mp_y_t},
        {'x':silk_x,'y':silk_y_t},
        {'x':-A/2-pad_size[0]/2-pad_edge_silk_center_offset,'y':silk_y_t},
        {'x':-A/2-pad_size[0]/2-pad_edge_silk_center_offset,'y':pad_y - pad_size[1]/2}],
        layer="F.SilkS", width=configuration['silk_line_width']))

    #add right line
    kicad_mod.append(PolygoneLine(polygone=[{'x':-silk_x,'y':silk_mp_y_t},
        {'x':-silk_x,'y':silk_y_t},
        {'x':A/2+pad_size[1]/2+pad_edge_silk_center_offset,'y':silk_y_t}],
        layer="F.SilkS", width=configuration['silk_line_width']))

    #add fabrication layer details
    kicad_mod.append(RectLine(start={'x':oxl,'y':oyt}, end={'x':oxr,'y':oyb},
        layer='F.Fab', width=configuration['fab_line_width']))

    #add designator for pin #1
    kicad_mod.append(PolygoneLine(polygone=[{'x': -A/2 - 0.5,'y': oyt},
                               {'x': -A/2,'y': oyt + 1/sqrt(2)},
                               {'x': -A/2 + 0.5,'y': oyt}],
                                layer='F.Fab', width=configuration['fab_line_width']))

    #add courtyard

    #courtyard corners
    cx1 = mpad_x - mounting_pad_size[0]/2 - configuration['courtyard_distance']
    cx2 = -mpad_x + mounting_pad_size[0]/2 + configuration['courtyard_distance']

    cy1 = pad_y - pad_size[1]/2 - configuration['courtyard_distance']
    cy2 = oyb + configuration['courtyard_distance']

    #make sure they lie on an 0.05mm grid

    cx1 = roundToBase(cx1, configuration['courtyard_grid'])
    cx2 = roundToBase(cx2, configuration['courtyard_grid'])

    cy1 = roundToBase(cy1, configuration['courtyard_grid'])
    cy2 = roundToBase(cy2, configuration['courtyard_grid'])

    kicad_mod.append(RectLine(start={'x':cx1,'y':cy1}, end={'x':cx2,'y':cy2},
        layer='F.CrtYd',width=configuration['courtyard_line_width']))

    center = [0,0.5]

    reference_fields = configuration['references']
    kicad_mod.append(Text(type='reference', text='REF**',
        **getTextFieldDetails(reference_fields[0], cy1, cy2, center)))

    for additional_ref in reference_fields[1:]:
        kicad_mod.append(Text(type='user', text='%R',
        **getTextFieldDetails(additional_ref, cy1, cy2, center)))

    value_fields = configuration['values']
    kicad_mod.append(Text(type='value', text=footprint_name,
        **getTextFieldDetails(value_fields[0], cy1, cy2, center)))

    for additional_value in value_fields[1:]:
        kicad_mod.append(Text(type='user', text='%V',
            **getTextFieldDetails(additional_value, cy1, cy2, center)))

    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}')

    lib_name = configuration['lib_name_format_string'].format(series=series)
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
    parser.add_argument('-c', '--config', type=str, nargs='?', help='the config file defining how the footprint will look like.', default='config_KLCv3.0.yaml')
    args = parser.parse_args()

    with open(args.config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    for pincount in [2,5,6,7,8,10,11,12,14,16,20,22,26,30]:
        generate_one_footprint(pincount, configuration)
