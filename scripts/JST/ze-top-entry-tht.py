#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from math import floor,ceil

from kicad_mod import KicadMod, createNumberedPadsTHT

# http://www.jst-mfg.com/product/pdf/eng/eZE.pdf

#ZE connector, top-entry THT, NO BOSS

pitch = 1.5

for pincount in range(17):

    for boss in [True, False]:
    
        if boss:
            suffix="1D"
            minPins = 2
        else:
            suffix="D"
            minPins=3
            
        if pincount < minPins:
            continue
            
        jst = "B{pincount:02}B-ZESK-{suff}".format(pincount=pincount,suff=suffix)

        # Through-hole type shrouded header, side entry type
        footprint_name = "JST_ZE_" + jst + "_{pincount:02}x{pitch:02}mm_Straight".format(pincount=pincount, pitch=pitch)

        print(footprint_name)
        kicad_mod = KicadMod(footprint_name)
        desc = "JST ZE series connector, " + jst + ", 1.50mm pitch, top entry through hole"
        
        if boss:
            desc += " with boss"
        kicad_mod.setDescription(desc)
        kicad_mod.setTags('connector jst ze top vertical straight tht through thru hole')

        #dimensions
        A = (pincount - 1) * 1.5
        B = A + 4.5

        #outline
        x1 = -1.55 - 0.7
        x2 = x1 + B

        xMid = x1 + B/2

        y2 = 0.65
        y1 = y2 - 5.75
        
        #add outline to F.Fab
        kicad_mod.addRectLine(
            {'x': x1, 'y': y1},
            {'x': x2, 'y': y2},
            'F.Fab', 0.15
            )

        #expand the outline a little bit
        out = 0.15
        x1 -= out
        x2 += out
        y1 -= out
        y2 += out

        # set general values
        kicad_mod.addText('reference', 'REF**', {'x':xMid, 'y':2}, 'F.SilkS')
        kicad_mod.addText('value', footprint_name, {'x':xMid, 'y':-6.5}, 'F.Fab')

        dia = 1.3
        drill = 0.7

        y_spacing = -2.0


        # create odd numbered pads
        createNumberedPadsTHT(kicad_mod, ceil(pincount/2), pitch * 2, drill, {'x':dia, 'y':dia},  increment=2)
        
        #create even numbered pads
        createNumberedPadsTHT(kicad_mod, floor(pincount/2), pitch * 2, drill, {'x':dia, 'y':dia}, starting=2, increment=2, y_off=y_spacing, x_off=pitch)

        #add mounting hole (only for the -1D option which has the boss)
        if boss:
            kicad_mod.addMountingHole(
            {'x': -1.65, 'y': -3.8},
            1.1
        )

        #draw the courtyard
        cy=0.5
        kicad_mod.addRectLine(
            {'x':x1-0.5,'y':y1-0.5},
            {'x':x2+0.5,'y':y2+0.5},
            "F.CrtYd", 0.05)

        kicad_mod.addRectLine({'x':x1,'y':y1},
                              {'x':x2,'y':y2})

        #draw the line at the top

        #thicknes t of sidewalls
        t = 0.8
        xa = xMid - A/2 - 0.25 + out
        xb = xMid + A/2 + 0.25 - out
        y3 = y1 + 1.7
        
        q = 0.4 #inner rect offset
        
        #outer rect
        kicad_mod.addRectLine(
            {'x': xa,'y': y1},
            {'x': xb,'y': y3}
            )
            
        #inner rect
        kicad_mod.addRectLine(
            {'x': xa+q,'y': y1+q},
            {'x': xb-q,'y': y3-q}
            )
        
        #left side
        if not boss:
            kicad_mod.addPolygoneLine([
                {'x': xa,'y': y3},
                {'x': x1+t,'y':y3},
                {'x': x1+t,'y':y2-t},
                {'x': -1,'y':y2-t},
            ])
        else: #boss were declared
            kicad_mod.addLine(
                {'x': xa,'y': y3},
                {'x': -0.9,'y': y3}
                )
                
            kicad_mod.addPolygoneLine([
                {'x': x1+t,'y': -3},
                {'x': x1+t,'y': y2-t},
                {'x': -1,'y': y2-t},
            ])
        #right side
        
        if pincount %2 == 0: #even number of pins
            xEnd = (pincount / 2 - 1) * (2 * pitch) + 1
        else:
            xEnd = floor(pincount / 2) * (2 * pitch) + 1
        
        kicad_mod.addPolygoneLine([
            {'x': xb,'y': y3},
            {'x': x2-t,'y': y3},
            {'x': x2-t,'y': y2-t},
            {'x': xEnd,'y': y2-t},
        ])
        
        #draw lines between pads
        for i in range(0, ceil(pincount/2) - 1):
        
            X1 = i * 2 * pitch + 1
            X2 = (i + 1) * 2 * pitch - 1
            kicad_mod.addLine(
                {'x': X1,'y': y2-t},
                {'x': X2,'y': y2-t},
                )
                
        #draw the 'vertical' lines where the actual pinny bits go
        
        #width of each slot w
        w = 0.15
        #clearance distance d
        d = 0.3
        for i in range(pincount):
            
            x = i * pitch
            
            Y1 = y3 + d
            Y2 = -dia/2 - d
            
            if i%2 == 1: #even pins are at 'odd' locations
                    
                Y2 += y_spacing
                
                #draw the top section
                kicad_mod.addPolygoneLine([
                {'x': x-w,'y': Y2},
                {'x': x-w,'y': Y1},
                {'x': x+w,'y': Y1},
                {'x': x+w,'y': Y2}
                ])
                
                #draw the bottom section
                Y1 = Y2 + 2 * d + dia
                Y2 = y2 - t - d
                
                kicad_mod.addPolygoneLine([
                {'x': x-w,'y': Y1},
                {'x': x-w,'y': Y2},
                {'x': x+w,'y': Y2},
                {'x': x+w,'y': Y1}
                ])
            else:
                
                kicad_mod.addPolygoneLine([
                {'x':x-w, 'y': Y2},
                {'x':x-w, 'y': Y1},
                {'x':x+w, 'y': Y1},
                {'x':x+w, 'y': Y2},
                ])

        # add pin-1 marking above the pin1
        
        d = 0.3
        l = 1.5
        xp1 = x1 - d
        xp2 = xp1 + l
        
        yp2 = y2 + d
        yp1 = yp2 - l
        
        pin1 = [
            {'x': xp1,'y': yp1},
            {'x': xp1,'y': yp2},
            {'x': xp2,'y': yp2},
        ]
        
        kicad_mod.addPolygoneLine(pin1)
        kicad_mod.addPolygoneLine(pin1,layer='F.Fab')

        # output kicad model
        f = open(footprint_name + ".kicad_mod","w")


        f.write(kicad_mod.__str__())

        f.close()
