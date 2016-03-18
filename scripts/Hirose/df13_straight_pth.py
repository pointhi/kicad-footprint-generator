#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from kicad_mod import KicadMod, createNumberedPadsTHT

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

pitch = 1.25

manu = "Hirose"

suffix = "Straight"

desc = "Hirose DF13 series connector, 1.25mm pitch, top entry PTH"
tags = "connector hirose df13 top straight vertical through thru hole"

for pincount in range(2,16):

    part = "DF13-{pincount:02}P-125DSA".format(pincount=pincount)
    
    footprint_name = "{0}_{1}_{2:02}x{3:.2f}mm_{4}".format(manu,part,pincount,pitch,suffix)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':2.5}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':4}, 'F.Fab')
    
    drill = 0.6

    x_dia = 0.95
    y_dia = 1.25
    
    # create pads
    createNumberedPadsTHT(kicad_mod, pincount, pitch, drill, {'x':x_dia, 'y':y_dia})
    
    A = (pincount - 1) * pitch
    B = A + 2.9
    
    x1 = -(B-A) / 2
    y1 = -2.2
    x2 = x1 + B
    y2 = 1.2
    
    #line offset 
    off = 0.1
    
    x1 -= off
    y1 -= off
    
    x2 += off
    y2 += off
    
    #draw the main outline around the footprint
    kicad_mod.addRectLine({'x':x1,'y':y1},{'x':x2,'y':y2})
    
    #add pin-1 marker
    
    xm = 0
    ym = -2.8
    
    m = 0.3
    
    kicad_mod.addPolygoneLine([{'x':xm,'y':ym},
                               {'x':xm - m,'y':ym - 2 * m},
                               {'x':xm + m,'y':ym - 2 * m},
                               {'x':xm,'y':ym}])
                               
    #side-wall thickness S
    
    S = 0.5
    
    #bottom line
    kicad_mod.addPolygoneLine([{'x':x1,'y':0},
                               {'x':x1+S,'y':0},
                               {'x':x1+S,'y':y2-S},
                               {'x':x2-S,'y':y2-S},
                               {'x':x2-S,'y':0},
                               {'x':x2,'y':0}])
                               
    #left mark
    
    #gap g
    g = 0.75
    
    kicad_mod.addPolygoneLine([{'x':x1,'y':-g},
                               {'x':x1+S,'y':-g},
                               {'x':x1+S,'y':y1+S*1.5},
                               {'x':x1+2*S,'y':y1+S*1.5},
                               {'x':x1+2*S,'y':y1}])
    
    kicad_mod.addPolygoneLine([{'x':x2,'y':-g},
                               {'x':x2-S,'y':-g},
                               {'x':x2-S,'y':y1+S*1.5},
                               {'x':x2-2*S,'y':y1+S*1.5},
                               {'x':x2-2*S,'y':y1}])
                               
    #middle line
    kicad_mod.addPolygoneLine([{'x':x1+2*S,'y':y1+1.5*S},
                               {'x':0.2*pitch,'y':y1+1.5*S},
                               {'x':0.2*pitch,'y':y1+0.5*S},
                               {'x':0.8*pitch,'y':y1+0.5*S},
                               {'x':0.8*pitch,'y':y1+1.5*S},
                               {'x':A-0.8*pitch,'y':y1+1.5*S},
                               {'x':A-0.8*pitch,'y':y1+0.5*S},
                               {'x':A-0.2*pitch,'y':y1+0.5*S},
                               {'x':A-0.2*pitch,'y':y1+1.5*S},
                               {'x':x2-2*S,'y':y1+1.5*S}])
    
    """
    #add pictures of pins
    #pin-width w
    #pin-length l
    w = 0.32
    l = 3.5
    
    py = -2.5
    
    kicad_mod.addLine({'x':x1+T,'y':py},{'x':x2-T,'y':py})
    
    kicad_mod.addLine({'x':x1+T,'y':py+1},{'x':x2-T,'y':py+1})
    
    for p in range(pincount):
        
        px = p * pitch
        
        kicad_mod.addPolygoneLine([{'x': px,'y': py},
                                   {'x': px-w,'y': py},
                                   {'x': px-w,'y': py-l+0.25*w},
                                   {'x': px,'y': py-l},
                                   {'x': px+w,'y': py-l+0.25*w},
                                   {'x': px+w,'y': py},
                                   {'x': px,'y': py}])
    
    
    """           
    #add a courtyard
    cy = 0.5
    
    kicad_mod.addRectLine({'x':x1-cy,'y':y1-cy},{'x':x2+cy,'y':y2+cy},"F.CrtYd",0.05)
    
    kicad_mod.model = "Connectors_Hirose.3dshapes/" + footprint_name + ".wrl"
    
    #shift the model along
    
    if pincount % 2 == 0: #even
        xOff = (pincount / 2 - 0.5) * pitch
    else:
        xOff = (pincount / 2) * pitch
        
    kicad_mod.model_pos['x'] = xOff / 25.4
    kicad_mod.model_rot['z'] = 180
    
    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")
    
    f.write(kicad_mod.__str__())

    f.close()
