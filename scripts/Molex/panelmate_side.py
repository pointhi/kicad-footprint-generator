#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from kicad_mod import KicadMod, createNumberedPadsSMD, grid

pitch = 1.25

manu = "Molex"
series = "Panelmate"

suffix = "Angled"


for pincount in [2,3,4,5,6,7,8,9,10,12,14,15,18,20,30]:

    part = "53780-{0:02}70".format(pincount)
    
    desc = "{0:} {1}".format(manu,series)
    desc += " series connector, {0:.2f}mm pitch, side entry SMT, P/N: {1:}".format(pitch,part)
    tags = "conn molex panelmate"

    footprint_name = "{0}-{1}_{2:02}x{3:.2f}mm_{4}".format(manu+"_"+series,part,pincount,pitch,suffix)

    print(footprint_name)
    
    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)
    
    kicad_mod.setAttribute('smd')

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-3}, 'F.SilkS')
    #kicad_mod.addText('user', '%R', {'x':0, 'y':-3}, 'F.Fab')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':7}, 'F.Fab')
    
    #pin pad size
    pad_w = 0.8
    pad_h = 1.9
    
    #component values
    A = (pincount - 1) * pitch
    B = A + 6.4
    
    kicad_mod.setCenterPos({'x':0, 'y':1.49})
    
    # create pads
    createNumberedPadsSMD(kicad_mod, pincount, pitch, {'x':pad_w,'y':pad_h},-1.9/2)
    
    #add mounting pads (no number)
    mpad_w = 1.3
    mpad_h = 3.35
    mpad_x = A/2 + 2.2 + 1.3 / 2
    mpad_y = 2.25 + 3.35 / 2 + 0.005

    kicad_mod.addPad('""', 'smd', 'rect', {'x':mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    kicad_mod.addPad('""', 'smd', 'rect', {'x':-mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    
    x1 = -B/2
    y1 = -0.4
    x2 = B/2
    y2 = 5.5
    
    #thickness of "arms"
    t = 1.9
    
    #depth of arms
    d = 1.0
    
    #angle of arms
    a = 0.4
    
    #add outline to F.Fab layer
    kicad_mod.addPolygoneLine([
        {'x': x2, 'y': y1},
        {'x': x1, 'y': y1},
        {'x': x1, 'y': y2},
        {'x': x1 + t, 'y': y2},
        {'x': x1 + t + a, 'y': y2 - d},
        {'x': x2 - t - a, 'y': y2 - d},
        {'x': x2 - t, 'y': y2},
        {'x': x2, 'y': y2},
        {'x': x2, 'y': y1},
        ], 'F.Fab', 0.15
    )
    
    #line offset 
    off = 0.15
    
    x1 -= off
    y1 -= off
    
    x2 += off
    y2 += off
    
    #offset from pads
    xo = 0.5
    
    t += 0.25
    
    
    #left SilkS
    kicad_mod.addPolygoneLine([{'x':-A/2 - pad_w/2 - xo,'y':y1},
                               {'x':x1,'y':y1},
                               {'x':x1,'y':mpad_y - mpad_h/2 - xo}])
                               
              
    #right SilkS
    kicad_mod.addPolygoneLine([{'x':A/2 + pad_w/2 + xo,'y':y1},
                               {'x':x2,'y':y1},
                               {'x':x2,'y':mpad_y - mpad_h/2 - xo}])                               
    
    
    #bottom SilkS
    kicad_mod.addPolygoneLine([{'x':-mpad_x + mpad_w/2 + xo,'y':y2},
                               {'x':x1+t,'y':y2},
                               {'x':x1+t+a,'y':y2-d},
                               {'x':x2-t-a,'y':y2-d},
                               {'x':x2-t,'y':y2},
                               {'x':mpad_x - mpad_w/2 - xo,'y':y2}])
                               
                               
    #add pin-1 marker
    
    xm = -A/2 - pad_w/2 - 0.5
    ym = -1.9/2 - 0.3
    
    m = 0.6

    pin1 = [
            {'x':xm,'y':ym},
            {'x':xm - m,'y':ym - m / 2},
            {'x':xm - m,'y':ym + m / 2},
            {'x':xm,'y':ym}]
            
    kicad_mod.addPolygoneLine(pin1)
    kicad_mod.addPolygoneLine(pin1,'F.Fab')
    
                               
    #add a courtyard
    cy = 0.5
    
    xo = 0.85
    
    cx1 = grid(-B/2 - cy - 0.6) + 0.25
    cy1 = -2.625 + 0.015 + 0.2
    cx2 = grid(B/2 + cy + 0.6) - 0.25
    cy2 = 4.5 + 1.90 - 0.05 / 2 - 0.085 - 0.1
    
    kicad_mod.addRectLine({'x':cx1,'y':cy1},{'x':cx2,'y':cy2},"F.CrtYd",0.05) 
    
    kicad_mod.model = "Connectors_Molex.3dshapes/" + footprint_name + ".wrl"
    
    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")
    
    f.write(kicad_mod.__str__())

    f.close()
