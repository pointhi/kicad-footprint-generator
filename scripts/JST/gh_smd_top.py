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

    jst_name = "BM{pincount:02}B-GHS-TBT".format(pincount=pincount)

    # SMT type shrouded header,
    footprint_name = "JST_GH_" + jst_name + "_{pincount:02}x1.25mm_Straight".format(pincount=pincount)
    
    print(footprint_name)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST GH series connector, " + jst_name + ", top entry type") 
    kicad_mod.setAttribute('smd')
    kicad_mod.setTags('connector jst GH SMT top vertical entry 1.25mm pitch')

    kicad_mod.setCenterPos({'x':0, 'y':-3.075})

    #draw outline on the F.Fab layer
    y1 = -4.25 / 2 - 2.25
    y2 = y1 + 4.25
    kicad_mod.addRectLine(
        {'x': -B/2,'y': y1},
        {'x':  B/2,'y': y2},
        'F.Fab', 0.15
    )
    
    # set general values
    kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-6.75}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':0, 'y':1.5}, 'F.Fab')

    #create outline
    # create Courtyard
    # output kicad model

    #create pads
    createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, {'x':pad_w,'y':pad_h},-4.75)

    #add mounting pads (no number)
    mpad_w = 1.0
    mpad_h = 2.8
    mpad_x = (B/2) - (mpad_w/2)
    mpad_y = -1.4

    kicad_mod.addPad('""', 'smd', 'rect', {'x':mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    kicad_mod.addPad('""', 'smd', 'rect', {'x':-mpad_x, 'y':mpad_y}, {'x':mpad_w, 'y':mpad_h}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

    #side-wall thickness
    T = 0.5
    
    #add bottom line
    kicad_mod.addPolygoneLine([{'x':-B/2+mpad_w+0.6,'y':0.05},
                            {'x':B/2-mpad_w-0.6,'y':0.05},
                            {'x':B/2-mpad_w-0.6,'y':0.05 - T},
                            {'x':-B/2+mpad_w+0.6,'y':0.05 - T},
                            {'x':-B/2+mpad_w+0.6,'y':0.05}])
                             
    #add left line
    kicad_mod.addPolygoneLine([{'x':-B/2-0.1,'y':-3.3},
                                {'x':-B/2-0.1,'y':-4.5},
                                {'x':-A/2-pad_w/2-0.4,'y':-4.5},
                                {'x':-A/2-pad_w/2-0.4,'y':-4.5+T},
                                {'x':-B/2-0.1+T,'y':-4.5+T},
                                {'x':-B/2-0.1+T,'y':-3.3},
                                {'x':-B/2-0.1,'y':-3.3}])

    #add right line
    kicad_mod.addPolygoneLine([{'x':B/2+0.1,'y':-3.3},
                                {'x':B/2+0.1,'y':-4.5},
                                {'x':A/2+pad_w/2+0.4,'y':-4.5},
                                {'x':A/2+pad_w/2+0.4,'y':-4.5+T},
                                {'x':B/2+0.1-T, 'y':-4.5+T},
                                {'x':B/2+0.1-T, 'y':-3.3},
                                {'x':B/2+0.1,'y':-3.3}])                                  
                                
                                
    #add designator for pin #1

    y1 = -5.25

    if pincount % 2 == 1: #odd pins
        x1 = -(pincount//2) * pad_spacing
    else: #even pins
        x1 = (-pincount/2 + 0.5) * pad_spacing
        
    xp = x1 - 1

    m = 0.6
       
    marker = [{'x':xp,'y':y1},
               {'x':xp-m,'y':y1-m/2},
               {'x':xp-m,'y':y1+m/2},
               {'x':xp,'y':y1}]

    kicad_mod.addPolygoneLine(marker)
    kicad_mod.addPolygoneLine(marker,layer='F.Fab')
                               
                               
    #add picture of each pin
    p = 0.25
    
    y = -2.5 

    for i in range(pincount):
    
        x = x1 + (i * pad_spacing)
        kicad_mod.addPolygoneLine([{'x': x-p,'y': y-p},
                                   {'x': x-p,'y': y+p},
                                   {'x': x+p,'y': y+p},
                                   {'x': x+p,'y': y-p},
                                   {'x': x-p,'y': y-p}])
                              
    #add courtyard
    kicad_mod.addRectLine({'x':-B/2-0.5,'y':-6.125},{'x':B/2+0.5,'y':0.525},'F.CrtYd',0.05)
    
    kicad_mod.model = "Connectors_JST.3dshapes/" + footprint_name + ".wrl"

    f = open(footprint_name + ".kicad_mod","w")

    f.write(kicad_mod.__str__())

    f.close()
