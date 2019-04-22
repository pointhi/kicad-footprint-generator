import sys
import os
import argparse
import yaml
import pprint

sys.path.append(os.path.join(sys.path[0], "../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA
from bump import *
from corners import *
from chamfers import *


class Dimensions(object):

    def __init__(self, base, variant, cut_pin=False, tab_linked=False):

        footprint = variant['footprint']
        device = variant['device']

        # FROM KLC
        self.fab_line_width_mm = 0.1
        self.fab_text_size = [1.0, 1.0]
        self.fab_text_thickness = 0.15
        self.fab_reference_text_size = [0.5, 0.5]
        self.fab_reference_text_thickness = 0.05
        self.silk_line_width_mm = 0.12
        self.silk_text_size = [1.0, 1.0]
        self.silk_text_thickness = 0.15
        self.courtyard_line_width_mm = 0.05
        self.courtyard_clearance_mm = 0.25
        self.courtyard_precision_mm = 0.01

        # NAME
        self.name = self._footprint_name(variant['manufacturer'], variant['series'])

        # PADS
        self.pad_offset_x_mm = (footprint['pad']['x_mm'] - footprint['x_mm']) / 2.0

        # FAB OUTLINE
        self.device_offset_x_mm = device['body']['x_mm'] / 2.0  # x coordinate of RHS of device
        self.body_x_mm = device['body']['x_mm']
        self.body_offset_y_mm = device['body']['y_mm'] / 2.0  # y coordinate of bottom of body
        
        # COURTYARD
        self.biggest_x_mm = footprint['x_mm']
        self.biggest_y_mm = device['body']['y_mm']
        if 'top' in device['projection']['sides'] or 'bottom' in device['projection']['sides']:
             self.biggest_y_mm += 2.0 * device['projection']['offset_mm']
        self.courtyard_offset_x_mm = self._round_to(self.courtyard_clearance_mm + self.biggest_x_mm / 2.0,
                                                   self.courtyard_precision_mm)
        self.courtyard_offset_y_mm = self._round_to(self.courtyard_clearance_mm + self.biggest_y_mm / 2.0,
                                                   self.courtyard_precision_mm)
        # SILKSCREEN
        self.label_centre_x_mm = 0
        self.label_centre_y_mm = self.courtyard_offset_y_mm + 1
        self.silk_offset_mm = (0.2, 0.2)  #  amount to shift silkscreen in X and Y directions to avoid overlapping fab lines


    def _round_to(self, n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int(n / precision + correction) * precision


    def _footprint_name(self, manufacturer, series):
        name = 'C_Trimmer_{m:s}_{s:s}'.format(m=manufacturer, s=series)
        return name


class CapacitorTrimmer(object):

    def __init__(self, config_file):
        self.FAMILY = None
        self.config = None


    def _load_config(self, config_file):
        try:
            devices = yaml.safe_load_all(open(config_file))
        except FileNotFoundError as fnfe:
            print(fnfe)
            return
        config = None
        for dev in devices:
            if dev['base']['family'] == self.FAMILY:
                config = dev
                break
        return config


    def _add_properties(self, m, variant):
        m.setDescription('{bd:s}, {vd:s}'.format(bd=self.config['base']['description'], vd=variant['datasheet']))
        m.setTags('{bk:s} {vk:s}'.format(bk=self.config['base']['keywords'], vk=variant['keywords']))
        m.setAttribute('smd')
        return m


    def _add_labels(self, m, variant, dim):
        m.append(Text(type='reference', text='REF**', size=dim.silk_text_size, thickness=dim.silk_text_thickness, at=[dim.label_centre_x_mm, -dim.label_centre_y_mm],
                      layer='F.SilkS'))
        m.append(Text(type='user', text='%R', size=dim.fab_reference_text_size, thickness=dim.fab_reference_text_thickness, at=[0, 0], layer='F.Fab'))
        m.append(Text(type='value', text=dim.name, size=dim.fab_text_size, thickness=dim.fab_text_thickness, at=[dim.label_centre_x_mm, dim.label_centre_y_mm], layer='F.Fab'))
        return m


    def _draw_pads(self, m, variant, dim):
        m.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                             at=[dim.pad_offset_x_mm, 0],
                             size=[variant['footprint']['pad']['x_mm'], variant['footprint']['pad']['y_mm']],
                             layers=Pad.LAYERS_SMT))
        m.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                             at=[-dim.pad_offset_x_mm, 0],
                             size=[variant['footprint']['pad']['x_mm'], variant['footprint']['pad']['y_mm']],
                             layers=Pad.LAYERS_SMT))
        return m


    def _draw_fab_outline(self, m, variant, dim, width, offset):
        # draw body
        right_x = dim.device_offset_x_mm
        left_x = right_x - dim.body_x_mm
        top_y = -dim.body_offset_y_mm
        bottom_y = -top_y
        if 'left' in variant['device']['chamfer']['sides']:
            chamfers = [{'corner': 'topleft', 'size': variant['device']['chamfer']['size_mm']}, 
                        {'corner': 'bottomleft', 'size': variant['device']['chamfer']['size_mm']}]
        elif 'right' in variant['device']['chamfer']['sides']:
            chamfers = [{'corner': 'topright', 'size': variant['device']['chamfer']['size_mm']}, 
                        {'corner': 'bottomright', 'size': variant['device']['chamfer']['size_mm']}]
        else:
            chamfers = []
        m = add_rect_chamfer(m, [left_x, top_y], [right_x, bottom_y], 'F.Fab', width, offset, chamfers)
        m.append(Circle(center=[0, 0], radius=dim.body_offset_y_mm, layer='F.Fab', width=width))
        # add frame extensions
        p = variant['device']['projection']
        if 'top' in p['sides']:
            m = add_bump(m, [0, top_y], p['x_side_mm'], p['offset_mm'], 'up', 'F.Fab', width, offset)
        if 'bottom' in p['sides']:
            m = add_bump(m, [0, bottom_y], p['x_side_mm'], p['offset_mm'], 'down', 'F.Fab', width, offset)
        if 'right' in p['sides']:
            m = add_bump(m, [right_x, 0], p['y_side_mm'], p['offset_mm'], 'right', 'F.Fab', width, offset)
        if 'left' in p['sides']:
            m = add_bump(m, [left_x, 0], p['y_side_mm'], p['offset_mm'], 'left', 'F.Fab', width, offset)
        return m


    def _draw_silk_outline(self, m, variant, dim, width, offset):
        right_x = dim.device_offset_x_mm
        left_x = right_x - dim.body_x_mm
        top_y = -dim.body_offset_y_mm
        bottom_y = -top_y
        if 'left' in variant['device']['chamfer']['sides']:
            chamfers = ['topleft', 'bottomleft']
        elif 'right' in variant['device']['chamfer']['sides']:
            chamfers = ['topright', 'bottomright']
        else:
            chamfers = []
        m = add_corners(m, [left_x, top_y], [right_x, bottom_y], 0.5, 0.5, 'F.SilkS', width, offset, chamfers)
        return m


    def _draw_courtyard(self, m ,dim):
        m.append(RectLine(start=[-dim.courtyard_offset_x_mm, -dim.courtyard_offset_y_mm],
                                  end=[dim.courtyard_offset_x_mm, dim.courtyard_offset_y_mm], layer='F.CrtYd',
                                  width=dim.courtyard_line_width_mm))
        return m


    def _add_3D_model(self, m, base, dim):
        m.append(
            Model(filename="{p:s}/{n:s}.wrl".format(p=base['3d_prefix'], n=dim.name), at=[0, 0, 0], scale=[1, 1, 1],
                  rotate=[0, 0, 0]))
        return m


    def _build_footprint(self, base, variant, cut_pin=False, tab_linked=False, verbose=False):

        # calculate dimensions and other attributes specific to this variant
        dim = Dimensions(base, variant, cut_pin, tab_linked)

        # initialise footprint
        kicad_mod = Footprint(dim.name)
        kicad_mod = self._add_properties(kicad_mod, variant)
        kicad_mod = self._add_labels(kicad_mod, variant, dim)

        # create pads
        kicad_mod = self._draw_pads(kicad_mod, variant, dim)

        # create fab outline
        kicad_mod = self._draw_fab_outline(kicad_mod, variant, dim, dim.fab_line_width_mm, (0, 0))

        # create silkscreen outline
        kicad_mod = self._draw_silk_outline(kicad_mod, variant, dim, dim.silk_line_width_mm, dim.silk_offset_mm)

        # create courtyard
        kicad_mod = self._draw_courtyard(kicad_mod, dim)

        # add 3D model
        kicad_mod = self._add_3D_model(kicad_mod, base, dim)

        # print render tree
        if verbose:
            print('\r\nMaking {n:s}'.format(n=dim.name))
            print(kicad_mod.getRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile('{:s}.kicad_mod'.format(dim.name))


    def build_series(self, verbose=False):
        print('Making {p:s}'.format(p=self.config['base']['description']))
        base = self.config['base']
        for variant in self.config['variants']:
            self._build_footprint(base, variant, verbose=verbose)


class StyleA(CapacitorTrimmer):

    def __init__(self, config_file):
        self.FAMILY = 'STYLE-A'
        self.config = self._load_config(config_file)


class StyleB(CapacitorTrimmer):

    def __init__(self, config_file):
        self.FAMILY = 'STYLE-B'
        self.config = self._load_config(config_file)


class StyleC(CapacitorTrimmer):

    def __init__(self, config_file):
        self.FAMILY = 'STYLE-C'
        self.config = self._load_config(config_file)


class StyleD(CapacitorTrimmer):

    def __init__(self, config_file):
        self.FAMILY = 'STYLE-D'
        self.config = self._load_config(config_file)


class Factory(object):

    def __init__(self, config_file):
        self._config_file = config_file
        self._parse_command_line()
        self.verbose = self._args.verbose
        self._create_build_list()

    def _parse_command_line(self):
        parser = argparse.ArgumentParser(description='Select which devices to make')
        parser.add_argument('--family', help='device families to make: STYLE-A | STYLE-B | STYLE-C | STYLE-D  (default is all families)',
                            type=str, nargs=1)
        parser.add_argument('-v', '--verbose', help='show detailed information while making the footprints',
                            action='store_true')
        self._args = parser.parse_args()

    def _create_build_list(self):
        if not self._args.family:
            self.build_list = [StyleA(self._config_file), StyleB(self._config_file), StyleC(self._config_file), StyleD(self._config_file)]
        else:
            self.build_list = []
            if 'STYLE-A' in self._args.family:
                self.build_list.append(StyleA(self._config_file))
            if 'STYLE-B' in self._args.family:
                self.build_list.append(StyleB(self._config_file))
            if 'STYLE-C' in self._args.family:
                self.build_list.append(StyleC(self._config_file))
            if 'STYLE-D' in self._args.family:
                self.build_list.append(StyleD(self._config_file))
            if not self.build_list:
                print('Family not recognised')

