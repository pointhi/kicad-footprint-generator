#!/usr/bin/env python

import sys
import os
from helpers import *
from global_params import *
import re

from options_manager import OptionManager

#sys.path.append(os.path.join(sys.path[0],"..","..")) # load KicadModTree path
#add KicadModTree to searchpath using export PYTHONPATH="${PYTHONPATH}<absolute path>/kicad-footprint-generator/"
from KicadModTree import *


from mstb_params import seriesParams, dimensions, generate_description, all_params

def generate_one_footprint(model, params, options):

    # Through-hole type shrouded header, Top entry type
    footprint_name = params.file_name

    length, width, upper_to_pin, left_to_pin, mount_hole_left, mount_hole_right, inner_len = dimensions(params)

    body_top_left=[left_to_pin,upper_to_pin]
    body_bottom_right=v_add(body_top_left,[length,width])

    silk_top_left=v_offset(body_top_left, options.silk_body_offset)
    silk_bottom_right=v_offset(body_bottom_right, options.silk_body_offset)

    center_x = (params.num_pins-1)/2.0*params.pin_pitch
    kicad_mod = Footprint(footprint_name)


    kicad_mod.setDescription(generate_description(params))
    kicad_mod.setTags(globalParams.manufacturer_tag + model)


    ################################################# Pads #################################################
    kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                        at=[0, 0], size=[seriesParams.pin_Sx, seriesParams.pin_Sy], \
                        drill=seriesParams.drill, layers=globalParams.pin_layers))
    for p in range(1,params.num_pins):
        Y = 0
        X = p * params.pin_pitch

        num = p+1
        kicad_mod.append(Pad(number=num, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL,
                            at=[X, Y], size=[seriesParams.pin_Sx, seriesParams.pin_Sy], \
                            drill=seriesParams.drill, layers=globalParams.pin_layers))
    if params.mount_hole:
        kicad_mod.append(Pad(number='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_left, size=[seriesParams.mount_drill, seriesParams.mount_drill], \
                            drill=seriesParams.mount_drill, layers=globalParams.mount_hole_layers))
        kicad_mod.append(Pad(number='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_right, size=[seriesParams.mount_drill, seriesParams.mount_drill], \
                            drill=seriesParams.mount_drill, layers=globalParams.mount_hole_layers))
    #add an outline around the pins

    ################################################# Silk and Fab #################################################
    kicad_mod.append(RectLine(start=silk_top_left, end=silk_bottom_right, layer='F.SilkS'))
    if options.with_fab_layer:
        kicad_mod.append(RectLine(start=body_top_left, end=body_bottom_right, layer='F.Fab', width=options.fab_line_width))
    if params.angled:
        lock_poly=[
            {'x':-1, 'y':0},
            {'x':1, 'y':0},
            {'x':1.5/2, 'y':-1.5},
            {'x':-1.5/2, 'y':-1.5},
            {'x':-1, 'y':0}
        ]
        lock_poly_fab=[
            {'x':-1, 'y':-options.silk_body_offset},
            {'x':1, 'y':-options.silk_body_offset},
            {'x':1.5/2, 'y':-1.5},
            {'x':-1.5/2, 'y':-1.5},
            {'x':-1, 'y':-options.silk_body_offset}
        ]
        kicad_mod.append(RectLine(start=[silk_top_left[0],silk_bottom_right[1]-1.5], end=[silk_bottom_right[0], silk_bottom_right[1]-1.5-1.8], layer='F.SilkS'))
        if options.inner_details_on_fab:
            kicad_mod.append(RectLine(start=[body_top_left[0],silk_bottom_right[1]-1.5], end=[body_bottom_right[0], silk_bottom_right[1]-1.5-1.8],
                layer='F.Fab', width=options.fab_line_width))
        if params.flanged:
            lock_translation = Translation(mount_hole_left[0], silk_bottom_right[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly))
            if options.inner_details_on_fab:
                lock_translation.append(PolygoneLine(polygone=lock_poly_fab, layer='F.Fab', width=options.fab_line_width))
            kicad_mod.append(lock_translation)
            lock_translation = Translation(mount_hole_right[0], silk_bottom_right[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly))
            if options.inner_details_on_fab:
                lock_translation.append(PolygoneLine(polygone=lock_poly_fab, layer='F.Fab', width=options.fab_line_width))
            kicad_mod.append(lock_translation)

        for i in range(params.num_pins):
            lock_translation = Translation(i*params.pin_pitch, silk_bottom_right[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly))
            if options.inner_details_on_fab:
                lock_translation.append(PolygoneLine(polygone=lock_poly_fab, layer='F.Fab', width=options.fab_line_width))
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
        kicad_mod.append(Line(start=[silk_top_left[0], pi1[1]-1], end=[silk_top_left[0]+outher_line_len, pi1[1]-1]))
        kicad_mod.append(Line(start=[silk_bottom_right[0], pi1[1]-1], end=[silk_bottom_right[0]-outher_line_len, pi1[1]-1]))
        if options.inner_details_on_fab:
            kicad_mod.append(Line(start=[body_top_left[0], pi1[1]-1], end=[body_top_left[0]+outher_line_len, pi1[1]-1], layer='F.Fab', width=options.fab_line_width))
            kicad_mod.append(Line(start=[body_bottom_right[0], pi1[1]-1], end=[body_bottom_right[0]-outher_line_len, pi1[1]-1], layer='F.Fab', width=options.fab_line_width))

        for i in range(params.num_pins -1):
            chamfer_edge = Translation(i*params.pin_pitch, pi1[1]-1)
            chamfer_edge.append(Line(start=[first_center-line_len/2.0, 0], end=[first_center+line_len/2.0, 0]))
            if options.inner_details_on_fab:
                chamfer_edge.append(Line(start=[first_center-line_len/2.0, 0], end=[first_center+line_len/2.0, 0], layer='F.Fab', width=options.fab_line_width))
            kicad_mod.append(chamfer_edge)

        flanged_line_left = (mount_hole_left[0]+1)
        lock_rect_silk={'start':[-1,0], 'end':[1,-top_thickness], 'layer':'F.SilkS'}
        lock_rect_fab={'start':[-1,0], 'end':[1,-top_thickness+options.silk_body_offset], 'layer':'F.Fab', 'width':options.fab_line_width}
        if params.flanged:
            lock_translation = Translation(mount_hole_left[0], pi1[1])
            lock_translation.append(RectLine(**lock_rect_silk))
            if options.inner_details_on_fab:
                lock_translation.append(RectLine(**lock_rect_fab))
            kicad_mod.append(lock_translation)
            lock_translation = Translation(mount_hole_right[0], pi1[1])
            lock_translation.append(RectLine(**lock_rect_silk))
            if options.inner_details_on_fab:
                lock_translation.append(RectLine(**lock_rect_fab))
            kicad_mod.append(lock_translation)

            chamfer_edge = Translation(0, pi1[1]-1)
            chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0]))
            if options.inner_details_on_fab:
                chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0], layer='F.Fab', width=options.fab_line_width))
            kicad_mod.append(chamfer_edge)
            chamfer_edge = Translation((params.num_pins-1)*params.pin_pitch+params.mount_hole_to_pin, pi1[1]-1)
            chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0]))
            if options.inner_details_on_fab:
                chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0], layer='F.Fab', width=options.fab_line_width))
            kicad_mod.append(chamfer_edge)


        for i in range(params.num_pins):
            lock_translation = Translation(i*params.pin_pitch, pi1[1])
            lock_translation.append(RectLine(**lock_rect_silk))
            if options.inner_details_on_fab:
                lock_translation.append(RectLine(**lock_rect_fab))
            kicad_mod.append(lock_translation)

        if params.flanged:
            kicad_mod.append(Circle(center=mount_hole_left, radius=1.9, layer='F.SilkS'))
            kicad_mod.append(Circle(center=mount_hole_right, radius=1.9, layer='F.SilkS'))
            if not params.mount_hole:
                kicad_mod.append(Circle(center=mount_hole_left, radius=1, layer='F.SilkS'))
                kicad_mod.append(Circle(center=mount_hole_right, radius=1, layer='F.SilkS'))

            if options.inner_details_on_fab:
                kicad_mod.append(Circle(center=mount_hole_left, radius=1.9, layer='F.Fab', width=options.fab_line_width))
                kicad_mod.append(Circle(center=mount_hole_right, radius=1.9, layer='F.Fab', width=options.fab_line_width))
                kicad_mod.append(Circle(center=mount_hole_left, radius=1, layer='F.Fab', width=options.fab_line_width))
                kicad_mod.append(Circle(center=mount_hole_right, radius=1, layer='F.Fab', width=options.fab_line_width))

        angle = -100.5
        arc_width = 4.0
        for i in range(params.num_pins):
            plug_arc = Translation(i*params.pin_pitch,0)
            plug_arc.append(Arc(start=[-arc_width/2.0,pi2[1]], center=[0,0.55], angle=angle))
            if options.inner_details_on_fab:
                plug_arc.append(Arc(start=[-arc_width/2.0,pi2[1]], center=[0,0.55], angle=angle, layer='F.Fab', width=options.fab_line_width))
            kicad_mod.append(plug_arc)

        for i in range(params.num_pins-1):
            lower_line = Translation(i*params.pin_pitch,pi2[1])
            lower_line.append(Line(start=[arc_width/2.0, 0], end=[params.pin_pitch-arc_width/2.0, 0], layer='F.SilkS'))
            if options.inner_details_on_fab:
                lower_line.append(Line(start=[arc_width/2.0, 0], end=[params.pin_pitch-arc_width/2.0, 0], layer='F.Fab', width=options.fab_line_width))
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
        if options.inner_details_on_fab:
            kicad_mod.append(PolygoneLine(polygone=poly, layer='F.Fab', width=options.fab_line_width))


    if params.mount_hole:
        kicad_mod.append(Circle(center=mount_hole_left, radius=seriesParams.mount_screw_head_r, layer='B.SilkS'))
        kicad_mod.append(Circle(center=mount_hole_right, radius=seriesParams.mount_screw_head_r, layer='B.SilkS'))
        if options.inner_details_on_fab:
            kicad_mod.append(Circle(center=mount_hole_left, radius=seriesParams.mount_screw_head_r, layer='B.Fab', width=options.fab_line_width))
            kicad_mod.append(Circle(center=mount_hole_right, radius=seriesParams.mount_screw_head_r, layer='B.Fab', width=options.fab_line_width))

    ################################################## Courtyard ##################################################
    #if params.angled:
        #p1=[p1[0],-seriesParams.pin_Sy/2]
    crtyd_top_left=v_offset(body_top_left, options.courtyard_distance)
    crtyd_bottom_right=v_offset(body_bottom_right, options.courtyard_distance)
    kicad_mod.append(RectLine(start=round_crty_point(crtyd_top_left), end=round_crty_point(crtyd_bottom_right), layer='F.CrtYd'))

    ################################################# Text Fields #################################################
    ref_pos_1=[center_x + (0 if params.num_pins > 2 else 1), crtyd_top_left[1]-0.7]
    ref_pos_2=[center_x, (3 if params.angled else 0)]
    kicad_mod.append(Text(type='reference', text='REF**', layer=('F.Fab' if options.reference_on_fab_layer else'F.SilkS'),
        at=(ref_pos_2 if options.reference_on_fab_layer else ref_pos_1)))
    if options.reference_on_fab_layer:
        kicad_mod.append(Text(type='user', text='%R', at=ref_pos_1, layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, layer='F.Fab', at=[center_x, crtyd_bottom_right[1]+1]))

    ################################################# Pin 1 Marker #################################################
    kicad_mod.append(PolygoneLine(polygone=create_marker_poly(crtyd_top_left[1])))

    #################################################### 3d file ###################################################
    p3dname = options.packages_3d + footprint_name + ".wrl"
    kicad_mod.append(Model(filename=p3dname,
                           at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(options.out_dir+footprint_name + ".kicad_mod")


if __name__ == "__main__":
    options = OptionManager()

    if options.parse_commands(sys.argv[1:]):
        if not os.path.exists(options.out_dir):
            os.makedirs(options.out_dir)
        model_filter_regobj=re.compile(options.model_filter)
        for model, params in all_params.iteritems():
            if model_filter_regobj.match(model):
                generate_one_footprint(model, params, options)
