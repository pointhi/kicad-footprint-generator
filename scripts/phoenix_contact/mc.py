#!/usr/bin/env python

import sys
import os
from helpers import *

sys.path.append(os.path.join(sys.path[0],"..","..")) # load KicadModTree path
from KicadModTree import *

lib_name="Connectors_Phoenix"
out_dir=lib_name+".pretty"+os.sep
packages_3d=lib_name+".3dshapes"+os.sep


from mc_params import globalParams, dimensions, generate_description, all_params


m ='MCV_01x02_GF_5.08mm_MH'

#to_generate = {m:all_params[m]}
to_generate=all_params

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for model, params in to_generate.iteritems():

    # Through-hole type shrouded header, Top entry type
    footprint_name = params.file_name

    calc_dim = dimensions(params)

    body_top_left=[calc_dim.left_to_pin,params.back_to_pin]
    body_bottom_right=v_add(body_top_left,[calc_dim.length,calc_dim.width])
    silk_top_left=v_offset(body_top_left, globalParams.silk_body_offset)
    silk_bottom_right=v_offset(body_bottom_right, globalParams.silk_body_offset)
    center_x = (params.num_pins-1)/2.0*params.pin_pitch
    kicad_mod = Footprint(footprint_name)


    kicad_mod.setDescription(generate_description(params))
    kicad_mod.setTags("phoenix contact " + model)
    # set general values
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[center_x, silk_top_left[1]-2], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[center_x,silk_bottom_right[1]+1.5], layer='F.Fab'))

    #add the pads
    for p in range(params.num_pins):
        Y = 0
        X = p * params.pin_pitch

        num = p+1
        kicad_mod.append(Pad(number=num, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL,
                            at=[X, Y], size=[globalParams.pin_Sx, globalParams.pin_Sy], \
                            drill=globalParams.drill, layers=globalParams.pin_layers))
    if params.mount_hole:
        kicad_mod.append(Pad(number='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=calc_dim.mount_hole_left, size=[globalParams.mount_drill, globalParams.mount_drill], \
                            drill=globalParams.mount_drill, layers=globalParams.mount_hole_layers))
        kicad_mod.append(Pad(number='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=calc_dim.mount_hole_right, size=[globalParams.mount_drill, globalParams.mount_drill], \
                            drill=globalParams.mount_drill, layers=globalParams.mount_hole_layers))
    #add an outline around the pins

    # create silscreen


    if params.angled:
        #kicad_mod.append(RectLine(start=silk_top_left, end=silk_bottom_right, layer='F.SilkS'))

        kicad_mod.append(Line(start=silk_top_left, end=[silk_top_left[0], silk_bottom_right[1]], layer='F.SilkS'))
        kicad_mod.append(Line(start=[silk_top_left[0], silk_bottom_right[1]], end=silk_bottom_right, layer='F.SilkS'))
        kicad_mod.append(Line(start=silk_bottom_right, end=[silk_bottom_right[0], silk_top_left[1]], layer='F.SilkS'))

        kicad_mod.append(Line(start=silk_top_left, end=[-globalParams.silkGab, silk_top_left[1]], layer='F.SilkS'))
        kicad_mod.append(Line(start=[silk_bottom_right[0], silk_top_left[1]], end=[(params.num_pins-1)*params.pin_pitch+globalParams.silkGab, silk_top_left[1]],\
                        layer='F.SilkS'))

        for p in range(params.num_pins-1):
            kicad_mod.append(Line(start=[p*params.pin_pitch+globalParams.silkGab, silk_top_left[1]], \
                            end=[(p+1)*params.pin_pitch-globalParams.silkGab, silk_top_left[1]], layer='F.SilkS'))

        left = silk_top_left[0] + (globalParams.flange_lenght if params.flanged else 0)
        right = silk_bottom_right[0] - (globalParams.flange_lenght if params.flanged else 0)
        scoreline_y = globalParams.scoreline_from_back+params.back_to_pin
        kicad_mod.append(Line(start=[left, scoreline_y], end=[right, scoreline_y], layer='F.SilkS'))
        if params.flanged:
            kicad_mod.append(Line(start=[left, silk_top_left[1]], end=[left, silk_bottom_right[1]], layer='F.SilkS'))
            kicad_mod.append(Line(start=[right, silk_top_left[1]], end=[right, silk_bottom_right[1]], layer='F.SilkS'))
    else:
        if not params.flanged:
            kicad_mod.append(RectLine(start=silk_top_left, end=silk_bottom_right, layer='F.SilkS'))
        else:
            flange_cutout = calc_dim.width-calc_dim.flange_width
            outline_poly=[
                    {'x':silk_top_left[0], 'y':silk_bottom_right[1]},
                    {'x':silk_bottom_right[0], 'y':silk_bottom_right[1]},
                    {'x':silk_bottom_right[0], 'y':silk_top_left[1]+flange_cutout},
                    {'x':silk_bottom_right[0]-globalParams.flange_lenght, 'y':silk_top_left[1]+flange_cutout},
                    {'x':silk_bottom_right[0]-globalParams.flange_lenght, 'y':silk_top_left[1]},
                    {'x':silk_top_left[0]+globalParams.flange_lenght, 'y':silk_top_left[1]},
                    {'x':silk_top_left[0]+globalParams.flange_lenght, 'y':silk_top_left[1]+flange_cutout},
                    {'x':silk_top_left[0], 'y':silk_top_left[1]+flange_cutout},
                    {'x':silk_top_left[0], 'y':silk_bottom_right[1]}
                ]
            kicad_mod.append(PolygoneLine(polygone=outline_poly))

        if params.flanged:
            kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=1.9, layer='F.SilkS'))
            kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=1.9, layer='F.SilkS'))
            if not params.mount_hole:
                kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=1, layer='F.SilkS'))
                kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=1, layer='F.SilkS'))

        for i in range(params.num_pins):
            lock_translation = Translation(i*params.pin_pitch, 0)
            plug_poly=[
                {'x':-globalParams.plug_arc_len/2.0, 'y':calc_dim.plug_front},
                {'x':-globalParams.plug_cut_len/2.0, 'y':calc_dim.plug_front},
                {'x':-globalParams.plug_cut_len/2.0, 'y':calc_dim.plug_front-globalParams.plug_cut_width},
                {'x':-globalParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_front-globalParams.plug_cut_width},
                {'x':-globalParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_back+globalParams.plug_trapezoid_width},
                {'x':-globalParams.plug_trapezoid_short/2.0, 'y':calc_dim.plug_back+globalParams.plug_trapezoid_width},
                {'x':-globalParams.plug_trapezoid_long/2.0, 'y':calc_dim.plug_back},
                {'x':globalParams.plug_trapezoid_long/2.0, 'y':calc_dim.plug_back},
                {'x':globalParams.plug_trapezoid_short/2.0, 'y':calc_dim.plug_back+globalParams.plug_trapezoid_width},
                {'x':globalParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_back+globalParams.plug_trapezoid_width},
                {'x':globalParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_front-globalParams.plug_cut_width},
                {'x':globalParams.plug_seperator_distance/2.0, 'y':calc_dim.plug_front-globalParams.plug_cut_width},
                {'x':globalParams.plug_cut_len/2.0, 'y':calc_dim.plug_front-globalParams.plug_cut_width},
                {'x':globalParams.plug_cut_len/2.0, 'y':calc_dim.plug_front},
                {'x':globalParams.plug_arc_len/2.0, 'y':calc_dim.plug_front}
            ]
            lock_translation.append(PolygoneLine(polygone=plug_poly))
            lock_translation.append(Arc(start=[-globalParams.plug_arc_len/2.0,calc_dim.plug_front], center=[0,calc_dim.plug_front+1.7], angle=47.6))
            kicad_mod.append(lock_translation)
    if params.angled:
        crtyd_top_left=v_offset([silk_top_left[0],-globalParams.pin_Sy/2], globalParams.courtyard_distance)
    else:
        crtyd_top_left=v_offset(body_top_left,globalParams.courtyard_distance)
    crtyd_bottom_right=v_offset(body_bottom_right,globalParams.courtyard_distance)
    kicad_mod.append(RectLine(start=round_crty_point(crtyd_top_left), end=round_crty_point(crtyd_bottom_right), layer='F.CrtYd'))
    if params.mount_hole:
        kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=globalParams.mount_screw_head_r, layer='B.SilkS'))
        kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=globalParams.mount_screw_head_r, layer='B.SilkS'))
        # kicad_mod.append(Circle(center=mount_hole_left, radius=mount_screw_head_r+0.25, layer='B.CrtYd'))
        # kicad_mod.append(Circle(center=mount_hole_right, radius=mount_screw_head_r+0.25, layer='B.CrtYd'))

    kicad_mod.append(Text(type='reference', text='REF**', at=[center_x + (0 if params.num_pins > 2 else 1), crtyd_top_left[1]-0.7], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[center_x, crtyd_bottom_right[1]+1], layer='F.Fab'))

    p3dname = packages_3d + footprint_name + ".wrl"
    kicad_mod.append(Model(filename=p3dname,
                           at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(out_dir+footprint_name + ".kicad_mod")
