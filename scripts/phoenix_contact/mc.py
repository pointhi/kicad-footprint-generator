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

from mc_params import seriesParams, dimensions, generate_description, all_params

def generate_one_footprint(motel, params, options):

    # Through-hole type shrouded header, Top entry type
    footprint_name = params.file_name

    calc_dim = dimensions(params)

    body_top_left=[calc_dim.left_to_pin,params.back_to_pin]
    body_bottom_right=v_add(body_top_left,[calc_dim.length,calc_dim.width])
    silk_top_left=v_offset(body_top_left, options.silk_body_offset)
    silk_bottom_right=v_offset(body_bottom_right, options.silk_body_offset)
    center_x = (params.num_pins-1)/2.0*params.pin_pitch
    kicad_mod = Footprint(footprint_name)


    kicad_mod.setDescription(generate_description(params))
    kicad_mod.setTags(globalParams.manufacturer_tag + model)

    #add the pads
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
                            at=calc_dim.mount_hole_left, size=[seriesParams.mount_drill, seriesParams.mount_drill], \
                            drill=seriesParams.mount_drill, layers=globalParams.mount_hole_layers))
        kicad_mod.append(Pad(number='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=calc_dim.mount_hole_right, size=[seriesParams.mount_drill, seriesParams.mount_drill], \
                            drill=seriesParams.mount_drill, layers=globalParams.mount_hole_layers))
    #add an outline around the pins

    # create silscreen


    if params.angled:
        #kicad_mod.append(RectLine(start=silk_top_left, end=silk_bottom_right, layer='F.SilkS'))

        kicad_mod.append(Line(start=silk_top_left, end=[silk_top_left[0], silk_bottom_right[1]], layer='F.SilkS'))
        kicad_mod.append(Line(start=[silk_top_left[0], silk_bottom_right[1]], end=silk_bottom_right, layer='F.SilkS'))
        kicad_mod.append(Line(start=silk_bottom_right, end=[silk_bottom_right[0], silk_top_left[1]], layer='F.SilkS'))

        kicad_mod.append(Line(start=silk_top_left, end=[-seriesParams.silkGab, silk_top_left[1]], layer='F.SilkS'))
        kicad_mod.append(Line(start=[silk_bottom_right[0], silk_top_left[1]], end=[(params.num_pins-1)*params.pin_pitch+seriesParams.silkGab, silk_top_left[1]],\
                        layer='F.SilkS'))

        for p in range(params.num_pins-1):
            kicad_mod.append(Line(start=[p*params.pin_pitch+seriesParams.silkGab, silk_top_left[1]], \
                            end=[(p+1)*params.pin_pitch-seriesParams.silkGab, silk_top_left[1]], layer='F.SilkS'))

        if options.with_fab_layer:
            kicad_mod.append(RectLine(start=body_top_left, end=body_bottom_right, layer='F.Fab', width=options.fab_line_width))

        left = silk_top_left[0] + (seriesParams.flange_lenght if params.flanged else 0)
        right = silk_bottom_right[0] - (seriesParams.flange_lenght if params.flanged else 0)
        scoreline_y = seriesParams.scoreline_from_back+params.back_to_pin
        kicad_mod.append(Line(start=[left, scoreline_y], end=[right, scoreline_y], layer='F.SilkS'))
        if options.inner_details_on_fab:
            kicad_mod.append(Line(start=[left +(0 if params.flanged else options.silk_body_offset), scoreline_y],
                end=[right-(0 if params.flanged else options.silk_body_offset), scoreline_y], layer='F.Fab', width=options.fab_line_width))
        if params.flanged:
            kicad_mod.append(Line(start=[left, silk_top_left[1]], end=[left, silk_bottom_right[1]], layer='F.SilkS'))
            kicad_mod.append(Line(start=[right, silk_top_left[1]], end=[right, silk_bottom_right[1]], layer='F.SilkS'))
            if options.inner_details_on_fab:
                kicad_mod.append(Line(start=[left, body_top_left[1]], end=[left, body_bottom_right[1]], layer='F.Fab', width=options.fab_line_width))
                kicad_mod.append(Line(start=[right, body_top_left[1]], end=[right, body_bottom_right[1]], layer='F.Fab', width=options.fab_line_width))
    else:
        if not params.flanged:
            kicad_mod.append(RectLine(start=silk_top_left, end=silk_bottom_right, layer='F.SilkS'))
            if options.with_fab_layer:
                kicad_mod.append(RectLine(start=body_top_left, end=body_bottom_right, layer='F.Fab', width=options.fab_line_width))
        else:
            flange_cutout = calc_dim.width-calc_dim.flange_width
            outline_poly=[
                    {'x':silk_top_left[0], 'y':silk_bottom_right[1]},
                    {'x':silk_bottom_right[0], 'y':silk_bottom_right[1]},
                    {'x':silk_bottom_right[0], 'y':silk_top_left[1]+flange_cutout},
                    {'x':silk_bottom_right[0]-seriesParams.flange_lenght, 'y':silk_top_left[1]+flange_cutout},
                    {'x':silk_bottom_right[0]-seriesParams.flange_lenght, 'y':silk_top_left[1]},
                    {'x':silk_top_left[0]+seriesParams.flange_lenght, 'y':silk_top_left[1]},
                    {'x':silk_top_left[0]+seriesParams.flange_lenght, 'y':silk_top_left[1]+flange_cutout},
                    {'x':silk_top_left[0], 'y':silk_top_left[1]+flange_cutout},
                    {'x':silk_top_left[0], 'y':silk_bottom_right[1]}
                ]
            kicad_mod.append(PolygoneLine(polygone=outline_poly))
            if options.with_fab_layer:
                outline_poly=offset_polyline(outline_poly,-options.silk_body_offset,(center_x,0))
                kicad_mod.append(PolygoneLine(polygone=outline_poly, layer="F.Fab", width=0.05))

        if params.flanged:
            kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=1.9, layer='F.SilkS'))
            kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=1.9, layer='F.SilkS'))
            if not params.mount_hole:
                kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=1, layer='F.SilkS'))
                kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=1, layer='F.SilkS'))
            if options.inner_details_on_fab:
                kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=1.9, layer='F.Fab', width=options.fab_line_width))
                kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=1.9, layer='F.Fab', width=options.fab_line_width))
                kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=1, layer='F.Fab', width=options.fab_line_width))
                kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=1, layer='F.Fab', width=options.fab_line_width))

        for i in range(params.num_pins):
            plug_outline_translation = Translation(i*params.pin_pitch, 0)
            plug_outline_poly=[
                {'x':-seriesParams.plug_arc_len/2.0, 'y':calc_dim.plug_front},
                {'x':-seriesParams.plug_cut_len/2.0, 'y':calc_dim.plug_front},
                {'x':-seriesParams.plug_cut_len/2.0, 'y':calc_dim.plug_front-seriesParams.plug_cut_width},
                {'x':-seriesParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_front-seriesParams.plug_cut_width},
                {'x':-seriesParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_back+seriesParams.plug_trapezoid_width},
                {'x':-seriesParams.plug_trapezoid_short/2.0, 'y':calc_dim.plug_back+seriesParams.plug_trapezoid_width},
                {'x':-seriesParams.plug_trapezoid_long/2.0, 'y':calc_dim.plug_back},
                {'x':seriesParams.plug_trapezoid_long/2.0, 'y':calc_dim.plug_back},
                {'x':seriesParams.plug_trapezoid_short/2.0, 'y':calc_dim.plug_back+seriesParams.plug_trapezoid_width},
                {'x':seriesParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_back+seriesParams.plug_trapezoid_width},
                {'x':seriesParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_front-seriesParams.plug_cut_width},
                {'x':seriesParams.plug_cut_len/2.0, 'y':calc_dim.plug_front-seriesParams.plug_cut_width},
                {'x':seriesParams.plug_cut_len/2.0, 'y':calc_dim.plug_front},
                {'x':seriesParams.plug_arc_len/2.0, 'y':calc_dim.plug_front}
            ]
            plug_outline_translation.append(PolygoneLine(polygone=plug_outline_poly))
            plug_outline_translation.append(Arc(start=[-seriesParams.plug_arc_len/2.0,calc_dim.plug_front], center=[0,calc_dim.plug_front+1.7], angle=47.6))
            if options.inner_details_on_fab:
                plug_outline_translation.append(PolygoneLine(polygone=plug_outline_poly,  layer="F.Fab", width=0.05))
                plug_outline_translation.append(Arc(start=[-seriesParams.plug_arc_len/2.0,calc_dim.plug_front], center=[0,calc_dim.plug_front+1.7], angle=47.6,  layer="F.Fab", width=0.05))
            kicad_mod.append(plug_outline_translation)
    if params.mount_hole:
        kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=seriesParams.mount_screw_head_r, layer='B.SilkS'))
        kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=seriesParams.mount_screw_head_r, layer='B.SilkS'))
        if options.inner_details_on_fab:
            kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=seriesParams.mount_screw_head_r, layer='B.Fab', width=options.fab_line_width))
            kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=seriesParams.mount_screw_head_r, layer='B.Fab', width=options.fab_line_width))

    ################################################## Courtyard ##################################################
    if params.angled:
        crtyd_top_left=v_offset([silk_top_left[0],-seriesParams.pin_Sy/2], options.courtyard_distance)
    else:
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
