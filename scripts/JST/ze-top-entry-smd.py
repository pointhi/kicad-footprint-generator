#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from math import floor,ceil

from kicad_mod import KicadMod, createNumberedPadsSMD

# http://www.jst-mfg.com/product/pdf/eng/eZE.pdf

#ZE connector, top-entry SMD

pitch = 1.5

for pincount in range(2,17):

    jst = "BM{pincount:02}B-ZESS-TBT".format(pincount=pincount)

    # Through-hole type shrouded header, side entry type
    footprint_name = "JST_ZE_" + jst + "_{pincount:02}x{pitch:02}mm_Straight".format(pincount=pincount, pitch=pitch)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setAttribute('smd') #this is an SMD part111one
    desc = "JST ZE series connector, " + jst + ", 1.50mm pitch, top entry surface mount"
    kicad_mod.setDescription(desc)
    kicad_mod.setTags('connector jst ze top vertical straight smt surface mount')

    #dimensions
    A = (pincount - 1) * 1.5
    B = A + 6
    
    #y-coords calculated based on drawing in datasheet
    #middle point of pads
    py = -6.7
    #middle point of mechanical pads
    my = -1.65
    
    #size of mechanical pads
    mw = 2.0
    mh = 3.3
    #x-pos of mechanical pads
    mx = A/2 + 1.7 + 1.8/2
    
    #middle point of connector
    ymid = (py + my) / 2
    
    kicad_mod.setCenterPos({'x': 0,'y': ymid})
    
    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-8.5 - 0.675}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':2}, 'F.Fab')
    
    #outline
    x1 = -B / 2
    x2 =  B / 2
    
    y2 = -0.4
    y1 = y2 - 5.8

    #expand the outline a little bit
    out = 0.2
    x1 -= out
    x2 += out
    y1 -= out
    y2 += out

    #pad size
    pw = 0.9
    ph = 2.5
    
    #create dem pads
    createNumberedPadsSMD(kicad_mod, pincount, -pitch, {'x': pw,'y': ph}, py)

    #create some sweet, sweet mechanical pads
    kicad_mod.addMountingPad(
    {'x': mx, 'y': my},
    {'x': mw, 'y': mh}
    )
    
    kicad_mod.addMountingPad(
    {'x': -mx, 'y': my},
    {'x': mw, 'y': mh}
    )
    
    #add pin-1 designation
    xm = A/2
    ym = py - ph/2 - 0.5
    
    m = 0.3
    
    kicad_mod.addPolygoneLine([
    {'x': xm,'y': ym},
    {'x': xm + m,'y': ym - 2*m},
    {'x': xm - m,'y': ym - 2*m},
    {'x': xm,'y': ym},
    ])
    
    #wall thickness t
    t = 0.8
    #line offset from pads o
    o = 0.5
    xo = A/2 + pw/2 + o #horizontal distance from numbered pads
    yo = my - mh/2 - o
    #draw left-hand line
    kicad_mod.addPolygoneLine([
    {'x': -xo,'y': y1},
    {'x': x1,'y': y1},
    {'x': x1,'y': yo},
    {'x': x1+t,'y': yo},
    {'x': x1+t,'y': y1+t},
    {'x': -xo,'y': y1+t},
    {'x': -xo,'y': y1},
    ])
    #draw right-hand line
    kicad_mod.addPolygoneLine([
    {'x': xo,'y': y1},
    {'x': x2,'y': y1},
    {'x': x2,'y': yo},
    {'x': x2-t,'y': yo},
    {'x': x2-t,'y': y1+t},
    {'x': xo,'y': y1+t},
    {'x': xo,'y': y1},
    ])
    
    #draw bottom line
    xa = -A/2 + o
    xb =  A/2 - o
    
    xo = mx - mw/2 - o
    
    #boss thickness b
    b = 1.5
    
    kicad_mod.addRectLine(
    {'x': -xo, 'y': y2 - b},
    {'x':  xo, 'y': y2}
    )
    
    #inner rect
    #rect thickness r
    r = 0.4
    kicad_mod.addRectLine(
    {'x': xa+r,'y': y2-b+r},
    {'x': xb-r,'y': y2-r})
    
    #left hand wall
    kicad_mod.addLine(
    {'x':  xa,'y': y2-b},
    {'x':  xa,'y': y2}
    )
    
    #right hand wall
    kicad_mod.addLine(
    {'x':  xb,'y': y2-b},
    {'x':  xb,'y': y2}
    )
    
    #add a "slot" for each of the pins
    for i in range(pincount):
        x = -A/2 + i * pitch
        
        #width of each pin
        w = 0.15
        
        ya = py + ph/2 + 0.6
        yb = y2 - b - 0.5
        
        kicad_mod.addRectLine(
        {'x': x-w,'y': ya},
        {'x': x+w,'y': yb}
        )
    
    
    #draw the courtyard
    cx2 = mx + mw/2 + 0.5
    cx1 = -cx2
    cy1 = -8.3 + 0.025
    cy2 = 0.5 - 0.025
    
    cy=0.5
    kicad_mod.addRectLine(
        {'x':cx1,'y':cy1},
        {'x':cx2,'y':cy2},
        "F.CrtYd", 0.05)
        
    

    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")


    f.write(kicad_mod.__str__())

    f.close()
