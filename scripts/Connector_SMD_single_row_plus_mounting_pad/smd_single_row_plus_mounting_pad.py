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

sys.path.append(os.path.join(sys.path[0], "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

def generate_one_footprint(pincount, series_definition, configuration, group_definition):
    mpn = series_definition['mpn_format_string'].format(pincount=pincount)
    pins_toward_bottom = series_definition['pad1_position'] == 'bottom-left'
    needs_additional_silk_pin1_marker = False

    pad_size = [series_definition['pad_size_x'],
        series_definition['rel_pad_y_outside_edge'] - series_definition['rel_pad_y_inside_edge']]
    pad_pos_y = -series_definition['rel_pad_y_outside_edge']/2 + pad_size[1]/2

    mounting_pad_size = series_definition['mounting_pad_size']
    mount_pad_y_pos = series_definition['rel_pad_y_outside_edge']/2 - mounting_pad_size[1]/2
    mount_pad_center_x_to_pin = series_definition['center_pad_to_mounting_pad_edge'] + mounting_pad_size[0]/2.0

    # center pin 1 to center pin n
    dimension_A = (pincount-1)*series_definition['pitch']

    body_edge = {}
    if pins_toward_bottom:
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
    footprint_name = configuration['fp_name_format_string'].format(man=group_definition['manufacturer'],
        series=series_definition['series'],
        mpn=mpn, num_rows=1, pins_per_row=pincount,
        pitch=series_definition['pitch'], orientation=orientation)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("JST {:s} series connector, {:s} ({:s}), generated with kicad-footprint-generator".format(series_definition['series'],
        mpn, series_definition['datasheet']))
    kicad_mod.setAttribute('smd')
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series_definition['series'],
        orientation=orientation, man=group_definition['manufacturer'],
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

    ######################### Body outline ###############################
    pad_edge_silk_center_offset = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
    pad_1_x_outside_edge = -dimension_A/2 - pad_size[0]/2

    if pins_toward_bottom: #Man i wish there where a rotate footprint function available.
        body_edge_pin = body_edge['bottom']
        body_edge_mount_pad = body_edge['top']
        silk_y_mp_pin_side = mount_pad_y_pos + mounting_pad_size[1]/2 + pad_edge_silk_center_offset
        mp_edge_outside = mount_pad_y_pos - mounting_pad_size[1]/2
        silk_y_mp_outside = mp_edge_outside - pad_edge_silk_center_offset
        pin_edge_outside = pad_pos_y + pad_size[1]/2
        silk_y_offset_pin_side = configuration['silk_fab_offset']
    else:
        body_edge_pin = body_edge['top']
        body_edge_mount_pad = body_edge['bottom']
        silk_y_mp_pin_side = mount_pad_y_pos - mounting_pad_size[1]/2 - pad_edge_silk_center_offset
        mp_edge_outside = mount_pad_y_pos + mounting_pad_size[1]/2
        silk_y_mp_outside = mp_edge_outside + pad_edge_silk_center_offset
        pin_edge_outside = pad_pos_y - pad_size[1]/2
        silk_y_offset_pin_side = -configuration['silk_fab_offset']


    # Pin side
    bounding_box_y_pin_side = pad_pos_y + (pad_size[1]/2 if pins_toward_bottom else -pad_size[1]/2)
    side_line_y_pin_side = body_edge_pin
    mp_inner_edge_x_left_silk = mount_pad_left_x_pos + mounting_pad_size[0]/2 + pad_edge_silk_center_offset
    modified_pinside_x_inner = body_edge['left']
    if 'edge_modifier_pin_side' in series_definition:
        modifier = series_definition['edge_modifier_pin_side']
        modified_pinside_x_inner = body_edge['left'] + modifier['width']

        if pins_toward_bottom:
            side_line_y_pin_side += modifier['length']
            if side_line_y_pin_side > bounding_box_y_pin_side:
                bounding_box_y_pin_side = side_line_y_pin_side
        else:
            side_line_y_pin_side -= modifier['length']
            if side_line_y_pin_side < bounding_box_y_pin_side:
                bounding_box_y_pin_side = side_line_y_pin_side

        poly_fab_pin_side=[
            {'x': body_edge['left'], 'y': side_line_y_pin_side},
            {'x': modified_pinside_x_inner, 'y': side_line_y_pin_side},
            {'x': modified_pinside_x_inner, 'y': body_edge_pin},
            {'x': -modified_pinside_x_inner, 'y': body_edge_pin},
            {'x': -modified_pinside_x_inner, 'y': side_line_y_pin_side},
            {'x': body_edge['right'], 'y': side_line_y_pin_side}
        ]

        if modifier['length'] < 0:
            silk_x_offset = -configuration['silk_fab_offset']
        else:
            silk_x_offset = configuration['silk_fab_offset']

        if modified_pinside_x_inner + silk_x_offset > pad_1_x_outside_edge - pad_edge_silk_center_offset:
            poly_silk_edge_left = [
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': silk_y_mp_pin_side},
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': side_line_y_pin_side + silk_y_offset_pin_side},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': side_line_y_pin_side + silk_y_offset_pin_side},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': pin_edge_outside}
            ]
            if abs(pin_edge_outside) - abs(side_line_y_pin_side + silk_y_offset_pin_side) < configuration['silk_line_lenght_min']:
                needs_additional_silk_pin1_marker = True

            poly_silk_edge_right = [
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': silk_y_mp_pin_side},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': side_line_y_pin_side + silk_y_offset_pin_side},
                {'x': -pad_1_x_outside_edge + pad_edge_silk_center_offset, 'y': side_line_y_pin_side + silk_y_offset_pin_side}
            ]

        else:
            poly_silk_edge_left = [
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': silk_y_mp_pin_side},
                {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': side_line_y_pin_side + silk_y_offset_pin_side},
                {'x': modified_pinside_x_inner + silk_x_offset, 'y': side_line_y_pin_side + silk_y_offset_pin_side},
                {'x': modified_pinside_x_inner + silk_x_offset, 'y': body_edge_pin + silk_y_offset_pin_side},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': body_edge_pin + silk_y_offset_pin_side},
                {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': pin_edge_outside}
            ]
            if abs(pin_edge_outside) - abs(body_edge_pin + silk_y_offset_pin_side) < configuration['silk_line_lenght_min']:
                needs_additional_silk_pin1_marker = True

            poly_silk_edge_right = [
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': silk_y_mp_pin_side},
                {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': side_line_y_pin_side + silk_y_offset_pin_side},
                {'x': -modified_pinside_x_inner - silk_x_offset, 'y': side_line_y_pin_side + silk_y_offset_pin_side},
                {'x': -modified_pinside_x_inner - silk_x_offset, 'y': body_edge_pin + silk_y_offset_pin_side},
                {'x': -pad_1_x_outside_edge + pad_edge_silk_center_offset, 'y': body_edge_pin + silk_y_offset_pin_side}
            ]
    else:
        poly_fab_pin_side=[
            {'x': body_edge['left'], 'y': body_edge_pin},
            {'x': body_edge['right'], 'y': body_edge_pin}
        ]
        poly_silk_edge_left = [
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': silk_y_mp_pin_side},
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': side_line_y_pin_side + silk_y_offset_pin_side},
            {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': body_edge_pin + silk_y_offset_pin_side},
            {'x': pad_1_x_outside_edge - pad_edge_silk_center_offset, 'y': pin_edge_outside}
        ]
        if abs(pin_edge_outside) - abs(body_edge_pin + silk_y_offset_pin_side) < configuration['silk_line_lenght_min']:
            needs_additional_silk_pin1_marker = True

        poly_silk_edge_right = [
            {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': silk_y_mp_pin_side},
            {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': side_line_y_pin_side + silk_y_offset_pin_side},
            {'x': -pad_1_x_outside_edge + pad_edge_silk_center_offset, 'y': body_edge_pin + silk_y_offset_pin_side}
        ]
    kicad_mod.append(PolygoneLine(polygone=poly_fab_pin_side, layer='F.Fab', width=configuration['fab_line_width']))
    if series_definition.get('no_automatic_silk_autline','False') != 'True':
        kicad_mod.append(PolygoneLine(polygone=poly_silk_edge_left, layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygoneLine(polygone=poly_silk_edge_right, layer='F.SilkS', width=configuration['silk_line_width']))

    # Mount pad side
    bounding_box_y_mount_pad_side = mount_pad_y_pos + (-mounting_pad_size[1]/2 if pins_toward_bottom else mounting_pad_size[1]/2)
    if abs(bounding_box_y_mount_pad_side) < abs(body_edge_mount_pad):
        bounding_box_y_mount_pad_side = body_edge_mount_pad
    mid_line_y_mount_pad_side = body_edge_mount_pad
    if 'edge_modifier_mount_pad_side' in series_definition:
        modifier = series_definition['edge_modifier_mount_pad_side']

        if 'width_start' in modifier:
            modified_mp_start_x_inner = - modifier['width_start']/2 # We assume centered body!
        if 'start_from_body_side' in modifier:
            modified_mp_start_x_inner = body_edge['left'] + modifier['start_from_body_side']
        modified_mp_end_x_inner = modified_mp_start_x_inner
        if 'width_end' in modifier:
            modified_mp_end_x_inner = - modifier['width_end']/2 # We assume centered body!
        if 'end_from_body_side' in modifier:
            modified_mp_end_x_inner = body_edge['left'] + modifier['end_from_body_side']

        if pins_toward_bottom:
            mid_line_y_mount_pad_side += modifier['depth']
            if mid_line_y_mount_pad_side < bounding_box_y_mount_pad_side:
                bounding_box_y_mount_pad_side = mid_line_y_mount_pad_side
        else:
            mid_line_y_mount_pad_side -= modifier['depth']
            if mid_line_y_mount_pad_side > bounding_box_y_mount_pad_side:
                bounding_box_y_mount_pad_side = mid_line_y_mount_pad_side

        if modifier['depth'] < 0:
            silk_x_offset = -configuration['silk_fab_offset']
        else:
            silk_x_offset = configuration['silk_fab_offset']

        poly_fab_mp_side=[
            {'x': body_edge['left'], 'y': body_edge_mount_pad},
            {'x': modified_mp_start_x_inner, 'y': body_edge_mount_pad},
            {'x': modified_mp_end_x_inner, 'y': mid_line_y_mount_pad_side},
            {'x': -modified_mp_end_x_inner, 'y': mid_line_y_mount_pad_side},
            {'x': -modified_mp_start_x_inner, 'y': body_edge_mount_pad},
            {'x': body_edge['right'], 'y': body_edge_mount_pad}
        ]

        poly_silk_mp_side=[
            {'x': mp_inner_edge_x_left_silk, 'y': body_edge_mount_pad - silk_y_offset_pin_side},
            {'x': modified_mp_start_x_inner + silk_x_offset, 'y': body_edge_mount_pad - silk_y_offset_pin_side},
            {'x': modified_mp_end_x_inner + silk_x_offset, 'y': mid_line_y_mount_pad_side - silk_y_offset_pin_side},
            {'x': -modified_mp_end_x_inner - silk_x_offset, 'y': mid_line_y_mount_pad_side - silk_y_offset_pin_side},
            {'x': -modified_mp_start_x_inner - silk_x_offset, 'y': body_edge_mount_pad - silk_y_offset_pin_side},
            {'x': -mp_inner_edge_x_left_silk, 'y': body_edge_mount_pad - silk_y_offset_pin_side}
        ]
        if modified_mp_start_x_inner + configuration['silk_fab_offset'] < mp_inner_edge_x_left_silk:
            poly_silk_mp_side=[
                {'x': mp_inner_edge_x_left_silk, 'y': mid_line_y_mount_pad_side - silk_y_offset_pin_side},
                {'x': -mp_inner_edge_x_left_silk, 'y': mid_line_y_mount_pad_side - silk_y_offset_pin_side}
            ]
    else:
        poly_fab_mp_side=[
            {'x': body_edge['left'], 'y': body_edge_mount_pad},
            {'x': body_edge['right'], 'y': body_edge_mount_pad}
        ]
        poly_silk_mp_side=[
            {'x': mp_inner_edge_x_left_silk, 'y': body_edge_mount_pad - silk_y_offset_pin_side},
            {'x': -mp_inner_edge_x_left_silk, 'y': body_edge_mount_pad - silk_y_offset_pin_side}
        ]

    if series_definition['rel_body_edge_y'] > pad_edge_silk_center_offset:
        poly_silk_mp_side[0]['x'] = body_edge['left']
        poly_silk_mp_side[len(poly_silk_mp_side)-1]['x'] = body_edge['right']

    if series_definition['rel_body_edge_y'] > pad_edge_silk_center_offset + configuration['silk_line_lenght_min']:
        poly_silk_mp_side[0]['x'] = body_edge['left'] - configuration['silk_fab_offset']
        poly_silk_mp_side[len(poly_silk_mp_side)-1]['x'] = body_edge['right'] + configuration['silk_fab_offset']

        poly_silk_mp_side.insert(0,{'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': silk_y_mp_outside})
        poly_silk_mp_side.append({'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': silk_y_mp_outside})

    if series_definition.get('no_automatic_silk_autline','False') != 'True':
        kicad_mod.append(PolygoneLine(polygone=poly_silk_mp_side, layer='F.SilkS', width=configuration['silk_line_width']))

    kicad_mod.append(PolygoneLine(polygone=poly_fab_mp_side, layer='F.Fab', width=configuration['fab_line_width']))

    kicad_mod.append(Line(start=[body_edge['left'], side_line_y_pin_side], end=[body_edge['left'], body_edge_mount_pad],
                            layer='F.Fab', width=configuration['fab_line_width']))

    kicad_mod.append(Line(start=[body_edge['right'], side_line_y_pin_side], end=[body_edge['right'], body_edge_mount_pad],
                            layer='F.Fab', width=configuration['fab_line_width']))

    ###################### Additional Drawing ###########################
    if 'additional_drawing' in series_definition:
        for drawing in series_definition['additional_drawing']:
            parseAdditionalDrawing(kicad_mod, drawing, configuration, series_definition, body_edge, pincount)

    ############################# CrtYd ##################################
    mp_left_edge = mount_pad_left_x_pos - mounting_pad_size[0]/2
    bounding_box_x1 = body_edge['left'] if body_edge['left'] < mp_left_edge else mp_left_edge
    bounding_box_x2 = -bounding_box_x1
    if pins_toward_bottom:
        bounding_box_y1 = bounding_box_y_mount_pad_side
        bounding_box_y2 = bounding_box_y_pin_side

    else:
        bounding_box_y1 = bounding_box_y_pin_side
        bounding_box_y2 = bounding_box_y_mount_pad_side


    cx1 = roundToBase(bounding_box_x1 - configuration['courtyard_distance'], configuration['courtyard_grid'])
    cx2 = roundToBase(bounding_box_x2 + configuration['courtyard_distance'], configuration['courtyard_grid'])

    cy1 = roundToBase(bounding_box_y1 - configuration['courtyard_distance'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box_y2 + configuration['courtyard_distance'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Pin 1 marker ##############################

    if series_definition['pad1_position'] == 'bottom-left':
        poly_pin1_marker = [
            {'x':-dimension_A/2 - configuration['fap_pin1_marker_length']/2,'y': body_edge['bottom']},
            {'x':-dimension_A/2,'y': body_edge['bottom'] - configuration['fap_pin1_marker_length']/sqrt(2)},
            {'x':-dimension_A/2 + configuration['fap_pin1_marker_length']/2,'y': body_edge['bottom']}
        ]
        poly_pin1_marker_small = [
            {'x':-dimension_A/2-configuration['fap_pin1_marker_length']/4,'y': cy2 + configuration['fap_pin1_marker_length']/sqrt(8)},
            {'x':-dimension_A/2,'y': cy2},
            {'x':-dimension_A/2+configuration['fap_pin1_marker_length']/4,'y': cy2 + configuration['fap_pin1_marker_length']/sqrt(8)},
            {'x':-dimension_A/2-configuration['fap_pin1_marker_length']/4,'y': cy2 + configuration['fap_pin1_marker_length']/sqrt(8)}
        ]
    else:
        poly_pin1_marker = [
            {'x':-dimension_A/2 - configuration['fap_pin1_marker_length']/2,'y': body_edge['top']},
            {'x':-dimension_A/2,'y': body_edge['top'] + configuration['fap_pin1_marker_length']/sqrt(2)},
            {'x':-dimension_A/2 + configuration['fap_pin1_marker_length']/2,'y': body_edge['top']}
        ]
        poly_pin1_marker_small = [
            {'x':-dimension_A/2-configuration['fap_pin1_marker_length']/4,'y': cy1 - configuration['fap_pin1_marker_length']/sqrt(8)},
            {'x':-dimension_A/2,'y': cy1},
            {'x':-dimension_A/2+configuration['fap_pin1_marker_length']/4,'y': cy1 - configuration['fap_pin1_marker_length']/sqrt(8)},
            {'x':-dimension_A/2-configuration['fap_pin1_marker_length']/4,'y': cy1 - configuration['fap_pin1_marker_length']/sqrt(8)}
        ]

    if modified_pinside_x_inner < -dimension_A/2 - configuration['fap_pin1_marker_length']/2:
        kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker, layer='F.Fab', width=configuration['fab_line_width']))
    else:
        kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker_small, layer='F.Fab', width=configuration['fab_line_width']))

    if needs_additional_silk_pin1_marker:
        kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker_small, layer='F.SilkS', width=configuration['silk_line_width']))


    ######################### Text Fields ###############################
    text_center = series_definition.get('text_inside_pos', 'center')
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position=text_center)

    ########################### file names ###############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(man=group_definition['manufacturer'],
        series=series_definition['series'])
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

def generate_series(configuration, series_definition, id, group_definition):
    pinrange_def_type, pinrange_def = series_definition['pinrange']
    if pinrange_def_type == 'range':
        pinrange = range(*pinrange_def)
    elif pinrange_def_type == 'list':
        pinrange = pinrange_def
    else:
        print("Pinrange definition error in part {:s}".format(id))
        return

    for pincount in pinrange:
        generate_one_footprint(pincount, series_definition, configuration, group_definition)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files holding information about what devices should be created.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='conn_config_KLCv3.yaml')
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
    for filepath in args.files:
        with open(filepath, 'r') as stream:
            try:
                yaml_file = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        series_definitions = yaml_file['device_definition']
        for series_definition_id in series_definitions:
            generate_series(configuration,
                series_definitions[series_definition_id], series_definition_id,
                yaml_file['group_definitions'])
