#!/usr/bin/env python

import argparse
from kicad_mod import KicadMod

parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('--type', help='what type of jst connector (default: B*B-PH-K)', default='B*B-PH-K', nargs=1) #TODO
args = parser.parse_args()

#http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

def createNumberedPadsTHT(kicad_mod, pincount, pad_spacing, pad_diameter, pad_size):
    for pad_number in range(1, pincount+1):
        pad_pos_x = (pad_number-1)*pad_spacing
        if pad_number == 1:
            kicad_mod.addPad(pad_number, 'thru_hole', 'rect', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])
        else:
            kicad_mod.addPad(pad_number, 'thru_hole', 'circle', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])

def createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, pad_size, pad_pos_y):
    for pad_number in range(1, pincount+1):
        pad_pos_x = (pad_number-1)*pad_spacing
        kicad_mod.addPad(pad_number, 'smd', 'rect', {'x':pad_pos_x, 'y':pad_pos_y}, pad_size, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

pincount = int(args.pincount[0])
connector_type = 'S*B-PH-SM4-TB'

if connector_type == 'B*B-PH-K':
    # Through-hole type shrouded header, Top entry type
    footprint_name = 'Connectors_JST_B{pincount}B-PH-K'.format(pincount=pincount)

    kicad_mod = KicadMod(footprint_name)

    # set general values
    kicad_mod.addText('reference', 'CON**', {'x':0, 'y':-3}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':pincount*2/2, 'y':4}, 'F.Fab')

    # create Silkscreen
    kicad_mod.addRectLine({'x':-1.95, 'y':2.8}, {'x':(pincount-1)*2+1.95, 'y':-1.7}, 'F.SilkS', 0.15)
    kicad_mod.addLine({'x':-1.95, 'y':2}, {'x':(pincount-1)*2+1.95, 'y':2}, 'F.SilkS', 0.15)
    kicad_mod.addPolygoneLine([{'x':0.5, 'y':-1.7}, {'x':0.5, 'y':-1}, {'x':(pincount-1)*2-0.5, 'y':-1}, {'x':(pincount-1)*2-0.5, 'y':-1.7}], 'F.SilkS', 0.15)

    # create Courtyard
    kicad_mod.addRectLine({'x':-1.95-0.25, 'y':2.8+0.25}, {'x':(pincount-1)*2+1.95+0.25, 'y':-1.7-0.25}, 'F.CrtYd', 0.05)

    createNumberedPadsTHT(kicad_mod, pincount, 2, 0.8, {'x':1.4, 'y':1.4})

    # save model
    kicad_mod.save('{footprint_name}.kicad_mod'.format(footprint_name=footprint_name))

elif connector_type == 'S*B-PH-K':
    # Through-hole type shrouded header, Side entry type
    footprint_name = 'Connectors_JST_S{pincount}B-PH-K'.format(pincount=pincount)

    kicad_mod = KicadMod(footprint_name)

    # set general values
    kicad_mod.addText('reference', 'CON**', {'x':0, 'y':-3}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':pincount*2/2, 'y':7}, 'F.Fab')

    # create Silkscreen
    kicad_mod.addPolygoneLine([{'x':0.5, 'y':6}
                              ,{'x':0.5, 'y':1.6}
                              ,{'x':(pincount-1)*2-0.5, 'y':1.6}
                              ,{'x':(pincount-1)*2-0.5, 'y':6}]
                              ,'F.SilkS', 0.15)
    
    kicad_mod.addPolygoneLine([{'x':-1.95+0.8, 'y':0}
                              ,{'x':-1.95+0.8, 'y':-1.6}
                              ,{'x':-1.95, 'y':-1.6}
                              ,{'x':-1.95, 'y':6}
                              ,{'x':(pincount-1)*2+1.95, 'y':6}
                              ,{'x':(pincount-1)*2+1.95, 'y':-1.6}
                              ,{'x':(pincount-1)*2+1.95-0.8, 'y':-1.6}
                              ,{'x':(pincount-1)*2+1.95-0.8, 'y':0}]
                             ,'F.SilkS', 0.15) #TODO

    # create Courtyard
    kicad_mod.addRectLine({'x':-1.95-0.25, 'y':6+0.25}, {'x':(pincount-1)*2+1.95+0.25, 'y':-1.6-0.25}, 'F.CrtYd', 0.05)

    createNumberedPadsTHT(kicad_mod, pincount, 2, 0.8, {'x':1.4, 'y':1.4})

    # save model
    kicad_mod.save('{footprint_name}.kicad_mod'.format(footprint_name=footprint_name))
    
elif connector_type == 'S*B-PH-SM4-TB':
    # SMT type shrouded header, Top entry type
    footprint_name = 'Connectors_JST_S{pincount}B-PH-K'.format(pincount=pincount)

    kicad_mod = KicadMod(footprint_name)

    # set general values
    kicad_mod.addText('reference', 'CON**', {'x':0, 'y':-3.5}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':pincount*2/2, 'y':7}, 'F.Fab')

    # create Silkscreen
    kicad_mod.addPolygoneLine([{'x':-3, 'y':-2.5}
                              ,{'x':(pincount-1)*2+3, 'y':-2.5}]
                              ,'F.SilkS', 0.15)
    kicad_mod.addPolygoneLine([{'x':0.5, 'y':-2.5}, {'x':0.5, 'y':-1.8}, {'x':(pincount-1)*2-0.5, 'y':-1.8}, {'x':(pincount-1)*2-0.5, 'y':-2.5}], 'F.SilkS', 0.15)
    #kicad_mod.addRectLine({'x':-3, 'y':2.8}, {'x':(pincount-1)*2+1.95, 'y':-1.7}, 'F.SilkS', 0.15)
    #kicad_mod.addLine({'x':-3, 'y':2}, {'x':(pincount-1)*2+1.95, 'y':2}, 'F.SilkS', 0.15)
    #kicad_mod.addPolygoneLine([{'x':0.5, 'y':-1.7}, {'x':0.5, 'y':-1}, {'x':(pincount-1)*2-0.5, 'y':-1}, {'x':(pincount-1)*2-0.5, 'y':-1.7}], 'F.SilkS', 0.15)

    # create Courtyard
    #kicad_mod.addRectLine({'x':-1.95-0.25, 'y':6+0.25}, {'x':(pincount-1)*2+1.95+0.25, 'y':-1.6-0.25}, 'F.CrtYd', 0.05)

    createNumberedPadsSMD(kicad_mod, pincount, 2, {'x':1, 'y':5.5}, 5.5/2-0.5)
    
    kicad_mod.addPad('""', 'smd', 'rect', {'x':-1.6-1.6/2, 'y':0}, {'x':1.6, 'y':3}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    kicad_mod.addPad('""', 'smd', 'rect', {'x':(pincount-1)*2+1.6+1.6/2, 'y':0}, {'x':1.6, 'y':3}, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
    # save model
    kicad_mod.save('{footprint_name}.kicad_mod'.format(footprint_name=footprint_name))
    
    
    
