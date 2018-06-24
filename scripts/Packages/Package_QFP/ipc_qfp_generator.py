#!/usr/bin/env python

import sys
import os
import argparse
import yaml
import math

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA
sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

ipc_density = 'nominal'
ipc_doc_file = '../ipc_definitions.yaml'
category = 'QFP'

DEFAULT_PASTE_COVERAGE = 0.65
DEFAULT_VIA_PASTE_CLEARANCE = 0.15
DEFAULT_MIN_ANNULAR_RING = 0.15

def roundToBase(value, base):
    return round(value/base) * base

class QFP():
    def __init__(self, configuration):
        self.configuration = configuration
        with open(ipc_doc_file, 'r') as ipc_stream:
            try:
                self.ipc_defintions = yaml.load(ipc_stream)
            except yaml.YAMLError as exc:
                print(exc)

    def calcPadDetails(self, device_params, ipc_data, ipc_round_base):
        # Zmax = Lmin + 2JT + √(CL^2 + F^2 + P^2)
        # Gmin = Smax − 2JH − √(CS^2 + F^2 + P^2)
        # Xmax = Wmin + 2JS + √(CW^2 + F^2 + P^2)

        # Some manufacturers do not list the terminal spacing (S) in their datasheet but list the terminal lenght (T)
        # Then one can calculate
        # Stol(RMS) = √(Ltol^2 + 2*^2)
        # Smin = Lmin - 2*Tmax
        # Smax(RMS) = Smin + Stol(RMS)

        F = self.configuration.get('manufacturing_tolerance', 0.1)
        P = self.configuration.get('placement_tolerance', 0.05)

        if 'overall_size_x_max' in device_params:
            overall_x_tol = device_params['overall_size_x_max'] - device_params['overall_size_x_min']
            overall_x_min = device_params['overall_size_x_min']
        else:
            overall_x_tol = 0
            overall_x_min = device_params['overall_size_x']

        if 'overall_size_y_max' in device_params:
            overall_y_tol = device_params['overall_size_y_max'] - device_params['overall_size_y_min']
            overall_y_min = device_params['overall_size_y_min']
        else:
            overall_y_tol = 0
            overall_y_min = device_params['overall_size_y']

        lead_len_tol = device_params['lead_len_max'] - device_params['lead_len_min']
        lead_width_tol = device_params['lead_width_max'] - device_params['lead_width_min']

        def calcPadLength(overall_min, overall_tol):
            Stol_RMS = math.sqrt(overall_tol**2+2*(lead_len_tol**2))
            Smin = overall_min - 2*device_params['lead_len_max']
            Smax_RMS = Smin + Stol_RMS

            Gmin = Smax_RMS - 2*ipc_data['heel'] - math.sqrt(Stol_RMS**2 + F**2 + P**2)


            Zmax = overall_min + 2*ipc_data['toe'] + math.sqrt(overall_tol**2 + F**2 + P**2)

            Zmax = roundToBase(Zmax, ipc_round_base['toe'])
            Gmin = roundToBase(Gmin, ipc_round_base['heel'])

            Zmax += device_params.get('pad_length_addition', 0)

            return Gmin, Zmax

        Gmin_x, Zmax_x = calcPadLength(overall_x_min, overall_x_tol)
        Gmin_y, Zmax_y = calcPadLength(overall_y_min, overall_y_tol)

        Xmax = device_params['lead_width_min'] + 2*ipc_data['side'] + math.sqrt(lead_width_tol**2 + F**2 + P**2)
        Xmax = roundToBase(Xmax, ipc_round_base['side'])

        Pad = {}
        Pad['left'] = {'center':[-(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['right'] = {'center':[(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['top'] = {'center':[0,-(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}
        Pad['bottom'] = {'center':[0,(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}

        return Pad
    def generateFootprint(self, device_params):
        has_EP = 'EP_size_x' in device_params or 'EP_size_x_min' in device_params
        if has_EP and 'thermal_vias' in device_params:
            self.__createFootprintVariant(device_params, has_EP, True)

        self.__createFootprintVariant(device_params, has_EP, False)

    def __createFootprintVariant(self, device_params, has_EP, with_thermal_vias):
        fab_line_width = self.configuration.get('fab_line_width', 0.1)
        silk_line_width = self.configuration.get('silk_line_width', 0.12)

        lib_name = self.configuration['lib_name_format_string'].format(category=category)

        if 'body_size_x' in device_params:
            size_x = device_params['body_size_x']
        else:
            size_x = (device_params['body_size_x_max'] + device_params['body_size_x_min'])/2

        if 'body_size_y' in device_params:
            size_y = device_params['body_size_y']
        else:
            size_y = (device_params['body_size_y_max'] + device_params['body_size_y_min'])/2

        pincount = device_params['num_pins_x']*2 + device_params['num_pins_y']*2

        ipc_reference = 'ipc_spec_gw_large_pitch' if device_params['pitch'] >= 0.625 else 'ipc_spec_gw_small_pitch'

        ipc_data_set = self.ipc_defintions[ipc_reference][ipc_density]
        ipc_round_base = self.ipc_defintions[ipc_reference]['round_base']

        pad_details = self.calcPadDetails(device_params, ipc_data_set, ipc_round_base)


        suffix = device_params.get('suffix', '').format(pad_x=pad_details['left']['size'][0],
            pad_y=pad_details['left']['size'][1])
        suffix_3d = suffix if device_params.get('include_suffix_in_3dpath', 'True') == 'True' else ""
        model3d_path_prefix = self.configuration.get('3d_model_prefix','${KISYS3DMOD}')

        if has_EP:
            name_format = self.configuration['fp_name_EP_format_string_no_trailing_zero']
            if 'EP_size_x' in device_params and 'EP_size_y' in device_params:
                EP_size = {'x':device_params['EP_size_x'], 'y':device_params['EP_size_y']}
            elif 'EP_size_x_max' in device_params and 'EP_size_x_min' in device_params and\
                    'EP_size_y_max' in device_params and 'EP_size_y_min' in device_params:
                EP_size = {
                    'x':(device_params['EP_size_x_max']+device_params['EP_size_x_min'])/2,
                    'y':(device_params['EP_size_y_max']+device_params['EP_size_y_min'])/2
                    }
            else:
                raise KeyError("Either nominal ep size in x and y direction must be given or min and max values for both directions.")
        else:
            name_format = self.configuration['fp_name_format_string_no_trailing_zero']
            EP_size = {'x':0, 'y':0}

        if 'custom_name_format' in device_params:
            name_format = device_params['custom_name_format']

        fp_name = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=device_params['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_params['pitch'],
            ep_size_x = EP_size['x'],
            ep_size_y = EP_size['y'],
            suffix=suffix,
            vias=self.configuration.get('thermal_via_suffix', '_ThermalVias') if with_thermal_vias else ''
            ).replace('__','_').lstrip('_')

        fp_name_2 = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=device_params['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_params['pitch'],
            ep_size_x = EP_size['x'],
            ep_size_y = EP_size['y'],
            suffix=suffix_3d,
            vias=''
            ).replace('__','_').lstrip('_')

        model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'\
            .format(
                model3d_path_prefix=model3d_path_prefix, lib_name=lib_name,
                fp_name=fp_name_2)
        #print(fp_name)
        #print(pad_details)

        kicad_mod = Footprint(fp_name)

                # init kicad footprint
        kicad_mod.setDescription(
            "{manufacturer} {mpn} {package}, {pincount} Pin ({datasheet}), generated with kicad-footprint-generator {scriptname}"\
            .format(
                manufacturer = device_params.get('manufacturer',''),
                package = device_params['device_type'],
                mpn = device_params.get('part_number',''),
                pincount = pincount,
                datasheet = device_params['size_source'],
                scriptname = os.path.basename(__file__).replace("  ", " ")
                ).lstrip())

        kicad_mod.setTags(self.configuration['keyword_fp_string']\
            .format(
                man=device_params.get('manufacturer',''),
                package=device_params['device_type'],
                category=category
            ).lstrip())
        kicad_mod.setAttribute('smd')

        pad_shape_details = {}
        pad_shape_details['shape'] = Pad.SHAPE_ROUNDRECT
        pad_shape_details['radius_ratio'] = configuration.get('round_rect_radius_ratio', 0)
        if 'round_rect_max_radius' in configuration:
            pad_shape_details['maximum_radius'] = configuration['round_rect_max_radius']

        if has_EP:
            if with_thermal_vias:
                thermals = device_params['thermal_vias']
                paste_coverage = thermals.get('EP_paste_coverage',
                                               device_params.get('EP_paste_coverage', DEFAULT_PASTE_COVERAGE))

                kicad_mod.append(ExposedPad(
                    number=pincount+1, size=EP_size,
                    paste_layout=thermals.get('EP_num_paste_pads'),
                    paste_coverage=paste_coverage,
                    via_layout=thermals.get('count', 0),
                    paste_between_vias=thermals.get('paste_between_vias'),
                    paste_rings_outside=thermals.get('paste_rings_outside'),
                    via_drill=thermals.get('drill', 0.3),
                    via_grid=thermals.get('grid'),
                    paste_avoid_via=thermals.get('paste_avoid_via', True),
                    via_paste_clarance=thermals.get('paste_via_clearance', DEFAULT_VIA_PASTE_CLEARANCE),
                    min_annular_ring=thermals.get('min_annular_ring', DEFAULT_MIN_ANNULAR_RING),
                    bottom_pad_min_size=thermals.get('bottom_min_size', 0),
                    **pad_shape_details
                    ))
            else:
                kicad_mod.append(ExposedPad(
                    number=pincount+1, size=EP_size,
                    paste_layout=device_params.get('EP_num_paste_pads', 1),
                    paste_coverage=device_params.get('EP_paste_coverage', DEFAULT_PASTE_COVERAGE),
                    **pad_shape_details
                    ))

        init = 1
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_y'],
            x_spacing=0, y_spacing=device_params['pitch'],
            **pad_details['left'],
            **pad_shape_details))

        init += device_params['num_pins_y']
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_x'],
            y_spacing=0, x_spacing=device_params['pitch'],
            **pad_details['bottom'],
            **pad_shape_details))

        init += device_params['num_pins_x']
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_y'],
            x_spacing=0, y_spacing=-device_params['pitch'],
            **pad_details['right'],
            **pad_shape_details))

        init += device_params['num_pins_y']
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_x'],
            y_spacing=0, x_spacing=-device_params['pitch'],
            **pad_details['top'],
            **pad_shape_details))


        body_edge = {
            'left': -device_params['body_size_x']/2,
            'right': device_params['body_size_x']/2,
            'top': -device_params['body_size_y']/2,
            'bottom': device_params['body_size_y']/2
            }

        bounding_box = {
            'left': pad_details['left']['center'][0] - pad_details['left']['size'][0]/2,
            'right': pad_details['right']['center'][0] + pad_details['right']['size'][0]/2,
            'top': pad_details['top']['center'][1] - pad_details['top']['size'][1]/2,
            'bottom': pad_details['bottom']['center'][1] + pad_details['bottom']['size'][1]/2
        }


        pad_width = pad_details['top']['size'][0]

        # ############################ SilkS ##################################

        silk_pad_offset = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
        silk_offset = configuration['silk_fab_offset']

        sx1 = -(device_params['pitch']*(device_params['num_pins_x']-1)/2.0
            + pad_width/2.0 + silk_pad_offset)

        sy1 = -(device_params['pitch']*(device_params['num_pins_y']-1)/2.0
            + pad_width/2.0 + silk_pad_offset)

        poly_silk = [
            {'x': sx1, 'y': body_edge['top']-silk_offset},
            {'x': body_edge['left']-silk_offset, 'y': body_edge['top']-silk_offset},
            {'x': body_edge['left']-silk_offset, 'y': sy1}
        ]

        kicad_mod.append(PolygoneLine(
            polygone=poly_silk,
            width=configuration['silk_line_width'],
            layer="F.SilkS"))
        kicad_mod.append(PolygoneLine(
            polygone=poly_silk,
            width=configuration['silk_line_width'],
            layer="F.SilkS", x_mirror=0))
        kicad_mod.append(PolygoneLine(
            polygone=poly_silk,
            width=configuration['silk_line_width'],
            layer="F.SilkS", y_mirror=0))
        kicad_mod.append(PolygoneLine(
            polygone=poly_silk,
            width=configuration['silk_line_width'],
            layer="F.SilkS", x_mirror=0, y_mirror=0))

        kicad_mod.append(Line(
            start={'x': body_edge['left']-silk_offset, 'y': sy1},
            end={'x': bounding_box['left'], 'y': sy1},
            width=configuration['silk_line_width'],
            layer="F.SilkS"))

        # # ######################## Fabrication Layer ###########################

        fab_bevel_size = min(configuration['fab_bevel_size_absolute'], configuration['fab_bevel_size_relative']*max(size_x, size_y))

        poly_fab = [
            {'x': body_edge['left']+fab_bevel_size, 'y': body_edge['top']},
            {'x': body_edge['right'], 'y': body_edge['top']},
            {'x': body_edge['right'], 'y': body_edge['bottom']},
            {'x': body_edge['left'], 'y': body_edge['bottom']},
            {'x': body_edge['left'], 'y': body_edge['top']+fab_bevel_size},
            {'x': body_edge['left']+fab_bevel_size, 'y': body_edge['top']},
        ]

        kicad_mod.append(PolygoneLine(
            polygone=poly_fab,
            width=configuration['fab_line_width'],
            layer="F.Fab"))

        # # ############################ CrtYd ##################################

        off = ipc_data_set['courtyard']
        grid = configuration['courtyard_grid']

        cy1=roundToBase(bounding_box['top']-off, grid)
        cy2=roundToBase(body_edge['top']-off, grid)
        cy3=-roundToBase(
            device_params['pitch']*(device_params['num_pins_y']-1)/2.0
            + pad_width/2.0 + off, grid)



        cx1=-roundToBase(
            device_params['pitch']*(device_params['num_pins_x']-1)/2.0
            + pad_width/2.0 + off, grid)
        cx2=roundToBase(body_edge['left']-off, grid)
        cx3=roundToBase(bounding_box['left']-off, grid)


        crty_poly_tl = [
            {'x':0, 'y':cy1},
            {'x':cx1, 'y':cy1},
            {'x':cx1, 'y':cy2},
            {'x':cx2, 'y':cy2},
            {'x':cx2, 'y':cy3},
            {'x':cx3, 'y':cy3},
            {'x':cx3, 'y':0}
        ]
        kicad_mod.append(PolygoneLine(polygone=crty_poly_tl,
            layer='F.CrtYd', width=configuration['courtyard_line_width']))
        kicad_mod.append(PolygoneLine(polygone=crty_poly_tl,
            layer='F.CrtYd', width=configuration['courtyard_line_width'],
            x_mirror=0))
        kicad_mod.append(PolygoneLine(polygone=crty_poly_tl,
            layer='F.CrtYd', width=configuration['courtyard_line_width'],
            y_mirror=0))
        kicad_mod.append(PolygoneLine(polygone=crty_poly_tl,
            layer='F.CrtYd', width=configuration['courtyard_line_width'],
            x_mirror=0, y_mirror=0))

        # ######################### Text Fields ###############################

        addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
            courtyard={'top': cy1, 'bottom': -cy1}, fp_name=fp_name, text_y_inside_position='center')

        ##################### Output and 3d model ############################

        kicad_mod.append(Model(filename=model_name))

        output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
        if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
            os.makedirs(output_dir)
        filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=fp_name)

        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files holding information about what devices should be created.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../package_config_KLCv3.yaml')
    parser.add_argument('--density', type=str, nargs='?', help='Density level (L,N,M)', default='N')
    parser.add_argument('--ipc_doc', type=str, nargs='?', help='IPC definition document', default='../ipc_definitions.yaml')
    parser.add_argument('--force_rectangle_pads', action='store_true', help='Force the generation of rectangle pads instead of rounded rectangle')
    args = parser.parse_args()

    if args.density == 'L':
        ipc_density = 'least'
    elif args.density == 'M':
        ipc_density = 'most'

    ipc_doc_file = args.ipc_doc

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    if args.force_rectangle_pads:
        configuration['round_rect_max_radius'] = None
        configuration['round_rect_radius_ratio'] = 0

    for filepath in args.files:
        qfp = QFP(configuration)

        with open(filepath, 'r') as command_stream:
            try:
                cmd_file = yaml.load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for pkg in cmd_file:
            qfp.generateFootprint(cmd_file[pkg])
