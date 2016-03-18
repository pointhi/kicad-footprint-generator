#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from kicad_mod import KicadMod, createNumberedPadsSMD, grid

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

pitch = 1.20

manu = "Molex_Pico-EZmate"

suffix = "Angled"


for pincount in range(2,8):

    part = "78181-"

    if pincount < 6:
        part += "00"
    else:
        part += "50"
    
    part += "{0:02}".format(pincount)
    
    desc = "Molex Pico-EZmate series connector, 1.20mm pitch, side entry SMT, P/N: " + part
    tags = "connector molex pico ezmate side angled horizontal surface mount SMD SMT"

    footprint_name = "{0}_{1:02}x{2:.2f}mm_{3}".format(manu,pincount,pitch,suffix)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)
    
    kicad_mod.setAttribute('smd')

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-5}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':3.5}, 'F.Fab')
    
    #pin pad size
    pad_w = 0.7
    pad_h = 1.2  
    
    #component values
    A = (pincount - 1) * pitch
    B = A + 2.9
    
    # create pads
    createNumberedPadsSMD(kicad_mod, pincount, pitch, {'x':pad_w,'y':pad_h},-1.8875)
    
    #add mounting pads (no number)
    mpad_w = 0.7
    mpad_h = 1.0
    mpad_x = (A/2) + 0.8 + 0.7/2
    mpad_y = 1.8875

    kicad_mod.addPad('""', 'smd', 'rect', {'x':mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    kicad_mod.addPad('""', 'smd', 'rect', {'x':-mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

    D = A + 3
    
    x1 = -D/2
    y1 = -2.2
    x2 = D/2
    y2 = 2.2
    
    #line offset 
    off = 0.1
    
    x1 -= off
    y1 -= off
    
    x2 += off
    y2 += off
    
    #offset from pads
    xo = 0.5
    
    #offset of angled setction
    ao = 0.5
    
    kicad_mod.addPolygoneLine([{'x':-A/2 - pad_w/2 - xo,'y':y1},
                               {'x':x1,'y':y1},
                               {'x':x1,'y':mpad_y - mpad_h/2 - xo}])
                               
                               
    kicad_mod.addPolygoneLine([{'x':A/2 + pad_w/2 + xo,'y':y1},
                               {'x':x2,'y':y1},
                               {'x':x2,'y':mpad_y - mpad_h/2 - xo}])                               
    
    
    kicad_mod.addPolygoneLine([{'x':-mpad_x + mpad_w/2 + xo,'y':y2},
                               {'x':-A/2,'y':y2},
                               {'x':-A/2 + ao,'y':y2 - ao},
                               {'x':A/2 - ao,'y':y2-ao},
                               {'x':A/2,'y':y2},
                               {'x':mpad_x - mpad_w/2 - xo,'y':y2}])
                               
                               
    #add pin-1 marker
    
    xm = -A/2
    ym = -3
    
    m = -0.3
    
    kicad_mod.addPolygoneLine([{'x':xm,'y':ym},
                               {'x':xm - m,'y':ym + 2 * m},
                               {'x':xm + m,'y':ym + 2 * m},
                               {'x':xm,'y':ym}])
                               
    #add a courtyard
    cy = 0.5
    
    xo = 0.85
    
    cx1 = grid(-D/2 - cy)
    cy1 = grid(-3.1)
    cx2 = grid(D/2 + cy)
    cy2 = grid(2.9)
    
    kicad_mod.addRectLine({'x':cx1,'y':cy1},{'x':cx2,'y':cy2},"F.CrtYd",0.05) 
    
    """
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
                                   {'x': px-w,'y': py-w}])
    
              
   
    
    """
    kicad_mod.model = "Connectors_Molex.3dshapes/" + footprint_name + ".wrl"
    
    #shift the model along
    
    xOff = 0
    yOff = 2.1
    
    kicad_mod.model_pos['x'] = xOff / 25.4
    kicad_mod.model_pos['y'] = yOff / 25.4
    #kicad_mod.model_rot['z'] = 180
    
    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")
    
    f.write(kicad_mod.__str__())

    f.close()
