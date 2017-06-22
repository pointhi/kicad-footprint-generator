#!/usr/bin/env python

import sys
import os
import math

from operator import add

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","tools")) # load kicad_mod path

from KicadModTree import *  # NOQA
from drawing_tools import *
from footprint_scripts_potentiometers import *


if __name__ == '__main__':

    A = {   '05': 8.64,
            '08': 12.45,
            '20': 27.69,
            '30': 40.39,
            '40': 53.09,
            '50': 65.79,
            '60': 78.49,
            '70': 91.19
        }

    B = {   '05': 5.08,
            '08': 8.89,
            '20': 24.13,
            '30': 36.83,
            '40': 49.53,
            '50': 62.23,
            '60': 74.93,
            '70': 87.63
        }

    C = {   '05': 2.54,
            '08': 3.81,
            '20': 10.16,
            '30': 13.97,
            '40': 20.32,
            '50': 26.67,
            '60': 20.32,
            '70': 34.29
        }

    D = {   '08': 1.27,
            '20': 7.62,
            '30': 11.43,
            '40': 17.78,
            '50': 24.13,
            '60': 17.78,
            '70': 31.75
        }


    E = {   '05': 12.45,
            '08': 16.26,
            '20': 31.50,
            '30': 44.20,
            '40': 56.90,
            '50': 69.60,
            '60': 82.30,
            '70': 95.00
        }

    F = {   '01': 3.81,
            '02': 4.60
        }

    G = {   '60': 40.64,
            '70': 73.66
        }

    H = {   '60': 38.10,
            '70': 71.12
        }

    POL = { '05': [ 3],
            '08': [ 5],
            '20': [15],
            '30': [21],
            '40': [31],
            '50': [41],
            '60': [31, 63],
            '70': [53, 115]
          }

    for weld in [True, False]:
        for pol in [True, False]:
            for pcb_thickness in ['01', '02']:
                for n in ['05', '08', '20', '30', '40', '50', '60', '70']:

                    fp_name = 'MECF-' + n + '-' + pcb_thickness + '-'
                    if pol == False:
                        fp_name = fp_name + 'NP-'
                    fp_name = fp_name + 'L-DV'
                    if weld == True:
                        fp_name = fp_name + '-WT'

                    fp_name = fp_name + '_Socket'

                    kicad_mod = Footprint(fp_name)

                    description = "Highspeed card edge connector for "
                    if pcb_thickness == '01':
                        description = description + '1.6mm'
                    else:
                        description = description + '2.4mm'

                    description = description + " PCB's with " + n + " contacts "

                    if pol == True:
                        description = description + '(polarized)'
                    else:
                        description = description + '(not polarized)'

                    #set the FP description
                    kicad_mod.setDescription(description)
                    kicad_mod.setAttribute('smd')

                    tags = "conn samtec card-edge high-speed"

                    #set the FP tags
                    kicad_mod.setTags(tags)


                    # set general values
                    kicad_mod.append(Text(type='reference', text='REF**', at=[0,3.81], layer='F.SilkS'))
                    kicad_mod.append(Text(type='user', text='%R', at=[0,0], layer='F.Fab'))
                    kicad_mod.append(Text(type='value', text=fp_name, at=[0,-3.81], layer='F.Fab'))

                    top = -(F[pcb_thickness]/2.0 + 0.9)
                    bot =  (F[pcb_thickness]/2.0 + 0.9)

                    left = 0
                    right = 0
                    if weld == True:
                        left = -(E[n]/2.0 + 0.91)
                        right = (E[n]/2.0 + 0.91)
                    else:
                        left = -(A[n]/2.0 + 0.91)
                        right = (A[n]/2.0 + 0.91)


                    top_left =  [left, top]
                    bot_right = [ right, bot]

                    # create Fab (exact outline)
                    kicad_mod.append(Line(start=[left + 1.27, bot], end=[right, bot], layer='F.Fab', width=0.10))   #bot line
                    kicad_mod.append(Line(start=[left, top], end=[ right, top], layer='F.Fab', width=0.10))   #top line
                    kicad_mod.append(Line(start=[left, bot - 1.27], end=[left, top], layer='F.Fab', width=0.10))   #left line
                    kicad_mod.append(Line(start=[right, bot], end=[ right, top], layer='F.Fab', width=0.10))   #right line
                    kicad_mod.append(Line(start=[left, bot - 1.27], end=[left + 1.27, bot], layer='F.Fab', width=0.10))   #corner

                    top = top - 0.11
                    bot = bot + 0.11
                    left = left - 0.11
                    right = right + 0.11

                    # create silscreen (exact + 0.11)
                    kicad_mod.append(Line(start=[round(left, 2) + 1.27, round(bot, 2)],
                                          end=[round(right, 2), round(bot, 2)], layer='F.SilkS', width=0.12)) #bot line
                    kicad_mod.append(Line(start=[round(left, 2), round(top, 2)],
                                          end=[round(right, 2), round(top, 2)], layer='F.SilkS', width=0.12)) #top line
                    kicad_mod.append(Line(start=[round(left, 2), round(bot, 2) - 1.27],
                                          end=[round(left, 2), round(top, 2)], layer='F.SilkS', width=0.12)) #left line
                    kicad_mod.append(Line(start=[round(right, 2), round( bot, 2)],
                                          end=[round(right, 2), round(top, 2)], layer='F.SilkS', width=0.12)) #right line
                    kicad_mod.append(Line(start=[round(left, 2) + 1.27, round(bot, 2) ],
                                          end=[round(left, 2), round(bot, 2) - 1.27], layer='F.SilkS', width=0.12))   #corner

                    top = top - 0.14
                    bot = bot + 0.14
                    left = left - 0.14
                    right = right + 0.14

                    # create courtyard (exact + 0.25)
                    kicad_mod.append(RectLine(start=[round(left,2), round(top,2)],
                                          end=[round(right,2), round(bot,2)], layer='F.CrtYd', width=0.05))





                    # create pads
                    for i in range(0,int(n)):
                        start = - B[n]/2.0

                        if pol == True:
                            if (i*2+1) not in POL[n]:
                                kicad_mod.append(Pad(number=i*2 + 1    , type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[start + i*1.27, F[pcb_thickness]/2.0], size=[0.66,1.35], drill=0.0, layers=['F.Cu', 'F.Mask', 'F.Paste']))
                                kicad_mod.append(Pad(number=i*2 + 2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[start + i*1.27, - F[pcb_thickness]/2.0], size=[0.66,1.35], drill=0.0, layers=['F.Cu', 'F.Mask', 'F.Paste']))
                        else:
                            kicad_mod.append(Pad(number=i*2 + 1    , type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[start + i*1.27, F[pcb_thickness]/2.0], size=[0.66,1.35], drill=0.0, layers=['F.Cu', 'F.Mask', 'F.Paste']))
                            kicad_mod.append(Pad(number=i*2 + 2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[start + i*1.27, - F[pcb_thickness]/2.0], size=[0.66,1.35], drill=0.0, layers=['F.Cu', 'F.Mask', 'F.Paste']))



                    kicad_mod.append(Pad(number="", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[-A[n]/2.0, 0],   size=[0.0,0.0], drill=1.45, layers=['*.Cu', '*.Mask']))
                    kicad_mod.append(Pad(number="", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[A[n]/2.0, 1.0], size=[0.0,0.0], drill=1.45, layers=['*.Cu', '*.Mask']))

                    if weld == True:
                        kicad_mod.append(Pad(number="", type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[-E[n]/2.0, 0],   size=[1.5,1.5], drill=1.00, layers=['*.Cu', '*.Mask']))
                        kicad_mod.append(Pad(number="", type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[ E[n]/2.0, 0.0], size=[1.5,1.5], drill=1.00, layers=['*.Cu', '*.Mask']))

                    # output kicad model
                    #print(kicad_mod

                    # print render tree
                    #print(kicad_mod.getRenderTree())
                    #print(kicad_mod.getCompleteRenderTree())

                    # write file
                    file_handler = KicadFileHandler(kicad_mod)
                    file_handler.writeFile(fp_name + ".kicad_mod")






