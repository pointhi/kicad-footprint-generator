#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from kicad_mod import KicadMod, createNumberedPadsTHT

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

pitch = 2.50

for pincount in range(2,16):

    jst = "S{pincount:02}B-EH".format(pincount=pincount)
    
    # Through-hole type shrouded header, side entry type
    footprint_name = "JST_EH_" + jst + "_{pincount:02}x2.50mm_Angled".format(pincount=pincount)
    
    print(footprint_name)
    
    A = (pincount - 1) * pitch
    B = A + 5.0

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST EH series connector, " + jst + ", 2.50mm pitch, side entry")
    kicad_mod.setTags('connector jst eh side horizontal angled')

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':3}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':A/2, 'y':-8}, 'F.Fab')
    
    drill = 0.9

    dia = 1.85
    
    # create pads
    createNumberedPadsTHT(kicad_mod, pincount, pitch, drill, {'x':dia, 'y':dia})
    
    x1 = -2.5
    y1 = -6.7
    x2 = x1 + B
    y2 = 1.5
    
    #draw the main outline around the footprint
    kicad_mod.addRectLine({'x':x1,'y':y1},{'x':x2,'y':y2},'F.Fab',0.15)
    
    #line offset 
    off = 0.15
    
    x1 -= off
    y1 -= off
    
    x2 += off
    y2 += off
    
    
    T = 1.5
    
    y3 = y2 - 2.2
    
    kicad_mod.addPolygoneLine([{'x':x1+T,'y':y3},
                               {'x':x1+T,'y':y2},
                               {'x':x1,'y':y2},
                               {'x':x1,'y':y1},
                               {'x':x2,'y':y1},
                               {'x':x2,'y':y2},
                               {'x':x2-T,'y':y2},
                               {'x':x2-T,'y':y3}])
    
    kicad_mod.addPolygoneLine([{'x':x1,'y':y1+T},
                               {'x':x1+T,'y':y1+T},
                               {'x':x1+T,'y':y3},
                               {'x':x1,'y':y3}])
                               
    kicad_mod.addPolygoneLine([{'x':x2,'y':y1+T},
                           {'x':x2-T,'y':y1+T},
                           {'x':x2-T,'y':y3},
                           {'x':x2,'y':y3}])
                           
    
    
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
    
    #add pin-1 marker
    
    xm = 0
    ym = 1.5
    
    m = 0.3
    
    pin = [{'x':xm,'y':ym},
           {'x':xm - m,'y':ym + 2 * m},
           {'x':xm + m,'y':ym + 2 * m},
           {'x':xm,'y':ym}]
    kicad_mod.addPolygoneLine(pin)
    kicad_mod.addPolygoneLine(pin,layer='F.Fab')
                               
    #add a courtyard
    cy = 0.5
    
    kicad_mod.addRectLine({'x':x1-cy,'y':y1-cy},{'x':x2+cy,'y':y2+cy},"F.CrtYd",0.05)
    
    kicad_mod.model = "Connectors_JST.3dshapes/" + footprint_name + ".wrl"
    
    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")
    

    f.write(kicad_mod.__str__())

    f.close()
