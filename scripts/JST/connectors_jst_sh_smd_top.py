#!/usr/bin/env python

import sys
sys.path.append("../../kicad_mod") # load kicad_mod path

import argparse
from kicad_mod import KicadMod, createNumberedPadsSMD

parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
args = parser.parse_args()

# http://www.jst-mfg.com/product/pdf/eng/eSH.pdf

pincount = int(args.pincount[0])

pad_spacing = 1.
start_pos_x = -(pincount-1)*pad_spacing/2.
end_pos_x = (pincount-1)*pad_spacing/2.

# SMT type shrouded header, Top entry type
footprint_name = 'JST_SH_BM{pincount:02g}B-SRSS-TB_{pincount:02g}x1.00mm_Straight'.format(pincount=pincount)

kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription("http://www.jst-mfg.com/product/pdf/eng/eSH.pdf")
kicad_mod.setAttribute('smd')
kicad_mod.setTags('connector jst sh')
kicad_mod.setCenterPos({'x':0, 'y':2.525/2})

# set general values
kicad_mod.addText('reference', 'REF**', {'x':start_pos_x, 'y':-2-0.2375}, 'F.SilkS')
kicad_mod.addText('value', footprint_name, {'x':0, 'y':4.5+0.2625}, 'F.Fab')

# create Silkscreen
kicad_mod.addLine({'x':start_pos_x-0.4, 'y':-0.7}, {'x':end_pos_x+0.4, 'y':-0.7}, 'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':start_pos_x-1.5, 'y':1.2}
                          ,{'x':start_pos_x-1.5, 'y':2.2}
                          ,{'x':start_pos_x-0.6, 'y':2.2}]
                          ,'F.SilkS', 0.15)

kicad_mod.addRectLine({'x':start_pos_x-1, 'y':2.2}, {'x':start_pos_x-1, 'y':1.2}, 'F.SilkS', 0.15)
kicad_mod.addRectLine({'x':start_pos_x-1, 'y':1.6}, {'x':start_pos_x-1.5, 'y':1.6}, 'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':end_pos_x+1.5, 'y':1.2}
                          ,{'x':end_pos_x+1.5, 'y':2.2}
                          ,{'x':end_pos_x+0.6, 'y':2.2}]
                          ,'F.SilkS', 0.15)

kicad_mod.addRectLine({'x':end_pos_x+1, 'y':2.2}, {'x':end_pos_x+1, 'y':1.2}, 'F.SilkS', 0.15)
kicad_mod.addRectLine({'x':end_pos_x+1, 'y':1.6}, {'x':end_pos_x+1.5, 'y':1.6}, 'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':start_pos_x-0.4, 'y':0.2}
                          ,{'x':start_pos_x-0.4, 'y':-0.3}
                          ,{'x':end_pos_x+0.4, 'y':-0.3}
                          ,{'x':end_pos_x+0.4, 'y':0.2}] 
                          ,'F.SilkS', 0.15)
                          
kicad_mod.addPolygoneLine([{'x':start_pos_x-0.4, 'y':0.8}
                          ,{'x':start_pos_x-0.4, 'y':2.525-1.55/2-0.3}
                          ,{'x':end_pos_x+0.4, 'y':2.525-1.55/2-0.3}
                          ,{'x':end_pos_x+0.4, 'y':0.8}] 
                          ,'F.SilkS', 0.15)                     
                          
for i in range(0, pincount):
    middle_x = start_pos_x+i*pad_spacing
    kicad_mod.addLine({'x':middle_x, 'y':0.2}, {'x':middle_x, 'y':0.4}, 'F.SilkS', 0.15)

kicad_mod.addCircle({'x':start_pos_x-1, 'y':2.2+0.65}, {'x':0.25, 'y':0}, 'F.SilkS', 0.15)

# create Courtyard
kicad_mod.addRectLine({'x':start_pos_x-0.7-1.2-0.5, 'y':3.3+0.5+0.0125}, {'x':end_pos_x+0.7+1.2+0.5, 'y':-0.9-0.5-0.0375}, 'F.CrtYd', 0.05)

# create pads
createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, {'x':0.6, 'y':1.55}, 2.525)
kicad_mod.addPad('""', 'smd', 'rect', {'x':start_pos_x-0.7-1.2/2, 'y':0}, {'x':1.2, 'y':1.8}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
kicad_mod.addPad('""', 'smd', 'rect', {'x':end_pos_x+0.7+1.2/2, 'y':0}, {'x':1.2, 'y':1.8}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

# output kicad model
print(kicad_mod)
