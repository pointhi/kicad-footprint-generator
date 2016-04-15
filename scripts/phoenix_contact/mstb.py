#!/usr/bin/env python

import sys
import os
from collections import namedtuple
sys.path.append(os.path.join(sys.path[0],"..","..")) # load KicadModTree path

from KicadModTree import *

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf


def v_add(p1,p2):
    return [p1[0]+p2[0],p1[1]+p2[1]]

lib_name="Connectors_Phoenix"
out_dir=lib_name+".pretty"+os.sep
packages_3d=lib_name+".3dshapes"+os.sep

Params = namedtuple("Params",[
    'file_name',
    'angled',
    'flanged',
    'num_pins',
    'pin_pitch',
    'mount_hole'
])

def generate_params(num_pins, series_name, pin_pitch, angled, flanged, mount_hole=False):
    return Params(
        file_name="PhonixContact_" + series_name + "_01x" + ('%02d' % num_pins) + "_"\
        + ('%.2f' % pin_pitch) + "mm_" + ('Angled' if angled else 'Vertical')\
        + ('_ThreadedFlange' + ('_MountHole' if mount_hole else '') if flanged else ''),
        angled=angled,
        flanged=flanged,
        num_pins=num_pins,
        pin_pitch=pin_pitch,
        mount_hole=mount_hole
    )


all_params = {
    'MSTBA_01x02_5.00mm' : generate_params( 2, "MSTBA", 5.0, True, False),
    'MSTBA_01x03_5.00mm' : generate_params( 3, "MSTBA", 5.0, True, False),
    'MSTBA_01x04_5.00mm' : generate_params( 4, "MSTBA", 5.0, True, False),
    'MSTBA_01x05_5.00mm' : generate_params( 5, "MSTBA", 5.0, True, False),
    'MSTBA_01x06_5.00mm' : generate_params( 6, "MSTBA", 5.0, True, False),
    'MSTBA_01x07_5.00mm' : generate_params( 7, "MSTBA", 5.0, True, False),
    'MSTBA_01x08_5.00mm' : generate_params( 8, "MSTBA", 5.0, True, False),
    'MSTBA_01x09_5.00mm' : generate_params( 9, "MSTBA", 5.0, True, False),
    'MSTBA_01x10_5.00mm' : generate_params(10, "MSTBA", 5.0, True, False),
    'MSTBA_01x11_5.00mm' : generate_params(11, "MSTBA", 5.0, True, False),
    'MSTBA_01x12_5.00mm' : generate_params(12, "MSTBA", 5.0, True, False),
    'MSTB_01x02_5.00mm' : generate_params( 2, "MSTB", 5.0, True, True),
    'MSTB_01x03_5.00mm' : generate_params( 3, "MSTB", 5.0, True, True),
    'MSTB_01x04_5.00mm' : generate_params( 4, "MSTB", 5.0, True, True),
    'MSTB_01x05_5.00mm' : generate_params( 5, "MSTB", 5.0, True, True),
    'MSTB_01x06_5.00mm' : generate_params( 6, "MSTB", 5.0, True, True),
    'MSTB_01x07_5.00mm' : generate_params( 7, "MSTB", 5.0, True, True),
    'MSTB_01x08_5.00mm' : generate_params( 8, "MSTB", 5.0, True, True),
    'MSTB_01x09_5.00mm' : generate_params( 9, "MSTB", 5.0, True, True),
    'MSTB_01x10_5.00mm' : generate_params(10, "MSTB", 5.0, True, True),
    'MSTB_01x11_5.00mm' : generate_params(11, "MSTB", 5.0, True, True),
    'MSTB_01x12_5.00mm' : generate_params(12, "MSTB", 5.0, True, True),
    'MSTB_01x02_5.00mm_MH' : generate_params( 2, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x03_5.00mm_MH' : generate_params( 3, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x04_5.00mm_MH' : generate_params( 4, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x05_5.00mm_MH' : generate_params( 5, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x06_5.00mm_MH' : generate_params( 6, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x07_5.00mm_MH' : generate_params( 7, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x08_5.00mm_MH' : generate_params( 8, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x09_5.00mm_MH' : generate_params( 9, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x10_5.00mm_MH' : generate_params(10, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x11_5.00mm_MH' : generate_params(11, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTB_01x12_5.00mm_MH' : generate_params(12, "MSTB", 5.0, True, True, mount_hole=True),
    'MSTBVA_01x02_5.00mm' : generate_params( 2, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x03_5.00mm' : generate_params( 3, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x04_5.00mm' : generate_params( 4, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x05_5.00mm' : generate_params( 5, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x06_5.00mm' : generate_params( 6, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x07_5.00mm' : generate_params( 7, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x08_5.00mm' : generate_params( 8, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x09_5.00mm' : generate_params( 9, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x10_5.00mm' : generate_params(10, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x11_5.00mm' : generate_params(11, "MSTBVA", 5.0, False, False),
    'MSTBVA_01x12_5.00mm' : generate_params(12, "MSTBVA", 5.0, False, False),
    'MSTBV_01x02_5.00mm' : generate_params( 2, "MSTBV", 5.0, False, True),
    'MSTBV_01x03_5.00mm' : generate_params( 3, "MSTBV", 5.0, False, True),
    'MSTBV_01x04_5.00mm' : generate_params( 4, "MSTBV", 5.0, False, True),
    'MSTBV_01x05_5.00mm' : generate_params( 5, "MSTBV", 5.0, False, True),
    'MSTBV_01x06_5.00mm' : generate_params( 6, "MSTBV", 5.0, False, True),
    'MSTBV_01x07_5.00mm' : generate_params( 7, "MSTBV", 5.0, False, True),
    'MSTBV_01x08_5.00mm' : generate_params( 8, "MSTBV", 5.0, False, True),
    'MSTBV_01x09_5.00mm' : generate_params( 9, "MSTBV", 5.0, False, True),
    'MSTBV_01x10_5.00mm' : generate_params(10, "MSTBV", 5.0, False, True),
    'MSTBV_01x11_5.00mm' : generate_params(11, "MSTBV", 5.0, False, True),
    'MSTBV_01x12_5.00mm' : generate_params(12, "MSTBV", 5.0, False, True),
    'MSTBV_01x02_5.00mm_MH' : generate_params( 2, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x03_5.00mm_MH' : generate_params( 3, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x04_5.00mm_MH' : generate_params( 4, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x05_5.00mm_MH' : generate_params( 5, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x06_5.00mm_MH' : generate_params( 6, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x07_5.00mm_MH' : generate_params( 7, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x08_5.00mm_MH' : generate_params( 8, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x09_5.00mm_MH' : generate_params( 9, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x10_5.00mm_MH' : generate_params(10, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x11_5.00mm_MH' : generate_params(11, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBV_01x12_5.00mm_MH' : generate_params(12, "MSTBV", 5.0, False, True, mount_hole=True),
    'MSTBA_01x02_5.08mm' : generate_params( 2, "MSTBA", 5.08, True, False),
    'MSTBA_01x03_5.08mm' : generate_params( 3, "MSTBA", 5.08, True, False),
    'MSTBA_01x04_5.08mm' : generate_params( 4, "MSTBA", 5.08, True, False),
    'MSTBA_01x05_5.08mm' : generate_params( 5, "MSTBA", 5.08, True, False),
    'MSTBA_01x06_5.08mm' : generate_params( 6, "MSTBA", 5.08, True, False),
    'MSTBA_01x07_5.08mm' : generate_params( 7, "MSTBA", 5.08, True, False),
    'MSTBA_01x08_5.08mm' : generate_params( 8, "MSTBA", 5.08, True, False),
    'MSTBA_01x09_5.08mm' : generate_params( 9, "MSTBA", 5.08, True, False),
    'MSTBA_01x10_5.08mm' : generate_params(10, "MSTBA", 5.08, True, False),
    'MSTBA_01x11_5.08mm' : generate_params(11, "MSTBA", 5.08, True, False),
    'MSTBA_01x12_5.08mm' : generate_params(12, "MSTBA", 5.08, True, False),
    'MSTB_01x02_5.08mm' : generate_params( 2, "MSTB", 5.08, True, True),
    'MSTB_01x03_5.08mm' : generate_params( 3, "MSTB", 5.08, True, True),
    'MSTB_01x04_5.08mm' : generate_params( 4, "MSTB", 5.08, True, True),
    'MSTB_01x05_5.08mm' : generate_params( 5, "MSTB", 5.08, True, True),
    'MSTB_01x06_5.08mm' : generate_params( 6, "MSTB", 5.08, True, True),
    'MSTB_01x07_5.08mm' : generate_params( 7, "MSTB", 5.08, True, True),
    'MSTB_01x08_5.08mm' : generate_params( 8, "MSTB", 5.08, True, True),
    'MSTB_01x09_5.08mm' : generate_params( 9, "MSTB", 5.08, True, True),
    'MSTB_01x10_5.08mm' : generate_params(10, "MSTB", 5.08, True, True),
    'MSTB_01x11_5.08mm' : generate_params(11, "MSTB", 5.08, True, True),
    'MSTB_01x12_5.08mm' : generate_params(12, "MSTB", 5.08, True, True),
    'MSTB_01x02_5.08mm_MH' : generate_params( 2, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x03_5.08mm_MH' : generate_params( 3, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x04_5.08mm_MH' : generate_params( 4, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x05_5.08mm_MH' : generate_params( 5, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x06_5.08mm_MH' : generate_params( 6, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x07_5.08mm_MH' : generate_params( 7, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x08_5.08mm_MH' : generate_params( 8, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x09_5.08mm_MH' : generate_params( 9, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x10_5.08mm_MH' : generate_params(10, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x11_5.08mm_MH' : generate_params(11, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTB_01x12_5.08mm_MH' : generate_params(12, "MSTB", 5.08, True, True, mount_hole=True),
    'MSTBVA_01x02_5.08mm' : generate_params( 2, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x03_5.08mm' : generate_params( 3, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x04_5.08mm' : generate_params( 4, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x05_5.08mm' : generate_params( 5, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x06_5.08mm' : generate_params( 6, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x07_5.08mm' : generate_params( 7, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x08_5.08mm' : generate_params( 8, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x09_5.08mm' : generate_params( 9, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x10_5.08mm' : generate_params(10, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x11_5.08mm' : generate_params(11, "MSTBVA", 5.08, False, False),
    'MSTBVA_01x12_5.08mm' : generate_params(12, "MSTBVA", 5.08, False, False),
    'MSTBV_01x02_5.08mm' : generate_params( 2, "MSTBV", 5.08, False, True),
    'MSTBV_01x03_5.08mm' : generate_params( 3, "MSTBV", 5.08, False, True),
    'MSTBV_01x04_5.08mm' : generate_params( 4, "MSTBV", 5.08, False, True),
    'MSTBV_01x05_5.08mm' : generate_params( 5, "MSTBV", 5.08, False, True),
    'MSTBV_01x06_5.08mm' : generate_params( 6, "MSTBV", 5.08, False, True),
    'MSTBV_01x07_5.08mm' : generate_params( 7, "MSTBV", 5.08, False, True),
    'MSTBV_01x08_5.08mm' : generate_params( 8, "MSTBV", 5.08, False, True),
    'MSTBV_01x09_5.08mm' : generate_params( 9, "MSTBV", 5.08, False, True),
    'MSTBV_01x10_5.08mm' : generate_params(10, "MSTBV", 5.08, False, True),
    'MSTBV_01x11_5.08mm' : generate_params(11, "MSTBV", 5.08, False, True),
    'MSTBV_01x12_5.08mm' : generate_params(12, "MSTBV", 5.08, False, True),
    'MSTBV_01x02_5.08mm_MH' : generate_params( 2, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x03_5.08mm_MH' : generate_params( 3, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x04_5.08mm_MH' : generate_params( 4, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x05_5.08mm_MH' : generate_params( 5, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x06_5.08mm_MH' : generate_params( 6, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x07_5.08mm_MH' : generate_params( 7, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x08_5.08mm_MH' : generate_params( 8, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x09_5.08mm_MH' : generate_params( 9, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x10_5.08mm_MH' : generate_params(10, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x11_5.08mm_MH' : generate_params(11, "MSTBV", 5.08, False, True, mount_hole=True),
    'MSTBV_01x12_5.08mm_MH' : generate_params(12, "MSTBV", 5.08, False, True, mount_hole=True)
}

drill = 1.4
mount_drill = 2.4
pin_Sx = 2.1
pin_Sy = 4.2

def dimensions(num_pins, pitch, angled, flanged):
    lenght = (num_pins-1)*pitch + (3*pitch if flanged else pitch+2)
    width = 12 if angled else 8.6
    upper_to_pin = -2 if angled else -8.6+3.8
    left_to_pin = -7.5 if flanged else -3.5
    mount_hole_y = 2.5 if angled else 0.0
    mount_hole_left = [-pitch,mount_hole_y]
    mount_hole_right = [num_pins*pitch,mount_hole_y]
    return lenght, width, upper_to_pin, left_to_pin,\
        mount_hole_left, mount_hole_right

m = 'MSTB_01x02_5.00mm_MH'
to_generate = {m:all_params[m]}

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for model, params in to_generate.iteritems():

    # Through-hole type shrouded header, Top entry type
    footprint_name = params.file_name

    length, width, upper_to_pin, left_to_pin, mount_hole_left, mount_hole_right\
        = dimensions(params.num_pins, params.pin_pitch, params.angled, params.flanged)

    kicad_mod = Footprint(footprint_name)


    kicad_mod.setDescription("placeholder")
    kicad_mod.setTags("phonix contact " + model)

    # set general values
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, -3], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5, 3], layer='F.Fab'))

    #add the pads
    for p in range(params.num_pins):
        Y = 0
        X = p * params.pin_pitch

        num = p+1
        kicad_mod.append(Pad(number=num, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL,
                            at=[X, Y], size=[pin_Sx, pin_Sy], drill=drill, layers=['*.Cu', '*.Mask', '*.Paste']))
    if params.mount_hole:
        kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_left, size=[drill, drill], drill=drill, layers=['*.Mask']))
        kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_right, size=[drill, drill], drill=drill, layers=['*.Mask']))
    #add an outline around the pins

    # create silscreen
    p1=[left_to_pin,upper_to_pin]
    p2=v_add(p1,[length,width])
    kicad_mod.append(RectLine(start=p1, end=p2, layer='F.SilkS'))

    # create courtyard
    p1=v_add(p1,[-0.25,-0.25])
    p2=v_add(p2,[0.25,0.25])
    kicad_mod.append(RectLine(start=p1, end=p2, layer='F.CrtYd'))

    #kicad_mod.addRectLine()

    # y1 = -1
    # x1 = -1
    # x2 = (rows - 1) * pitch + 1
    # y2 = (pincount - 1) * pitch + 1
    #
    # if rows == 1:
    #     kicad_mod.addPolygoneLine([{'y':x1,'x':y1 + pitch},{'y':x2,'x':y1+pitch}])
    #
    # elif rows == 2:
    #     kicad_mod.addPolygoneLine([{'y':x1,'x':y1 + pitch},
    #                                {'y':x1 + pitch,'x':y1+pitch},
    #                                {'y':x1 + pitch,'x':y1},
    #                                {'y':x2,'x':y1},
    #                                {'y':x2,'x':y1+pitch}])
    #
    # kicad_mod.addPolygoneLine([
    #                            {'y':x2,'x':y1 + pitch},
    #                            {'y':x2,'x':y2 + 0.2},
    #                            {'y':x1,'x':y2 + 0.2},
    #                            {'y':x1,'x':y1 + pitch}])
    #
    # d = 0.6
    #
    # #add a keepout
    # kicad_mod.addPolygoneLine([{'y':x1-d,'x':y1-d},
    #                            {'y':x2+d,'x':y1-d},
    #                            {'y':x2+d,'x':y2+d},
    #                            {'y':x1-d,'x':y2+d},
    #                            {'y':x1-d,'x':y1-d}],"F.CrtYd",0.05)
    #
    #
    # d = 0.5
    #
    # #add a pin-1 designator
    # kicad_mod.addPolygoneLine([{'y':x1-d,'x':0},
    #                            {'y':x1-d,'x':y1-d},
    #                            {'y':0,'x':y1-d}])
    #
    # #add the model
    p3dname = packages_3d + footprint_name + ".wrl"
    kicad_mod.append(Model(filename=p3dname,
                           at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
    # kicad_mod.model_rot['z'] = 0
    # if rows == 2:
    #     kicad_mod.model_pos['y'] = -pitch * 0.5 / 25.4
    #
    # if pincount % 2 == 0: #even
    #     kicad_mod.model_pos['x'] = (pincount / 2 - 0.5) * pitch / 25.4
    # else:
    #     kicad_mod.model_pos['x'] = (pincount / 2) * pitch / 25.4
    #
    # # output kicad model
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(out_dir+footprint_name + ".kicad_mod")
