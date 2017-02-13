#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from math import floor,ceil

from kicad_mod import KicadMod, createNumberedPadsTHT

# http://www.jst-mfg.com/product/pdf/eng/eZE.pdf

pitch = 1.5

for pincount in range(2,17):

    jst = "S{pincount:02}B-ZESK-2D".format(pincount=pincount)

    # Through-hole type shrouded header, side entry type
    footprint_name = "JST_ZE_" + jst + "_{pincount:02}x{pitch:02}mm_Angled".format(pincount=pincount, pitch=pitch)

    print(footprint_name)
    
    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST ZE series connector, " + jst + ", 1.50mm pitch, side entry through hole")
    kicad_mod.setTags('connector jst ze side horizontal angled tht through thru hole')

    #dimensions
    A = (pincount - 1) * 1.5
    B = A + 4.5

    #outline
    x1 = -1.55 - 0.7
    x2 = x1 + B

    xMid = x1 + B/2

    y2 = 3.7 + 3.65
    y1 = y2 - 7.8 - 0.2
    
    #add outline to F.Fab
    kicad_mod.addRectLine(
        {'x': x1, 'y': y1},
        {'x': x2, 'y': y2},
        'F.Fab', 0.15
        )

    #expand the outline a little bit
    out = 0.15
    x1 -= out
    x2 += out
    y1 -= out
    y2 += out

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':xMid, 'y':-2}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':xMid, 'y':9}, 'F.Fab')

    dia = 1.35
    drill = 0.7

    y_spacing = 3.70


    # create odd numbered pads
    createNumberedPadsTHT(kicad_mod, ceil(pincount/2), pitch * 2, drill, {'x':dia, 'y':dia},  increment=2)
    #create even numbered pads
    createNumberedPadsTHT(kicad_mod, floor(pincount/2), pitch * 2, drill, {'x':dia, 'y':dia}, starting=2, increment=2, y_off=y_spacing, x_off=pitch)

    #add mounting holes
    kicad_mod.addMountingHole(
        {'x': -1.55, 'y': 1.85},
        1.1
    )

    kicad_mod.addMountingHole(
        {'x': A+1.55    , 'y': 1.85},
        1.1
    )

    #draw the courtyard
    cy=0.5
    kicad_mod.addRectLine(
        {'x':x1-0.5,'y':y1-0.5},
        {'x':x2+0.5,'y':y2+0.5},
        "F.CrtYd", 0.05)

    kicad_mod.addRectLine({'x':x1,'y':y1},
                          {'x':x2,'y':y2})

    #draw the line at the bottom

    xa = xMid - A/2 + out
    xb = xMid + A/2 - out
    y3 = y2 - 1
    kicad_mod.addPolygoneLine([
        {'x':xa,'y':y2},
        {'x':xa,'y':y3},
        {'x':xb,'y':y3},
        {'x':xb,'y':y2}
    ])

    # add pin-1 marker
    D = 0.3
    L = 1.5
    pin_1 = [
        {'x': x1-D,'y': y1-D+L},
        {'x': x1-D,'y':  y1-D},
        {'x': x1-D + L,'y':  y1-D},
    ]
    
    kicad_mod.addPolygoneLine(pin_1)
    kicad_mod.addPolygoneLine(pin_1,layer='F.Fab')
    
    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")


    f.write(kicad_mod.__str__())

    f.close()
