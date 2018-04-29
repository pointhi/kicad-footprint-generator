#!/usr/bin/env python

import sys
import os
import argparse
import yaml
import math
from math import sqrt

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA
sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

ipc_density = 'nominal'
ipc_doc_file = '../ipc_definitions.yaml'
category = 'DFN_QFN'

def roundToBase(value, base):
    return round(value/base) * base

class DFN():
    def __init__(self, configuration):
        self.configuration = configuration
        with open(ipc_doc_file, 'r') as ipc_stream:
            try:
                self.ipc_defintions = yaml.load(ipc_stream)
            except yaml.YAMLError as exc:
                print(exc)

    def calcExposedPad(self, device_params):
        F = self.configuration.get('manufacturing_tolerance', 0.1)
        P = self.configuration.get('placement_tolerance', 0.05)


        ipc_reference = 'ipc_spec_flat_no_lead_pull_back'
        used_density = device_params.get('ipc_density', ipc_density)
        ipc_data_set = self.ipc_defintions[ipc_reference][used_density]
        ipc_round_base = self.ipc_defintions[ipc_reference]['round_base']

        if 'EP_size_x_min' in device_params:
            Xtol = device_params['EP_size_x_max'] - device_params['EP_size_x_min']
            Xmin = device_params['EP_size_x_min']
        else:
            Xtol = 0
            Xmin = device_params['EP_size_x']

        if 'EP_size_y_min' in device_params:
            Ytol = device_params['EP_size_y_max'] - device_params['EP_size_y_min']
            Ymin = device_params['EP_size_y_min']
        else:
            Ytol = 0
            Ymin = device_params['EP_size_y']

        per_fillet = ipc_data_set['side']
        rd_base = ipc_round_base['side']

        EP_Pad = {'at':[0,0],
            'size':{
            'x': roundToBase(Xmin + 2*per_fillet + sqrt(Xtol**2+F**2+P**2), rd_base),
            'y': roundToBase(Ymin + 2*per_fillet + sqrt(Ytol**2+F**2+P**2), rd_base)
            },
            'layers':['F.Cu', 'F.Mask'],
            'type':Pad.TYPE_SMT, 'shape':Pad.SHAPE_RECT
            }

        c = sqrt(device_params.get('EP_paste_coverage', 0.65))
        nx = device_params.get('EP_num_paste_pads_x', 1)
        ny = device_params.get('EP_num_paste_pads_y', 1)

        paste_rd_base = rd_base

        paste_size_x = roundToBase(EP_Pad['size']['x']*c/nx, paste_rd_base)
        paste_size_y = roundToBase(EP_Pad['size']['y']*c/ny, paste_rd_base)

        dx = (EP_Pad['size']['x'] - paste_size_x*nx)/(nx+1)
        dy = (EP_Pad['size']['y'] - paste_size_y*ny)/(ny+1)

        grid_x = roundToBase(paste_size_x + dx, paste_rd_base)
        grid_y = roundToBase(paste_size_y + dy, paste_rd_base)

        EP_Paste = {'inner_array':{
            'solder_paste_margin_ratio': 1e-8,
            'solder_paste_margin': 1e-6,
            'layers':['F.Paste'],
            'size':[paste_size_x, paste_size_y],
            'initial':"",
            'increment':0,
            'pincount':nx,
            'x_spacing':grid_x,
            'type':Pad.TYPE_SMT, 'shape':Pad.SHAPE_RECT
            },
            'ny':ny, 'grid_y':grid_y
            }
        return EP_Pad, EP_Paste


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

        if 'body_size_x_max' in device_params:
            body_x_tol = device_params['body_size_x_max'] - device_params['body_size_x_min']
            outside_x_min = device_params['body_size_x_min']
            outside_x_tol = body_x_tol
        else:
            outside_x_min = device_params['body_size_x']
            outside_x_tol = 0

        if 'body_size_y_max' in device_params:
            body_y_tol = device_params['body_size_y_max'] - device_params['body_size_y_min']
            outside_y_min = device_params['body_size_y_min']
            outside_y_tol = body_y_tol
        else:
            outside_y_tol = 0
            outside_y_min = device_params['body_size_y']

        lead_len_tol = device_params['lead_len_max'] - device_params['lead_len_min']

        lead_width_tol = device_params['lead_width_max'] - device_params['lead_width_min']

        def calcPadLength(outside_min, outside_tol):
            Stol_RMS = math.sqrt(outside_tol**2+2*(lead_len_tol**2))
            Smin = outside_min - 2*device_params['lead_len_max']
            Smax_RMS = Smin + Stol_RMS

            Gmin = Smax_RMS - 2*ipc_data['heel'] - math.sqrt(Stol_RMS**2 + F**2 + P**2)

            Zmax = outside_min + 2*ipc_data['toe'] + math.sqrt(outside_tol**2 + F**2 + P**2)

            Zmax = roundToBase(Zmax, ipc_round_base['toe'])
            Gmin = roundToBase(Gmin, ipc_round_base['heel'])

            Zmax += device_params.get('pad_length_addition', 0)

            return Gmin, Zmax


        Gmin_x, Zmax_x = calcPadLength(outside_x_min, outside_x_tol)
        #print("Omin {} Otol {}".format(outside_y_min, outside_y_tol))
        Gmin_y, Zmax_y = calcPadLength(outside_y_min, outside_y_tol)
        #print("Gy {} Zy {}".format(Gmin_y, Zmax_y))

        Xmax = device_params['lead_width_min'] + 2*ipc_data['side'] + math.sqrt(lead_width_tol**2 + F**2 + P**2)
        Xmax = roundToBase(Xmax, ipc_round_base['side'])

        Pad = {}
        Pad['left'] = {'center':[-(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['right'] = {'center':[(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['top'] = {'center':[0,-(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}
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

        if device_params.get('ipc_class', 'qfn') == 'qfn_pull_back':
            ipc_reference = 'ipc_spec_flat_no_lead_pull_back'
        else:
            ipc_reference = 'ipc_spec_flat_no_lead'

        used_density = device_params.get('ipc_density', ipc_density)
        ipc_data_set = self.ipc_defintions[ipc_reference][used_density]
        ipc_round_base = self.ipc_defintions[ipc_reference]['round_base']

        pad_details = self.calcPadDetails(device_params, ipc_data_set, ipc_round_base)


        suffix = device_params.get('suffix', '').format(pad_x=pad_details['left']['size'][0],
            pad_y=pad_details['left']['size'][1])
        suffix_3d = suffix if device_params.get('include_suffix_in_3dpath', 'True') == 'True' else ""
        model3d_path_prefix = self.configuration.get('3d_model_prefix','${KISYS3DMOD}')

        has_EP = 'EP_size_x' in device_params or 'EP_size_x_min' in device_params

        if has_EP:
            name_format = self.configuration['fp_name_EP_format_string_no_trailing_zero']
            EP_params, EP_paste_pads = self.calcExposedPad(device_params)
        else:
            name_format = self.configuration['fp_name_EP_format_string_no_trailing_zero']
            EP_params = {'size':{'x':0, 'y':0}}

        fp_name = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=device_params['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_params['pitch'],
            ep_size_x = EP_params['size']['x'],
            ep_size_y = EP_params['size']['y'],
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
            ep_size_x = EP_params['size']['x'],
            ep_size_y = EP_params['size']['y'],
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


        if has_EP:
            kicad_mod.append(Pad(
                number=pincount+1,
                **EP_params
                ))
            cy = -((EP_paste_pads['ny']-1)*EP_paste_pads['grid_y'])/2
            for i in range(EP_paste_pads['ny']):
                kicad_mod.append(PadArray(center=[0,cy], **EP_paste_pads['inner_array']))
                cy += EP_paste_pads['grid_y']

        init = 1
        if device_params['num_pins_x'] == 0:
            kicad_mod.append(PadArray(
                initial= init,
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                layers=Pad.LAYERS_SMT,
                pincount=device_params['num_pins_y'],
                x_spacing=0, y_spacing=device_params['pitch'],
                **pad_details['left']))
            init += device_params['num_pins_y']
            kicad_mod.append(PadArray(
                initial= init,
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                layers=Pad.LAYERS_SMT,
                pincount=device_params['num_pins_y'],
                x_spacing=0, y_spacing=-device_params['pitch'],
                **pad_details['right']))
        elif device_params['num_pins_y'] == 0:
            #for devices with clockwise numbering
            kicad_mod.append(PadArray(
                initial= init,
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                layers=Pad.LAYERS_SMT,
                pincount=device_params['num_pins_x'],
                y_spacing=0, x_spacing=device_params['pitch'],
                **pad_details['top']))
            init += device_params['num_pins_x']
            kicad_mod.append(PadArray(
                initial= init,
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                layers=Pad.LAYERS_SMT,
                pincount=device_params['num_pins_x'],
                y_spacing=0, x_spacing=-device_params['pitch'],
                **pad_details['bottom']))
        else:
            kicad_mod.append(PadArray(
                initial= init,
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                layers=Pad.LAYERS_SMT,
                pincount=device_params['num_pins_y'],
                x_spacing=0, y_spacing=device_params['pitch'],
                **pad_details['left']))

            init += device_params['num_pins_y']
            kicad_mod.append(PadArray(
                initial= init,
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                layers=Pad.LAYERS_SMT,
                pincount=device_params['num_pins_x'],
                y_spacing=0, x_spacing=device_params['pitch'],
                **pad_details['bottom']))

            init += device_params['num_pins_x']
            kicad_mod.append(PadArray(
                initial= init,
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                layers=Pad.LAYERS_SMT,
                pincount=device_params['num_pins_y'],
                x_spacing=0, y_spacing=-device_params['pitch'],
                **pad_details['right']))

            init += device_params['num_pins_y']
            kicad_mod.append(PadArray(
                initial= init,
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                layers=Pad.LAYERS_SMT,
                pincount=device_params['num_pins_x'],
                y_spacing=0, x_spacing=-device_params['pitch'],
                **pad_details['top']))


        body_edge = {
            'left': -device_params['body_size_x']/2,
            'right': device_params['body_size_x']/2,
            'top': -device_params['body_size_y']/2,
            'bottom': device_params['body_size_y']/2
            }

        bounding_box = body_edge.copy()

        if device_params['num_pins_y'] > 0:
            bounding_box['left'] = pad_details['left']['center'][0] - pad_details['left']['size'][0]/2

            bounding_box['right'] = pad_details['right']['center'][0] + pad_details['right']['size'][0]/2

        if device_params['num_pins_x'] > 0:
            bounding_box['top'] = pad_details['top']['center'][1] - pad_details['top']['size'][1]/2

            bounding_box['bottom'] = pad_details['bottom']['center'][1] + pad_details['bottom']['size'][1]/2

        pad_width = pad_details['top']['size'][0]

        # ############################ SilkS ##################################

        silk_pad_offset = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
        silk_offset = configuration['silk_fab_offset']
        if device_params['num_pins_x'] == 0:
            kicad_mod.append(Line(
                start={'x':0,
                    'y':body_edge['top']-silk_offset},
                end={'x':body_edge['right'],
                    'y':body_edge['top']-silk_offset},
                width=configuration['silk_line_width'],
                layer="F.SilkS", x_mirror=0))
            kicad_mod.append(Line(
                start={'x':body_edge['left'],
                    'y':body_edge['bottom']+silk_offset},
                end={'x':body_edge['right'],
                    'y':body_edge['bottom']+silk_offset},
                width=configuration['silk_line_width'],
                layer="F.SilkS", x_mirror=0))
        elif device_params['num_pins_y'] == 0:
            kicad_mod.append(Line(
                start={'y':0,
                    'x':body_edge['left']-silk_offset},
                end={'y':body_edge['bottom'],
                    'x':body_edge['left']-silk_offset},
                width=configuration['silk_line_width'],
                layer="F.SilkS", x_mirror=0))
            kicad_mod.append(Line(
                start={'y':body_edge['top'],
                    'x':body_edge['right']+silk_offset},
                end={'y':body_edge['bottom'],
                    'x':body_edge['right']+silk_offset},
                width=configuration['silk_line_width'],
                layer="F.SilkS", x_mirror=0))
        else:
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
                layer="F.SilkS", x_mirror=0))

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

        kicad_mod.append(RectLine(
            start={
                'x':roundToBase(bounding_box['left']-off, grid),
                'y':cy1
                },
            end={
                'x':roundToBase(bounding_box['right']+off, grid),
                'y':roundToBase(bounding_box['bottom']+off, grid)
                },
            width=configuration['courtyard_line_width'],
            layer='F.CrtYd'))

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

    for filepath in args.files:
        dfn = DFN(configuration)

        with open(filepath, 'r') as command_stream:
            try:
                cmd_file = yaml.load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for pkg in cmd_file:
            dfn.generateFootprint(cmd_file[pkg])
