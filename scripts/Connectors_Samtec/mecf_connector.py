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

    K = {   '05': 8.10,
            '08': 11.91,
            '20': 27.15,
            '30': 39.85,
            '40': 52.55,
            '50': 65.25,
            '60': 77.95,
            '70': 90.65
        }

    L = {   '05': 2.79,
            '08': 4.06,
            '20': 10.41,
            '30': 14.22,
            '40': 20.57,
            '50': 26.92,
            '60': 20.57,
            '70': 34.54
        }

    M = {   '60': 40.89,
            '70': 73.91
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


    for pol in [True, False]:
        for n in ['05', '08', '20', '30', '40', '50', '60', '70']:

            fp_name = 'MECF-' + n + '-0_-'
            if pol == False:
                fp_name = fp_name + 'NP-'
            fp_name = fp_name + 'L-DV'


            fp_name = fp_name + '_Edge'

            kicad_mod = Footprint(fp_name)

            description = "Highspeed card edge connector for PCB's with " + n + " contacts "

            if pol == True:
                description = description + '(polarized)'
            else:
                description = description + '(not polarized)'

            kicad_mod.setAttribute('virtual')

            #set the FP description
            kicad_mod.setDescription(description)

            tags = "conn samtec card-edge high-speed"

            #set the FP tags
            kicad_mod.setTags(tags)


            # set general values
            kicad_mod.append(Text(type='reference', text='REF**', at=[0,-6.35], layer='F.SilkS'))
            kicad_mod.append(Text(type='user', text='%R', at=[0,-2.54], layer='F.Fab'))
            kicad_mod.append(Text(type='value', text=fp_name, at=[0,-3.81], layer='F.Fab'))

            top = -(5.0)
            bot =  (5.0)

            left = -(K[n]/2.0)
            right = (K[n]/2.0)


            top_left =  [left, top]
            bot_right = [ right, bot]

            # create Fab Back(exact outline)
            kicad_mod.append(Line(start=[left + 1.27, bot], end=[right, bot], layer='F.Fab', width=0.10))   #bot line
            kicad_mod.append(Line(start=[left, top], end=[ right, top], layer='F.Fab', width=0.10))   #top line
            kicad_mod.append(Line(start=[left, bot - 1.27], end=[left, top], layer='F.Fab', width=0.10))   #left line
            kicad_mod.append(Line(start=[right, bot], end=[ right, top], layer='F.Fab', width=0.10))   #right line
            kicad_mod.append(Line(start=[left, bot - 1.27], end=[left + 1.27, bot], layer='F.Fab', width=0.10))   #corner

            # create Fab Front(exact outline)
            kicad_mod.append(Line(start=[left, bot], end=[right, bot], layer='B.Fab', width=0.10))   #bot line
            kicad_mod.append(Line(start=[left, top], end=[ right, top], layer='B.Fab', width=0.10))   #top line
            kicad_mod.append(Line(start=[left, bot ], end=[left, top], layer='B.Fab', width=0.10))   #left line
            kicad_mod.append(Line(start=[right, bot], end=[ right, top], layer='B.Fab', width=0.10))   #right line


            top = top - 0.11
            #bot = bot + 0.11
            left = left - 0.11
            right = right + 0.11

            # create silscreen Back(exact + 0.11)
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

            # create silscreen Front(exact + 0.11)
            kicad_mod.append(Line(start=[round(left, 2), round(bot, 2)],
                                  end=[round(right, 2), round(bot, 2)], layer='B.SilkS', width=0.12)) #bot line
            kicad_mod.append(Line(start=[round(left, 2), round(top, 2)],
                                  end=[round(right, 2), round(top, 2)], layer='B.SilkS', width=0.12)) #top line
            kicad_mod.append(Line(start=[round(left, 2), round(bot, 2)],
                                  end=[round(left, 2), round(top, 2)], layer='B.SilkS', width=0.12)) #left line
            kicad_mod.append(Line(start=[round(right, 2), round( bot, 2)],
                                  end=[round(right, 2), round(top, 2)], layer='B.SilkS', width=0.12)) #right line

            top = top - 0.14
            #bot = bot + 0.14
            left = left - 0.14
            right = right + 0.14

            # create courtyard (exact + 0.25)
            kicad_mod.append(RectLine(start=[round(left, 2), round(top,2) ],
                                  end=[round(right, 2) , round(bot, 2)], layer='F.CrtYd', width=0.05))
            kicad_mod.append(RectLine(start=[round(left,2), round(top,2) ],
                                  end=[round(right, 2), round(bot,2) ], layer='B.CrtYd', width=0.05))




            top = -5.0
            bot =  5.0
            slot_height = 7.0


            ## create cutout
            kicad_mod.append(Line(start=[-K[n]/2.0, bot, 2],
                                  end=[-K[n]/2.0, top, 2], layer='Edge.Cuts', width=0.12)) #left line
            kicad_mod.append(Line(start=[K[n]/2.0, bot, 2],
                                  end=[K[n]/2.0, top], layer='Edge.Cuts', width=0.12)) #right line


            ## grid ends
            nextGrid = math.ceil((K[n]/2.0)/0.25 + 1.0) * 0.25
            kicad_mod.append(Line(start=[-nextGrid, top, 2],
                end=[-K[n]/2.0, top, 2], layer='Edge.Cuts', width=0.12)) #left line
            kicad_mod.append(Line(start=[+nextGrid, top, 2],
                end=[K[n]/2.0, top], layer='Edge.Cuts', width=0.12)) #right line



            if pol == True:   # Cutouts

                kicad_mod.append(Line(start=[-K[n]/2.0, bot],
                                      end=[-K[n]/2.0+L[n]-1.24/2.0, bot], layer='Edge.Cuts', width=0.12)) #bot line

                kicad_mod.append(Line(start=[-K[n]/2.0+L[n]-1.24/2.0, bot],
                                      end=[-K[n]/2.0+L[n]-1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=0.12)) #up
                kicad_mod.append(Line(start=[-K[n]/2.0+L[n]+1.24/2.0, bot],
                                      end=[-K[n]/2.0+L[n]+1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=0.12)) #down
                kicad_mod.append(Line(start=[-K[n]/2.0+L[n]-1.24/2.0, bot - slot_height],
                                      end=[-K[n]/2.0+L[n]+1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=0.12)) #cut

                if n in ['60','70']:
                    kicad_mod.append(Line(start=[-K[n]/2.0+L[n]+1.24/2.0, bot],
                                      end=[-K[n]/2.0+M[n]-1.24/2.0, bot], layer='Edge.Cuts', width=0.12)) #bot line

                    kicad_mod.append(Line(start=[-K[n]/2.0+M[n]-1.24/2.0, bot],
                                      end=[-K[n]/2.0+M[n]-1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=0.12)) #up
                    kicad_mod.append(Line(start=[-K[n]/2.0+M[n]+1.24/2.0, bot],
                                      end=[-K[n]/2.0+M[n]+1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=0.12)) #down
                    kicad_mod.append(Line(start=[-K[n]/2.0+M[n]-1.24/2.0, bot - slot_height],
                                      end=[-K[n]/2.0+M[n]+1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=0.12)) #cut

                    kicad_mod.append(Line(start=[-K[n]/2.0+M[n]+1.24/2.0, bot],
                                      end=[K[n]/2.0, bot], layer='Edge.Cuts', width=0.12)) #bot line
                else:
                    kicad_mod.append(Line(start=[-K[n]/2.0+L[n]+1.24/2.0, bot],
                                      end=[K[n]/2.0, bot], layer='Edge.Cuts', width=0.12)) #bot line

            else:
                kicad_mod.append(Line(start=[-K[n]/2.0, bot],
                                      end=[K[n]/2.0, bot], layer='Edge.Cuts', width=0.12)) #bot line



            # create pads
            for i in range(0,int(n)):
                start = - K[n]/2.0 + 1.52

                if pol == True:
                    if (i*2+1) not in POL[n]:
                        kicad_mod.append(Pad(number=i*2 + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[start + i*1.27, bot - 2.0 - 0.5], size=[0.56,4.00], drill=0.0, layers=['F.Cu', 'F.Mask', 'F.Paste']))
                        kicad_mod.append(Pad(number=i*2 + 2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[start + i*1.27, bot - 2.0 - 0.5], size=[0.56,4.00], drill=0.0, layers=['B.Cu', 'B.Mask', 'B.Paste']))
                else:
                    kicad_mod.append(Pad(number=i*2 + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[start + i*1.27, bot - 2.0 - 0.5], size=[0.56,4.00], drill=0.0, layers=['F.Cu', 'F.Mask', 'F.Paste']))
                    kicad_mod.append(Pad(number=i*2 + 2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[start + i*1.27, bot - 2.0 - 0.5], size=[0.56,4.00], drill=0.0, layers=['B.Cu', 'B.Mask', 'B.Paste']))



            # output kicad model
            #print(kicad_mod

            # print render tree
            #print(kicad_mod.getRenderTree())
            #print(kicad_mod.getCompleteRenderTree())

            # write file
            file_handler = KicadFileHandler(kicad_mod)
            file_handler.writeFile(fp_name + ".kicad_mod")






