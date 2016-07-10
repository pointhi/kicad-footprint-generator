#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(sys.path[0],"..","..")) # load KicadModTree path
from KicadModTree import *


def v_add(p1,p2):
    return [p1[0]+p2[0],p1[1]+p2[1]]

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

    p1=[calc_dim.left_to_pin,params.back_to_pin]
    p2=v_add(p1,[calc_dim.length,calc_dim.width])
    center_x = (params.num_pins-1)/2.0*params.pin_pitch
    kicad_mod = Footprint(footprint_name)


    kicad_mod.setDescription(generate_description(params))
    kicad_mod.setTags("phoenix contact " + model)
    # set general values
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[center_x, p1[1]-2], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[center_x,p2[1]+1.5], layer='F.Fab'))

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
        #kicad_mod.append(RectLine(start=p1, end=p2, layer='F.SilkS'))

        kicad_mod.append(Line(start=p1, end=[p1[0], p2[1]], layer='F.SilkS'))
        kicad_mod.append(Line(start=[p1[0], p2[1]], end=p2, layer='F.SilkS'))
        kicad_mod.append(Line(start=p2, end=[p2[0], p1[1]], layer='F.SilkS'))

        kicad_mod.append(Line(start=p1, end=[-globalParams.silkGab, p1[1]], layer='F.SilkS'))
        kicad_mod.append(Line(start=[p2[0], p1[1]], end=[(params.num_pins-1)*params.pin_pitch+globalParams.silkGab, p1[1]],\
                        layer='F.SilkS'))

        for p in range(params.num_pins-1):
            kicad_mod.append(Line(start=[p*params.pin_pitch+globalParams.silkGab, p1[1]], \
                            end=[(p+1)*params.pin_pitch-globalParams.silkGab, p1[1]], layer='F.SilkS'))

        left = p1[0] + (globalParams.flange_lenght if params.flanged else 0)
        right = p2[0] - (globalParams.flange_lenght if params.flanged else 0)
        scoreline_y = globalParams.scoreline_from_back+params.back_to_pin
        kicad_mod.append(Line(start=[left, scoreline_y], end=[right, scoreline_y], layer='F.SilkS'))
        if params.flanged:
            kicad_mod.append(Line(start=[left, p1[1]], end=[left, p2[1]], layer='F.SilkS'))
            kicad_mod.append(Line(start=[right, p1[1]], end=[right, p2[1]], layer='F.SilkS'))
    else:
        if not params.flanged:
            kicad_mod.append(RectLine(start=p1, end=p2, layer='F.SilkS'))
        else:
            flange_cutout = calc_dim.width-calc_dim.flange_width
            outline_poly=[
                    {'x':p1[0], 'y':p2[1]},
                    {'x':p2[0], 'y':p2[1]},
                    {'x':p2[0], 'y':p1[1]+flange_cutout},
                    {'x':p2[0]-globalParams.flange_lenght, 'y':p1[1]+flange_cutout},
                    {'x':p2[0]-globalParams.flange_lenght, 'y':p1[1]},
                    {'x':p1[0]+globalParams.flange_lenght, 'y':p1[1]},
                    {'x':p1[0]+globalParams.flange_lenght, 'y':p1[1]+flange_cutout},
                    {'x':p1[0], 'y':p1[1]+flange_cutout},
                    {'x':p1[0], 'y':p2[1]}
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
            lock_translation.append(Arc(start=[-globalParams.plug_arc_len/2.0,calc_dim.plug_front], center=[0,p2[1]+0.5], angle=59.5))
            kicad_mod.append(lock_translation)
    if params.angled:
        p1=[p1[0],-globalParams.pin_Sy/2]
    p1=v_add(p1,[-globalParams.courtyard_distance, -globalParams.courtyard_distance])
    p2=v_add(p2,[globalParams.courtyard_distance, globalParams.courtyard_distance])
    kicad_mod.append(RectLine(start=p1, end=p2, layer='F.CrtYd'))
    if params.mount_hole:
        kicad_mod.append(Circle(center=calc_dim.mount_hole_left, radius=globalParams.mount_screw_head_r, layer='B.SilkS'))
        kicad_mod.append(Circle(center=calc_dim.mount_hole_right, radius=globalParams.mount_screw_head_r, layer='B.SilkS'))
        # kicad_mod.append(Circle(center=mount_hole_left, radius=mount_screw_head_r+0.25, layer='B.CrtYd'))
        # kicad_mod.append(Circle(center=mount_hole_right, radius=mount_screw_head_r+0.25, layer='B.CrtYd'))


    p3dname = packages_3d + footprint_name + ".wrl"
    kicad_mod.append(Model(filename=p3dname,
                           at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(out_dir+footprint_name + ".kicad_mod")
