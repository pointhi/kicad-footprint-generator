#!/usr/bin/env python

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import sys
import os
import argparse
import yaml
import pprint

sys.path.append(os.path.join(sys.path[0], "../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', help='device type to build: TO-252 | TO-263 | TO-268  (default is all)', type=str, nargs=1)
    parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true')
    return parser.parse_args()


<<<<<<< Updated upstream
def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision


def footprint_name(package, num_pins, add_tab, tab_number):
    tab_suffix = '_TabPin' if add_tab else ''
    pins = str(num_pins)
    tab = str(tab_number) if add_tab else ''
    name = '{p:s}-{ps:s}{ts:s}{tn:s}'.format(p=package, ps=pins, ts=tab_suffix, tn=tab)
    return name


def build_footprint(base, variant, cut_pin=False, tab_linked=False):

    CENTRE_PIN = 1 + variant['pins'] // 2
    TAB_PIN_NUMBER = CENTRE_PIN if (tab_linked or cut_pin) else variant['pins'] + 1

    NAME = footprint_name(base['package'], variant['pins'] - 1 if cut_pin else variant['pins'], not cut_pin, TAB_PIN_NUMBER)

    PAD_1_X_MM = (variant['pad']['x_mm'] - base['footprint']['overall_x_mm']) / 2.0
    PAD_1_Y_MM = -variant['pitch_mm'] * (variant['pins'] - 1) / 2.0
    TAB_POS_X_MM = (base['footprint']['overall_x_mm'] - base['footprint']['tab']['x_mm']) / 2.0
    TAB_POS_Y_MM = 0.0

    dev = base['device']
    DEVICE_OFFSET_X_MM = dev['overall_x_mm'] / 2.0
    TAB_X_MM = dev['tab']['x_mm']
    TAB_OFFSET_Y_MM = dev['tab']['y_mm'] / 2.0
    BODY_X_MM = dev['body']['x_mm']
    BODY_OFFSET_Y_MM = dev['body']['y_mm'] / 2.0
    CORNER = 1.0

    COURTYARD_CLEARANCE = 0.25
    COURTYARD_PRECISION = 0.01
    biggest_x_mm = base['footprint']['overall_x_mm']
    biggest_y_mm = max(base['footprint']['tab']['y_mm'], base['device']['body']['y_mm'], PAD_1_Y_MM + variant['pad']['y_mm'] / 2.0) 
    COURTYARD_OFFSET_X_MM = round_to(COURTYARD_CLEARANCE + biggest_x_mm / 2.0, COURTYARD_PRECISION)
    COURTYARD_OFFSET_Y_MM = round_to(COURTYARD_CLEARANCE + biggest_y_mm / 2.0, COURTYARD_PRECISION)

    LABEL_X_MM = 0
    LABEL_Y_MM = COURTYARD_OFFSET_Y_MM + 1

    SILK_LINE_NUDGE = 0.20

    FAB_LINE_WIDTH_MM = 0.1
    SILK_LINE_WIDTH_MM = 0.12
    COURTYARD_LINE_WIDTH_MM = 0.05

    SPLIT_PASTE = (base['footprint']['split_paste'] == 'on')


    def add_properties(m):
        m.setDescription('{bd:s}, {vd:s}'.format(bd=base['description'], vd=variant['datasheet']))
        m.setTags('{bk:s} {vk:s}'.format(bk=base['keywords'], vk=variant['keywords']))
        m.setAttribute('smd')
        return m


    def add_labels(m):
        m.append(Text(type='reference', text='REF**', size=[1,1], at=[LABEL_X_MM, -LABEL_Y_MM], layer='F.SilkS'))
        m.append(Text(type='user', text='%R', size=[1,1], at=[0, 0], layer='F.Fab'))
        m.append(Text(type='value', text=NAME, at=[LABEL_X_MM, LABEL_Y_MM], layer='F.Fab'))
        return m


    def draw_tab(m, layer):
        right_x = DEVICE_OFFSET_X_MM
        left_x = right_x - TAB_X_MM
        top_y = -TAB_OFFSET_Y_MM
        bottom_y = -top_y
        tab_outline = [[left_x, top_y], [right_x, top_y], [right_x, bottom_y], [left_x, bottom_y]]
        m.append(PolygoneLine(polygone=tab_outline, layer=layer, width=FAB_LINE_WIDTH_MM))
        return m


    def draw_body(m, layer):
        right_x = DEVICE_OFFSET_X_MM - TAB_X_MM
        left_x = right_x - BODY_X_MM
        top_y = -BODY_OFFSET_Y_MM
        bottom_y = -top_y
        body_outline = [[right_x, top_y], [right_x, bottom_y], [left_x, bottom_y],\
                        [left_x, top_y + CORNER], [left_x + CORNER, top_y], [right_x, top_y]]
        m.append(PolygoneLine(polygone=body_outline, layer=layer, width=FAB_LINE_WIDTH_MM))
        return m


    def draw_pins(m, layer):
        right_x = DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM
        left_x = right_x - variant['pin']['x_mm']
        pin_1_top_y_mm = PAD_1_Y_MM - (variant['pin']['y_mm'] / 2.0)
        body_corner_bottom_y_mm = -BODY_OFFSET_Y_MM + CORNER
        pin_1_extend_mm = (body_corner_bottom_y_mm - pin_1_top_y_mm) if (pin_1_top_y_mm < body_corner_bottom_y_mm) else 0.0
        for pin in range(1, variant['pins'] + 1):
            if not (pin == CENTRE_PIN and cut_pin):
                top_y = PAD_1_Y_MM + ((pin - 1) * variant['pitch_mm']) - (variant['pin']['y_mm'] / 2.0)
                bottom_y = PAD_1_Y_MM + ((pin - 1) * variant['pitch_mm']) + (variant['pin']['y_mm'] / 2.0)
                pin_outline = [[right_x + (pin_1_extend_mm if pin == 1 else 0), top_y],\
                               [left_x , top_y], [left_x, bottom_y], [right_x, bottom_y]]
                kicad_mod.append(PolygoneLine(polygone=pin_outline, layer=layer, width=FAB_LINE_WIDTH_MM))
        return m


    def draw_outline(m, layer):
        m = draw_tab(m, layer)
        m = draw_body(m, layer)
        m = draw_pins(m, layer)
        return m


    def draw_markers(m, layer):
        magic_number = 1.3  # TODO needs better name
        other_magic_number = 1.5  #  TODO needs better name
        right_x = DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM + magic_number
        middle_x = DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM - SILK_LINE_NUDGE
        left_x = PAD_1_X_MM - variant['pad']['x_mm'] / 2.0
        top_y = -BODY_OFFSET_Y_MM - SILK_LINE_NUDGE
        bottom_y = PAD_1_Y_MM - variant['pad']['y_mm'] / 2.0 - other_magic_number * SILK_LINE_NUDGE
        top_marker = [[right_x, top_y], [middle_x, top_y], [middle_x, bottom_y], [left_x, bottom_y]]
        m.append(PolygoneLine(polygone=top_marker, layer=layer, width=SILK_LINE_WIDTH_MM))
        top_y = -top_y
        bottom_y = -bottom_y
        left_x = DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM - magic_number
        bottom_marker = [[right_x, top_y], [middle_x, top_y], [middle_x, bottom_y], [left_x, bottom_y]]
        m.append(PolygoneLine(polygone=bottom_marker, layer=layer, width=SILK_LINE_WIDTH_MM))
        return m


    def draw_pads(m):
        for pin in range(1, variant['pins'] + 1):
            if not (pin == CENTRE_PIN and cut_pin):
                kicad_mod.append(Pad(number=pin, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                                     at=[PAD_1_X_MM, PAD_1_Y_MM + (pin - 1) * variant['pitch_mm']],\
                                     size=[variant['pad']['x_mm'], variant['pad']['y_mm']], \
                                     layers=Pad.LAYERS_SMT))
        tab_layers = Pad.LAYERS_SMT[:]
        if SPLIT_PASTE:
            tab_layers.remove('F.Paste')
        paste_layers = Pad.LAYERS_SMT[:]
        paste_layers.remove('F.Mask')
        kicad_mod.append(Pad(number=TAB_PIN_NUMBER, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                             at=[TAB_POS_X_MM, TAB_POS_Y_MM],\
                             size=[base['footprint']['tab']['x_mm'], base['footprint']['tab']['y_mm']], \
                             layers=tab_layers))
        if SPLIT_PASTE:
            gutter_mm = base['footprint']['paste_gutter_mm']
            paste_x_mm = (base['footprint']['tab']['x_mm'] - gutter_mm) / 2.0
            paste_y_mm = (base['footprint']['tab']['y_mm'] - gutter_mm) / 2.0
            paste_offset_x_mm = (paste_x_mm + gutter_mm) / 2.0
            paste_offset_y_mm = (paste_y_mm + gutter_mm) / 2.0
            left_x = TAB_POS_X_MM - paste_offset_x_mm
            right_x = TAB_POS_X_MM + paste_offset_x_mm
            top_y = TAB_POS_Y_MM - paste_offset_y_mm
            bottom_y = TAB_POS_Y_MM + paste_offset_y_mm
            for pad_xy in [[right_x, bottom_y], [left_x, top_y], [right_x, top_y], [left_x, bottom_y]]:
                kicad_mod.append(Pad(number=TAB_PIN_NUMBER, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                                     at=pad_xy, size=[paste_x_mm, paste_y_mm], layers=paste_layers))
        return m


    # initialise footprint
    kicad_mod = Footprint(NAME)
    kicad_mod = add_properties(kicad_mod)
    kicad_mod = add_labels(kicad_mod)

    # create pads
    kicad_mod = draw_pads(kicad_mod)

    # create fab outline 
    kicad_mod = draw_outline(kicad_mod, 'F.Fab')

    # create silkscreen marks and pin 1 marker 
    kicad_mod = draw_markers(kicad_mod, 'F.SilkS')

    # create courtyard
    kicad_mod.append(RectLine(start=[-COURTYARD_OFFSET_X_MM, -COURTYARD_OFFSET_Y_MM],\
                              end=[COURTYARD_OFFSET_X_MM, COURTYARD_OFFSET_Y_MM], layer='F.CrtYd', width=COURTYARD_LINE_WIDTH_MM))

    # add 3D model
    kicad_mod.append(Model(filename="{p:s}/{n:s}.wrl".format(p=base['3d_prefix'], n=NAME), at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    # print render tree
    if args.verbose:
        print(kicad_mod.getRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{:s}.kicad_mod'.format(NAME))


def build_family(config):
    print('Building family {f:s}'.format(f=config['base']['package']))
    base = config['base']
    for variant in config['variants']:
        if 'uncut' in variant['centre_pin']:
            build_footprint(base, variant)
            build_footprint(base, variant, tab_linked=True)
        if 'cut' in variant['centre_pin']:
            build_footprint(base, variant, cut_pin=True)


if __name__ == '__main__':

    print('Building DPAK')

    args = get_args()

    print('Rebuilding DPAK')

    from DPAK import DPAK, TO252, TO263, TO268

    CONFIG = 'DPAK_config.yaml' 

    if args.family:
        build_list = []
        pass
    else:
        build_list = [TO252(CONFIG), TO263(CONFIG), TO268(CONFIG)]
        
    for package in build_list:
        package.build_family(verbose=args.verbose)


"""

    devices = yaml.load_all(open('DPAK_config.yaml'))

    for device in devices:
        if args.family:
            if args.family[0] == device['base']['package']:
                build_family(device)
        else:
            build_family(device)


