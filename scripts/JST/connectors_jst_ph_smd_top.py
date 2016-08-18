#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

import argparse
from kicad_mod import KicadMod, createNumberedPadsSMD

parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
args = parser.parse_args()

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

pincount = int(args.pincount[0])

pad_spacing = 2
start_pos_x = -(pincount-1)*pad_spacing/2
end_pos_x = (pincount-1)*pad_spacing/2

# SMT type shrouded header, Top entry type
footprint_name = 'JST_PH_B{pincount}B-PH-SM4-TB_{pincount:02}x2.00mm_Straight'.format(pincount=pincount)

kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription("http://www.jst-mfg.com/product/pdf/eng/ePH.pdf")
kicad_mod.setAttribute('smd')
kicad_mod.setTags('connector jst ph')
kicad_mod.setCenterPos({'x':0, 'y':(4.75-1.9+0.6)/2})

# set general values
kicad_mod.addText('reference', 'REF**', {'x':start_pos_x-0.5, 'y':-3-0.275}, 'F.SilkS')
kicad_mod.addText('value', footprint_name, {'x':0, 'y':7-0.025}, 'F.Fab')

# create Silkscreen

kicad_mod.addPolygoneLine([{'x':start_pos_x-3, 'y':-1.3}
                          ,{'x':start_pos_x-3, 'y':-1.9}
                          ,{'x':end_pos_x+3, 'y':-1.9}
                          ,{'x':end_pos_x+3, 'y':-1.3}]
                          ,'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':start_pos_x-3, 'y':2.5}
                          ,{'x':start_pos_x-3, 'y':3.1}
                          ,{'x':start_pos_x-0.9, 'y':3.1}]
                          ,'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':end_pos_x+3, 'y':2.5}
                          ,{'x':end_pos_x+3, 'y':3.1}
                          ,{'x':end_pos_x+0.9, 'y':3.1}]
                          ,'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':start_pos_x+0.5, 'y':-1.9}
                          ,{'x':start_pos_x+0.5, 'y':-1.2}
                          ,{'x':start_pos_x-1.2, 'y':-1.2} # -1.45
                          ,{'x':start_pos_x-1.2, 'y':2.3}
                          ,{'x':start_pos_x-0.9, 'y':2.3}] 
                          ,'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':end_pos_x-0.5, 'y':-1.9}
                          ,{'x':end_pos_x-0.5, 'y':-1.2}
                          ,{'x':end_pos_x+1.2, 'y':-1.2} # +1.45
                          ,{'x':end_pos_x+1.2, 'y':2.3}
                          ,{'x':end_pos_x+0.9, 'y':2.3}] 
                          ,'F.SilkS', 0.15)

for i in range(0, pincount-1):
    middle_x = start_pos_x+1+i*2
    start_x = middle_x-0.1
    end_x = middle_x+0.1
    kicad_mod.addLine({'x':start_x, 'y':3.1}, {'x':end_x, 'y':3.1}, 'F.SilkS', 0.15)
    kicad_mod.addLine({'x':start_x, 'y':2.3}, {'x':end_x, 'y':2.3}, 'F.SilkS', 0.15)
    kicad_mod.addPolygoneLine([{'x':start_x, 'y':2.3}
                              ,{'x':start_x, 'y':1.8}
                              ,{'x':end_x, 'y':1.8}
                              ,{'x':end_x, 'y':2.3}], 'F.SilkS', 0.15)
    kicad_mod.addLine({'x':middle_x, 'y':2.3}, {'x':middle_x, 'y':1.8}, 'F.SilkS', 0.15)

kicad_mod.addCircle({'x':start_pos_x-2.95+0.8+0.75, 'y':3.1+0.75}, {'x':0.25, 'y':0}, 'F.SilkS', 0.15)

# create Courtyard
kicad_mod.addRectLine({'x':start_pos_x-1.6-1.6-0.5, 'y':5.6+0.275 + 0.25}, {'x':end_pos_x+1.6+1.6+0.5, 'y':-1.9-0.275-0.25}, 'F.CrtYd', 0.05)

# create pads
createNumberedPadsSMD(kicad_mod, pincount, 2, {'x':1, 'y':5.5}, 4.75-1.9) #TODO y
kicad_mod.addPad('""', 'smd', 'rect', {'x':start_pos_x-1.6-1.6/2, 'y':0.6}, {'x':1.6, 'y':3}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
kicad_mod.addPad('""', 'smd', 'rect', {'x':end_pos_x+1.6+1.6/2, 'y':0.6}, {'x':1.6, 'y':3}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

# output kicad model
print(kicad_mod)
