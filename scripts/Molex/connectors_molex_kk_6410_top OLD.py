#!/usr/bin/env python

import sys
sys.path.append("../../kicad_mod") # load kicad_mod path

import argparse
from kicad_mod import KicadMod


def createNumberedPadsTHT(kicad_mod, pincount, pad_spacing, pad_diameter, pad_size):
    for pad_number in range(1, pincount+1):
        pad_pos_x = (pad_number-1)*pad_spacing
        if pad_number == 1:
            kicad_mod.addPad(pad_number, 'thru_hole', 'rect', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask'])
        elif pad_size['x'] == pad_size['y']:
            kicad_mod.addPad(pad_number, 'thru_hole', 'circle', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask'])
        else:
            kicad_mod.addPad(pad_number, 'thru_hole', 'oval', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask'])


parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
args = parser.parse_args()

# http://www.molex.com/pdm_docs/sd/022272021_sd.pdf

pincount = int(args.pincount[0])
pad_spacing = 2.54
start_pos_x = 0
end_pos_x = (pincount-1)*pad_spacing

# Through-hole type shrouded header, Top entry type
footprint_name = 'Molex_KK-6410-{pincount:02g}_{pincount:02g}x2.54mm_Straight'.format(pincount=pincount)

kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription("Connector Headers with Friction Lock, 22-27-2{pincount:02g}1, http://www.molex.com/pdm_docs/sd/022272021_sd.pdf".format(pincount=pincount))
kicad_mod.setTags('connector molex kk_6410 22-27-2{pincount:02g}1'.format(pincount=pincount))

# set general values
kicad_mod.addText('reference', 'REF**', {'x':start_pos_x+1, 'y':-4.5}, 'F.SilkS')
kicad_mod.addText('value', footprint_name, {'x':(pincount-1)*pad_spacing/2., 'y':4.5}, 'F.Fab')








# create Silkscreen

kicad_mod.addRectLine({'x':start_pos_x-2.54/2-0.1, 'y':-3.02}, {'x':end_pos_x+2.54/2+0.1, 'y':2.98}, 'F.SilkS', 0.12)

#ramps
if pincount <= 6:
    # single ramp
    kicad_mod.addPolygoneLine([{'x':start_pos_x, 'y':2.98}
                              ,{'x':start_pos_x, 'y':1.98}
                              ,{'x':end_pos_x, 'y':1.98}
                              ,{'x':end_pos_x, 'y':2.98}], 'F.SilkS', 0.12)
    kicad_mod.addPolygoneLine([{'x':start_pos_x, 'y':1.98}
                              ,{'x':start_pos_x+0.25, 'y':1.55}
                              ,{'x':end_pos_x-0.25, 'y':1.55}
                              ,{'x':end_pos_x, 'y':1.98}], 'F.SilkS', 0.12)
    kicad_mod.addLine({'x':start_pos_x+0.25, 'y':2.98}, {'x':start_pos_x+0.25, 'y':1.98}, 'F.SilkS', 0.12)
    kicad_mod.addLine({'x':end_pos_x-0.25, 'y':2.98}, {'x':end_pos_x-0.25, 'y':1.98}, 'F.SilkS', 0.12)
else:
    # two ramps
    kicad_mod.addPolygoneLine([{'x':start_pos_x, 'y':2.98}
                              ,{'x':start_pos_x, 'y':1.98}
                              ,{'x':start_pos_x+2*pad_spacing, 'y':1.98}
                              ,{'x':start_pos_x+2*pad_spacing, 'y':2.98}], 'F.SilkS', 0.12)
    kicad_mod.addPolygoneLine([{'x':start_pos_x, 'y':1.98}
                              ,{'x':start_pos_x+0.25, 'y':1.55}
                              ,{'x':start_pos_x+2*pad_spacing, 'y':1.55}
                              ,{'x':start_pos_x+2*pad_spacing, 'y':1.98}], 'F.SilkS', 0.12)
    kicad_mod.addLine({'x':start_pos_x+0.25, 'y':2.98}, {'x':start_pos_x+0.25, 'y':1.98}, 'F.SilkS', 0.12)
    #kicad_mod.addLine({'x':start_pos_x+2*pad_spacing-0.25, 'y':2.98}, {'x':start_pos_x+2*pad_spacing-0.25, 'y':1.98}, 'F.SilkS', 0.12)
    
    kicad_mod.addPolygoneLine([{'x':end_pos_x, 'y':2.98}
                              ,{'x':end_pos_x, 'y':1.98}
                              ,{'x':end_pos_x-2*pad_spacing, 'y':1.98}
                              ,{'x':end_pos_x-2*pad_spacing, 'y':2.98}], 'F.SilkS', 0.12)
    kicad_mod.addPolygoneLine([{'x':end_pos_x, 'y':1.98}
                              ,{'x':end_pos_x-0.25, 'y':1.55}
                              ,{'x':end_pos_x-2*pad_spacing, 'y':1.55}
                              ,{'x':end_pos_x-2*pad_spacing, 'y':1.98}], 'F.SilkS', 0.12)
    #kicad_mod.addLine({'x':end_pos_x-2*pad_spacing+0.25, 'y':2.98}, {'x':end_pos_x-2*pad_spacing+0.25, 'y':1.98}, 'F.SilkS', 0.12)
    kicad_mod.addLine({'x':end_pos_x-0.25, 'y':2.98}, {'x':end_pos_x-0.25, 'y':1.98}, 'F.SilkS', 0.12)

for i in range(0, pincount):
    middle_x = start_pos_x+i*pad_spacing
    start_x = middle_x-1.6/2
    end_x = middle_x+1.6/2
    kicad_mod.addPolygoneLine([{'x':start_x, 'y':-3.02}
                              ,{'x':start_x, 'y':-2.4}
                              ,{'x':end_x, 'y':-2.4}
                              ,{'x':end_x, 'y':-3.02}], 'F.SilkS', 0.12)

def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

# create Courtyard
kicad_mod.addRectLine({'x':round_to(start_pos_x-2.54/2-0.5-0.03-0.1, 0.05), 'y':2.98+0.5+0.02}, {'x':round_to(end_pos_x+2.54/2+0.5+0.03+0.1, 0.05), 'y':-3.02-0.5-0.03}, 'F.CrtYd', 0.05)

# create pads
createNumberedPadsTHT(kicad_mod, pincount, pad_spacing, 1.2, {'x':2, 'y':2.6})

# output kicad model
print(kicad_mod)
