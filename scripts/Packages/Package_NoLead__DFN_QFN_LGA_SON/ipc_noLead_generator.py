#!/usr/bin/env python3

import sys
import os
import argparse
import yaml
import math
from math import sqrt
import warnings

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA
sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields
from ipc_pad_size_calculators import *
from quad_dual_pad_border import add_dual_or_quad_pad_border

sys.path.append(os.path.join(sys.path[0], "..", "utils"))
from ep_handling_utils import getEpRoundRadiusParams

ipc_density = 'nominal'
ipc_doc_file = '../ipc_definitions.yaml'
category = 'NoLead'
default_library = 'Package_DFN_QFN'

DEFAULT_PASTE_COVERAGE = 0.65
DEFAULT_VIA_PASTE_CLEARANCE = 0.15
DEFAULT_MIN_ANNULAR_RING = 0.15

SILK_MIN_LEN = 0.1

DEBUG_LEVEL = 0

def roundToBase(value, base):
    return round(value/base) * base

class NoLead():
    def __init__(self, configuration):
        self.configuration = configuration
        with open(ipc_doc_file, 'r') as ipc_stream:
            try:
                self.ipc_defintions = yaml.safe_load(ipc_stream)

                self.configuration['min_ep_to_pad_clearance'] = 0.2

                #ToDo: find a settings file that can contain these.
                self.configuration['paste_radius_ratio'] = 0.25
                self.configuration['paste_maximum_radius'] = 0.25

                if 'ipc_generic_rules' in self.ipc_defintions:
                    self.configuration['min_ep_to_pad_clearance'] = self.ipc_defintions['ipc_generic_rules'].get('min_ep_to_pad_clearance', 0.2)

            except yaml.YAMLError as exc:
                print(exc)

    def calcPadDetails(self, device_dimensions, EP_size, ipc_data, ipc_round_base):
        # Zmax = Lmin + 2JT + √(CL^2 + F^2 + P^2)
        # Gmin = Smax − 2JH − √(CS^2 + F^2 + P^2)
        # Xmax = Wmin + 2JS + √(CW^2 + F^2 + P^2)

        # Some manufacturers do not list the terminal spacing (S) in their datasheet but list the terminal lenght (T)
        # Then one can calculate
        # Stol(RMS) = √(Ltol^2 + 2*^2)
        # Smin = Lmin - 2*Tmax
        # Smax(RMS) = Smin + Stol(RMS)

        manf_tol = {
            'F': self.configuration.get('manufacturing_tolerance', 0.1),
            'P': self.configuration.get('placement_tolerance', 0.05)
        }

        pull_back_0 = TolerancedSize(nominal=0)
        pull_back = device_dimensions.get('lead_to_edge', pull_back_0)

        if 'lead_center_pos_x' in device_dimensions or 'lead_center_pos_y' in device_dimensions:
            Gmin_x, Zmax_x, Xmax = ipc_pad_center_plus_size(ipc_data, ipc_round_base, manf_tol,
                    center_position=device_dimensions.get('lead_center_pos_x', TolerancedSize(nominal=0)),
                    lead_length=device_dimensions.get('lead_len_H'),
                    lead_width=device_dimensions['lead_width'])

            Gmin_y, Zmax_y, Xmax_y_ignored = ipc_pad_center_plus_size(ipc_data, ipc_round_base, manf_tol,
                    center_position=device_dimensions.get('lead_center_pos_y', TolerancedSize(nominal=0)),
                    lead_length=device_dimensions.get('lead_len_H'),
                    lead_width=device_dimensions['lead_width'])
        else:
            Gmin_x, Zmax_x, Xmax = ipc_body_edge_inside_pull_back(
                    ipc_data, ipc_round_base, manf_tol,
                    body_size=device_dimensions['body_size_x'],
                    lead_width=device_dimensions['lead_width'],
                    lead_len=device_dimensions.get('lead_len_H'),
                    body_to_inside_lead_edge=device_dimensions.get('body_to_inside_lead_edge'),
                    heel_reduction=device_dimensions.get('heel_reduction', 0),
                    pull_back=pull_back
                    )

            Gmin_y, Zmax_y, Xmax_y_ignored = ipc_body_edge_inside_pull_back(
                    ipc_data, ipc_round_base, manf_tol,
                    body_size=device_dimensions['body_size_y'],
                    lead_width=device_dimensions['lead_width'],
                    lead_len=device_dimensions.get('lead_len_V'),
                    body_to_inside_lead_edge=device_dimensions.get('body_to_inside_lead_edge'),
                    heel_reduction=device_dimensions.get('heel_reduction', 0),
                    pull_back=pull_back
                    )

        min_ep_to_pad_clearance = self.configuration['min_ep_to_pad_clearance']

        heel_reduction_max = 0

        if Gmin_x - 2*min_ep_to_pad_clearance < EP_size['x']:
            heel_reduction_max = ((EP_size['x'] + 2*min_ep_to_pad_clearance - Gmin_x)/2)
            #print('{}, {}, {}'.format(Gmin_x, EP_size['x'], min_ep_to_pad_clearance))
            Gmin_x = EP_size['x'] + 2*min_ep_to_pad_clearance
        if Gmin_y - 2*min_ep_to_pad_clearance < EP_size['y']:
            heel_reduction = ((EP_size['y'] + 2*min_ep_to_pad_clearance - Gmin_y)/2)
            if heel_reduction>heel_reduction_max:
                heel_reduction_max = heel_reduction
            Gmin_y = EP_size['y'] + 2*min_ep_to_pad_clearance

        heel_reduction_max += device_dimensions.get('heel_reduction', 0) #include legacy stuff
        if heel_reduction_max > 0 and DEBUG_LEVEL >= 1:
            print('Heel reduced by {:.4f} to reach minimum EP to pad clearances'.format(heel_reduction_max))

        Pad = {}
        Pad['left'] = {'center':[-(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['right'] = {'center':[(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['top'] = {'center':[0,-(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}
        Pad['bottom'] = {'center':[0,(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}

        return Pad

    @staticmethod
    def deviceDimensions(device_size_data, fp_id):
        unit = device_size_data.get('unit')
        dimensions = {
            'body_size_x': TolerancedSize.fromYaml(device_size_data, base_name='body_size_x', unit=unit),
            'body_size_y': TolerancedSize.fromYaml(device_size_data, base_name='body_size_y', unit=unit),
            'lead_width': TolerancedSize.fromYaml(device_size_data, base_name='lead_width', unit=unit),
            'pitch': TolerancedSize.fromYaml(device_size_data, base_name='pitch', unit=unit).nominal
        }
        dimensions['has_EP'] = False
        if 'EP_size_x_min' in device_size_data and 'EP_size_x_max' in device_size_data or 'EP_size_x' in device_size_data:
            dimensions['EP_size_x'] = TolerancedSize.fromYaml(device_size_data, base_name='EP_size_x', unit=unit)
            dimensions['EP_size_y'] = TolerancedSize.fromYaml(device_size_data, base_name='EP_size_y', unit=unit)
            dimensions['has_EP'] = True
            dimensions['EP_center_x'] = TolerancedSize(nominal=0)
            dimensions['EP_center_y'] = TolerancedSize(nominal=0)
            if 'EP_center_x' in device_size_data and 'EP_center_y' in device_size_data:
                dimensions['EP_center_x'] = TolerancedSize.fromYaml(device_size_data, base_name='EP_center_x', unit=unit)
                dimensions['EP_center_y'] = TolerancedSize.fromYaml(device_size_data, base_name='EP_center_y', unit=unit)

        if 'heel_reduction' in device_size_data:
            print(
                "\033[1;35mThe use of manual heel reduction is deprecated. It is automatically calculated from the minimum EP to pad clearance (ipc config file)\033[0m"
            )
            dimensions['heel_reduction'] = device_size_data.get('heel_reduction', 0)

        if 'lead_to_edge' in device_size_data:
            dimensions['lead_to_edge'] = TolerancedSize.fromYaml(device_size_data, base_name='lead_to_edge', unit=unit)

        if 'lead_center_pos_x' in device_size_data:
            dimensions['lead_center_pos_x'] = TolerancedSize.fromYaml(device_size_data, base_name='lead_center_pos_x', unit=unit)
        if 'lead_center_to_center_x' in device_size_data:
            dimensions['lead_center_pos_x'] = TolerancedSize.fromYaml(device_size_data, base_name='lead_center_to_center_x', unit=unit)/2

        if 'lead_center_pos_y' in device_size_data:
            dimensions['lead_center_pos_y'] = TolerancedSize.fromYaml(device_size_data, base_name='lead_center_pos_y', unit=unit)
        if 'lead_center_to_center_y' in device_size_data:
            dimensions['lead_center_pos_y'] = TolerancedSize.fromYaml(device_size_data, base_name='lead_center_to_center_y', unit=unit)/2

        dimensions['lead_len_H'] = None
        dimensions['lead_len_V'] = None
        if 'lead_len_H' in device_size_data and 'lead_len_V' in device_size_data:
            dimensions['lead_len_H'] = TolerancedSize.fromYaml(device_size_data, base_name='lead_len_H', unit=unit)
            dimensions['lead_len_V'] = TolerancedSize.fromYaml(device_size_data, base_name='lead_len_V', unit=unit)
        elif 'lead_len' in device_size_data or (
                'lead_len_min' in device_size_data and 'lead_len_max' in device_size_data):
            dimensions['lead_len_H'] = TolerancedSize.fromYaml(device_size_data, base_name='lead_len', unit=unit)
            dimensions['lead_len_V'] = dimensions['lead_len_H']

        if 'body_to_inside_lead_edge' in device_size_data:
            dimensions['body_to_inside_lead_edge'] = TolerancedSize.fromYaml(device_size_data, base_name='body_to_inside_lead_edge', unit=unit)
        elif dimensions['lead_len_H'] is None:
            raise KeyError('{}: Either lead lenght or inside lead to edge dimension must be given.'.format(fp_id))

        return dimensions

    def generateFootprint(self, device_params, fp_id):
        print('Building footprint for parameter set: {}'.format(fp_id))
        device_dimensions = NoLead.deviceDimensions(device_params, fp_id)

        if device_dimensions['has_EP'] and 'thermal_vias' in device_params:
            self.__createFootprintVariant(device_params, device_dimensions, True)

        self.__createFootprintVariant(device_params, device_dimensions, False)

    def __createFootprintVariant(self, device_params, device_dimensions, with_thermal_vias):
        fab_line_width = self.configuration.get('fab_line_width', 0.1)
        silk_line_width = self.configuration.get('silk_line_width', 0.12)

        lib_name = device_params.get('library', default_library)

        pincount = device_params['num_pins_x']*2 + device_params['num_pins_y']*2

        default_ipc_config = 'qfn_pull_back' if 'lead_to_edge' in device_params else 'qfn'
        if device_params.get('ipc_class', default_ipc_config) == 'qfn_pull_back':
            ipc_reference = 'ipc_spec_flat_no_lead_pull_back'
        else:
            ipc_reference = 'ipc_spec_flat_no_lead'

        used_density = device_params.get('ipc_density', ipc_density)
        ipc_data_set = self.ipc_defintions[ipc_reference][used_density]
        ipc_round_base = self.ipc_defintions[ipc_reference]['round_base']

        layout = ''
        if device_dimensions['has_EP']:
            name_format = self.configuration['fp_name_EP_format_string_no_trailing_zero']
            if 'EP_size_x_overwrite' in device_params:
                EP_size = {
                    'x':device_params['EP_size_x_overwrite'],
                    'y':device_params['EP_size_y_overwrite']
                    }
            else:
                EP_size = {
                    'x':device_dimensions['EP_size_x'].nominal,
                    'y':device_dimensions['EP_size_y'].nominal
                    }
            EP_center = {
                'x':device_dimensions['EP_center_x'].nominal,
                'y':device_dimensions['EP_center_y'].nominal
                }
        else:
            name_format = self.configuration['fp_name_format_string_no_trailing_zero']
            if device_params.get('use_name_format', 'QFN') == 'LGA':
                name_format = self.configuration['fp_name_lga_format_string_no_trailing_zero']
                if device_params['num_pins_x'] > 0 and device_params['num_pins_y'] > 0:
                    layout = self.configuration['lga_layout_border'].format(
                        nx=device_params['num_pins_x'], ny=device_params['num_pins_y'])

            EP_size = {'x':0, 'y':0}

        if 'custom_name_format' in device_params:
            name_format = device_params['custom_name_format']

        pad_details = self.calcPadDetails(device_dimensions, EP_size, ipc_data_set, ipc_round_base)


        pad_suffix = '_Pad{pad_x:.2f}x{pad_y:.2f}mm'.format(pad_x=pad_details['left']['size'][0],
            pad_y=pad_details['left']['size'][1])
        pad_suffix = '' if device_params.get('include_pad_size', 'none') not in ('fp_name_only', 'both') else pad_suffix
        pad_suffix_3d = '' if device_params.get('include_pad_size', 'none') not in ('both') else pad_suffix

        suffix = device_params.get('suffix', '')
        suffix_3d = suffix if device_params.get('include_suffix_in_3dpath', 'True') == 'True' else ""

        model3d_path_prefix = self.configuration.get('3d_model_prefix','${KISYS3DMOD}')

        size_x = device_dimensions['body_size_x'].nominal
        size_y = device_dimensions['body_size_y'].nominal

        fp_name = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=device_params['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_dimensions['pitch'],
            layout=layout,
            ep_size_x = EP_size['x'],
            ep_size_y = EP_size['y'],
            suffix=pad_suffix,
            suffix2=suffix,
            vias=self.configuration.get('thermal_via_suffix', '_ThermalVias') if with_thermal_vias else ''
            ).replace('__','_').lstrip('_')

        fp_name_2 = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=device_params['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_dimensions['pitch'],
            layout=layout,
            ep_size_x = EP_size['x'],
            ep_size_y = EP_size['y'],
            suffix=pad_suffix_3d,
            suffix2=suffix_3d,
            vias=''
            ).replace('__','_').lstrip('_')

        if 'fp_name_prefix' in device_params:
            prefix = device_params['fp_name_prefix']
            if not prefix.endswith('_'):
                prefix += '_'
            fp_name = prefix + fp_name
            fp_name_2 = prefix + fp_name_2

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

        pad_radius = add_dual_or_quad_pad_border(kicad_mod, self.configuration, pad_details, device_params)

        if device_dimensions['has_EP']:
            pad_shape_details = getEpRoundRadiusParams(device_params, self.configuration, pad_radius)
            ep_pad_number = device_params.get('EP_pin_number', pincount+1)
            if with_thermal_vias:
                thermals = device_params['thermal_vias']
                paste_coverage = thermals.get('EP_paste_coverage',
                                               device_params.get('EP_paste_coverage', DEFAULT_PASTE_COVERAGE))

                kicad_mod.append(ExposedPad(
                    number=ep_pad_number, size=EP_size,
                    at=EP_center,
                    paste_layout=thermals.get('EP_num_paste_pads', device_params.get('EP_num_paste_pads', 1)),
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
                    kicad4_compatible=args.kicad4_compatible,
                    **pad_shape_details
                    ))
            else:
                kicad_mod.append(ExposedPad(
                    number=ep_pad_number, size=EP_size,
                    at=EP_center,
                    paste_layout=device_params.get('EP_num_paste_pads', 1),
                    paste_coverage=device_params.get('EP_paste_coverage', DEFAULT_PASTE_COVERAGE),
                    kicad4_compatible=args.kicad4_compatible,
                    **pad_shape_details
                    ))

        body_edge = {
            'left': -size_x/2,
            'right': size_x/2,
            'top': -size_y/2,
            'bottom': size_y/2
            }

        bounding_box = body_edge.copy()

        if device_params['num_pins_x'] == 0 and EP_size['y'] > size_y:
                bounding_box['top'] = -EP_size['y']/2
                bounding_box['bottom'] = EP_size['y']/2

        if device_params['num_pins_y'] == 0 and EP_size['x'] > size_x:
                bounding_box['left'] = -EP_size['x']/2
                bounding_box['right'] = EP_size['x']/2

        if device_params['num_pins_y'] > 0:
            bounding_box['left'] = pad_details['left']['center'][0] - pad_details['left']['size'][0]/2

            bounding_box['right'] = pad_details['right']['center'][0] + pad_details['right']['size'][0]/2

        if device_params['num_pins_x'] > 0:
            bounding_box['top'] = pad_details['top']['center'][1] - pad_details['top']['size'][1]/2

            bounding_box['bottom'] = pad_details['bottom']['center'][1] + pad_details['bottom']['size'][1]/2

        pad_width = pad_details['top']['size'][0]

        for key in body_edge:
            if bounding_box[key] < 0:
                bounding_box[key] = min(bounding_box[key], body_edge[key])
            else:
                bounding_box[key] = max(bounding_box[key], body_edge[key])

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
                layer="F.SilkS"))
            kicad_mod.append(Line(
                start={'x':body_edge['left'],
                    'y':body_edge['bottom']+silk_offset},
                end={'x':body_edge['right'],
                    'y':body_edge['bottom']+silk_offset},
                width=configuration['silk_line_width'],
                layer="F.SilkS", y_mirror=0))
        elif device_params['num_pins_y'] == 0:
            kicad_mod.append(Line(
                start={'y':0,
                    'x':body_edge['left']-silk_offset},
                end={'y':body_edge['bottom'],
                    'x':body_edge['left']-silk_offset},
                width=configuration['silk_line_width'],
                layer="F.SilkS"))
            kicad_mod.append(Line(
                start={'y':body_edge['top'],
                    'x':body_edge['right']+silk_offset},
                end={'y':body_edge['bottom'],
                    'x':body_edge['right']+silk_offset},
                width=configuration['silk_line_width'],
                layer="F.SilkS", x_mirror=0))
        else:
            sx1 = -(device_dimensions['pitch']*(device_params['num_pins_x']-1)/2.0
                + pad_width/2.0 + silk_pad_offset)

            sy1 = -(device_dimensions['pitch']*(device_params['num_pins_y']-1)/2.0
                + pad_width/2.0 + silk_pad_offset)

            poly_silk = [
                {'x': sx1, 'y': body_edge['top']-silk_offset},
                {'x': body_edge['left']-silk_offset, 'y': body_edge['top']-silk_offset},
                {'x': body_edge['left']-silk_offset, 'y': sy1}
            ]
            if sx1 - SILK_MIN_LEN < body_edge['left']-silk_offset:
                poly_silk = poly_silk[1:]
            if sy1 - SILK_MIN_LEN < body_edge['top']-silk_offset:
                poly_silk = poly_silk[:-1]
            if len(poly_silk) > 1:
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
                if len(poly_silk) > 2:
                    kicad_mod.append(Line(
                        start={'x': sx1, 'y': body_edge['top']-silk_offset},
                        end={'x': body_edge['left']-silk_offset, 'y': body_edge['top']-silk_offset},
                        width=configuration['silk_line_width'],
                        layer="F.SilkS"))

        # # ######################## Fabrication Layer ###########################

        fab_bevel_size = min(configuration['fab_bevel_size_absolute'], configuration['fab_bevel_size_relative']*min(size_x, size_y))

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
    parser.add_argument('--density', type=str, nargs='?', help='IPC density level (L,N,M)', default='N')
    parser.add_argument('--ipc_doc', type=str, nargs='?', help='IPC definition document', default='../ipc_definitions.yaml')
    parser.add_argument('--force_rectangle_pads', action='store_true', help='Force the generation of rectangle pads instead of rounded rectangle')
    parser.add_argument('--kicad4_compatible', action='store_true', help='Create footprints kicad 4 compatible')
    parser.add_argument('-v', '--verbose', action='count', help='set debug level')
    args = parser.parse_args()

    if args.density == 'L':
        ipc_density = 'least'
    elif args.density == 'M':
        ipc_density = 'most'

    if args.verbose:
        DEBUG_LEVEL = args.verbose

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

    if args.force_rectangle_pads or args.kicad4_compatible:
        configuration['round_rect_max_radius'] = None
        configuration['round_rect_radius_ratio'] = 0

    configuration['kicad4_compatible'] = args.kicad4_compatible

    for filepath in args.files:
        no_lead = NoLead(configuration)

        with open(filepath, 'r') as command_stream:
            try:
                cmd_file = yaml.safe_load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for pkg in cmd_file:
            no_lead.generateFootprint(cmd_file[pkg], pkg)
