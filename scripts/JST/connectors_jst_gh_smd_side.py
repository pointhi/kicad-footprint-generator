    #!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

#import argparse
from kicad_mod import KicadMod, createNumberedPadsSMD

#parser = argparse.ArgumentParser()
#parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
#parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
#args = parser.parse_args()

# http://www.jst-mfg.com/product/pdf/eng/eGH.pdf

#pincount = int(args.pincount[0])

for pincount in range(2,16):

    pad_spacing = 1.25
    start_pos_x = -(pincount-1)*pad_spacing/2
    end_pos_x = (pincount-1)*pad_spacing/2

    pad_w = 0.6
    pad_h = 1.8

    A = (pincount - 1) * 1.25
    B = 3.25 + pincount * 1.25
    
    #A and B should be 0.1mm resolution
    A = int(A/0.1) * 0.1
    B = int(B/0.1) * 0.1

    jst_name = "SM{pincount:02}B-GHS-TB".format(pincount=pincount)

    # SMT type shrouded header,
    footprint_name = "JST_GH_" + jst_name + "_{pincount:02}x1.25mm_Angled".format(pincount=pincount)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST GH series connector, " + jst_name + ", side entry type") 
    kicad_mod.setAttribute('smd')
    kicad_mod.setTags('connector jst GH SMT side horizontal entry 1.25mm pitch')

    kicad_mod.setCenterPos({'x':0, 'y':-2.95})

    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-7.5}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':1.5}, 'F.Fab')

    #create outline
    # create Courtyard
    # output kicad model

    #create pads
    createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, {'x':pad_w,'y':pad_h},-4.55)

    #add mounting pads (no number)
    mpad_w = 1.0
    mpad_h = 2.8
    mpad_x = (B/2) - (mpad_w/2)
    mpad_y = -1.35

    kicad_mod.addPad('""', 'smd', 'rect', {'x':mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    kicad_mod.addPad('""', 'smd', 'rect', {'x':-mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

    T = 0.5
    
    #add bottom line
    kicad_mod.addPolygoneLine([{'x':-B/2+mpad_w+0.6,'y':-0.1},
                            {'x':B/2-mpad_w-0.6,'y':-0.1}])
                             
    #add left line
    kicad_mod.addPolygoneLine([{'x':-B/2-0.1,'y':-3.3},
                                {'x':-B/2-0.1,'y':-4.4},
                                {'x':-A/2-pad_w/2-0.5,'y':-4.4},
                                {'x':-A/2-pad_w/2-0.5,'y':-4.4+T},
                                {'x':-B/2-0.1+T,'y':-4.4+T},
                                {'x':-B/2-0.1+T,'y':-3.3},
                                {'x':-B/2-0.1,'y':-3.3}])

    #add right line
    kicad_mod.addPolygoneLine([{'x':B/2+0.1,'y':-3.3},
                                {'x':B/2+0.1,'y':-4.4},
                                {'x':A/2+pad_w/2+0.5,'y':-4.4},
                                {'x':A/2+pad_w/2+0.5,'y':-4.4+T},
                                {'x':B/2+0.1-T,'y':-4.4+T},
                                {'x':B/2+0.1-T,'y':-3.3},
                                {'x':B/2+0.1,'y':-3.3}])                                  

    #add designator for pin #1

    y1 = -6.25
    x1 = 0

    if pincount % 2 == 1: #odd pins
        x1 = -(pincount//2) * pad_spacing
    else: #even pins
        x1 = (-pincount/2 + 0.5) * pad_spacing
                              

    kicad_mod.addPolygoneLine([{'x':x1,'y':y1},
                               {'x':x1-0.25,'y':y1-0.5},
                               {'x':x1+0.25,'y':y1-0.5},
                               {'x':x1,'y':y1}])
                               
    #add pin picures
    p = 0.25
    
    y = -0.1 - p
    
    for i in range(pincount):
        x = x1 + (i * pad_spacing)
        
        kicad_mod.addPolygoneLine([{'x': x - p,'y': y + p},
                                   {'x': x - p,'y': y - 5 * p},
                                   {'x': x + p,'y': y - 5 * p},
                                   {'x': x + p,'y': y + p}])
                              
    #add courtyard
    
    #courtyard corners
    cx1 = -B/2 - 0.5
    cx2 =  B/2 + 0.5
    
    cy1 = -6.1
    cy2 = 0.55
    
    #make sure they lie on an 0.05mm grid
    
    cx1 = int(cx1/0.05) * 0.05
    cx2 = int(cx2/0.05) * 0.05
    
    cy1 = int(cy1/0.05) * 0.05
    cy2 = int(cy2/0.05) * 0.05
    
    kicad_mod.addRectLine({'x':cx1,'y':cy1},{'x':cx2,'y':cy2},'F.CrtYd',0.05)

    f = open(footprint_name + ".kicad_mod","w")

    f.write(kicad_mod.__str__())

    f.close()
