#!/usr/bin/env python

import sys
import os
import argparse
import yaml
import math

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA
sys.path.append(os.path.join(sys.path[0], "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

size_definition_path = "size_definitions/"
def roundToBase(value, base):
    return round(value/base) * base

class TwoTerminalSMDchip():
    def __init__(self, command_file, configuration):
        self.configuration = configuration
        with open(command_file, 'r') as command_stream:
            try:
                self.footprint_group_definitions = yaml.load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        ipc_doc = configuration['ipc_definition']
        with open(ipc_doc, 'r') as ipc_stream:
            try:
                self.ipc_defintions = yaml.load(ipc_stream)
            except yaml.YAMLError as exc:
                print(exc)



    def calcPadDetails(self, device_params, ipc_data, ipc_round_base, footprint_group_data):
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

        Ltol = device_params['body_length_max']-device_params['body_length_min']

        if 'terminal_width_min' in device_params:
            terminal_width_min = device_params['terminal_width_min']
            terminal_width_max = device_params['terminal_width_max']
        else:
            terminal_width_min = device_params['body_width_min']
            terminal_width_max = device_params['body_width_max']

        width_tolerance = terminal_width_max - terminal_width_min

        if 'terminator_spacing_max' in device_params:
            Tmin = (device_params['body_length_max'] - device_params['terminator_spacing_max'])/2
            Tmax = (device_params['body_length_min'] - device_params['terminator_spacing_min'])/2
            Ttol = (Tmax-Tmin)
            Stol_RMS = math.sqrt(Ltol**2+2*(Ttol**2))
            Smax_RMS = device_params['terminator_spacing_min'] + Stol_RMS
            Gmin = Smax_RMS - 2*ipc_data['heel'] - math.sqrt(Stol_RMS**2 + F**2 + P**2)

        else:
            Ttol = (device_params['terminal_length_max'] - device_params['terminal_length_min'])
            Stol_RMS = math.sqrt(Ltol**2+2*(Ttol**2))
            Smin = device_params['body_length_min'] - 2*device_params['terminal_length_max']
            Smax_RMS = Smin + Stol_RMS

            Gmin = Smax_RMS - 2*ipc_data['heel'] - math.sqrt(Stol_RMS**2 + F**2 + P**2)

        Zmax = device_params['body_length_min'] + 2*ipc_data['toe'] + math.sqrt(Ltol**2 + F**2 + P**2)
        Xmax = terminal_width_min + 2*ipc_data['side'] + math.sqrt(width_tolerance**2 + F**2 + P**2)

        Zmax = roundToBase(Zmax, ipc_round_base['toe'])
        Gmin = roundToBase(Gmin, ipc_round_base['heel'])
        Xmax = roundToBase(Xmax, ipc_round_base['side'])

        Zmax += footprint_group_data.get('pad_length_addition', 0)
        Pad = {'at':[-(Zmax+Gmin)/4,0], 'size':[(Zmax-Gmin)/2,Xmax]}
        Paste = None

        if 'paste_pad' in footprint_group_data:
            rel_reduction_factor = footprint_group_data['paste_pad'].get('all_sides_rel', 0.9)
            x_abs_reduction = (1 - rel_reduction_factor)*Pad['size'][0]
            Zmax -= 2*x_abs_reduction
            Gmin += 2*x_abs_reduction - 2 * footprint_group_data['paste_pad'].get('heel_abs',0)
            Xmax *= rel_reduction_factor
            Paste = {'at':[-(Zmax+Gmin)/4,0], 'size':[(Zmax-Gmin)/2,Xmax]}

        return Pad, Paste

    def generateFootprints(self):
        fab_line_width = self.configuration.get('fab_line_width', 0.1)
        silk_line_width = self.configuration.get('silk_line_width', 0.12)

        for group_name in self.footprint_group_definitions:
            #print(device_group)
            footprint_group_data = self.footprint_group_definitions[group_name]

            device_size_docs = footprint_group_data['size_definitions']
            package_size_defintions={}
            for device_size_doc in device_size_docs:
                with open(size_definition_path+device_size_doc, 'r') as size_stream:
                    try:
                        package_size_defintions.update(yaml.load(size_stream))
                    except yaml.YAMLError as exc:
                        print(exc)

            for size_name in package_size_defintions:
                device_size_data = package_size_defintions[size_name]

                ipc_reference = footprint_group_data['ipc_reference']
                ipc_density = footprint_group_data['ipc_density']
                ipc_data_set = self.ipc_defintions[ipc_reference][ipc_density]
                ipc_round_base = self.ipc_defintions[ipc_reference]['round_base']

                pad_details, paste_details = self.calcPadDetails(device_size_data, ipc_data_set, ipc_round_base, footprint_group_data)
                #print(calc_pad_details())
                #print("generate {name}.kicad_mod".format(name=footprint))

                suffix = footprint_group_data.get('suffix', '').format(pad_x=pad_details['size'][0],
                    pad_y=pad_details['size'][1])
                prefix = footprint_group_data['prefix']

                model3d_path_prefix = self.configuration.get('3d_model_prefix','${KISYS3DMOD}')
                suffix_3d = suffix if footprint_group_data.get('include_suffix_in_3dpath', 'True') == 'True' else ""

                code_metric = device_size_data.get('code_metric')
                code_letter = device_size_data.get('code_letter')
                code_imperial = device_size_data.get('code_imperial')

                if 'code_letter' in device_size_data:
                    name_format = self.configuration['fp_name_tantal_format_string']
                else:
                    if 'code_metric' in device_size_data:
                        name_format = self.configuration['fp_name_format_string']
                    else:
                        name_format = self.configuration['fp_name_non_metric_format_string']

                fp_name = name_format.format(prefix=prefix,
                    code_imperial=code_imperial, code_metric=code_metric,
                    code_letter=code_letter, suffix=suffix)
                fp_name_2 = name_format.format(prefix=prefix,
                    code_imperial=code_imperial, code_letter=code_letter,
                    code_metric=code_metric, suffix=suffix_3d)
                model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
                    model3d_path_prefix=model3d_path_prefix, lib_name=footprint_group_data['fp_lib_name'], fp_name=fp_name_2)
                #print(fp_name)
                #print(pad_details)

                kicad_mod = Footprint(fp_name)

                # init kicad footprint
                kicad_mod.setDescription(footprint_group_data['description'].format(code_imperial=code_imperial,
                    code_metric=code_metric, code_letter=code_letter,
                    size_info=device_size_data.get('size_info')))
                kicad_mod.setTags(footprint_group_data['keywords'])
                kicad_mod.setAttribute('smd')

                if paste_details is not None:
                    kicad_mod.append(Pad(number= 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        layers=['F.Cu', 'F.Mask'], **pad_details))
                    pad_details['at'][0] *= (-1)
                    kicad_mod.append(Pad(number= 2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        layers=['F.Cu', 'F.Mask'], **pad_details))

                    kicad_mod.append(Pad(number= '', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        layers=['F.Paste'], **paste_details))
                    paste_details['at'][0] *= (-1)
                    kicad_mod.append(Pad(number= '', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        layers=['F.Paste'], **paste_details))
                else:
                    kicad_mod.append(Pad(number= 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        layers=Pad.LAYERS_SMT, **pad_details))
                    pad_details['at'][0] *= (-1)
                    kicad_mod.append(Pad(number= 2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        layers=Pad.LAYERS_SMT, **pad_details))

                fab_outline = self.configuration.get('fab_outline', 'typical')
                if fab_outline == 'max':
                    outline_size = [device_size_data['body_length_max'], device_size_data['body_width_max']]
                elif fab_outline == 'min':
                    outline_size = [device_size_data['body_length_min'], device_size_data['body_width_min']]
                else:
                    outline_size = [device_size_data['body_length'], device_size_data['body_width']]

                if footprint_group_data.get('polarization_mark', 'False') == 'True':
                    polararity_marker_size = self.configuration.get('fab_polarity_factor', 0.25)
                    polararity_marker_size *= (outline_size[1] if outline_size[1] < outline_size[0] else outline_size[0])

                    polarity_marker_thick_line = False

                    polarity_max_size = self.configuration.get('fab_polarity_max_size', 1)
                    if polararity_marker_size > polarity_max_size:
                        polararity_marker_size = polarity_max_size
                    polarity_min_size = self.configuration.get('fab_polarity_min_size', 0.25)
                    if polararity_marker_size < polarity_min_size:
                        if polararity_marker_size < polarity_min_size*0.6:
                            polarity_marker_thick_line = True
                        polararity_marker_size = polarity_min_size

                    silk_x_left = -abs(pad_details['at'][0]) - pad_details['size'][0]/2 - \
                        self.configuration['silk_pad_clearance'] - silk_line_width/2

                    silk_y_bottom = self.configuration['silk_pad_clearance'] + silk_line_width/2 + \
                        (outline_size[1] if outline_size[1]> pad_details['size'][1] else pad_details['size'][1])/2

                    if polarity_marker_thick_line:
                        kicad_mod.append(RectLine(start=[-outline_size[0]/2, outline_size[1]/2],
                            end=[outline_size[0]/2, -outline_size[1]/2],
                            layer='F.Fab', width=fab_line_width))
                        x = -outline_size[0]/2 + fab_line_width
                        kicad_mod.append(Line(start=[x, outline_size[1]/2],
                            end=[x, -outline_size[1]/2],
                            layer='F.Fab', width=fab_line_width))
                        x += fab_line_width
                        if x < -fab_line_width/2:
                            kicad_mod.append(Line(start=[x, outline_size[1]/2],
                                end=[x, -outline_size[1]/2],
                                layer='F.Fab', width=fab_line_width))

                        kicad_mod.append(Circle(center=[silk_x_left-0.05, 0],
                            radius=0.05, layer="F.SilkS", width=0.1))
                    else:
                        poly_fab= [
                            {'x':outline_size[0]/2,'y':-outline_size[1]/2},
                            {'x':polararity_marker_size - outline_size[0]/2,'y':-outline_size[1]/2},
                            {'x':-outline_size[0]/2,'y':polararity_marker_size-outline_size[1]/2},
                            {'x':-outline_size[0]/2,'y':outline_size[1]/2},
                            {'x':outline_size[0]/2,'y':outline_size[1]/2},
                            {'x':outline_size[0]/2,'y':-outline_size[1]/2}
                        ]
                        kicad_mod.append(PolygoneLine(polygone=poly_fab, layer='F.Fab', width=fab_line_width))

                        poly_silk = [
                            {'x':outline_size[0]/2,'y':-silk_y_bottom},
                            {'x':silk_x_left,'y':-silk_y_bottom},
                            {'x':silk_x_left,'y':silk_y_bottom},
                            {'x':outline_size[0]/2,'y':silk_y_bottom}
                        ]
                        kicad_mod.append(PolygoneLine(polygone=poly_silk, layer='F.SilkS', width=silk_line_width))
                else:
                    kicad_mod.append(RectLine(start=[-outline_size[0]/2, outline_size[1]/2],
                        end=[outline_size[0]/2, -outline_size[1]/2],
                        layer='F.Fab', width=fab_line_width))

                    pad_spacing = 2*abs(pad_details['at'][0])-pad_details['size'][0]
                    if pad_spacing > 2*self.configuration['silk_pad_clearance'] + \
                            self.configuration['silk_line_lenght_min'] + self.configuration['silk_line_width']:
                        silk_outline_x = pad_spacing/2 - silk_line_width - self.configuration['silk_pad_clearance']
                        silk_outline_y = outline_size[1]/2 + self.configuration['silk_fab_offset']

                        kicad_mod.append(Line(start=[-silk_outline_x, -silk_outline_y],
                            end=[silk_outline_x, -silk_outline_y], layer='F.SilkS', width=silk_line_width))
                        kicad_mod.append(Line(start=[-silk_outline_x, silk_outline_y],
                            end=[silk_outline_x, silk_outline_y], layer='F.SilkS', width=silk_line_width))

                CrtYd_rect = [None,None]
                CrtYd_rect[0] = roundToBase(2 * abs(pad_details['at'][0]) + \
                    pad_details['size'][0] + 2 * ipc_data_set['courtyard'], 0.02)
                if pad_details['size'][1] > outline_size[1]:
                    CrtYd_rect[1] = pad_details['size'][1] + 2 * ipc_data_set['courtyard']
                else:
                    CrtYd_rect[1] = outline_size[1] + 2 * ipc_data_set['courtyard']

                CrtYd_rect[1] = roundToBase(CrtYd_rect[1], 0.02)

                kicad_mod.append(RectLine(start=[-CrtYd_rect[0]/2, CrtYd_rect[1]/2],
                    end=[CrtYd_rect[0]/2, -CrtYd_rect[1]/2],
                    layer='F.CrtYd', width=self.configuration['courtyard_line_width']))

                ######################### Text Fields ###############################

                addTextFields(kicad_mod=kicad_mod, configuration=configuration,
                    body_edges={'left':-outline_size[0]/2,'right':outline_size[0]/2,
                                'top':-outline_size[1]/2,'bottom':outline_size[1]/2},
                    courtyard={'top':-CrtYd_rect[1]/2, 'bottom':CrtYd_rect[1]/2}, fp_name=fp_name, text_y_inside_position='center')

                kicad_mod.append(Model(filename=model_name))
                output_dir = '{lib_name:s}.pretty/'.format(lib_name=footprint_group_data['fp_lib_name'])
                if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
                    os.makedirs(output_dir)
                filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=fp_name)

                file_handler = KicadFileHandler(kicad_mod)
                file_handler.writeFile(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files holding information about what devices should be created.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='config_KLCv3.0.yaml')
    args = parser.parse_args()

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
    args = parser.parse_args()

    for filepath in args.files:
        two_terminal_smd =TwoTerminalSMDchip(filepath, configuration)
        two_terminal_smd.generateFootprints()
