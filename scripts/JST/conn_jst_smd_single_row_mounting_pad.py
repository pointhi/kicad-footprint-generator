#!/usr/bin/env python
# Generator for jst smd connectors (single row with two mounting pads)

import sys
import os

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from helpers import *
from KicadModTree import *
from math import sqrt

def generate_one_footprint(pincount, series_definition, configuration):
    has_fin = 'body_fin_protrusion' in series_definition and 'body_fin_width' in series_definition
    jst_name = series_definition['mpn_format_string'].format(pincount=pincount)

    pad_size = [series_definition['pad_size_x'],
        series_definition['rel_pad_y_outside_edge'] - series_definition['rel_pad_y_inside_edge']]
    pad_pos_y = -series_definition['rel_pad_y_outside_edge']/2 + pad_size[1]/2

    mounting_pad_size = series_definition['mounting_pad_size']
    mount_pad_y_pos = series_definition['rel_pad_y_outside_edge']/2 - mounting_pad_size[1]/2
    mount_pad_center_x_to_pin = series_definition['center_pad_to_mounting_pad_edge'] + mounting_pad_size[0]/2.0

    # center pin 1 to center pin n
    dimension_A = (pincount-1)*series_definition['pitch']

    body_edge = {}
    if series_definition['pad1_position'] == 'bottom-left':
        pad_pos_y *= -1
        mount_pad_y_pos *= -1
        mount_pad_edge_y_outside = mount_pad_y_pos - mounting_pad_size[1]/2
        body_edge['top'] = mount_pad_edge_y_outside - series_definition['rel_body_edge_y']
        body_edge['bottom'] = body_edge['top'] + series_definition['body_size_y']
    else:
        mount_pad_edge_y_outside = mount_pad_y_pos + mounting_pad_size[1]/2
        body_edge['bottom'] = mount_pad_edge_y_outside + series_definition['rel_body_edge_y']
        body_edge['top'] = body_edge['bottom'] - series_definition['body_size_y']

    body_edge['right'] = dimension_A/2 + series_definition['rel_body_edge_x']
    body_edge['left'] = -body_edge['right']

    orientation = configuration['orientation_options'][series_definition['orientation']]
    footprint_name = configuration['fp_name_format_string'].format(series=series_definition['series'],
        mpn=jst_name, num_rows=1, pins_per_row=pincount,
        pitch=series_definition['pitch'], orientation=orientation)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("JST {:s} series connector, {:s} ({:s})".format(series_definition['series'],
        jst_name, series_definition['datasheet']))
    kicad_mod.setAttribute('smd')
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series_definition['series'],
        orientation=orientation,
        entry=configuration['entry_direction'][series_definition['orientation']]))


    ############################# Pads ##################################
    kicad_mod.append(PadArray(center=[0, pad_pos_y], x_spacing=series_definition['pitch'], pincount=pincount,
        size=pad_size, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))

    mount_pad_left_x_pos = -dimension_A/2 - mount_pad_center_x_to_pin
    kicad_mod.append(Pad(number ='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[mount_pad_left_x_pos, mount_pad_y_pos],
                        size=mounting_pad_size,
                        layers=Pad.LAYERS_SMT))
    kicad_mod.append(Pad(number ='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[-mount_pad_left_x_pos, mount_pad_y_pos],
                        size=mounting_pad_size,
                        layers=Pad.LAYERS_SMT))

    ############################# CrtYd ##################################
    mp_left_edge = mount_pad_left_x_pos - mounting_pad_size[0]/2
    bounding_box_x1 = body_edge['left'] if body_edge['left'] < mp_left_edge else mp_left_edge
    bounding_box_x2 = -bounding_box_x1
    if series_definition['pad1_position'] == 'bottom-left':
        mp_top_edge = mount_pad_y_pos - mounting_pad_size[1]/2
        mp_bottom_edge = mp_top_edge + mounting_pad_size[1]
        bounding_box_y1 = body_edge['top'] if body_edge['top'] < mp_top_edge else mp_top_edge
        bounding_box_y2 = pad_pos_y + pad_size[1]/2
        if has_fin:
            fin_y_outside_edge = body_edge['bottom'] + series_definition['body_fin_protrusion']
            if fin_y_outside_edge > bounding_box_y2:
                bounding_box_y2 = fin_y_outside_edge
    else:
        mp_bottom_edge = mount_pad_y_pos + mounting_pad_size[1]/2
        mp_top_edge = mp_bottom_edge - mounting_pad_size[1]
        bounding_box_y1 = pad_pos_y - pad_size[1]/2
        bounding_box_y2 = body_edge['bottom'] if body_edge['bottom'] > mp_bottom_edge else mp_bottom_edge
        if has_fin:
            fin_y_outside_edge = body_edge['top'] - series_definition['body_fin_protrusion']
            if fin_y_outside_edge < bounding_box_y1:
                bounding_box_y1 = fin_y_outside_edge



    cx1 = roundToBase(bounding_box_x1 - configuration['courtyard_distance'], configuration['courtyard_grid'])
    cx2 = roundToBase(bounding_box_x2 + configuration['courtyard_distance'], configuration['courtyard_grid'])

    cy1 = roundToBase(bounding_box_y1 - configuration['courtyard_distance'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box_y2 + configuration['courtyard_distance'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Body outline ###############################
    pad_edge_silk_center_offset = configuration['silk_pad_clearence'] + configuration['silk_line_width']/2
    pad_1_x_outside_edge = -dimension_A/2 - pad_size[0]/2

    if has_fin:
        fin_x_inside_edge = {}
        fin_x_inside_edge['left'] = body_edge['left'] + series_definition['body_fin_width']
        fin_x_inside_edge['right'] = -fin_x_inside_edge['left']
        if series_definition['pad1_position'] == 'bottom-left':
            poly_outline = [
                {'x': body_edge['left'], 'y': body_edge['top']},
                {'x': body_edge['right'], 'y': body_edge['top']},
                {'x': body_edge['right'], 'y': fin_y_outside_edge},
                {'x': fin_x_inside_edge['right'], 'y': fin_y_outside_edge},
                {'x': fin_x_inside_edge['right'], 'y': body_edge['bottom']},
                {'x': fin_x_inside_edge['left'], 'y': body_edge['bottom']},
                {'x': fin_x_inside_edge['left'], 'y': fin_y_outside_edge},
                {'x': body_edge['left'], 'y': fin_y_outside_edge},
                {'x': body_edge['left'], 'y': body_edge['top']}
            ]
            poly_silk_edge_left = [
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': mp_bottom_edge + pad_edge_silk_center_offset},
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': fin_y_outside_edge + configuration['silk_fab_offset']},
                {'x': fin_x_inside_edge['left'] + configuration['silk_fab_offset'], 'y': fin_y_outside_edge + configuration['silk_fab_offset']},
                {'x': fin_x_inside_edge['left'] + configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': pad_pos_y + pad_size[1]/2}
            ]
            poly_silk_edge_right = [
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': mp_bottom_edge + pad_edge_silk_center_offset},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': fin_y_outside_edge + configuration['silk_fab_offset']},
                {'x': fin_x_inside_edge['right'] - configuration['silk_fab_offset'], 'y': fin_y_outside_edge + configuration['silk_fab_offset']},
                {'x': fin_x_inside_edge['right'] - configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': -pad_1_x_outside_edge + pad_edge_silk_center_offset, 'y': body_edge['bottom'] + configuration['silk_fab_offset']}
            ]

        else:
            poly_outline = [
                {'x': body_edge['left'], 'y': body_edge['bottom']},
                {'x': body_edge['right'], 'y': body_edge['bottom']},
                {'x': body_edge['right'], 'y': fin_y_outside_edge},
                {'x': fin_x_inside_edge['right'], 'y': fin_y_outside_edge},
                {'x': fin_x_inside_edge['right'], 'y': body_edge['top']},
                {'x': fin_x_inside_edge['left'], 'y': body_edge['top']},
                {'x': fin_x_inside_edge['left'], 'y': fin_y_outside_edge},
                {'x': body_edge['left'], 'y': fin_y_outside_edge},
                {'x': body_edge['left'], 'y': body_edge['bottom']}
            ]
            poly_silk_edge_left = [
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': mp_top_edge - pad_edge_silk_center_offset},
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': fin_y_outside_edge - configuration['silk_fab_offset']},
                {'x': fin_x_inside_edge['left'] + configuration['silk_fab_offset'], 'y': fin_y_outside_edge - configuration['silk_fab_offset']},
                {'x': fin_x_inside_edge['left'] + configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': pad_pos_y - pad_size[1]/2}
            ]
            poly_silk_edge_right = [
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': mp_top_edge - pad_edge_silk_center_offset},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': fin_y_outside_edge - configuration['silk_fab_offset']},
                {'x': fin_x_inside_edge['right'] - configuration['silk_fab_offset'], 'y': fin_y_outside_edge - configuration['silk_fab_offset']},
                {'x': fin_x_inside_edge['right'] - configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': -pad_1_x_outside_edge + pad_edge_silk_center_offset, 'y': body_edge['top'] - configuration['silk_fab_offset']}
            ]

        kicad_mod.append(PolygoneLine(polygone=poly_outline, layer='F.Fab', width=configuration['fab_line_width']))
    #################################  no fin #################################
    else:
        kicad_mod.append(RectLine(
            start=[body_edge['left'], body_edge['top']],
            end=[body_edge['right'], body_edge['bottom']],
            layer='F.Fab', width=configuration['fab_line_width']))
        if series_definition['pad1_position'] == 'bottom-left':
            poly_silk_edge_left = [
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': mp_bottom_edge + pad_edge_silk_center_offset},
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': pad_pos_y + pad_size[1]/2}
            ]
            poly_silk_edge_right = [
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': mp_bottom_edge + pad_edge_silk_center_offset},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': -pad_1_x_outside_edge + pad_edge_silk_center_offset, 'y': body_edge['bottom'] + configuration['silk_fab_offset']}
            ]
        else:
            poly_silk_edge_left = [
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': mp_top_edge - pad_edge_silk_center_offset},
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': pad_pos_y - pad_size[1]/2}
            ]
            poly_silk_edge_right = [
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': mp_top_edge - pad_edge_silk_center_offset},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': -pad_1_x_outside_edge + pad_edge_silk_center_offset, 'y': body_edge['top'] - configuration['silk_fab_offset']}
            ]

    kicad_mod.append(PolygoneLine(polygone=poly_silk_edge_left, layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=poly_silk_edge_right, layer='F.SilkS', width=configuration['silk_line_width']))

    #########################################################################
    mp_inner_edge_x_left = mount_pad_left_x_pos + mounting_pad_size[0]/2 + pad_edge_silk_center_offset
    if series_definition['pad1_position'] == 'bottom-left':
        if series_definition['rel_body_edge_y'] > pad_edge_silk_center_offset:
            #todo: check min lenght
            poly_silk_mp_side = [
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': mp_top_edge - pad_edge_silk_center_offset},
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': mp_top_edge - pad_edge_silk_center_offset}
            ]
        else:
            poly_silk_mp_side = [
                {'x': mp_inner_edge_x_left, 'y': body_edge['top'] - configuration['silk_fab_offset']},
                {'x': -mp_inner_edge_x_left, 'y': body_edge['top'] - configuration['silk_fab_offset']}
            ]
    else:
        if series_definition['rel_body_edge_y'] > pad_edge_silk_center_offset:
            #todo: check min lenght
            poly_silk_mp_side = [
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': mp_bottom_edge + pad_edge_silk_center_offset},
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': mp_bottom_edge + pad_edge_silk_center_offset}
            ]
        else:
            poly_silk_mp_side = [
                {'x': mp_inner_edge_x_left, 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
                {'x': -mp_inner_edge_x_left, 'y': body_edge['bottom'] + configuration['silk_fab_offset']}
            ]
    kicad_mod.append(PolygoneLine(polygone=poly_silk_mp_side, layer='F.SilkS', width=configuration['silk_line_width']))

    ######################### Pin 1 marker ##############################
    if series_definition['pad1_position'] == 'bottom-left':
        poly_pin1_marker = [
            {'x':-dimension_A/2 - configuration['fap_pin1_marker_length']/2,'y': body_edge['bottom']},
            {'x':-dimension_A/2,'y': body_edge['bottom'] - configuration['fap_pin1_marker_length']/sqrt(2)},
            {'x':-dimension_A/2 + configuration['fap_pin1_marker_length']/2,'y': body_edge['bottom']}
        ]
    else:
        poly_pin1_marker = [
            {'x':-dimension_A/2 - configuration['fap_pin1_marker_length']/2,'y': body_edge['top']},
            {'x':-dimension_A/2,'y': body_edge['top'] + configuration['fap_pin1_marker_length']/sqrt(2)},
            {'x':-dimension_A/2 + configuration['fap_pin1_marker_length']/2,'y': body_edge['top']}
        ]
    kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker, layer='F.Fab', width=configuration['fab_line_width']))
    ######################### Text Fields ###############################

    text_center = series_definition['ref_text_inside_pos']
    reference_fields = configuration['references']
    kicad_mod.append(Text(type='reference', text='REF**',
        **getTextFieldDetails(reference_fields[0], cy1, cy2, text_center)))

    for additional_ref in reference_fields[1:]:
        kicad_mod.append(Text(type='user', text='%R',
        **getTextFieldDetails(additional_ref, cy1, cy2, text_center)))

    value_fields = configuration['values']
    kicad_mod.append(Text(type='value', text=footprint_name,
        **getTextFieldDetails(value_fields[0], cy1, cy2, text_center)))

    for additional_value in value_fields[1:]:
        kicad_mod.append(Text(type='user', text='%V',
            **getTextFieldDetails(additional_value, cy1, cy2, text_center)))


    ########################### file names ###############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}')

    lib_name = configuration['lib_name_format_string'].format(series=series_definition['series'])
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

def generate_series(configuration, series_definition, id):
    pinrange_def_type, pinrange_def = series_definition['pinrange']
    if pinrange_def_type == 'range':
        pinrange = range(*pinrange_def)
    elif pinrange_def_type == 'list':
        pinrange = pinrange_def
    else:
        print("Pinrange definition error in part {:s}".format(id))
        return

    for pincount in pinrange:
        generate_one_footprint(pincount, series_definition, configuration)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files holding information about what devices should be created.')
    parser.add_argument('-c', '--config', type=str, nargs='?', help='the config file defining how the footprint will look like.', default='config_KLCv3.0.yaml')
    args = parser.parse_args()

    with open(args.config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    for filepath in args.files:
        with open(filepath, 'r') as series_stream:
            try:
                series_definitions = yaml.load(series_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for series_definition_id in series_definitions:
            generate_series(configuration, series_definitions[series_definition_id], series_definition_id)
