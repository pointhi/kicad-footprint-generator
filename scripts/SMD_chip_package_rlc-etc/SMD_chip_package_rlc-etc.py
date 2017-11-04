#!/usr/bin/env python

import sys
import os
import argparse
import yaml
import math

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA

# def create_footprint(name, **kwargs):
#     kicad_mod = Footprint(name)
#
#     # init kicad footprint
#     kicad_mod.setDescription(kwargs['description'])
#     kicad_mod.setTags('Capacitor Electrolytic')
#     kicad_mod.setAttribute('smd')
#
#     # set general values
#     text_offset_y = kwargs['width'] / 2. + kwargs['courtjard'] + 0.8
#
#     kicad_mod.append(Text(type='reference', text='REF**', at=[0, -text_offset_y], layer='F.SilkS'))
#     kicad_mod.append(Text(type='value', text=name, at=[0, text_offset_y], layer='F.Fab'))
#
#     # create fabrication layer
#     fab_x = kwargs['length'] / 2.
#     fab_y = kwargs['width'] / 2.
#     fab_edge = 1
#     fab_x_edge = fab_x - fab_edge
#     fab_y_edge = fab_y - fab_edge
#     kicad_mod.append(Line(start=[fab_x, -fab_y], end=[fab_x, fab_y], layer='F.Fab'))
#     kicad_mod.append(Line(start=[-fab_x_edge, -fab_y], end=[fab_x, -fab_y], layer='F.Fab'))
#     kicad_mod.append(Line(start=[-fab_x_edge, fab_y], end=[fab_x, fab_y], layer='F.Fab'))
#     kicad_mod.append(Line(start=[-fab_x, -fab_y_edge], end=[-fab_x, fab_y_edge], layer='F.Fab'))
#
#     kicad_mod.append(Line(start=[-fab_x, -fab_y_edge], end=[-fab_x_edge, -fab_y], layer='F.Fab'))
#     kicad_mod.append(Line(start=[-fab_x, fab_y_edge], end=[-fab_x_edge, fab_y], layer='F.Fab'))
#
#     fab_text_x = kwargs['pad_spacing'] / 2. + kwargs['pad_length'] / 4.
#     kicad_mod.append(Text(type='user', text='+', at=[-fab_text_x, 0], layer='F.Fab'))
#
#     # create silkscreen
#     silk_x = kwargs['length'] / 2. + 0.11
#     silk_y = kwargs['width'] / 2. + 0.11
#     silk_y_start = kwargs['pad_width'] / 2. + 0.3
#     silk_x_edge = fab_x - fab_edge + 0.05
#     silk_y_edge = fab_y - fab_edge + 0.05
#
#     kicad_mod.append(Line(start=[silk_x, silk_y], end=[silk_x, silk_y_start], layer='F.SilkS'))
#     kicad_mod.append(Line(start=[silk_x, -silk_y], end=[silk_x, -silk_y_start], layer='F.SilkS'))
#     kicad_mod.append(Line(start=[-silk_x_edge, -silk_y], end=[silk_x, -silk_y], layer='F.SilkS'))
#     kicad_mod.append(Line(start=[-silk_x_edge, silk_y], end=[silk_x, silk_y], layer='F.SilkS'))
#
#     if silk_y_edge > silk_y_start:
#         kicad_mod.append(Line(start=[-silk_x, silk_y_edge], end=[-silk_x, silk_y_start], layer='F.SilkS'))
#         kicad_mod.append(Line(start=[-silk_x, -silk_y_edge], end=[-silk_x, -silk_y_start], layer='F.SilkS'))
#
#         kicad_mod.append(Line(start=[-silk_x, -silk_y_edge], end=[-silk_x_edge, -silk_y], layer='F.SilkS'))
#         kicad_mod.append(Line(start=[-silk_x, silk_y_edge], end=[-silk_x_edge, silk_y], layer='F.SilkS'))
#     else:
#         silk_x_cut = silk_x - (silk_y_start - silk_y_edge) # because of the 45 degree edge we can user a simple apporach
#         silk_y_edge_cut = silk_y_start
#
#         kicad_mod.append(Line(start=[-silk_x_cut, -silk_y_edge_cut], end=[-silk_x_edge, -silk_y], layer='F.SilkS'))
#         kicad_mod.append(Line(start=[-silk_x_cut, silk_y_edge_cut], end=[-silk_x_edge, silk_y], layer='F.SilkS'))
#
#     silk_cane_x_start = math.cos(math.asin(silk_y_start / (kwargs['diameter'] / 2.))) * (kwargs['diameter'] / 2.)
#     silk_cane_angle = 180 - math.acos(2 * (silk_cane_x_start / kwargs['diameter'])) * 360. / math.pi # TODO 180
#
#     kicad_mod.append(Arc(center=[0, 0], start=[-silk_cane_x_start, -silk_y_start], angle=silk_cane_angle,layer='F.SilkS'))
#     kicad_mod.append(Arc(center=[0, 0], start=[silk_cane_x_start, silk_y_start], angle=silk_cane_angle, layer='F.SilkS'))
#
#     # create courtyard
#     courtjard_x = kwargs['pad_spacing'] / 2. + kwargs['pad_length'] + kwargs['courtjard']
#     courtjard_y = kwargs['width'] / 2. + kwargs['courtjard']
#
#     kicad_mod.append(RectLine(start=[courtjard_x, courtjard_y], end=[-courtjard_x, -courtjard_y], layer='F.CrtYd'))
#
#     # '+' sign on silkscreen
#     silk_text_x = courtjard_x- 0.6
#     silk_text_y = courtjard_y - 0.6
#     kicad_mod.append(Text(type='user', text='+', at=[-silk_text_x, silk_text_y], layer='F.SilkS'))
#
#     # all pads have this kwargs, so we only write them once
#     pad_kwargs = {'type': Pad.TYPE_SMT,
#                   'shape': Pad.SHAPE_RECT,
#                   'layers': ['F.Cu', 'F.Mask', 'F.Paste']}
#
#     # create pads
#     x_pad_spacing = kwargs['pad_spacing'] / 2. + kwargs['pad_length'] / 2.
#     kicad_mod.append(Pad(number= 1, at=[-x_pad_spacing, 0],
#                          size=[kwargs['pad_length'], kwargs['pad_width']], **pad_kwargs))
#     kicad_mod.append(Pad(number= 2, at=[x_pad_spacing, 0],
#                          size=[kwargs['pad_length'], kwargs['pad_width']], **pad_kwargs))
#
#     # add model
#     kicad_mod.append(Model(filename="example.3dshapes/{name}.wrl".format(name=name),
#                             at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
#
#     # write file
#     file_handler = KicadFileHandler(kicad_mod)
#     file_handler.writeFile('{name}.kicad_mod'.format(name=name))

def roundToBase(value, base):
    return round(value/base) * base

class TwoTerminalSMDchip():
    def __init__(self, command_file, configuration):
        self.configuration = configuration
        with open(command_file, 'r') as command_stream:
            try:
                footprint_commands = yaml.load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        ipc_doc = footprint_commands['ipc_definition']
        with open(ipc_doc, 'r') as ipc_stream:
            try:
                self.ipc_defintions = yaml.load(ipc_stream)
            except yaml.YAMLError as exc:
                print(exc)

        self.footprint_group_definitions = footprint_commands['device_groups']

    def calcPadDetails(self, device_params, ipc_data, ipc_round_base, footprint_group_data):
        # Zmax = Lmin + 2JT + √(CL^2 + F^2 + P^2)
        # Gmin = Smax − 2JH − √(CS^2 + F^2 + P^2)
        # Xmax = Wmin + 2JS + √(CW^2 + F^2 + P^2)

        # Some manufacturers do not list the terminal spacing (S) in their datasheet but list the terminal lenght (T)
        # Then one can calculate
        # Stol(RMS) = √(Ltol^2 + 2*Ttol^2)
        # Smin = Lmin - 2*Tmax
        # Smax(RMS) = Smin + Stol(RMS)

        F = self.configuration.get('manufacturing_tolerance', 0.1)
        P = self.configuration.get('placement_tolerance', 0.05)

        length_tolerance = device_params['body_length_max']-device_params['body_length_min']
        width_tolerance = device_params['body_width_max']-device_params['body_width_min']

        if 'terminator_spacing_max' in device_params:
            spacing_tolerance = device_params['terminator_spacing_max']-device_params['terminator_spacing_min']
            Gmin = device_params['terminator_spacing_max'] - 2*ipc_data['heel'] - math.sqrt(spacing_tolerance**2 + F**2 + P**2)
        else:
            terminal_tolerance = device_params['terminal_length_max'] - device_params['terminal_length_min']
            spacing_tolerance = math.sqrt(length_tolerance**2+terminal_tolerance**2)
            Smin = device_params['body_length_min'] - 2*device_params['terminal_length_max']
            Smax = Smin + spacing_tolerance

            Gmin = Smax - 2*ipc_data['heel'] - math.sqrt(spacing_tolerance**2 + F**2 + P**2)

        Zmax = device_params['body_length_min'] + 2*ipc_data['toe'] + math.sqrt(length_tolerance**2 + F**2 + P**2)
        Xmax = device_params['body_width_min'] + 2*ipc_data['side'] + math.sqrt(width_tolerance**2 + F**2 + P**2)

        Zmax = roundToBase(Zmax, ipc_round_base['toe'])
        Gmin = roundToBase(Gmin, ipc_round_base['heel'])
        Xmax = roundToBase(Xmax, ipc_round_base['side'])

        Zmax += footprint_group_data.get('pad_length_addition', 0)

        return {'at':[-(Zmax+Gmin)/4,0], 'size':[(Zmax-Gmin)/2,Xmax], 'Z':Zmax,'G':Gmin,'W':Xmax}

    def getTextFieldDetails(self, field_definition, body_size):
        position_y = field_definition['position'][0]
        at = [0,0]


        if body_size[0] < body_size[1] and position_y == 'center':
            rotation = 1
        else:
            rotation = 0

        if 'size' in field_definition:
            size = field_definition['size']
            rotation = 0
        elif 'size_min' in field_definition and 'size_max' in field_definition:
            # We want at least 3 char reference designators space. If we can't fit these we move the reverence to the outside.
            size_max = field_definition['size_max']
            size_min = field_definition['size_min']
            if body_size[rotation] >= 4*size_max[1]:
                if body_size[0] >= 4*size_max[1]:
                    rotation = 0
                size = size_max
            elif body_size[rotation] < 4*size_min[1]:
                size = size_min
                if body_size[rotation] < 3*size_min[1]:
                    if position_y == 'center':
                        rotation = 0
                        position_y = 'top'
            else:
                fs = roundToBase(body_size[rotation]/4, 0.01)
                size = [fs, fs]
        else:
            rotation = 0
            position_y = 'top'
            size = [1,1]

        text_outside_y_pos = fs = roundToBase(body_size[1]/2+5/4.0*size[0], 0.01)
        if position_y == 'top':
            at = [0, -text_outside_y_pos]
        elif position_y == 'bottom':
            at = [0, text_outside_y_pos]

        fontwidth = roundToBase(field_definition['thickness_factor']*size[0], 0.01)
        return {'at': at, 'size': size, 'layer': field_definition['layer'], 'thickness': fontwidth, 'rotation': rotation*90}

    def generateFootprints(self):
        fab_line_width = self.configuration.get('fab_line_width', 0.1)
        silk_line_width = self.configuration.get('silk_line_width', 0.12)

        for group_name in self.footprint_group_definitions:
            #print(device_group)
            footprint_group_data = self.footprint_group_definitions[group_name]

            device_size_docs = footprint_group_data['size_definitions']
            package_size_defintions={}
            for device_size_doc in device_size_docs:
                with open(device_size_doc, 'r') as size_stream:
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

                pad_details = self.calcPadDetails(device_size_data, ipc_data_set, ipc_round_base, footprint_group_data)
                #print(calc_pad_details())
                #print("generate {name}.kicad_mod".format(name=footprint))

                suffix = footprint_group_data.get('suffix', '').format(pad_x=pad_details['size'][0], pad_y=pad_details['size'][1])
                prefix = footprint_group_data['prefix']
                code_imperial = device_size_data['code_imperial']
                name_format = self.configuration['fp_name_format_string']
                if 'code_metric' in device_size_data:
                    code_metric = device_size_data['code_metric']
                    fp_name = name_format.format(prefix=prefix, code_imperial=code_imperial, code_metric=code_metric, suffix=suffix)
                else:
                    name_format_non_metric = self.configuration['fp_name_non_metric_format_string']
                    fp_name = name_format_non_metric.format(prefix=prefix, code_imperial=code_imperial, suffix=suffix)
                #print(fp_name)
                #print(pad_details)

                kicad_mod = Footprint(fp_name)

                # init kicad footprint
                kicad_mod.setDescription(footprint_group_data['description'].format(code_imperial=code_imperial, code_metric=code_metric, size_info=device_size_data.get('size_info')))
                kicad_mod.setTags(footprint_group_data['keywords'])
                kicad_mod.setAttribute('smd')

                kicad_mod.append(Pad(number= 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT, **pad_details))
                pad_details['at'][0] *= (-1)
                kicad_mod.append(Pad(number= 2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT, **pad_details))

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
                        self.configuration['pad_silk_clearance'] - silk_line_width/2

                    silk_y_bottom = self.configuration['pad_silk_clearance'] + silk_line_width/2 + \
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
                    if pad_spacing > 2*self.configuration['pad_silk_clearance'] + \
                            self.configuration['silk_line_lenght_min'] + self.configuration['silk_line_width']:
                        silk_outline_x = pad_spacing/2 - silk_line_width - self.configuration['pad_silk_clearance']
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

                reference_fields = self.configuration['references']
                kicad_mod.append(Text(type='reference', text='REF**',
                    **self.getTextFieldDetails(reference_fields[0], outline_size)))

                for additional_ref in reference_fields[1:]:
                    kicad_mod.append(Text(type='user', text='%R',
                    **self.getTextFieldDetails(additional_ref, outline_size)))

                value_fields = self.configuration['values']
                kicad_mod.append(Text(type='value', text=fp_name,
                    **self.getTextFieldDetails(value_fields[0], outline_size)))

                for additional_value in value_fields[1:]:
                    kicad_mod.append(Text(type='user', text='%V',
                        **self.getTextFieldDetails(additional_value, outline_size)))

                modeld_path_prefix = self.configuration.get('3d_model_prefix','${KISYS3DMOD}')
                if footprint_group_data.get('include_suffix_in_3dpath', 'True') == 'True':
                    model_name = '{modeld_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
                        modeld_path_prefix=modeld_path_prefix, lib_name=footprint_group_data['fp_lib_name'], fp_name=fp_name)
                else:
                    fp_name_2 = name_format.format(prefix=prefix, code_imperial=code_imperial, code_metric=code_metric, suffix="")
                    model_name = '{modeld_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
                        modeld_path_prefix=modeld_path_prefix, lib_name=footprint_group_data['fp_lib_name'], fp_name=fp_name_2)

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
    parser.add_argument('-c', '--config', type=str, nargs='?', help='the config file defining how the footprint will look like.', default='config_KLCv3.0.yaml')

    args = parser.parse_args()

    with open(args.config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    for filepath in args.files:
        two_terminal_smd =TwoTerminalSMDchip(filepath, configuration)
        two_terminal_smd.generateFootprints()
