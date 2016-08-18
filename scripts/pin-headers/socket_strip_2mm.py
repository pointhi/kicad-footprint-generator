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
        footprint_name = 'Socket_Strip_Straight_{rows:01}x{pincount:02}_Pitch2.00mm'.format(rows=rows,pincount=pincount)

        kicad_mod = KicadMod(footprint_name)
        
        if rows == 1:
            rlabel = "single"
        elif rows == 2:
            rlabel = "double"
        
        kicad_mod.setDescription("Through hole socket strip, {rows}x{pincount:02}, 2.00mm pitch, ".format(rows=rows,pincount=pincount) + rlabel + " row")
        kicad_mod.setTags("socket strip " + rlabel + " row")

        # set general values
        kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-3}, 'F.SilkS')
        kicad_mod.addText('value', footprint_name, {'x':0, 'y':-5}, 'F.Fab')
        
        #add the pads
        for r in range(rows):
            for p in range(pincount):
            
                
                Y = r * pitch
                X = p * pitch
                
                num = r + 1 + (p * rows)
                
                if (num == 1): type = "rect"
                else: type = "circle"
                
                kicad_mod.addPad(num, "thru_hole", type, {'x':X,'y':Y}, {'x':size,'y':size}, drill, ['*.Cu', '*.Mask'])

        #add an outline around the pins
        
        y1 = -1
        x1 = -1
        x2 = (rows - 1) * pitch + 1
        y2 = (pincount - 1) * pitch + 1
        
        if rows == 1:
            kicad_mod.addPolygoneLine([{'y':x1,'x':y1 + pitch},{'y':x2,'x':y1+pitch}])
            
        elif rows == 2:
            kicad_mod.addPolygoneLine([{'y':x1,'x':y1 + pitch},
                                       {'y':x1 + pitch,'x':y1+pitch},
                                       {'y':x1 + pitch,'x':y1},
                                       {'y':x2,'x':y1},
                                       {'y':x2,'x':y1+pitch}])
        
        kicad_mod.addPolygoneLine([
                                   {'y':x2,'x':y1 + pitch},
                                   {'y':x2,'x':y2 + 0.2},
                                   {'y':x1,'x':y2 + 0.2},
                                   {'y':x1,'x':y1 + pitch}])
        
        d = 0.6
        
        #add a keepout
        kicad_mod.addPolygoneLine([{'y':x1-d,'x':y1-d},
                                   {'y':x2+d,'x':y1-d},
                                   {'y':x2+d,'x':y2+d},
                                   {'y':x1-d,'x':y2+d},
                                   {'y':x1-d,'x':y1-d}],"F.CrtYd",0.05)
        
        
        d = 0.5
        
        #add a pin-1 designator
        kicad_mod.addPolygoneLine([{'y':x1-d,'x':0},
                                   {'y':x1-d,'x':y1-d},
                                   {'y':0,'x':y1-d}])
                                   
        #add the model
        kicad_mod.model = "Socket_Strips.3dshapes/" + footprint_name + ".wrl"
        kicad_mod.model_rot['z'] = 0
        if rows == 2:
            kicad_mod.model_pos['y'] = -pitch * 0.5 / 25.4
            
        if pincount % 2 == 0: #even
            kicad_mod.model_pos['x'] = (pincount / 2 - 0.5) * pitch / 25.4
        else:
            kicad_mod.model_pos['x'] = (pincount / 2) * pitch / 25.4
                
        # output kicad model
        f = open(footprint_name + ".kicad_mod","w")

        f.write(kicad_mod.__str__())

        f.close()
