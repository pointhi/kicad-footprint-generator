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


from mstb_params import globalParams, dimensions, generate_description, all_params


m ='GMSTBV_01x03_7.62mm_MH'
m1='GMSTBV_01x03_7.62mm'
m2='MSTBV_01x03_5.00mm_MH'
m3='MSTBV_01x03_5.08mm_MH'
m4='GMSTBVA_01x03_7.62mm'
#to_generate = {m:all_params[m],m1:all_params[m1],m2:all_params[m2],m3:all_params[m3],m4:all_params[m4]}
to_generate=all_params

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for model, params in to_generate.iteritems():

    # Through-hole type shrouded header, Top entry type
    footprint_name = params.file_name

    length, width, upper_to_pin, left_to_pin, mount_hole_left, mount_hole_right, inner_len = dimensions(params)

    p1=[left_to_pin,upper_to_pin]
    p2=v_add(p1,[length,width])
    center_x = (params.num_pins-1)/2.0*params.pin_pitch
    kicad_mod = Footprint(footprint_name)


    kicad_mod.setDescription(generate_description(params))
    kicad_mod.setTags("phonix contact " + model)

    # set general values
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[center_x, p1[1]-1], layer='F.SilkS'))
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
                            at=mount_hole_left, size=[globalParams.mount_drill, globalParams.mount_drill], \
                            drill=globalParams.mount_drill, layers=globalParams.mount_hole_layers))
        kicad_mod.append(Pad(number='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_right, size=[globalParams.mount_drill, globalParams.mount_drill], \
                            drill=globalParams.mount_drill, layers=globalParams.mount_hole_layers))
    #add an outline around the pins

    # create silscreen

    kicad_mod.append(RectLine(start=p1, end=p2, layer='F.SilkS'))

    if params.angled:
        lock_poly=[
            {'x':-1, 'y':0},
            {'x':1, 'y':0},
            {'x':1.5/2, 'y':-1.5},
            {'x':-1.5/2, 'y':-1.5},
            {'x':-1, 'y':0}
        ]
        kicad_mod.append(RectLine(start=[p1[0],p2[1]-1.5], end=[p2[0], p2[1]-1.5-1.8], layer='F.SilkS'))
        if params.flanged:
            lock_translation = Translation(mount_hole_left[0], p2[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly))
            kicad_mod.append(lock_translation)
            lock_translation = Translation(mount_hole_right[0], p2[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly))
            kicad_mod.append(lock_translation)

        for i in range(params.num_pins):
            lock_translation = Translation(i*params.pin_pitch, p2[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly))
            kicad_mod.append(lock_translation)
    else:
        inner_width = 5.3 #measured
        top_thickness = 1.7 #measured
        pi1 = [p1[0]+(length-inner_len)/2.0, p1[1]+top_thickness]
        pi2 = [p2[0]-(length-inner_len)/2.0, pi1[1]+inner_width]
        #kicad_mod.append(RectLine(start=pi1, end=pi2, layer='F.SilkS'))

        first_center = params.pin_pitch/2.0
        line_len = params.pin_pitch-2
        outher_line_len = (-left_to_pin-1 + mount_hole_left[0]) if params.flanged else (-left_to_pin-1)
        kicad_mod.append(Line(start=[p1[0], pi1[1]-1], end=[p1[0]+outher_line_len, pi1[1]-1]))
        kicad_mod.append(Line(start=[p2[0], pi1[1]-1], end=[p2[0]-outher_line_len, pi1[1]-1]))
        for i in range(params.num_pins -1):
            chamfer_edge = Translation(i*params.pin_pitch, pi1[1]-1)
            chamfer_edge.append(Line(start=[first_center-line_len/2.0, 0], end=[first_center+line_len/2.0, 0]))
            kicad_mod.append(chamfer_edge)

        flanged_line_left = (mount_hole_left[0]+1)
        if params.flanged:
            lock_translation = Translation(mount_hole_left[0], pi1[1])
            lock_translation.append(RectLine(start=[-1,0], end=[1,-top_thickness], layer='F.SilkS'))
            kicad_mod.append(lock_translation)
            lock_translation = Translation(mount_hole_right[0], pi1[1])
            lock_translation.append(RectLine(start=[-1,0], end=[1,-top_thickness], layer='F.SilkS'))
            kicad_mod.append(lock_translation)

            chamfer_edge = Translation(0, pi1[1]-1)
            chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0]))
            kicad_mod.append(chamfer_edge)
            chamfer_edge = Translation((params.num_pins-1)*params.pin_pitch+params.mount_hole_to_pin, pi1[1]-1)
            chamfer_edge.append(Line(start=[flanged_line_left, 0], end=[-1, 0]))
            kicad_mod.append(chamfer_edge)


        for i in range(params.num_pins):
            lock_translation = Translation(i*params.pin_pitch, pi1[1])
            lock_translation.append(RectLine(start=[-1,0], end=[1,-top_thickness], layer='F.SilkS'))
            kicad_mod.append(lock_translation)

        if params.flanged:
            kicad_mod.append(Circle(center=mount_hole_left, radius=1.9, layer='F.SilkS'))
            kicad_mod.append(Circle(center=mount_hole_right, radius=1.9, layer='F.SilkS'))
            kicad_mod.append(Circle(center=mount_hole_left, radius=1, layer='F.SilkS'))
            kicad_mod.append(Circle(center=mount_hole_right, radius=1, layer='F.SilkS'))

        angle = -100.5
        arc_width = 4.0
        for i in range(params.num_pins):
            plug_arc = Translation(i*params.pin_pitch,0)
            plug_arc.append(Arc(start=[-arc_width/2.0,pi2[1]], center=[0,0.55], angle=angle))
            kicad_mod.append(plug_arc)

        for i in range(params.num_pins-1):
            lower_line = Translation(i*params.pin_pitch,pi2[1])
            lower_line.append(Line(start=[arc_width/2.0, 0], end=[params.pin_pitch-arc_width/2.0, 0], layer='F.SilkS'))
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
    # create courtyard
    #if params.angled:
        #p1=[p1[0],-globalParams.pin_Sy/2]
    p1=v_add(p1,[-globalParams.courtyard_distance, -globalParams.courtyard_distance])
    p2=v_add(p2,[globalParams.courtyard_distance, globalParams.courtyard_distance])
    kicad_mod.append(RectLine(start=p1, end=p2, layer='F.CrtYd'))
    if params.mount_hole:
        kicad_mod.append(Circle(center=mount_hole_left, radius=globalParams.mount_screw_head_r, layer='B.SilkS'))
        kicad_mod.append(Circle(center=mount_hole_right, radius=globalParams.mount_screw_head_r, layer='B.SilkS'))
        # kicad_mod.append(Circle(center=mount_hole_left, radius=mount_screw_head_r+0.25, layer='B.CrtYd'))
        # kicad_mod.append(Circle(center=mount_hole_right, radius=mount_screw_head_r+0.25, layer='B.CrtYd'))


    p3dname = packages_3d + footprint_name + ".wrl"
    kicad_mod.append(Model(filename=p3dname,
                           at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(out_dir+footprint_name + ".kicad_mod")
