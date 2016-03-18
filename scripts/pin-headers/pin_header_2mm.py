#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

from kicad_mod import KicadMod, createNumberedPadsTHT

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf


drill = 0.8
size = 1.35
pitch = 2.00

for rows in [1,2]:
    for pincount in range(2,41): #range(1,21):

        # Through-hole type shrouded header, Top entry type
        footprint_name = 'Pin_Header_Straight_{rows:01}x{pincount:02}_Pitch2.00mm'.format(rows=rows,pincount=pincount)

        kicad_mod = KicadMod(footprint_name)
        
        if rows == 1:
            rlabel = "single"
        elif rows == 2:
            rlabel = "double"
        
        kicad_mod.setDescription("Through hole pin header, {rows}x{pincount:02}, 2.00mm pitch, ".format(rows=rows,pincount=pincount) + rlabel + " row")
        kicad_mod.setTags("pin header " + rlabel + " row")

        # set general values
        kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-5}, 'F.SilkS')
        kicad_mod.addText('value', footprint_name, {'x':0, 'y':-3}, 'F.Fab')
        
        #add the pads
        for r in range(rows):
            for p in range(pincount):
                X = r * pitch
                Y = p * pitch
                
                num = r + 1 + (p * rows)
                
                if num == 1: type = "rect"
                else: type = "circle"
                
                kicad_mod.addPad(num, "thru_hole", type, {'x':X,'y':Y}, {'x':size,'y':size}, drill, ['*.Cu', '*.Mask'])

        #add an outline around the pins
        
        y1 = -1
        x1 = -1
        x2 = (rows - 1) * pitch + 1
        y2 = (pincount - 1) * pitch + 1
        
        if rows == 1:
            kicad_mod.addPolygoneLine([{'x':x1,'y':y1 + pitch},{'x':x2,'y':y1+pitch}])
            
        elif rows == 2:
            kicad_mod.addPolygoneLine([{'x':x1,'y':y1 + pitch},
                                       {'x':x1 + pitch,'y':y1+pitch},
                                       {'x':x1 + pitch,'y':y1},
                                       {'x':x2,'y':y1},
                                       {'x':x2,'y':y1+pitch}])
        
        kicad_mod.addPolygoneLine([
                                   {'x':x2,'y':y1 + pitch},
                                   {'x':x2,'y':y2},
                                   {'x':x1,'y':y2},
                                   {'x':x1,'y':y1 + pitch}])
        
        d = 0.6
        
        #add a keepout
        kicad_mod.addPolygoneLine([{'x':x1-d,'y':y1-d},
                                   {'x':x2+d,'y':y1-d},
                                   {'x':x2+d,'y':y2+d},
                                   {'x':x1-d,'y':y2+d},
                                   {'x':x1-d,'y':y1-d}],"F.CrtYd",0.05)
        
        
        d = 0.5
        
        #add a pin-1 designator
        kicad_mod.addPolygoneLine([{'x':x1-d,'y':0},
                                   {'x':x1-d,'y':y1-d},
                                   {'x':0,'y':y1-d}])
                                   
        #add the model
        kicad_mod.model = "Pin_Headers.3dshapes/" + footprint_name + ".wrl"
        kicad_mod.model_rot['z'] = 90
        if rows == 2:
            kicad_mod.model_pos['x'] = pitch * 0.5 / 25.4
            
        if pincount % 2 == 0: #even
            kicad_mod.model_pos['y'] = -(pincount / 2 - 0.5) * pitch / 25.4
        else:
            kicad_mod.model_pos['y'] = -(pincount / 2) * pitch / 25.4
                
        # output kicad model
        f = open(footprint_name + ".kicad_mod","w")

        f.write(kicad_mod.__str__())

        f.close()
