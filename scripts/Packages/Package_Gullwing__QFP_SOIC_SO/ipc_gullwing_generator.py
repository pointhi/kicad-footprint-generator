#!/usr/bin/env python3

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
from ipc_pad_size_calculators import *
from quad_dual_pad_border import add_dual_or_quad_pad_border
from drawing_tools import nearestSilkPointOnOrthogonalLine

sys.path.append(os.path.join(sys.path[0], "..", "utils"))
from ep_handling_utils import getEpRoundRadiusParams

ipc_density = 'nominal'
ipc_doc_file = '../ipc_definitions.yaml'

DEFAULT_PASTE_COVERAGE = 0.65
DEFAULT_VIA_PASTE_CLEARANCE = 0.15
DEFAULT_MIN_ANNULAR_RING = 0.15

def roundToBase(value, base):
    return round(value/base) * base

class Gullwing():
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

        Gmin_x, Zmax_x, Xmax = ipc_gull_wing(
                ipc_data, ipc_round_base, manf_tol,
                device_dimensions['lead_width'],
                device_dimensions['overall_size_x'],
                lead_len=device_dimensions.get('lead_len'),
                heel_reduction=device_dimensions.get('heel_reduction', 0)
                )

        Gmin_y, Zmax_y, Xmax_y_ignored = ipc_gull_wing(
                ipc_data, ipc_round_base, manf_tol,
                device_dimensions['lead_width'],
                device_dimensions['overall_size_y'],
                lead_len=device_dimensions.get('lead_len'),
                heel_reduction=device_dimensions.get('heel_reduction', 0)
                )

        min_ep_to_pad_clearance = configuration['min_ep_to_pad_clearance']

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

        Pad = {}
        Pad['left'] = {'center':[-(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['right'] = {'center':[(Zmax_x+Gmin_x)/4, 0], 'size':[(Zmax_x-Gmin_x)/2,Xmax]}
        Pad['top'] = {'center':[0,-(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}
        Pad['bottom'] = {'center':[0,(Zmax_y+Gmin_y)/4], 'size':[Xmax,(Zmax_y-Gmin_y)/2]}

        return Pad

    @staticmethod
    def deviceDimensions(device_size_data):
        dimensions = {
            'body_size_x': TolerancedSize.fromYaml(device_size_data, base_name='body_size_x'),
            'body_size_y': TolerancedSize.fromYaml(device_size_data, base_name='body_size_y'),
            'lead_width': TolerancedSize.fromYaml(device_size_data, base_name='lead_width'),
            'lead_len': TolerancedSize.fromYaml(device_size_data, base_name='lead_len')
        }
        dimensions['has_EP'] = False
        if 'EP_size_x_min' in device_size_data and 'EP_size_x_max' in device_size_data or 'EP_size_x' in device_size_data:
            dimensions['EP_size_x'] = TolerancedSize.fromYaml(device_size_data, base_name='EP_size_x')
            dimensions['EP_size_y'] = TolerancedSize.fromYaml(device_size_data, base_name='EP_size_y')
            dimensions['has_EP'] = True

        if 'EP_mask_x' in device_size_data:
            dimensions['EP_mask_x'] = TolerancedSize.fromYaml(device_size_data, base_name='EP_mask_x')
            dimensions['EP_mask_y'] = TolerancedSize.fromYaml(device_size_data, base_name='EP_mask_y')

        dimensions['heel_reduction'] = device_size_data.get('heel_reduction', 0)

        if 'overall_size_x' in device_size_data or 'overall_size_y' in device_size_data:
            if 'overall_size_x' in device_size_data:
                dimensions['overall_size_x'] = TolerancedSize.fromYaml(device_size_data, base_name='overall_size_x')
            else:
                dimensions['overall_size_x'] = TolerancedSize.fromYaml(device_size_data, base_name='overall_size_y')

            if 'overall_size_y' in device_size_data:
                dimensions['overall_size_y'] = TolerancedSize.fromYaml(device_size_data, base_name='overall_size_y')
            else:
                dimensions['overall_size_y'] = TolerancedSize.fromYaml(device_size_data, base_name='overall_size_x')
        else:
            raise KeyError("Either overall size x or overall size y must be given (Outside to outside lead dimensions)")

        return dimensions

    def generateFootprint(self, device_params, header):
        dimensions = Gullwing.deviceDimensions(device_params)

        if dimensions['has_EP'] and 'thermal_vias' in device_params:
            self.__createFootprintVariant(device_params, header, dimensions, True)

        self.__createFootprintVariant(device_params, header, dimensions, False)

    def __createFootprintVariant(self, device_params, header, dimensions, with_thermal_vias):
        fab_line_width = self.configuration.get('fab_line_width', 0.1)
        silk_line_width = self.configuration.get('silk_line_width', 0.12)

        lib_name = self.configuration['lib_name_format_string'].format(category=header['library_Suffix'])

        size_x = dimensions['body_size_x'].nominal
        size_y = dimensions['body_size_y'].nominal

        pincount = device_params['num_pins_x']*2 + device_params['num_pins_y']*2

        ipc_reference = 'ipc_spec_gw_large_pitch' if device_params['pitch'] >= 0.625 else 'ipc_spec_gw_small_pitch'
        if device_params.get('force_small_pitch_ipc_definition', False):
            ipc_reference = 'ipc_spec_gw_small_pitch'

        used_density = device_params.get('ipc_density', ipc_density)
        ipc_data_set = self.ipc_defintions[ipc_reference][used_density]
        ipc_round_base = self.ipc_defintions[ipc_reference]['round_base']

        pitch = device_params['pitch']

        name_format = self.configuration['fp_name_format_string_no_trailing_zero']
        EP_size = {'x':0, 'y':0}
        EP_mask_size = {'x':0, 'y':0}

        if dimensions['has_EP']:
            name_format = self.configuration['fp_name_EP_format_string_no_trailing_zero']
            if 'EP_size_x_overwrite' in device_params:
                EP_size = {
                    'x':device_params['EP_size_x_overwrite'],
                    'y':device_params['EP_size_y_overwrite']
                    }
            else:
                EP_size = {
                    'x':dimensions['EP_size_x'].nominal,
                    'y':dimensions['EP_size_y'].nominal
                    }
            if 'EP_mask_x' in dimensions:
                name_format = self.configuration['fp_name_EP_custom_mask_format_string_no_trailing_zero']
                EP_mask_size = {'x':dimensions['EP_mask_x'].nominal, 'y':dimensions['EP_mask_y'].nominal}
        EP_size = Vector2D(EP_size)

        pad_details = self.calcPadDetails(dimensions, EP_size, ipc_data_set, ipc_round_base)

        if 'custom_name_format' in device_params:
            name_format = device_params['custom_name_format']

        suffix = device_params.get('suffix', '').format(pad_x=pad_details['left']['size'][0],
            pad_y=pad_details['left']['size'][1])
        suffix_3d = suffix if device_params.get('include_suffix_in_3dpath', 'True') == 'True' else ""
        model3d_path_prefix = self.configuration.get('3d_model_prefix','${KISYS3DMOD}')

        fp_name = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=header['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_params['pitch'],
            ep_size_x = EP_size['x'],
            ep_size_y = EP_size['y'],
            mask_size_x = EP_mask_size['x'],
            mask_size_y = EP_mask_size['y'],
            suffix=suffix,
            suffix2="",
            vias=self.configuration.get('thermal_via_suffix', '_ThermalVias') if with_thermal_vias else ''
            ).replace('__','_').lstrip('_')

        fp_name_2 = name_format.format(
            man=device_params.get('manufacturer',''),
            mpn=device_params.get('part_number',''),
            pkg=header['device_type'],
            pincount=pincount,
            size_y=size_y,
            size_x=size_x,
            pitch=device_params['pitch'],
            ep_size_x = EP_size['x'],
            ep_size_y = EP_size['y'],
            mask_size_x = EP_mask_size['x'],
            mask_size_y = EP_mask_size['y'],
            suffix=suffix_3d,
            suffix2="",
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
                package = header['device_type'],
                mpn = device_params.get('part_number',''),
                pincount = pincount,
                datasheet = device_params['size_source'],
                scriptname = os.path.basename(__file__).replace("  ", " ")
                ).lstrip())

        kicad_mod.setTags(self.configuration['keyword_fp_string']\
            .format(
                man=device_params.get('manufacturer',''),
                package=header['device_type'],
                category=header['library_Suffix']
            ).lstrip())
        kicad_mod.setAttribute('smd')

        pad_radius = add_dual_or_quad_pad_border(kicad_mod, configuration, pad_details, device_params)

        EP_round_radius = 0
        if dimensions['has_EP']:
            pad_shape_details = getEpRoundRadiusParams(device_params, self.configuration, pad_radius)
            EP_mask_size = EP_mask_size if EP_mask_size['x'] > 0 else None

            if with_thermal_vias:
                thermals = device_params['thermal_vias']
                paste_coverage = thermals.get('EP_paste_coverage',
                                               device_params.get('EP_paste_coverage', DEFAULT_PASTE_COVERAGE))

                EP = ExposedPad(
                    number=pincount+1, size=EP_size, mask_size=EP_mask_size,
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
                    )
            else:
                EP = ExposedPad(
                    number=pincount+1, size=EP_size, mask_size=EP_mask_size,
                    paste_layout=device_params.get('EP_num_paste_pads', 1),
                    paste_coverage=device_params.get('EP_paste_coverage', DEFAULT_PASTE_COVERAGE),
                    **pad_shape_details
                    )

            kicad_mod.append(EP)
            EP_round_radius = EP.getRoundRadius()

        body_edge = {
            'left': -dimensions['body_size_x'].nominal/2,
            'right': dimensions['body_size_x'].nominal/2,
            'top': -dimensions['body_size_y'].nominal/2,
            'bottom': dimensions['body_size_y'].nominal/2
            }

        bounding_box = {
            'left': pad_details['left']['center'][0] - pad_details['left']['size'][0]/2,
            'right': pad_details['right']['center'][0] + pad_details['right']['size'][0]/2,
            'top': pad_details['top']['center'][1] - pad_details['top']['size'][1]/2,
            'bottom': pad_details['bottom']['center'][1] + pad_details['bottom']['size'][1]/2
        }

        if device_params['num_pins_x'] == 0:
            bounding_box['top'] = body_edge['top']
            bounding_box['bottom'] = body_edge['bottom']
            if EP_size['y'] > dimensions['body_size_y'].nominal:
                bounding_box['top'] = -EP_size['y']/2
                bounding_box['bottom'] = EP_size['y']/2

        if device_params['num_pins_y'] == 0:
            bounding_box['left'] = body_edge['left']
            bounding_box['right'] = body_edge['right']
            if EP_size['x'] > dimensions['body_size_x'].nominal:
                bounding_box['left'] = -EP_size['x']/2
                bounding_box['right'] = EP_size['x']/2


        pad_width = pad_details['top']['size'][0]

        # ############################ SilkS ##################################
        silk_pad_offset = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
        silk_offset = configuration['silk_fab_offset']

        right_pads_silk_bottom = (device_params['num_pins_y']-1)*device_params['pitch']/2\
            +pad_details['right']['size'][1]/2+silk_pad_offset
        silk_bottom = body_edge['bottom']+silk_offset
        if EP_size['y']/2 <= body_edge['bottom'] and right_pads_silk_bottom >= silk_bottom:
            silk_bottom = max(silk_bottom, EP_size['y']/2+silk_pad_offset)

        silk_bottom = max(silk_bottom, right_pads_silk_bottom)
        silk_bottom = min(body_edge['bottom']+silk_pad_offset, silk_bottom)

        bottom_pads_silk_right = (device_params['num_pins_x']-1)*device_params['pitch']/2\
            +pad_details['bottom']['size'][0]/2+silk_pad_offset
        silk_right = body_edge['right']+silk_offset
        if EP_size['x']/2 <= body_edge['right'] and bottom_pads_silk_right >= silk_right:
            silk_right = max(silk_right, EP_size['x']/2+silk_pad_offset)
        silk_right = max(silk_right, bottom_pads_silk_right)
        silk_right = min(body_edge['right']+silk_pad_offset, silk_right)


        min_lenght = configuration.get('silk_line_lenght_min', 0)
        silk_corner_bottom_right = Vector2D(silk_right, silk_bottom)

        silk_point_bottom_inside = nearestSilkPointOnOrthogonalLine(
            pad_size=EP_size,
            pad_position=[0, 0],
            pad_radius=EP_round_radius,
            fixed_point=silk_corner_bottom_right,
            moving_point=Vector2D(0, silk_bottom),
            silk_pad_offset=silk_pad_offset,
            min_lenght=min_lenght)

        if silk_point_bottom_inside is not None and device_params['num_pins_x'] > 0:
            silk_point_bottom_inside = nearestSilkPointOnOrthogonalLine(
                pad_size=pad_details['bottom']['size'],
                pad_position=[
                    pad_details['bottom']['center'][0]+(device_params['num_pins_x']-1)/2*pitch,
                    pad_details['bottom']['center'][1]],
                pad_radius=pad_radius,
                fixed_point=silk_corner_bottom_right,
                moving_point=silk_point_bottom_inside,
                silk_pad_offset=silk_pad_offset,
                min_lenght=min_lenght)

        silk_point_right_inside = nearestSilkPointOnOrthogonalLine(
            pad_size=EP_size,
            pad_position=[0, 0],
            pad_radius=EP_round_radius,
            fixed_point=silk_corner_bottom_right,
            moving_point=Vector2D(silk_right, 0),
            silk_pad_offset=silk_pad_offset,
            min_lenght=min_lenght)
        if silk_point_right_inside is not None and device_params['num_pins_y'] > 0:
            silk_point_right_inside = nearestSilkPointOnOrthogonalLine(
                pad_size=pad_details['right']['size'],
                pad_position=[
                    pad_details['right']['center'][0],
                    pad_details['right']['center'][1]+(device_params['num_pins_y']-1)/2*pitch],
                pad_radius=pad_radius,
                fixed_point=silk_corner_bottom_right,
                moving_point=silk_point_right_inside,
                silk_pad_offset=silk_pad_offset,
                min_lenght=min_lenght)

        if silk_point_bottom_inside is None and silk_point_right_inside is not None:
            silk_corner_bottom_right['y'] = body_edge['bottom']
            silk_corner_bottom_right = nearestSilkPointOnOrthogonalLine(
                pad_size=pad_details['bottom']['size'],
                pad_position=[
                    pad_details['bottom']['center'][0]+(device_params['num_pins_x']-1)/2*pitch,
                    pad_details['bottom']['center'][1]],
                pad_radius=pad_radius,
                fixed_point=silk_point_right_inside,
                moving_point=silk_corner_bottom_right,
                silk_pad_offset=silk_pad_offset,
                min_lenght=min_lenght)

        elif silk_point_right_inside is None and silk_point_bottom_inside is not None:
            silk_corner_bottom_right['x'] = body_edge['right']
            silk_corner_bottom_right = nearestSilkPointOnOrthogonalLine(
                pad_size=pad_details['right']['size'],
                pad_position=[
                    pad_details['right']['center'][0],
                    pad_details['right']['center'][1]+(device_params['num_pins_y']-1)/2*pitch],
                pad_radius=pad_radius,
                fixed_point=silk_point_bottom_inside,
                moving_point=silk_corner_bottom_right,
                silk_pad_offset=silk_pad_offset,
                min_lenght=min_lenght)

        poly_bottom_right = []
        if silk_point_bottom_inside is not None:
            poly_bottom_right.append(silk_point_bottom_inside)
        poly_bottom_right.append(silk_corner_bottom_right)
        if silk_point_right_inside is not None:
            poly_bottom_right.append(silk_point_right_inside)

        if len(poly_bottom_right) > 1 and silk_corner_bottom_right is not None:
            kicad_mod.append(PolygoneLine(
                polygone=poly_bottom_right,
                width=configuration['silk_line_width'],
                layer="F.SilkS"))
            kicad_mod.append(PolygoneLine(
                polygone=poly_bottom_right,
                width=configuration['silk_line_width'],
                layer="F.SilkS", x_mirror=0))
            kicad_mod.append(PolygoneLine(
                polygone=poly_bottom_right,
                width=configuration['silk_line_width'],
                layer="F.SilkS", y_mirror=0))

            if device_params['num_pins_y'] > 0:
                if len(poly_bottom_right)>2:
                    kicad_mod.append(PolygoneLine(
                        polygone=poly_bottom_right,
                        width=configuration['silk_line_width'],
                        layer="F.SilkS", y_mirror=0, x_mirror=0))
                    kicad_mod.append(Line(
                        start={'x': -silk_right, 'y': -right_pads_silk_bottom},
                        end={'x': bounding_box['left'], 'y': -right_pads_silk_bottom},
                        width=configuration['silk_line_width'],
                        layer="F.SilkS"))
                elif silk_corner_bottom_right['y'] >= right_pads_silk_bottom and silk_point_bottom_inside is not None:
                    kicad_mod.append(Line(
                        start=-silk_point_bottom_inside,
                        end={'x': bounding_box['left'], 'y': -silk_point_bottom_inside['y']},
                        width=configuration['silk_line_width'],
                        layer="F.SilkS"))
            else:
                if len(poly_bottom_right)>2:
                    poly_bottom_right[0]['x']=bottom_pads_silk_right
                    kicad_mod.append(PolygoneLine(
                        polygone=poly_bottom_right,
                        width=configuration['silk_line_width'],
                        layer="F.SilkS", y_mirror=0, x_mirror=0))
                    kicad_mod.append(Line(
                        start={'x': -bottom_pads_silk_right, 'y': -silk_corner_bottom_right['y']},
                        end={'x': -bottom_pads_silk_right, 'y': bounding_box['top']},
                        width=configuration['silk_line_width'],
                        layer="F.SilkS"))
                elif silk_corner_bottom_right['x'] >= bottom_pads_silk_right and silk_point_right_inside is not None:
                    kicad_mod.append(Line(
                        start=-silk_point_right_inside,
                        end={'x': -silk_point_right_inside['x'], 'y': bounding_box['top']},
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

        if device_params['num_pins_y'] == 0 or device_params['num_pins_x'] == 0:
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

        else:
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
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints. See readme.md for details about the parameter file format.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files holding information about what devices should be created.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../package_config_KLCv3.yaml')
    parser.add_argument('--density', type=str, nargs='?', help='IPC density level (L,N,M)', default='N')
    parser.add_argument('--ipc_doc', type=str, nargs='?', help='IPC definition document', default='../ipc_definitions.yaml')
    parser.add_argument('--force_rectangle_pads', action='store_true', help='Force the generation of rectangle pads instead of rounded rectangle')
    parser.add_argument('--kicad4_compatible', action='store_true', help='Create footprints compatible with version 4 (avoids round-rect and custom pads).')
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

    if args.force_rectangle_pads or args.kicad4_compatible:
        configuration['round_rect_max_radius'] = None
        configuration['round_rect_radius_ratio'] = 0

    configuration['kicad4_compatible'] = args.kicad4_compatible

    for filepath in args.files:
        gw = Gullwing(configuration)

        with open(filepath, 'r') as command_stream:
            try:
                cmd_file = yaml.safe_load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        header = cmd_file.pop('FileHeader')

        for pkg in cmd_file:
            print("generating part for parameter set {}".format(pkg))
            gw.generateFootprint(cmd_file[pkg], header)
