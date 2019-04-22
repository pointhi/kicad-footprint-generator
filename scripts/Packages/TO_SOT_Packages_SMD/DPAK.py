import sys
import os
import argparse
import yaml
import pprint

sys.path.append(os.path.join(sys.path[0], "../../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA


class Dimensions(object):

    def __init__(self, base, variant, cut_pin=False, tab_linked=False):
        # FROM KLC
        self.fab_line_width_mm = 0.1
        self.silk_line_width_mm = 0.12
        self.courtyard_line_width_mm = 0.05
        self.courtyard_clearance_mm = 0.25
        self.courtyard_precision_mm = 0.01

        # PIN NUMBERING
        self.centre_pin = 1 + variant['pins'] // 2
        self.tab_pin_number= self.centre_pin if (tab_linked or cut_pin) else variant['pins'] + 1

        # NAME
        self.name = self.footprint_name(base['series'], (variant['pins'] - 1) if cut_pin else variant['pins'],
                                        not cut_pin, self.tab_pin_number)
        # PADS
        self.pad_1_centre_x_mm = (variant['pad']['x_mm'] / 2.0) - (base['footprint']['x_mm'] / 2.0)
        self.pad_1_centre_y_mm = -variant['pitch_mm'] * (variant['pins'] - 1) / 2.0
        self.tab_centre_x_mm = (base['footprint']['x_mm'] - base['footprint']['tab']['x_mm']) / 2.0
        self.tab_centre_y_mm = 0.0
        self.split_paste = (base['footprint']['split_paste'] == 'on')

        # FAB OUTLINE
        self.device_offset_x_mm = base['device']['x_mm'] / 2.0  # x coordinate of RHS of device
        self.tab_project_x_mm = base['device']['tab']['project_x_mm']
        self.tab_offset_y_mm = base['device']['tab']['y_mm'] / 2.0  # y coordinate of bottom of tab
        self.body_x_mm = base['device']['body']['x_mm']
        self.body_offset_y_mm = base['device']['body']['y_mm'] / 2.0  # y coordinate of bottom of body
        self.corner_mm = 1.0  #  x and y size of chamfered corner on top left of body -- from KLC

        # COURTYARD
        self.biggest_x_mm = base['footprint']['x_mm']
        self.biggest_y_mm = max(base['footprint']['tab']['y_mm'], base['device']['body']['y_mm'],
                                       2.0 * self.pad_1_centre_y_mm + variant['pad']['y_mm'])
        self.courtyard_offset_x_mm = self.round_to(self.courtyard_clearance_mm + self.biggest_x_mm / 2.0,
                                                   self.courtyard_precision_mm)
        self.courtyard_offset_y_mm = self.round_to(self.courtyard_clearance_mm + self.biggest_y_mm / 2.0,
                                                   self.courtyard_precision_mm)
        # SILKSCREEN
        self.label_centre_x_mm = 0
        self.label_centre_y_mm = self.courtyard_offset_y_mm + 1
        self.silk_line_nudge_mm = 0.20  #  amount to shift to stop silkscreen lines overlapping fab lines


    def round_to(self, n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int(n / precision + correction) * precision


    def footprint_name(self, series, num_pins, add_tab, tab_number):
        tab_suffix = '_TabPin' if add_tab else ''
        pins = str(num_pins)
        tab = str(tab_number) if add_tab else ''
        name = '{p:s}-{ps:s}{ts:s}{tn:s}'.format(p=series, ps=pins, ts=tab_suffix, tn=tab)
        return name


class DPAK(object):

    def __init__(self, config_file):
        self.SERIES = None
        self.config = None


    def load_config(self, config_file):
        try:
            devices = yaml.safe_load_all(open(config_file))
        except FileNotFoundError as fnfe:
            print(fnfe)
            return
        config = None
        for dev in devices:
            if dev['base']['series'] == self.SERIES:
                config = dev
                break
        return config


    def add_properties(self, m, variant):
        m.setDescription('{bd:s}, {vd:s}'.format(bd=self.config['base']['description'], vd=variant['datasheet']))
        m.setTags('{bk:s} {vk:s}'.format(bk=self.config['base']['keywords'], vk=variant['keywords']))
        m.setAttribute('smd')
        return m


    def add_labels(self, m, variant, dim):
        m.append(Text(type='reference', text='REF**', size=[1,1], at=[dim.label_centre_x_mm, -dim.label_centre_y_mm],
                      layer='F.SilkS'))
        m.append(Text(type='user', text='%R', size=[1,1], at=[0, 0], layer='F.Fab'))
        m.append(Text(type='value', text=dim.name, at=[dim.label_centre_x_mm, dim.label_centre_y_mm], layer='F.Fab'))
        return m


    def draw_tab(self, m, dim):
        right_x = dim.device_offset_x_mm
        left_x = right_x - dim.tab_project_x_mm
        top_y = -dim.tab_offset_y_mm
        bottom_y = -top_y
        tab_outline = [[left_x, top_y], [right_x, top_y], [right_x, bottom_y], [left_x, bottom_y]]
        m.append(PolygoneLine(polygone=tab_outline, layer='F.Fab', width=dim.fab_line_width_mm))
        return m


    def draw_body(self, m, dim):
        right_x = dim.device_offset_x_mm - dim.tab_project_x_mm
        left_x = right_x - dim.body_x_mm
        top_y = -dim.body_offset_y_mm
        bottom_y = -top_y
        body_outline = [[right_x, top_y], [right_x, bottom_y], [left_x, bottom_y],\
                        [left_x, top_y + dim.corner_mm], [left_x + dim.corner_mm, top_y], [right_x, top_y]]
        m.append(PolygoneLine(polygone=body_outline, layer='F.Fab', width=dim.fab_line_width_mm))
        return m


    def draw_pins(self, m, variant, dim, cut_pin):
        right_x = dim.device_offset_x_mm - dim.tab_project_x_mm - dim.body_x_mm
        left_x = right_x - variant['pin']['x_mm']
        pin_1_top_y = dim.pad_1_centre_y_mm - (variant['pin']['y_mm'] / 2.0)
        body_corner_bottom_y = -dim.body_offset_y_mm + dim.corner_mm
        pin_1_extend = (body_corner_bottom_y - pin_1_top_y) if (pin_1_top_y < body_corner_bottom_y) else 0.0
        for pin in range(1, variant['pins'] + 1):
            if not (pin == dim.centre_pin and cut_pin):
                top_y = dim.pad_1_centre_y_mm + ((pin - 1) * variant['pitch_mm']) - (variant['pin']['y_mm'] / 2.0)
                bottom_y = dim.pad_1_centre_y_mm + ((pin - 1) * variant['pitch_mm']) + (variant['pin']['y_mm'] / 2.0)
                pin_outline = [[right_x + (pin_1_extend if pin == 1 else 0), top_y],
                               [left_x , top_y], [left_x, bottom_y], [right_x, bottom_y]]
                m.append(PolygoneLine(polygone=pin_outline, layer='F.Fab', width=dim.fab_line_width_mm))
        return m


    def draw_outline(self, m, variant, dim, cut_pin=False):
        m = self.draw_tab(m, dim)
        m = self.draw_body(m, dim)
        m = self.draw_pins(m, variant, dim, cut_pin)
        return m


    def draw_markers(self, m, variant, dim):
        magic_number = 1.3  # TODO needs better name
        other_magic_number = 1.5  #  TODO needs better name
        right_x = dim.device_offset_x_mm - dim.tab_project_x_mm - dim.body_x_mm + magic_number
        middle_x = dim.device_offset_x_mm - dim.tab_project_x_mm - dim.body_x_mm - dim.silk_line_nudge_mm
        left_x = dim.pad_1_centre_x_mm - variant['pad']['x_mm'] / 2.0
        top_y = -dim.body_offset_y_mm - dim.silk_line_nudge_mm
        bottom_y = dim.pad_1_centre_y_mm - variant['pad']['y_mm'] / 2.0 - other_magic_number * dim.silk_line_nudge_mm
        top_marker = [[right_x, top_y], [middle_x, top_y], [middle_x, bottom_y], [left_x, bottom_y]]
        m.append(PolygoneLine(polygone=top_marker, layer='F.SilkS', width=dim.silk_line_width_mm))
        top_y = -top_y
        bottom_y = -bottom_y
        left_x = dim.device_offset_x_mm - dim.tab_project_x_mm - dim.body_x_mm - magic_number
        bottom_marker = [[right_x, top_y], [middle_x, top_y], [middle_x, bottom_y], [left_x, bottom_y]]
        m.append(PolygoneLine(polygone=bottom_marker, layer='F.SilkS', width=dim.silk_line_width_mm))
        return m


    def draw_pads(self, m, base, variant, dim, cut_pin):
        for pin in range(1, variant['pins'] + 1):
            if not (pin == dim.centre_pin and cut_pin):
                m.append(Pad(number=pin, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                                     at=[dim.pad_1_centre_x_mm, dim.pad_1_centre_y_mm + (pin - 1) * variant['pitch_mm']],
                                     size=[variant['pad']['x_mm'], variant['pad']['y_mm']],
                                     layers=Pad.LAYERS_SMT))
        tab_layers = Pad.LAYERS_SMT[:]
        if dim.split_paste:
            tab_layers.remove('F.Paste')
        paste_layers = Pad.LAYERS_SMT[:]
        paste_layers.remove('F.Mask')
        m.append(Pad(number=dim.tab_pin_number, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                             at=[dim.tab_centre_x_mm, dim.tab_centre_y_mm],
                             size=[base['footprint']['tab']['x_mm'], base['footprint']['tab']['y_mm']],
                             layers=tab_layers))
        if dim.split_paste:
            gutter = base['footprint']['paste_gutter_mm']
            paste_x_mm = (base['footprint']['tab']['x_mm'] - gutter) / 2.0
            paste_y_mm = (base['footprint']['tab']['y_mm'] - gutter) / 2.0
            paste_offset_x = (paste_x_mm + gutter) / 2.0
            paste_offset_y = (paste_y_mm + gutter) / 2.0
            left_x = dim.tab_centre_x_mm - paste_offset_x
            right_x = dim.tab_centre_x_mm + paste_offset_x
            top_y = dim.tab_centre_y_mm - paste_offset_y
            bottom_y = dim.tab_centre_y_mm + paste_offset_y
            for pad_xy in [[right_x, bottom_y], [left_x, top_y], [right_x, top_y], [left_x, bottom_y]]:
                m.append(Pad(number=dim.tab_pin_number, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                                     at=pad_xy, size=[paste_x_mm, paste_y_mm], layers=paste_layers))
        return m


    def add_3D_model(self, m, base, dim):
        m.append(
            Model(filename="{p:s}/{n:s}.wrl".format(p=base['3d_prefix'], n=dim.name), at=[0, 0, 0], scale=[1, 1, 1],
                  rotate=[0, 0, 0]))
        return m


    def draw_courtyard(self, m ,dim):
        m.append(RectLine(start=[-dim.courtyard_offset_x_mm, -dim.courtyard_offset_y_mm],
                                  end=[dim.courtyard_offset_x_mm, dim.courtyard_offset_y_mm], layer='F.CrtYd',
                                  width=dim.courtyard_line_width_mm))
        return m


    def build_footprint(self, base, variant, cut_pin=False, tab_linked=False, verbose=False):

        # calculate dimensions and other attributes specific to this variant
        dim = Dimensions(base, variant, cut_pin, tab_linked)

        # initialise footprint
        kicad_mod = Footprint(dim.name)
        kicad_mod = self.add_properties(kicad_mod, variant)
        kicad_mod = self.add_labels(kicad_mod, variant, dim)

        # create pads
        kicad_mod = self.draw_pads(kicad_mod, base, variant, dim, cut_pin)

        # create fab outline
        kicad_mod = self.draw_outline(kicad_mod, variant, dim, cut_pin)

        # create silkscreen marks and pin 1 marker
        kicad_mod = self.draw_markers(kicad_mod, variant, dim)

        # create courtyard
        kicad_mod = self.draw_courtyard(kicad_mod, dim)

        # add 3D model
        kicad_mod = self.add_3D_model(kicad_mod, base, dim)

        # print render tree
        if verbose:
            print(kicad_mod.getRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile('{:s}.kicad_mod'.format(dim.name))


    def build_series(self, verbose=False):
        print('Building {p:s}'.format(p=self.config['base']['description']))
        base = self.config['base']
        for variant in self.config['variants']:
            if 'uncut' in variant['centre_pin']:
                self.build_footprint(base, variant, verbose=verbose)
                self.build_footprint(base, variant, tab_linked=True, verbose=verbose)
            if 'cut' in variant['centre_pin']:
                self.build_footprint(base, variant, cut_pin=True, verbose=verbose)


class TO252(DPAK):

    def __init__(self, config_file):
        self.SERIES = 'TO-252'
        self.config = self.load_config(config_file)


class TO263(DPAK):

    def __init__(self, config_file):
        self.SERIES = 'TO-263'
        self.config = self.load_config(config_file)


class TO268(DPAK):

    def __init__(self, config_file):
        self.SERIES = 'TO-268'
        self.config = self.load_config(config_file)

class ATPAK(DPAK):

    def __init__(self, config_file):
        self.SERIES = 'ATPAK'
        self.config = self.load_config(config_file)
