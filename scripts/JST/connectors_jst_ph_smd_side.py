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

# SMT type shrouded header, Side entry type
footprint_name = 'JST_PH_S{pincount}B-PH-SM4-TB_{pincount:02}x2.00mm_Angled'.format(pincount=pincount)

kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription("http://www.jst-mfg.com/product/pdf/eng/ePH.pdf")
kicad_mod.setAttribute('smd')
kicad_mod.setTags('connector jst ph')
kicad_mod.setCenterPos({'x':0, 'y':5.55/2})

# set general values
kicad_mod.addText('reference', 'REF**', {'x':start_pos_x-0.5, 'y':-3-0.225}, 'F.SilkS')
kicad_mod.addText('value', footprint_name, {'x':0, 'y':8.5+0.275}, 'F.Fab')

# create Silkscreen

kicad_mod.addPolygoneLine([{'x':start_pos_x+0.5, 'y':7}
                          ,{'x':start_pos_x+0.5, 'y':6} # 2.75
                          ,{'x':end_pos_x-0.5, 'y':6}
                          ,{'x':end_pos_x-0.5, 'y':7}]
                          ,'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':start_pos_x-0.9, 'y':1}
                          ,{'x':start_pos_x-2.95+0.8, 'y':1}
                          ,{'x':start_pos_x-2.95+0.8, 'y':-0.6}
                          ,{'x':start_pos_x-2.95, 'y':-0.6}
                          ,{'x':start_pos_x-2.95, 'y':3.5}]
                          ,'F.SilkS', 0.15)

kicad_mod.addLine({'x':start_pos_x-2.95+0.8, 'y':1}, {'x':start_pos_x-2.95, 'y':1}, 'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':end_pos_x+0.9, 'y':1}
                          ,{'x':end_pos_x+2.95-0.8, 'y':1}
                          ,{'x':end_pos_x+2.95-0.8, 'y':-0.6}
                          ,{'x':end_pos_x+2.95, 'y':-0.6}
                          ,{'x':end_pos_x+2.95, 'y':3.5}]
                          ,'F.SilkS', 0.15)

kicad_mod.addLine({'x':end_pos_x+2.95-0.8, 'y':1}, {'x':end_pos_x+2.95, 'y':1}, 'F.SilkS', 0.15)

kicad_mod.addLine({'x':start_pos_x-1.2, 'y':7}, {'x':end_pos_x+1.2, 'y':7}, 'F.SilkS', 0.15)

kicad_mod.addRectLine({'x':start_pos_x-1.2, 'y':2.1}, {'x':start_pos_x-0.2, 'y':5.5}, 'F.SilkS', 0.15)
kicad_mod.addRectLine({'x':end_pos_x+1.2, 'y':2.1}, {'x':end_pos_x+0.2, 'y':5.5}, 'F.SilkS', 0.15)

for i in range(0, pincount-1):
    middle_x = start_pos_x+1+i*2
    start_x = middle_x-0.1
    end_x = middle_x+0.1
    kicad_mod.addLine({'x':start_x, 'y':1}, {'x':end_x, 'y':1}, 'F.SilkS', 0.15)

kicad_mod.addCircle({'x':start_pos_x-2.95+0.8+0.75, 'y':0.25}, {'x':0.25, 'y':0}, 'F.SilkS', 0.15)

# create Courtyard
kicad_mod.addRectLine({'x':start_pos_x-1.6-1.6-0.5, 'y':7.25+0.275+0.25}, {'x':end_pos_x+1.6+1.6+0.5, 'y':-1.75-0.275-0.25}, 'F.CrtYd', 0.05)

# create pads
createNumberedPadsSMD(kicad_mod, pincount, 2, {'x':1, 'y':3.5}, 0)
kicad_mod.addPad('""', 'smd', 'rect', {'x':start_pos_x-1.6-1.6/2, 'y':5.55}, {'x':1.6, 'y':3.4}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
kicad_mod.addPad('""', 'smd', 'rect', {'x':end_pos_x+1.6+1.6/2, 'y':5.55}, {'x':1.6, 'y':3.4}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

# output kicad model
print(kicad_mod)
