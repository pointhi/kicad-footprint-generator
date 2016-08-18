#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

import argparse
from kicad_mod import KicadMod, createNumberedPadsTHT

parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
args = parser.parse_args()

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

pincount = int(args.pincount[0])

# Through-hole type shrouded header, Side entry type
footprint_name = 'JST_PH_S{pincount}B-PH-K_{pincount:02}x2.00mm_Angled'.format(pincount=pincount)

kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription("http://www.jst-mfg.com/product/pdf/eng/ePH.pdf")
kicad_mod.setTags('connector jst ph')

# set general values
kicad_mod.addText('reference', 'REF**', {'x':0, 'y':-2.5}, 'F.SilkS')
kicad_mod.addText('value', footprint_name, {'x':(pincount-1)*2/2, 'y':7.5}, 'F.Fab')

# create Silkscreen
kicad_mod.addPolygoneLine([{'x':0.5, 'y':6.25}
                          ,{'x':0.5, 'y':2}
                          ,{'x':(pincount-1)*2-0.5, 'y':2}
                          ,{'x':(pincount-1)*2-0.5, 'y':6.25}]
                          ,'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':-0.9, 'y':0.25}
                          ,{'x':-1.95+0.7, 'y':0.25}
                          ,{'x':-1.95+0.7, 'y':-1.35}
                          ,{'x':-1.95, 'y':-1.35}
                          ,{'x':-1.95, 'y':6.25}
                          ,{'x':(pincount-1)*2+1.95, 'y':6.25}
                          ,{'x':(pincount-1)*2+1.95, 'y':-1.35}
                          ,{'x':(pincount-1)*2+1.95-0.7, 'y':-1.35}
                          ,{'x':(pincount-1)*2+1.95-0.7, 'y':0.25}
                          ,{'x':(pincount-1)*2+0.9, 'y':0.25}]
                         ,'F.SilkS', 0.15) #TODO

kicad_mod.addPolygoneLine([{'x':0, 'y':-1.2}
                          ,{'x':-0.4, 'y':-1.6}
                          ,{'x':0.4, 'y':-1.6}
                          ,{'x':0, 'y':-1.2}]
                          ,'F.SilkS', 0.15)

kicad_mod.addLine({'x':-1.95, 'y':0.25}, {'x':-1.95+0.7, 'y':0.25}, 'F.SilkS', 0.15)
kicad_mod.addLine({'x':(pincount-1)*2+1.95, 'y':0.25}, {'x':(pincount-1)*2+1.95-0.7, 'y':0.25}, 'F.SilkS', 0.15)

kicad_mod.addRectLine({'x':-1.3, 'y':2.5}, {'x':-0.3, 'y':4.1}, 'F.SilkS', 0.15)
kicad_mod.addRectLine({'x':(pincount-1)*2+1.3, 'y':2.5}, {'x':(pincount-1)*2+0.3, 'y':4.1}, 'F.SilkS', 0.15)
kicad_mod.addLine({'x':-0.3, 'y':4.1}, {'x':-0.3, 'y':6.25}, 'F.SilkS', 0.15)
kicad_mod.addLine({'x':-0.8, 'y':4.1}, {'x':-0.8, 'y':6.25}, 'F.SilkS', 0.15)

for i in range(0, pincount-1):
    middle_x = 1+i*2
    start_x = middle_x-0.1
    end_x = middle_x+0.1
    kicad_mod.addLine({'x':start_x, 'y':0.25}, {'x':end_x, 'y':0.25}, 'F.SilkS', 0.15)

# create Courtyard
kicad_mod.addRectLine({'x':-1.95-0.5, 'y':6.25+0.5}, {'x':(pincount-1)*2+1.95+0.5, 'y':-1.35-0.5}, 'F.CrtYd', 0.05)

# create pads
createNumberedPadsTHT(kicad_mod, pincount, 2, 0.7, {'x':1.2, 'y':1.7})

# output kicad model
print(kicad_mod)
