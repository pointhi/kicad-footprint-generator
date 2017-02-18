#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from kicad_mod import KicadMod, createNumberedPadsSMD, grid

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

pitch = 1.25

manu = "Hirose"

suffix = "Straight"

desc = "Hirose DF13 series connector, 1.25mm pitch, top entry SMT"
tags = "connector hirose df13 top straight vertical surface mount SMD SMT"

for pincount in range(2,16):

    part = "DF13C-{pincount:02}P-1.25V".format(pincount=pincount)
    
    footprint_name = "{0}_{1}_{2:02}x{3:.2f}mm_{4}".format(manu,part,pincount,pitch,suffix)

    print(footprint_name)
    
    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)
    
    kicad_mod.setAttribute('smd')

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-3.1}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':4.9}, 'F.Fab')
    
    #pin pad size
    pad_w = 0.7
    pad_h = 1.8
    
    kicad_mod.setCenterPos({'x':0,'y':0.4})
    
    #component values
    A = (pincount - 1) * pitch
    B = A + 2.9
    
    # create pads
    createNumberedPadsSMD(kicad_mod, pincount, pitch, {'x':pad_w,'y':pad_h},-1)
    
    #add mounting pads (no number)
    mpad_w = 1.6
    mpad_h = 2.2
    mpad_x = (B/2) + (mpad_w/2)
    mpad_y = 1.8

    kicad_mod.addPad('""', 'smd', 'rect', {'x':mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    kicad_mod.addPad('""', 'smd', 'rect', {'x':-mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

    
    A = (pincount - 1) * pitch
    B = A + 2.9 + 1.5
    
    x1 = -B/2
    y1 = 0
    x2 = B / 2
    y2 = 3.5
    
    #draw the connector outline on the F.Fab layer
    kicad_mod.addRectLine(
        {'x': x1,'y': y1},
        {'x': x2,'y': y2},
        'F.Fab', 0.15
    )
    
    #line offset 
    off = 0.15
    
    x1 -= off
    y1 -= off
    
    x2 += off
    y2 += off
    
    q = 0.75
    
    #draw the top line
    kicad_mod.addLine({'x':x1,'y':y1},{'x':-A/2-q,'y':y1})
    kicad_mod.addLine({'x':x2,'y':y1},{'x':A/2+q,'y':y1})
    
    #draw the side lines
    kicad_mod.addLine({'x':x1,'y':y1},{'x':x1,'y':0.3})
    kicad_mod.addLine({'x':x2,'y':y1},{'x':x2,'y':0.3})
    
    #draw the bottom line
    kicad_mod.addLine({'x':x1,'y':y2},{'x':x2,'y':y2})
    
    a = 0.4
    
    kicad_mod.addLine({'x':x1,'y':y2},{'x':x1,'y':y2-a})
    kicad_mod.addLine({'x':x2,'y':y2},{'x':x2,'y':y2-a})
    
    xm = -A/2- 1
    ym = -1
    
    m = 0.3
    
    kicad_mod.addPolygoneLine([{'x':xm,'y':ym},
                               {'x':xm - 2 * m,'y':ym - m},
                               {'x':xm - 2 * m,'y':ym + m},
                               {'x':xm,'y':ym}])
                               
    
    #add pictures of pins
    #pin-width w
    #pin-length l
    w = 0.25
    
    py = 2.3
    
    for p in range(pincount):
        
        px = -A/2 + p * pitch
        
        kicad_mod.addPolygoneLine([{'x': px-w,'y': py-w},
                                   {'x': px-w,'y': py+w},
                                   {'x': px+w,'y': py+w},
                                   {'x': px+w,'y': py-w},
                                   {'x': px-w,'y': py-w}], 'F.Fab')
    
              
    #add a courtyard
    cy = 0.5
    
    xo = 0.85
    
    cx1 = grid(x1-cy-xo)
    cy1 = grid(y1-cy-1.85)
    cx2 = grid(x2+cy+xo)
    cy2 = grid(y2+cy)
    
    kicad_mod.addRectLine({'x':cx1,'y':cy1},{'x':cx2,'y':cy2},"F.CrtYd",0.05) 
    
    kicad_mod.model = "Connectors_Hirose.3dshapes/" + footprint_name + ".wrl"
    
    #shift the model along
    
    xOff = 0
    yOff = -0.7
        
    kicad_mod.model_pos['x'] = xOff / 25.4
    kicad_mod.model_pos['y'] = yOff / 25.4
    
    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")
    
    f.write(kicad_mod.__str__())

    f.close()
