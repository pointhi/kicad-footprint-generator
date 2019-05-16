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
category = 'LCC'

def roundToBase(value, base):
    return round(value/base) * base

def params_inch_to_metric(device_params):
    for key in device_params:
        if type(device_params[key]) in [int, float] and 'num_' not in key:
            device_params[key] = device_params[key]*25.4

class QFP():
    def __init__(self, configuration):
        self.configuration = configuration
        with open(ipc_doc_file, 'r') as ipc_stream:
            try:
                self.ipc_defintions = yaml.safe_load(ipc_stream)
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

        lead_width_tol = device_params['lead_width_max'] - device_params['lead_width_min']

        def calcPadLength(overall, body, lead_inside=None, lead_center=None):
            overall_tol = overall['max']-overall['min']
            if lead_inside:
                Tmin = (overall['max'] - lead_inside['max'])/2
                Tmax = (overall['min'] - lead_inside['min'])/2
                Ttol = Tmax - Tmin
                inside_tol = lead_inside['max'] - lead_inside['min']
                Stol_RMS = math.sqrt(overall_tol**2+inside_tol**2)
                Smax_RMS = lead_inside['min'] + Stol_RMS
            elif lead_center:
                body_tol = body['max']-body['min']
                Tmin = (body['max'] - lead_center['max'])
                Tmax = (body['min'] - lead_center['min'])
                Ttol = Tmax - Tmin
                center_tol = lead_center['max'] - lead_center['min']
                Stol_RMS = math.sqrt(body_tol**2+center_tol**2)
                Smax_RMS = body['max'] - 2*Tmin + Stol_RMS
            else:
                lead_len_tol = device_params['lead_len_max'] - device_params['lead_len_min']
                Stol_RMS = math.sqrt(overall_tol**2+2*(lead_len_tol**2))
                Smin = overall['min'] - 2*device_params['lead_len_max']
                Smax_RMS = Smin + Stol_RMS

            Gmin = Smax_RMS - 2*ipc_data['heel'] - math.sqrt(Stol_RMS**2 + F**2 + P**2)

            Zmax = overall['min'] + 2*ipc_data['toe'] + math.sqrt(overall_tol**2 + F**2 + P**2)

            Zmax = roundToBase(Zmax, ipc_round_base['toe'])
            Gmin = roundToBase(Gmin, ipc_round_base['heel'])

            Zmax += device_params.get('pad_length_addition', 0)

            return Gmin, Zmax
        overall_x={
            'min':device_params.get('overall_size_x_min', device_params.get('overall_size_x')),
            'max':device_params.get('overall_size_x_max', device_params.get('overall_size_x'))
            }
        overall_y={
            'min':device_params.get('overall_size_y_min', device_params.get('overall_size_y')),
            'max':device_params.get('overall_size_y_max', device_params.get('overall_size_y'))
            }

        body_x={
            'min':device_params.get('body_size_x_min', device_params.get('body_size_x')),
            'max':device_params.get('body_size_x_max', device_params.get('body_size_x'))
            }
        body_y={
            'min':device_params.get('body_size_y_min', device_params.get('body_size_y')),
            'max':device_params.get('body_size_y_max', device_params.get('body_size_y'))
            }

        if 'lead_inside_x_min' in device_params:
            Gmin_x, Zmax_x = calcPadLength(
                overall=overall_x,
                body=body_x,
                lead_inside={
                    'min':device_params['lead_inside_x_min'],
                    'max':device_params['lead_inside_x_max']}
                 )
            Gmin_y, Zmax_y = calcPadLength(
                overall=overall_y,
                body=body_y,
                lead_inside={
                    'min':device_params['lead_inside_y_min'],
                    'max':device_params['lead_inside_y_max']}
                )
        elif 'lead_center_distance_x_min' in device_params:
            Gmin_x, Zmax_x = calcPadLength(
                overall=overall_x,
                body=body_x,
                lead_center={
                    'min':device_params['lead_center_distance_x_min'],
                    'max':device_params['lead_center_distance_x_max']}
                 )
            Gmin_y, Zmax_y = calcPadLength(
                overall=overall_y,
                body=body_y,
                lead_center={
                    'min':device_params['lead_center_distance_y_min'],
                    'max':device_params['lead_center_distance_y_max']}
                 )
        else:
            Gmin_x, Zmax_x = calcPadLength(
                overall=overall_x,
                body=body_x
                )

            Gmin_y, Zmax_y = calcPadLength(
                overall=overall_y,
                body=body_y
                )


        Xmax = device_params['lead_width_min'] + 2*ipc_data['side'] + math.sqrt(lead_width_tol**2 + F**2 + P**2)
        Xmax = roundToBase(Xmax, ipc_round_base['side'])

        Pad = {}
        Pad['first'] = {'start':[-((device_params['num_pins_x']-1)%2)/2*device_params['pitch'], -(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}

        Pad['left'] = {'center':[-(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['right'] = {'center':[(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['top'] = {'start':[(device_params['num_pins_x']-1)/2*device_params['pitch'],-(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}
        Pad['bottom'] = {'center':[0,(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}

        return Pad

    def generateFootprint(self, device_params):
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

        ipc_reference = 'ipc_spec_j_lead'

        ipc_data_set = self.ipc_defintions[ipc_reference][ipc_density]
        ipc_round_base = self.ipc_defintions[ipc_reference]['round_base']

        pad_details = self.calcPadDetails(device_params, ipc_data_set, ipc_round_base)


        suffix = device_params.get('suffix', '').format(pad_x=pad_details['left']['size'][0],
            pad_y=pad_details['left']['size'][1])
        suffix_3d = suffix if device_params.get('include_suffix_in_3dpath', 'True') == 'True' else ""

        model3d_path_prefix = self.configuration.get('3d_model_prefix','${KISYS3DMOD}')
        name_format = self.configuration['fp_name_format_string']

        fp_name = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=device_params['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_params['pitch'],
            suffix=suffix
            ).replace('__','_').lstrip('_')

        fp_name_2 = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=device_params['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_params['pitch'],
            suffix=suffix_3d
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

        init = 1
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=int(math.ceil(device_params['num_pins_x']/2)),
            x_spacing=-device_params['pitch'], y_spacing=0,
            **pad_details['first'], **pad_shape_details))

        init += int(math.ceil(device_params['num_pins_x']/2))
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_y'],
            x_spacing=0, y_spacing=device_params['pitch'],
            **pad_details['left'], **pad_shape_details))

        init += device_params['num_pins_y']
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_x'],
            y_spacing=0, x_spacing=device_params['pitch'],
            **pad_details['bottom'], **pad_shape_details))

        init += device_params['num_pins_x']
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_y'],
            x_spacing=0, y_spacing=-device_params['pitch'],
            **pad_details['right'], **pad_shape_details))

        init += device_params['num_pins_y']
        kicad_mod.append(PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=int(math.floor(device_params['num_pins_x']/2)),
            y_spacing=0, x_spacing=-device_params['pitch'],
            **pad_details['top'], **pad_shape_details))


        body_edge = {
            'left': -size_x/2,
            'right': size_x/2,
            'top': -size_y/2,
            'bottom': size_y/2
            }

        bounding_box = {
            'left': pad_details['left']['center'][0] - pad_details['left']['size'][0]/2,
            'right': pad_details['right']['center'][0] + pad_details['right']['size'][0]/2,
            'top': pad_details['top']['start'][1] - pad_details['top']['size'][1]/2,
            'bottom': pad_details['bottom']['center'][1] + pad_details['bottom']['size'][1]/2
        }


        pad_width = pad_details['top']['size'][0]
        p1_x = pad_details['first']['start'][0]

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
            layer="F.SilkS", x_mirror=0))
        kicad_mod.append(PolygoneLine(
            polygone=poly_silk,
            width=configuration['silk_line_width'],
            layer="F.SilkS", y_mirror=0))
        kicad_mod.append(PolygoneLine(
            polygone=poly_silk,
            width=configuration['silk_line_width'],
            layer="F.SilkS", x_mirror=0, y_mirror=0))

        silk_off_45 = silk_offset/sqrt(2)
        poly_silk_tl = [
            {'x': sx1, 'y': body_edge['top']-silk_offset},
            {'x': body_edge['left']+device_params['body_chamfer']-silk_off_45, 'y': body_edge['top']-silk_offset},
            {'x': body_edge['left']-silk_offset, 'y': body_edge['top']+device_params['body_chamfer']-silk_off_45},
            {'x': body_edge['left']-silk_offset, 'y': sy1}
        ]
        kicad_mod.append(PolygoneLine(
            polygone=poly_silk_tl,
            width=configuration['silk_line_width'],
            layer="F.SilkS"))

        # # ######################## Fabrication Layer ###########################

        fab_bevel_size = min(configuration['fab_bevel_size_absolute'], configuration['fab_bevel_size_relative']*min(size_x, size_y))
        fab_bevel_y = fab_bevel_size/sqrt(2)
        poly_fab = [
            {'x': p1_x, 'y': body_edge['top']+fab_bevel_y},
            {'x': p1_x+fab_bevel_size/2, 'y': body_edge['top']},
            {'x': body_edge['right'], 'y': body_edge['top']},
            {'x': body_edge['right'], 'y': body_edge['bottom']},
            {'x': body_edge['left'], 'y': body_edge['bottom']},
            {'x': body_edge['left'], 'y': body_edge['top']+device_params['body_chamfer']},
            {'x': body_edge['left']+device_params['body_chamfer'], 'y': body_edge['top']},
            {'x': p1_x-fab_bevel_size/2, 'y': body_edge['top']},
            {'x': p1_x, 'y': body_edge['top']+fab_bevel_y}
        ]

        kicad_mod.append(PolygoneLine(
            polygone=poly_fab,
            width=configuration['fab_line_width'],
            layer="F.Fab"))

        # # ############################ CrtYd ##################################

        off = ipc_data_set['courtyard']
        grid = configuration['courtyard_grid']
        off_45 = off*math.tan(math.radians(45.0/2))

        cy1=roundToBase(bounding_box['top']-off, grid)
        cy2=roundToBase(body_edge['top']-off, grid)
        cy3=-roundToBase(
            device_params['pitch']*(device_params['num_pins_y']-1)/2.0
            + pad_width/2.0 + off, grid)
        cy4=roundToBase(body_edge['top']+device_params['body_chamfer']-off_45, grid)



        cx1=-roundToBase(
            device_params['pitch']*(device_params['num_pins_x']-1)/2.0
            + pad_width/2.0 + off, grid)
        cx2=roundToBase(body_edge['left']-off, grid)
        cx3=roundToBase(bounding_box['left']-off, grid)
        cx4=roundToBase(body_edge['left']+device_params['body_chamfer']-off_45, grid)


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
            layer='F.CrtYd', width=configuration['courtyard_line_width'],
            x_mirror=0))
        kicad_mod.append(PolygoneLine(polygone=crty_poly_tl,
            layer='F.CrtYd', width=configuration['courtyard_line_width'],
            y_mirror=0))
        kicad_mod.append(PolygoneLine(polygone=crty_poly_tl,
            layer='F.CrtYd', width=configuration['courtyard_line_width'],
            x_mirror=0, y_mirror=0))

        crty_poly_tl_ch = [
            {'x':0, 'y':cy1},
            {'x':cx1, 'y':cy1},
            {'x':cx1, 'y':cy2},
            {'x':cx4, 'y':cy2},
            {'x':cx2, 'y':cy4},
            {'x':cx2, 'y':cy3},
            {'x':cx3, 'y':cy3},
            {'x':cx3, 'y':0}
        ]
        kicad_mod.append(PolygoneLine(polygone=crty_poly_tl_ch,
            layer='F.CrtYd', width=configuration['courtyard_line_width']))

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
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.safe_load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    if args.force_rectangle_pads:
        configuration['round_rect_max_radius'] = None
        configuration['round_rect_radius_ratio'] = 0

    for filepath in args.files:
        qfp = QFP(configuration)

        with open(filepath, 'r') as command_stream:
            try:
                cmd_file = yaml.safe_load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for pkg in cmd_file:
            if cmd_file[pkg].get('units', 'mm') == 'inches':
                params_inch_to_metric(cmd_file[pkg])
            qfp.generateFootprint(cmd_file[pkg])
