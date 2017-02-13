#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from kicad_mod import KicadMod, createNumberedPadsTHT

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

pitch = 2.50

for pincount in range(2,16):

    jst = "B{pincount:02}B-EH-A".format(pincount=pincount)
    
    # Through-hole type shrouded header, Top entry type
    footprint_name = "JST_EH_" + jst + "_{pincount:02}x2.50mm_Straight".format(pincount=pincount)
    
    print(footprint_name)
    
    A = (pincount - 1) * pitch
    B = A + 5.0

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST EH series connector, " + jst + ", 2.50mm pitch, top entry")
    kicad_mod.setTags('connector jst eh top vertical straight')

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-3}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':A/2, 'y':3.5}, 'F.Fab')
    
    drill = 0.9

    dia = 1.85
    
    # create pads
    createNumberedPadsTHT(kicad_mod, pincount, pitch, drill, {'x':dia, 'y':dia})
    
   
    
    x1 = -2.5
    y1 = -1.6
    x2 = x1 + B
    y2 = y1 + 3.8
    
    #draw the main outline on F.Fab layer
    kicad_mod.addRectLine({'x':x1,'y':y1},{'x':x2,'y':y2},'F.Fab',0.15)
    
    #line offset 
    off = 0.15
    
    x1 -= off
    y1 -= off
    
    x2 += off
    y2 += off
    
    #draw the main outline around the footprint
    kicad_mod.addRectLine({'x':x1,'y':y1},{'x':x2,'y':y2})
    
    T = 0.5
    
    #add top line
    kicad_mod.addPolygoneLine([{'x': x1,'y': 0},
                               {'x': x1 + T,'y': 0},
                               {'x': x1 + T,'y': y1 + T},
                               {'x': x2 - T,'y': y1 + T},
                               {'x': x2 - T,'y': 0},
                               {'x': x2,'y':0}])

    #add bottom line (left)
    kicad_mod.addPolygoneLine([{'x':x1,'y':y2-3*T},
                               {'x':x1+2*T,'y':y2-3*T},
                               {'x':x1+2*T,'y':y2}])

    #add bottom line (right)
    kicad_mod.addPolygoneLine([{'x':x2,'y':y2-3*T},
                               {'x':x2-2*T,'y':y2-3*T},
                               {'x':x2-2*T,'y':y2}])                               
                               
    #add pin-1 marker
    D = 0.3
    L = 2.5
    pin = [
        {'x': x1-D,'y': y2+D-L},
        {'x': x1-D,'y': y2+D},
        {'x': x1-D+L,'y': y2+D},
    ]
    
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
