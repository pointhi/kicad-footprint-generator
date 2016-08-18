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

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST EH series connector, " + jst + ", 2.50mm pitch, top entry")
    kicad_mod.setTags('connector jst eh top vertical straight')

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-3}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':5}, 'F.Fab')
    
    drill = 0.9

    dia = 1.85
    
    # create pads
    createNumberedPadsTHT(kicad_mod, pincount, pitch, drill, {'x':dia, 'y':dia})
    
    A = (pincount - 1) * pitch
    B = A + 5.0
    
    x1 = -2.5
    y1 = -1.6
    x2 = x1 + B
    y2 = y1 + 3.8
    
    
    #line offset 
    off = 0.2
    
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
    
    xm = 0
    ym = 2.75
    
    m = 0.3
    
    kicad_mod.addPolygoneLine([{'x':xm,'y':ym},
                               {'x':xm - m,'y':ym + 2 * m},
                               {'x':xm + m,'y':ym + 2 * m},
                               {'x':xm,'y':ym}])
                               
    #add a courtyard
    cy = 0.5
    
    kicad_mod.addRectLine({'x':x1-cy,'y':y1-cy},{'x':x2+cy,'y':y2+cy},"F.CrtYd",0.05)
    
    kicad_mod.model = "Connectors_JST.3dshapes/" + footprint_name + ".wrl"
    
    #shift the model along
    
    if pincount % 2 == 0: #even
        xOff = (pincount / 2 - 0.5) * pitch
    else:
        xOff = (pincount / 2) * pitch
        
    kicad_mod.model_pos['x'] = xOff / 25.4
    
    # output kicad model
    f = open(footprint_name + ".kicad_mod","w")
    

    f.write(kicad_mod.__str__())

    f.close()
