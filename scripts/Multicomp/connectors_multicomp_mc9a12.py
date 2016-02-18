#!/usr/bin/env python

import sys
sys.path.append("../../kicad_mod") # load kicad_mod path

import argparse
from kicad_mod import KicadMod, createNumberedPadsTHT

parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
args = parser.parse_args()

# http://www.farnell.com/datasheets/1520732.pdf

pincount = int(args.pincount[0])
pad_spacing = 2.54
start_pos_x = 0
end_pos_x = pad_spacing*(pincount-2)/2

# Through-hole type shrouded header, Top entry type
footprint_name = 'Multicomp_MC9A12-{pincount:02g}34_2x{pincount_half:02g}x2.54mm_Straight'.format(pincount=pincount, pincount_half=pincount/2) # TODO: name

kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription('http://www.farnell.com/datasheets/1520732.pdf')
kicad_mod.setTags('connector multicomp MC9A MC9A12')

# set general values
kicad_mod.addText('reference', 'REF**', {'x':start_pos_x-3, 'y':-7}, 'F.SilkS')
kicad_mod.addText('value', footprint_name, {'x':end_pos_x/2., 'y':5}, 'F.Fab')

# create Silkscreen

# outline
kicad_mod.addRectLine({'x':start_pos_x-3.87-1.2, 'y':3.2}, {'x':end_pos_x+3.87+1.2, 'y':-pad_spacing-3.2}, 'F.SilkS', 0.15)

# slot(s)
if pincount < 60:
    kicad_mod.addPolygoneLine([{'x':((start_pos_x+end_pos_x)/2)-4.45/2, 'y':3.2}
                              ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2, 'y':1.9}
                              ,{'x':start_pos_x-3.87, 'y':1.9}
                              ,{'x':start_pos_x-3.87, 'y':-pad_spacing-1.9}
                              ,{'x':end_pos_x+3.87, 'y':-pad_spacing-1.9}
                              ,{'x':end_pos_x+3.87, 'y':1.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2, 'y':1.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2, 'y':3.2}], 'F.SilkS', 0.15)
else:
    kicad_mod.addPolygoneLine([{'x':((start_pos_x+end_pos_x)/2)-4.45/2-7.3-4.1, 'y':3.2}
                              ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2-7.3-4.1, 'y':1.9}
                              ,{'x':start_pos_x-3.87, 'y':1.9}
                              ,{'x':start_pos_x-3.87, 'y':-pad_spacing-1.9}
                              ,{'x':end_pos_x+3.87, 'y':-pad_spacing-1.9}
                              ,{'x':end_pos_x+3.87, 'y':1.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2+7.3+4.1, 'y':1.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2+7.3+4.1, 'y':3.2}], 'F.SilkS', 0.15)

    kicad_mod.addPolygoneLine([{'x':((start_pos_x+end_pos_x)/2)-4.45/2-7.3, 'y':3.2}
                              ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2-7.3, 'y':1.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2, 'y':1.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2, 'y':3.2}], 'F.SilkS', 0.15)
    
    kicad_mod.addPolygoneLine([{'x':((start_pos_x+end_pos_x)/2)+4.45/2+7.3, 'y':3.2}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2+7.3, 'y':1.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2, 'y':1.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2, 'y':3.2}], 'F.SilkS', 0.15)

# lines above the footprint
kicad_mod.addPolygoneLine([{'x':end_pos_x/2-0.25, 'y':-pad_spacing-3.2}
                          ,{'x':end_pos_x/2-0.25, 'y':-pad_spacing-3.2-0.2}
                          ,{'x':end_pos_x/2+0.25, 'y':-pad_spacing-3.2-0.2}
                          ,{'x':end_pos_x/2+0.25, 'y':-pad_spacing-3.2}], 'F.SilkS', 0.15)
kicad_mod.addLine({'x':end_pos_x/2-0.25, 'y':-pad_spacing-3.2-0.1}, {'x':end_pos_x/2+0.25, 'y':-pad_spacing-3.2-0.1}, 'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':end_pos_x+2.4-0.25, 'y':-pad_spacing-3.2}
                          ,{'x':end_pos_x+2.4-0.25, 'y':-pad_spacing-3.2-0.2}
                          ,{'x':end_pos_x+2.4+0.25, 'y':-pad_spacing-3.2-0.2}
                          ,{'x':end_pos_x+2.4+0.25, 'y':-pad_spacing-3.2}], 'F.SilkS', 0.15)
kicad_mod.addLine({'x':end_pos_x+2.4-0.25, 'y':-pad_spacing-3.2-0.1}, {'x':end_pos_x+2.4+0.25, 'y':-pad_spacing-3.2-0.1}, 'F.SilkS', 0.15)

kicad_mod.addPolygoneLine([{'x':start_pos_x-2.4-0.25, 'y':-pad_spacing-3.2}
                          ,{'x':start_pos_x-2.4-0.25, 'y':-pad_spacing-3.2-0.2}
                          ,{'x':start_pos_x-2.4+0.25, 'y':-pad_spacing-3.2-0.2}
                          ,{'x':start_pos_x-2.4+0.25, 'y':-pad_spacing-3.2}], 'F.SilkS', 0.15)
kicad_mod.addLine({'x':start_pos_x-2.4-0.25, 'y':-pad_spacing-3.2-0.1}, {'x':start_pos_x-2.4+0.25, 'y':-pad_spacing-3.2-0.1}, 'F.SilkS', 0.15)

# triangle which is pointing at 1
kicad_mod.addPolygoneLine([{'x':start_pos_x-2.2, 'y':0.6}
                          ,{'x':start_pos_x-2.2, 'y':-0.6}
                          ,{'x':start_pos_x-1.6, 'y':0}
                          ,{'x':start_pos_x-2.2, 'y':0.6}], 'F.SilkS', 0.15)

# create Courtyard
def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

kicad_mod.addRectLine({'x':round_to(start_pos_x-3.87-1.2-0.5,0.05), 'y':3.2+0.5}, {'x':round_to(end_pos_x+3.87+1.2+0.5,0.05), 'y':round_to(-pad_spacing-3.2-0.5,0.05)}, 'F.CrtYd', 0.05)

# create pads
pad_diameter = 1
pad_size = {'x':1.7, 'y':1.7}

for pad_number in range(1, pincount, 2):
    pad_pos_x = (pad_number-1)/2*pad_spacing
    if pad_number == 1:
        kicad_mod.addPad(pad_number, 'thru_hole', 'rect', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])
    else:
        kicad_mod.addPad(pad_number, 'thru_hole', 'circle', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])

    kicad_mod.addPad(pad_number+1, 'thru_hole', 'circle', {'x':pad_pos_x, 'y':-pad_spacing}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])

# output kicad model
print(kicad_mod)
