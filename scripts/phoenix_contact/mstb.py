#!/usr/bin/env python

import sys
import os
from helpers import *
import re
import fnmatch
import argparse
import yaml

from options_manager import OptionManager

#sys.path.append(os.path.join(sys.path[0],"..","..")) # load KicadModTree path
#add KicadModTree to searchpath using export PYTHONPATH="${PYTHONPATH}<absolute path>/kicad-footprint-generator/"
from KicadModTree import *


from mstb_params import seriesParams, dimensions, generate_description, all_params

series = ['MSTB', '2,5']

def getTextFieldDetails(field_definition, crtyd_top, crtyd_bottom, center_x, params):
    position_y = field_definition['position']

    top_pos =[center_x + (0 if params.num_pins > 2 else 1),
        crtyd_top - field_definition['size'][1]/2.0]
    inner_ref = [center_x + (0 if params.num_pins > 2 else 1),
        (3 if params.angled else -3)]

    inner_value = [center_x, crtyd_bottom - 1.0 - field_definition['size'][1]/2.0]

    bottom_pos = [center_x, crtyd_bottom + field_definition['size'][1]/2.0]
    if position_y == 'top':
        at = top_pos
    elif position_y == 'inside_top':
        at = inner_ref
    elif position_y == 'inside_bottom':
        at = inner_value
    elif position_y == 'bottom':
        at = bottom_pos
    else:
        at = [0,0]

    return {'at': at, 'size': field_definition['size'], 'layer': field_definition['layer'], 'thickness': field_definition['fontwidth']}

def generate_one_footprint(model, params, configuration):

    subseries, connector_style = params.series_name.split('-')
    pitch_mpn = ''
    if params.pin_pitch == 5.08:
        pitch_mpn = '-5,08'
    elif params.pin_pitch == 7.62:
        pitch_mpn = '-7,62'
    lib_name = configuration['lib_name_format_str'].format(series=series[0], style=series[1], pitch=params.pin_pitch)
    mpn = configuration['mpn_format_string'].format(subseries=subseries, style = connector_style,
        rating=series[1], num_pins=params.num_pins, pitch=pitch_mpn)
    footprint_name = configuration['fp_name_format_string'].format(man = configuration['manufacturer'], series = series[0], mpn = mpn, num_rows = 1,
        num_pins = params.num_pins, pitch = params.pin_pitch,
        orientation = configuration['orientation_str'][1] if params.angled else configuration['orientation_str'][0],
        flanged = configuration['flanged_str'][1] if params.flanged else configuration['flanged_str'][0],
        mount_hole = configuration['mount_hole_str'][1] if params.mount_hole else configuration['mount_hole_str'][0])

    length, width, upper_to_pin, left_to_pin, mount_hole_left, mount_hole_right, inner_len = dimensions(params)

    body_top_left=[left_to_pin,upper_to_pin]
    body_bottom_right=v_add(body_top_left,[length,width])

    silk_top_left=v_offset(body_top_left, configuration['silk_body_offset'])
    silk_bottom_right=v_offset(body_bottom_right, configuration['silk_body_offset'])

    center_x = (params.num_pins-1)/2.0*params.pin_pitch
    kicad_mod = Footprint(footprint_name)


    kicad_mod.setDescription(generate_description(params))
    kicad_mod.setTags(configuration['keywords_format_string'].format(mpn=mpn, param_name=model,
        order_info = ', '.join(params.order_info)))


    ################################################# Pads #################################################
    kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                        at=[0, 0], size=[params.pin_Sx, params.pin_Sy], \
                        drill=seriesParams.drill, layers=configuration['pin_layers']))
    for p in range(1,params.num_pins):
        Y = 0
        X = p * params.pin_pitch

        num = p+1
        kicad_mod.append(Pad(number=num, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL,
                            at=[X, Y], size=[params.pin_Sx, params.pin_Sy], \
                            drill=seriesParams.drill, layers=configuration['pin_layers']))
    if params.mount_hole:
        kicad_mod.append(Pad(number='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_left, size=[seriesParams.mount_drill, seriesParams.mount_drill], \
                            drill=seriesParams.mount_drill, layers=configuration['mount_hole_layers']))
        kicad_mod.append(Pad(number='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_right, size=[seriesParams.mount_drill, seriesParams.mount_drill], \
                            drill=seriesParams.mount_drill, layers=configuration['mount_hole_layers']))
    #add an outline around the pins

    ################################################# Silk and Fab #################################################
    kicad_mod.append(RectLine(start=silk_top_left, end=silk_bottom_right, layer='F.SilkS', width=configuration['silk_line_width']))
    if configuration['with_fab_layer']:
        kicad_mod.append(RectLine(start=body_top_left, end=body_bottom_right, layer='F.Fab', width=configuration['fab_line_width']))
    if params.angled:
        lock_poly=[
            {'x':-1, 'y':0},
            {'x':1, 'y':0},
            {'x':1.5/2, 'y':-1.5},
            {'x':-1.5/2, 'y':-1.5},
            {'x':-1, 'y':0}
        ]
        lock_poly_fab=[
            {'x':-1, 'y':-configuration['silk_body_offset']},
            {'x':1, 'y':-configuration['silk_body_offset']},
            {'x':1.5/2, 'y':-1.5},
            {'x':-1.5/2, 'y':-1.5},
            {'x':-1, 'y':-configuration['silk_body_offset']}
        ]
        kicad_mod.append(RectLine(start=[silk_top_left[0],silk_bottom_right[1]-1.5], end=[silk_bottom_right[0], silk_bottom_right[1]-1.5-1.8], layer='F.SilkS', width=configuration['silk_line_width']))
        if configuration['inner_details_on_fab']:
            kicad_mod.append(RectLine(start=[body_top_left[0],silk_bottom_right[1]-1.5], end=[body_bottom_right[0], silk_bottom_right[1]-1.5-1.8],
                layer='F.Fab', width=configuration['fab_line_width']))
        if params.flanged:
            lock_translation = Translation(mount_hole_left[0], silk_bottom_right[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly, layer='F.SilkS', width=configuration['silk_line_width']))
            if configuration['inner_details_on_fab']:
                lock_translation.append(PolygoneLine(polygone=lock_poly_fab, layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(lock_translation)
            lock_translation = Translation(mount_hole_right[0], silk_bottom_right[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly, layer='F.SilkS', width=configuration['silk_line_width']))
            if configuration['inner_details_on_fab']:
                lock_translation.append(PolygoneLine(polygone=lock_poly_fab, layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(lock_translation)

        for i in range(params.num_pins):
            lock_translation = Translation(i*params.pin_pitch, silk_bottom_right[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly, layer='F.SilkS', width=configuration['silk_line_width']))
            if configuration['inner_details_on_fab']:
                lock_translation.append(PolygoneLine(polygone=lock_poly_fab, layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(lock_translation)
    else:
        inner_width = 5.3 #measured

        pi1 = [body_top_left[0]+(length-inner_len)/2.0, body_top_left[1]+1.7] # 1.7mm measured
        top_thickness = pi1[1]-silk_top_left[1]
        pi2 = [body_bottom_right[0]-(length-inner_len)/2.0, pi1[1]+inner_width]
        #kicad_mod.append(RectLine(start=pi1, end=pi2, layer='F.SilkS'))

        first_center = params.pin_pitch/2.0
        line_len = params.pin_pitch-2
        outher_line_len = (-left_to_pin-1 + mount_hole_left[0]) if params.flanged else (-left_to_pin-1)
        kicad_mod.append(Line(start=[silk_top_left[0], pi1[1]-1], end=[silk_top_left[0]+outher_line_len, pi1[1]-1], layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[silk_bottom_right[0], pi1[1]-1], end=[silk_bottom_right[0]-outher_line_len, pi1[1]-1], layer='F.SilkS', width=configuration['silk_line_width']))
        if configuration['inner_details_on_fab']:
            kicad_mod.append(Line(start=[body_top_left[0], pi1[1]-1], end=[body_top_left[0]+outher_line_len, pi1[1]-1], layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(Line(start=[body_bottom_right[0], pi1[1]-1], end=[body_bottom_right[0]-outher_line_len, pi1[1]-1], layer='F.Fab', width=configuration['fab_line_width']))

        for i in range(params.num_pins -1):
            chamfer_edge = Translation(i*params.pin_pitch, pi1[1]-1)
            chamfer_edge.append(Line(start=[first_center-line_len/2.0, 0], end=[first_center+line_len/2.0, 0], layer='F.SilkS', width=configuration['silk_line_width']))
            if configuration['inner_details_on_fab']:
                chamfer_edge.append(Line(start=[first_center-line_len/2.0, 0], end=[first_center+line_len/2.0, 0], layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(chamfer_edge)

        flanged_line_left = (mount_hole_left[0]+1)
        lock_rect_silk={'start':[-1,0], 'end':[1,-top_thickness], 'layer':'F.SilkS', 'width':configuration['silk_line_width']}
        lock_rect_fab={'start':[-1,0], 'end':[1,-top_thickness+configuration['silk_body_offset']], 'layer':'F.Fab', 'width':configuration['fab_line_width']}
        if params.flanged:
            lock_translation = Translation(mount_hole_left[0], pi1[1])
            lock_translation.append(RectLine(**lock_rect_silk))
            if configuration['inner_details_on_fab']:
                lock_translation.append(RectLine(**lock_rect_fab))
            kicad_mod.append(lock_translation)
            lock_translation = Translation(mount_hole_right[0], pi1[1])
            lock_translation.append(RectLine(**lock_rect_silk))
            if configuration['inner_details_on_fab']:
                lock_translation.append(RectLine(**lock_rect_fab))
            kicad_mod.append(lock_translation)

            chamfer_edge = Translation(0, pi1[1]-1)
            chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0], layer='F.SilkS', width=configuration['silk_line_width']))
            if configuration['inner_details_on_fab']:
                chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0], layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(chamfer_edge)
            chamfer_edge = Translation((params.num_pins-1)*params.pin_pitch+params.mount_hole_to_pin, pi1[1]-1)
            chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0], layer='F.SilkS', width=configuration['silk_line_width']))
            if configuration['inner_details_on_fab']:
                chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0], layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(chamfer_edge)


        for i in range(params.num_pins):
            lock_translation = Translation(i*params.pin_pitch, pi1[1])
            lock_translation.append(RectLine(**lock_rect_silk))
            if configuration['inner_details_on_fab']:
                lock_translation.append(RectLine(**lock_rect_fab))
            kicad_mod.append(lock_translation)

        if params.flanged:
            kicad_mod.append(Circle(center=mount_hole_left, radius=1.9, layer='F.SilkS', width=configuration['silk_line_width']))
            kicad_mod.append(Circle(center=mount_hole_right, radius=1.9, layer='F.SilkS', width=configuration['silk_line_width']))
            if not params.mount_hole:
                kicad_mod.append(Circle(center=mount_hole_left, radius=1, layer='F.SilkS', width=configuration['silk_line_width']))
                kicad_mod.append(Circle(center=mount_hole_right, radius=1, layer='F.SilkS', width=configuration['silk_line_width']))

            if configuration['inner_details_on_fab']:
                kicad_mod.append(Circle(center=mount_hole_left, radius=1.9, layer='F.Fab', width=configuration['fab_line_width']))
                kicad_mod.append(Circle(center=mount_hole_right, radius=1.9, layer='F.Fab', width=configuration['fab_line_width']))
                kicad_mod.append(Circle(center=mount_hole_left, radius=1, layer='F.Fab', width=configuration['fab_line_width']))
                kicad_mod.append(Circle(center=mount_hole_right, radius=1, layer='F.Fab', width=configuration['fab_line_width']))

        angle = -100.5
        arc_width = 4.0
        for i in range(params.num_pins):
            plug_arc = Translation(i*params.pin_pitch,0)
            plug_arc.append(Arc(start=[-arc_width/2.0,pi2[1]], center=[0,0.55], angle=angle, layer='F.SilkS', width=configuration['silk_line_width']))
            if configuration['inner_details_on_fab']:
                plug_arc.append(Arc(start=[-arc_width/2.0,pi2[1]], center=[0,0.55], angle=angle, layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(plug_arc)

        for i in range(params.num_pins-1):
            lower_line = Translation(i*params.pin_pitch,pi2[1])
            lower_line.append(Line(start=[arc_width/2.0, 0], end=[params.pin_pitch-arc_width/2.0, 0], layer='F.SilkS', width=configuration['silk_line_width']))
            if configuration['inner_details_on_fab']:
                lower_line.append(Line(start=[arc_width/2.0, 0], end=[params.pin_pitch-arc_width/2.0, 0], layer='F.Fab', width=configuration['fab_line_width']))
            kicad_mod.append(lower_line)

        arc_to_side = pi1[0]+arc_width/2.0
        poly=[
            {'x':pi1[0]-arc_to_side, 'y':pi2[1]},
            {'x':pi1[0], 'y':pi2[1]},
            {'x':pi1[0], 'y':pi1[1]},
            {'x':pi2[0], 'y':pi1[1]},
            {'x':pi2[0], 'y':pi2[1]},
            {'x':pi2[0]+arc_to_side, 'y':pi2[1]}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly))
        if configuration['inner_details_on_fab']:
            kicad_mod.append(PolygoneLine(polygone=poly, layer='F.Fab', width=configuration['fab_line_width']))


    if params.mount_hole:
        kicad_mod.append(Circle(center=mount_hole_left, radius=seriesParams.mount_screw_head_r+configuration['silk_body_offset'], layer='B.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Circle(center=mount_hole_right, radius=seriesParams.mount_screw_head_r+configuration['silk_body_offset'], layer='B.SilkS', width=configuration['silk_line_width']))

        kicad_mod.append(Circle(center=mount_hole_right, radius=seriesParams.mount_screw_head_r, layer='B.Fab', width=configuration['fab_line_width']))
        kicad_mod.append(Circle(center=mount_hole_left, radius=seriesParams.mount_screw_head_r, layer='B.Fab', width=configuration['fab_line_width']))

    ################################################## Courtyard ##################################################
    #if params.angled:
        #p1=[p1[0],-seriesParams.pin_Sy/2]
    crtyd_top_left=v_offset(body_top_left, configuration['courtyard_distance'])
    crtyd_bottom_right=v_offset(body_bottom_right, configuration['courtyard_distance'])
    kicad_mod.append(RectLine(start=round_crty_point(crtyd_top_left, configuration['courtyard_grid']), end=round_crty_point(crtyd_bottom_right, configuration['courtyard_grid']), layer='F.CrtYd'))

    if params.mount_hole and configuration['courtyard_for_mountscrews']:
        kicad_mod.append(Circle(center=mount_hole_right, radius=seriesParams.mount_screw_head_r+configuration['courtyard_distance'], layer='B.CrtYd', width=configuration['courtyard_line_width']))
        kicad_mod.append(Circle(center=mount_hole_left, radius=seriesParams.mount_screw_head_r+configuration['courtyard_distance'], layer='B.CrtYd', width=configuration['courtyard_line_width']))

    ################################################# Text Fields #################################################
    #getTextFieldDetails(field_definition, crtyd_top, crtyd_bottom, center_x, params)
    reference_fields = configuration['references']
    kicad_mod.append(Text(type='reference', text='REF**',
        **getTextFieldDetails(reference_fields[0], crtyd_top_left[1], crtyd_bottom_right[1], center_x, params)))

    for additional_ref in reference_fields[1:]:
        kicad_mod.append(Text(type='user', text='%R',
        **getTextFieldDetails(additional_ref, crtyd_top_left[1], crtyd_bottom_right[1], center_x, params)))

    value_fields = configuration['values']
    kicad_mod.append(Text(type='value', text=footprint_name,
        **getTextFieldDetails(value_fields[0], crtyd_top_left[1], crtyd_bottom_right[1], center_x, params)))

    for additional_value in value_fields[1:]:
        kicad_mod.append(Text(type='user', text='%V',
            **getTextFieldDetails(additional_value, crtyd_top_left[1], crtyd_bottom_right[1], center_x, params)))

    ################################################# Pin 1 Marker #################################################
    if not params.angled:
        kicad_mod.append(PolygoneLine(polygone=create_pin1_marker_triangle(silk_top_left[1]-0.2),
            layer='F.SilkS', width=configuration['silk_line_width']))
        if configuration['with_fab_layer']:
            kicad_mod.append(PolygoneLine(
                polygone=create_pin1_marker_triangle(bottom_y = -params.pin_Sy/2- 0.75,
                    dimensions = [1, 1], with_top_line = True),
                layer='F.Fab', width=configuration['fab_line_width']))
    else:
        y_bottom_silk_marker = (silk_top_left[1] if silk_top_left[1] < -params.pin_Sy/2 else -params.pin_Sy/2) - 0.2
        kicad_mod.append(PolygoneLine(polygone=create_pin1_marker_triangle(y_bottom_silk_marker),
            layer='F.SilkS', width=configuration['silk_line_width']))
        if configuration['with_fab_layer']:
            kicad_mod.append(PolygoneLine(
                polygone=create_pin1_marker_triangle(bottom_y = -0.5,
                    dimensions = [1.9, -body_top_left[1]-0.5], with_top_line = False),
                layer='F.Fab', width=configuration['fab_line_width']))

    #################################################### 3d file ###################################################
    p3dname = '{prefix:s}{lib_name:s}.3dshapes/{fp_name}.wrl'.format(prefix = configuration.get('3d_model_prefix', '${KISYS3DMOD}/'), lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=p3dname,
                           at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    file_handler = KicadFileHandler(kicad_mod)
    out_dir = '{:s}.pretty/'.format(lib_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    file_handler.writeFile('{:s}.pretty/{:s}.kicad_mod'.format(lib_name, footprint_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--model_filter', type=str, nargs='?',
                        help='define a filter for what should be generated.', default="*")
    parser.add_argument('-c', '--config', type=str, nargs='?', help='the config file defining how the footprint will look like.', default='config_KLCv2.0.yaml')
    args = parser.parse_args()

    with open(args.config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    model_filter_regobj=re.compile(fnmatch.translate(args.model_filter))
    for model, params in all_params.items():
        if model_filter_regobj.match(model):
            generate_one_footprint(model, params, configuration)
