#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from kicad_mod import KicadMod, createNumberedPadsSMD, grid

pitch = 1.50

manu = "Molex_PicoLock"

suffix = "Angled"


for pincount in [4,6,7,8,10,12]:

    part = "504050{0:02}91".format(pincount)
    
    desc = "Molex PicoLock series connector, {0:.2f}mm pitch, side entry SMT, P/N: {1:}".format(pitch,part)
    tags = "conn molex pico lock"

    footprint_name = "{0}-{1}_{2:02}x{3:.2f}mm_{4}".format(manu,part,pincount,pitch,suffix)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)
    
    kicad_mod.setAttribute('smd')

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-5.5}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':5}, 'F.Fab')
    
    #pin pad size
    pad_w = 0.6
    pad_h = 1.0 
    
    #component values
    A = (pincount - 1) * pitch
    B = A + 5.25
    
    kicad_mod.setCenterPos({'x':0, 'y':0.2})
    
    # create pads
    createNumberedPadsSMD(kicad_mod, pincount, pitch, {'x':pad_w,'y':pad_h},-2.6)
    
    #add mounting pads (no number)
    mpad_w = 1.25
    mpad_h = 1.8
    mpad_x = A/2 + 1.7 + 1.25 / 2 + 0.1
    mpad_y = 3

    kicad_mod.addPad('""', 'smd', 'rect', {'x':mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    kicad_mod.addPad('""', 'smd', 'rect', {'x':-mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    
    x1 = -B/2
    y1 = -2.4
    x2 = B/2
    y2 = 4
    
    #line offset 
    off = 0.1
    
    x1 -= off
    y1 -= off
    
    x2 += off
    y2 += off
    
    #offset from pads
    xo = 0.5
    
    #thickness of "arms"
    t = 2.1
    
    #depth of arms
    d = 2.0
    
    kicad_mod.addPolygoneLine([{'x':-A/2 - pad_w/2 - xo,'y':y1},
                               {'x':x1,'y':y1},
                               {'x':x1,'y':mpad_y - mpad_h/2 - xo}])
                               
                               
    kicad_mod.addPolygoneLine([{'x':A/2 + pad_w/2 + xo,'y':y1},
                               {'x':x2,'y':y1},
                               {'x':x2,'y':mpad_y - mpad_h/2 - xo}])                               
    
    
    kicad_mod.addPolygoneLine([{'x':-mpad_x + mpad_w/2 + xo,'y':y2},
                               {'x':x1+t,'y':y2},
                               {'x':x1+t,'y':y2-d},
                               {'x':x2-t,'y':y2-d},
                               {'x':x2-t,'y':y2},
                               {'x':mpad_x - mpad_w/2 - xo,'y':y2}])
                               
                               
    #add pin-1 marker
    
    xm = -A/2
    ym = -3.8
    
    m = -0.3
    
    kicad_mod.addPolygoneLine([{'x':xm,'y':ym},
                               {'x':xm - m,'y':ym + 2 * m},
                               {'x':xm + m,'y':ym + 2 * m},
                               {'x':xm,'y':ym}])
                               
    #add a courtyard
    cy = 0.5
    
    xo = 0.85
    
    cx1 = grid(-B/2 - cy - 0.7)
    cy1 = grid(-3.8)
    cx2 = grid(B/2 + cy + 0.7)
    cy2 = grid(4.5)
    
    kicad_mod.addRectLine({'x':cx1,'y':cy1},{'x':cx2,'y':cy2},"F.CrtYd",0.05) 
    
    kicad_mod.model = "Connectors_Molex.3dshapes/" + footprint_name + ".wrl"
    
    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")
    
    f.write(kicad_mod.__str__())

    f.close()
