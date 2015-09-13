#!/usr/bin/env python

import argparse
from kicad_mod import KicadMod

parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('--type', help='what type of jst connector (default: B*B-PH-K)', default='B*B-PH-K', nargs=1) #TODO
parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
args = parser.parse_args()

#http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

def createNumberedPadsTHT(kicad_mod, pincount, pad_spacing, pad_diameter, pad_size):
    for pad_number in range(1, pincount+1):
        pad_pos_x = (pad_number-1)*pad_spacing
        if pad_number == 1:
            kicad_mod.addPad(pad_number, 'thru_hole', 'rect', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])
        elif pad_size['x'] == pad_size['y']:
            kicad_mod.addPad(pad_number, 'thru_hole', 'circle', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])
        else:
            kicad_mod.addPad(pad_number, 'thru_hole', 'oval', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])

def createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, pad_size, pad_pos_y):
    for pad_number in range(1, pincount+1):
        pad_pos_x = (pad_number-1)*pad_spacing
        kicad_mod.addPad(pad_number, 'smd', 'rect', {'x':pad_pos_x, 'y':pad_pos_y}, pad_size, 0, ['F.Cu', 'F.Paste', 'F.Mask'])

pincount = int(args.pincount[0])
connector_type = 'B*B-PH-K'

if connector_type == 'B*B-PH-K':
    # Through-hole type shrouded header, Top entry type
    footprint_name = 'Connectors_JST_B{pincount}B-PH-K'.format(pincount=pincount)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST PH series connector, B{pincount}B-PH-K".format(pincount=pincount))

    # set general values
    kicad_mod.addText('reference', 'CON**', {'x':0, 'y':-3}, 'F.SilkS')
    kicad_mod.addText('value', footprint_name, {'x':(pincount-1)*2/2, 'y':4}, 'F.Fab')

    # create Silkscreen
    kicad_mod.addRectLine({'x':-1.95, 'y':2.8}, {'x':(pincount-1)*2+1.95, 'y':-1.7}, 'F.SilkS', 0.15)
    #kicad_mod.addLine({'x':-1.95, 'y':2}, {'x':(pincount-1)*2+1.95, 'y':2}, 'F.SilkS', 0.15)
    #kicad_mod.addPolygoneLine([{'x':0.5, 'y':-1.7}, {'x':0.5, 'y':-1.2}, {'x':(pincount-1)*2-0.5, 'y':-1.2}, {'x':(pincount-1)*2-0.5, 'y':-1.7}], 'F.SilkS', 0.15)
    
    kicad_mod.addPolygoneLine([{'x':0.5, 'y':-1.7}
                              ,{'x':0.5, 'y':-1.2}
                              ,{'x':-1.45, 'y':-1.2}
                              ,{'x':-1.45, 'y':2.3}
                              ,{'x':(pincount-1)*2+1.45, 'y':2.3}
                              ,{'x':(pincount-1)*2+1.45, 'y':-1.2}
                              ,{'x':(pincount-1)*2-0.5, 'y':-1.2}
                              ,{'x':(pincount-1)*2-0.5, 'y':-1.7}], 'F.SilkS', 0.15)

    kicad_mod.addLine({'x':-1.95, 'y':-0.5}, {'x':-1.45, 'y':-0.5}, 'F.SilkS', 0.15)
    kicad_mod.addLine({'x':-1.95, 'y':0.8}, {'x':-1.45, 'y':0.8}, 'F.SilkS', 0.15)
    
    kicad_mod.addLine({'x':(pincount-1)*2+1.45, 'y':-0.5}, {'x':(pincount-1)*2+1.95, 'y':-0.5}, 'F.SilkS', 0.15)
    kicad_mod.addLine({'x':(pincount-1)*2+1.45, 'y':0.8}, {'x':(pincount-1)*2+1.95, 'y':0.8}, 'F.SilkS', 0.15)

    kicad_mod.addPolygoneLine([{'x':-0.3, 'y':-1.7}
                              ,{'x':-0.3, 'y':-1.9}
                              ,{'x':-0.6, 'y':-1.9}
                              ,{'x':-0.6, 'y':-1.7}], 'F.SilkS', 0.15)
    kicad_mod.addLine({'x':-0.3, 'y':-1.8}, {'x':-0.6, 'y':-1.8}, 'F.SilkS', 0.15)

    for i in range(0, pincount-1):
        middle_x = 1+i*2
        start_x = middle_x-0.1
        end_x = middle_x+0.1
        kicad_mod.addPolygoneLine([{'x':start_x, 'y':2.3}
                                  ,{'x':start_x, 'y':1.8}
                                  ,{'x':end_x, 'y':1.8}
                                  ,{'x':end_x, 'y':2.3}], 'F.SilkS', 0.15)
        kicad_mod.addLine({'x':middle_x, 'y':2.3}, {'x':middle_x, 'y':1.8}, 'F.SilkS', 0.15)
        
    # create Courtyard
    kicad_mod.addRectLine({'x':-1.95-0.25, 'y':2.8+0.25}, {'x':(pincount-1)*2+1.95+0.25, 'y':-1.7-0.25}, 'F.CrtYd', 0.05)

    createNumberedPadsTHT(kicad_mod, pincount, 2, 0.8, {'x':1.2, 'y':1.7})

    # save model
    kicad_mod.save('Connectors_JST_PH/{footprint_name}.kicad_mod'.format(footprint_name=footprint_name))

elif connector_type == 'S*B-PH-K':
    # Through-hole type shrouded header, Side entry type
    footprint_name = 'Connectors_JST_S{pincount}B-PH-K'.format(pincount=pincount)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST PH series connector, S{pincount}B-PH-K".format(pincount=pincount))
    
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
    footprint_name = 'Connectors_JST_S{pincount}B-PH-SM4-TB'.format(pincount=pincount)

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST PH series connector, S{pincount}B-PH-SM4-TB".format(pincount=pincount))
    
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
    
    
    
