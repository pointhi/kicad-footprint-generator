#!/usr/bin/env python

import sys
sys.path.append("../../kicad_mod") # load kicad_mod path

import argparse
from kicad_mod import KicadMod, createNumberedPadsTHT

parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
args = parser.parse_args()

# http://www.farnell.com/cad/360651.pdf

pincount = int(args.pincount[0])
pad_spacing = 2.54
start_pos_x = 0
end_pos_x = pad_spacing*(pincount-2)/2

# Through-hole type shrouded header, Top entry type
footprint_name = "Multicomp_MC9A22-{pincount:02g}34_2x{pincount_half:02g}x2.54mm_Angled".format(pincount=pincount, pincount_half=pincount/2)

kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription('http://www.farnell.com/cad/360651.pdf')
kicad_mod.setTags('connector multicomp MC9A MC9A22')

# set general values
kicad_mod.addText('reference', 'REF**', {'x':start_pos_x-3, 'y':-15}, 'F.SilkS')
kicad_mod.addText('value', footprint_name, {'x':end_pos_x/2., 'y':-5.5}, 'F.Fab')

# create Silkscreen

# outline

kicad_mod.addRectLine({'x':start_pos_x-3.87-1.2, 'y':-pad_spacing-1.8}, {'x':end_pos_x+3.87+1.2, 'y':-pad_spacing-1.8-8.9}, 'F.SilkS', 0.15)


# slot(s)
def draw_pin_silk(slot_pin_x):
    kicad_mod.addPolygoneLine([{'x':slot_pin_x-0.4, 'y':-pad_spacing-1.8-8.9+6.6}
                              ,{'x':slot_pin_x-0.4, 'y':-pad_spacing-1.8-8.5}
                              ,{'x':slot_pin_x-0.2, 'y':-pad_spacing-1.8-8.7}
                              ,{'x':slot_pin_x+0.2, 'y':-pad_spacing-1.8-8.7}
                              ,{'x':slot_pin_x+0.4, 'y':-pad_spacing-1.8-8.5}
                              ,{'x':slot_pin_x+0.4, 'y':-pad_spacing-1.8-8.9+6.6}], 'F.SilkS', 0.15)
                              
kicad_mod.addPolygoneLine([{'x':((start_pos_x+end_pos_x)/2)-4.45/2, 'y':-pad_spacing-1.8-8.9}
                          ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2, 'y':-pad_spacing-1.8-8.9+6.6}
                          ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2, 'y':-pad_spacing-1.8-8.9+6.6}
                          ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2, 'y':-pad_spacing-1.8-8.9}], 'F.SilkS', 0.15)

if pincount%4 != 0:
    slot_pin_x = start_pos_x+((int)(pincount/4)*pad_spacing)

    draw_pin_silk(slot_pin_x)
else:
    slot_pin_x = start_pos_x+((int)(pincount/4-1)*pad_spacing)
    draw_pin_silk(slot_pin_x)
    
    slot_pin_x = start_pos_x+((int)(pincount/4)*pad_spacing)
    draw_pin_silk(slot_pin_x)
    
    if pincount >= 60:
        slot_pin_x = start_pos_x+((int)(pincount/4-1-4)*pad_spacing)
        draw_pin_silk(slot_pin_x)
        
        slot_pin_x = start_pos_x+((int)(pincount/4+4)*pad_spacing)
        draw_pin_silk(slot_pin_x)
    

if pincount >= 60:
    kicad_mod.addPolygoneLine([{'x':((start_pos_x+end_pos_x)/2)-4.45/2-7.3, 'y':-pad_spacing-1.8-8.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2-7.3, 'y':-pad_spacing-1.8-8.9+6.6}
                              ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2-7.3-4.1, 'y':-pad_spacing-1.8-8.9+6.6}
                              ,{'x':((start_pos_x+end_pos_x)/2)-4.45/2-7.3-4.1, 'y':-pad_spacing-1.8-8.9}], 'F.SilkS', 0.15)
  
    kicad_mod.addPolygoneLine([{'x':((start_pos_x+end_pos_x)/2)+4.45/2+7.3, 'y':-pad_spacing-1.8-8.9}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2+7.3, 'y':-pad_spacing-1.8-8.9+6.6}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2+7.3+4.1, 'y':-pad_spacing-1.8-8.9+6.6}
                              ,{'x':((start_pos_x+end_pos_x)/2)+4.45/2+7.3+4.1, 'y':-pad_spacing-1.8-8.9}], 'F.SilkS', 0.15)

# triangle which is pointing at 1
kicad_mod.addPolygoneLine([{'x':start_pos_x-1, 'y':-12.5}
                          ,{'x':start_pos_x+1, 'y':-12.5}
                          ,{'x':start_pos_x, 'y':-11}
                          ,{'x':start_pos_x-1, 'y':-12.5}], 'F.SilkS', 0.15)

# create Courtyard
def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

kicad_mod.addRectLine({'x':round_to(start_pos_x-3.87-1.2-0.5,0.05), 'y':1.7/2+0.5}, {'x':round_to(end_pos_x+3.87+1.2+0.5,0.05), 'y':round_to(-pad_spacing-1.8-8.9-0.5,0.05)}, 'F.CrtYd', 0.05)

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
    
    kicad_mod.addLine({'x':pad_pos_x-0.4, 'y':-1.1}, {'x':pad_pos_x-0.4, 'y':-pad_spacing+1.1}, 'F.SilkS', 0.15)
    kicad_mod.addLine({'x':pad_pos_x+0.4, 'y':-1.1}, {'x':pad_pos_x+0.4, 'y':-pad_spacing+1.1}, 'F.SilkS', 0.15)
    
    kicad_mod.addLine({'x':pad_pos_x-0.4, 'y':-pad_spacing-1.1}, {'x':pad_pos_x-0.4, 'y':-pad_spacing-1.8}, 'F.SilkS', 0.15)
    kicad_mod.addLine({'x':pad_pos_x+0.4, 'y':-pad_spacing-1.1}, {'x':pad_pos_x+0.4, 'y':-pad_spacing-1.8}, 'F.SilkS', 0.15)

# output kicad model
print(kicad_mod)
