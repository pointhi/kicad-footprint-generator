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


def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision


def footprint_name(package, num_pins, add_tab, tab_number):
    tab_suffix = '_TabPin' if add_tab else ''
    pins = str(num_pins)
    tab = str(tab_number) if add_tab else ''
    name = '{p:s}-{ps:s}Lead{ts:s}{tn:s}'.format(p=package, ps=pins, ts=tab_suffix, tn=tab)
    return name


def build_footprint(base, variant, cut_pin=False, tab_linked=False):

    CENTRE_PIN = 1 + variant['pins'] // 2
    TAB_PIN_NUMBER = CENTRE_PIN if tab_linked else variant['pins'] + 1

    NAME = footprint_name(base['package'], variant['pins'], not cut_pin, TAB_PIN_NUMBER)

    PAD_1_X_MM = (variant['pad']['x_mm'] - base['footprint']['x_mm']) / 2.0
    PAD_1_Y_MM = -variant['pitch'] * (variant['pins'] - 1) / 2.0
    TAB_POS_X_MM = (base['footprint']['x_mm'] - base['footprint']['tab_x_mm']) / 2.0
    TAB_POS_Y_MM = 0.0

    dev = base['device']
    DEVICE_OFFSET_X_MM = dev['x_mm'] / 2.0
    TAB_X_MM = dev['tab']['x_mm']
    TAB_OFFSET_Y_MM = dev['tab']['y_mm'] / 2.0
    BODY_X_MM = dev['body']['x_mm']
    BODY_OFFSET_Y_MM = dev['body']['y_mm'] / 2.0
    CORNER = 1.0

    COURTYARD_CLEARANCE = 0.25
    COURTYARD_PRECISION = 0.01
    biggest_x_mm = base['footprint']['x_mm']
    biggest_y_mm = max(base['footprint']['tab_y_mm'], base['device']['body']['y_mm'], PAD_1_Y_MM + variant['pad']['y_mm'] / 2.0) 
    COURTYARD_OFFSET_X_MM = round_to(COURTYARD_CLEARANCE + biggest_x_mm / 2.0, COURTYARD_PRECISION)
    COURTYARD_OFFSET_Y_MM = round_to(COURTYARD_CLEARANCE + biggest_y_mm / 2.0, COURTYARD_PRECISION)

    LABEL_X_MM = 0
    LABEL_Y_MM = COURTYARD_OFFSET_Y_MM + 0.7

    SILK_LINE_NUDGE = 0.15

    FAB_LINE_WIDTH_MM = 0.1
    SILK_LINE_WIDTH_MM = 0.12
    COURTYARD_LINE_WIDTH_MM = 0.05

    SPLIT_PASTE = (base['footprint']['split_paste'] == 'on')

    # initialise footprint
    kicad_mod = Footprint(NAME)
    kicad_mod.setDescription(variant['datasheet'])
    kicad_mod.setTags('{bk:s} {vk:s}'.format(bk=base['keywords'], vk=variant['keywords']))
    kicad_mod.setAttribute('smd')

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', size=[1,1], at=[LABEL_X_MM, -LABEL_Y_MM], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='%R', size=[1,1], at=[0, 0], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=NAME, at=[LABEL_X_MM, LABEL_Y_MM], layer='F.Fab'))

    # create pads
    for pin in range(1, variant['pins'] + 1):
        if not (pin == CENTRE_PIN and cut_pin):
            kicad_mod.append(Pad(number=pin, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                                 at=[PAD_1_X_MM, PAD_1_Y_MM + (pin - 1) * variant['pitch']],\
                                 size=[variant['pad']['x_mm'], variant['pad']['y_mm']], \
                                 layers=Pad.LAYERS_SMT))
    tab_layers = Pad.LAYERS_SMT[:]
    paste_layers = ['F.Paste']
    if SPLIT_PASTE:
        tab_layers.remove('F.Paste')
    kicad_mod.append(Pad(number=TAB_PIN_NUMBER, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                         at=[TAB_POS_X_MM, TAB_POS_Y_MM],\
                         size=[base['footprint']['tab_x_mm'], base['footprint']['tab_y_mm']], \
                         layers=tab_layers))
    paste_x_mm = (base['footprint']['tab_x_mm'] - base['footprint']['paste_gutter_mm']) / 2.0
    paste_y_mm = (base['footprint']['tab_y_mm'] - base['footprint']['paste_gutter_mm']) / 2.0
    paste_offset_x_mm = (paste_x_mm + base['footprint']['paste_gutter_mm']) / 2.0
    paste_offset_y_mm = (paste_y_mm + base['footprint']['paste_gutter_mm']) / 2.0
    kicad_mod.append(Pad(number=TAB_PIN_NUMBER, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                         at=[TAB_POS_X_MM + paste_offset_x_mm, TAB_POS_Y_MM + paste_offset_y_mm],\
                         size=[paste_x_mm, paste_y_mm], \
                         layers=paste_layers))
    kicad_mod.append(Pad(number=TAB_PIN_NUMBER, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                         at=[TAB_POS_X_MM - paste_offset_x_mm, TAB_POS_Y_MM - paste_offset_y_mm],\
                         size=[paste_x_mm, paste_y_mm], \
                         layers=paste_layers))
    kicad_mod.append(Pad(number=TAB_PIN_NUMBER, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                         at=[TAB_POS_X_MM + paste_offset_x_mm, TAB_POS_Y_MM - paste_offset_y_mm],\
                         size=[paste_x_mm, paste_y_mm], \
                         layers=paste_layers))
    kicad_mod.append(Pad(number=TAB_PIN_NUMBER, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,\
                         at=[TAB_POS_X_MM - paste_offset_x_mm, TAB_POS_Y_MM + paste_offset_y_mm],\
                         size=[paste_x_mm, paste_y_mm], \
                         layers=paste_layers))

    # create fab outline 
    tab_outline = [[DEVICE_OFFSET_X_MM - TAB_X_MM, -TAB_OFFSET_Y_MM], [DEVICE_OFFSET_X_MM, -TAB_OFFSET_Y_MM],\
                   [DEVICE_OFFSET_X_MM, TAB_OFFSET_Y_MM], [DEVICE_OFFSET_X_MM - TAB_X_MM, TAB_OFFSET_Y_MM]]
    body_outline = [[DEVICE_OFFSET_X_MM - TAB_X_MM, -BODY_OFFSET_Y_MM], [DEVICE_OFFSET_X_MM - TAB_X_MM, BODY_OFFSET_Y_MM],\
                   [DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM, BODY_OFFSET_Y_MM], [DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM, -BODY_OFFSET_Y_MM + CORNER],\
                   [DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM + CORNER, -BODY_OFFSET_Y_MM], [DEVICE_OFFSET_X_MM - TAB_X_MM, -BODY_OFFSET_Y_MM]]

    kicad_mod.append(PolygoneLine(polygone=tab_outline, layer='F.Fab', width=FAB_LINE_WIDTH_MM))
    kicad_mod.append(PolygoneLine(polygone=body_outline, layer='F.Fab', width=FAB_LINE_WIDTH_MM))

    # create silkscreen marks and pin 1 marker 
    top_outline = [[DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM + 1.3, -BODY_OFFSET_Y_MM - SILK_LINE_NUDGE],\
                   [DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM - SILK_LINE_NUDGE, -BODY_OFFSET_Y_MM - SILK_LINE_NUDGE],\
                   [DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM - SILK_LINE_NUDGE, PAD_1_Y_MM - variant['pad']['y_mm'] / 2.0 - SILK_LINE_NUDGE],
                   [PAD_1_X_MM - variant['pad']['x_mm'] / 2.0, PAD_1_Y_MM - variant['pad']['y_mm'] / 2.0 - SILK_LINE_NUDGE]]
    bottom_outline = [[DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM + 1.3, BODY_OFFSET_Y_MM + SILK_LINE_NUDGE],\
                     [DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM - SILK_LINE_NUDGE, BODY_OFFSET_Y_MM + SILK_LINE_NUDGE],\
                     [DEVICE_OFFSET_X_MM - TAB_X_MM - BODY_X_MM - SILK_LINE_NUDGE, -PAD_1_Y_MM + variant['pad']['y_mm'] / 2.0 + SILK_LINE_NUDGE]]
    kicad_mod.append(PolygoneLine(polygone=top_outline, layer='F.SilkS', width=SILK_LINE_WIDTH_MM))
    kicad_mod.append(PolygoneLine(polygone=bottom_outline, layer='F.SilkS', width=SILK_LINE_WIDTH_MM))


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

    devices = yaml.load_all(open('dpak-config.yaml'))

    for device in devices:
        if args.family:
            if args.family[0] == device['base']['package']:
                build_family(device)
        else:
            build_family(device)

