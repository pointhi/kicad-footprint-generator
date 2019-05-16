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
from ipc_pad_size_calculators import *

def create_footprint(name, configuration, **kwargs):
    kicad_mod = Footprint(name)

    # init kicad footprint
    datasheet = ", " + kwargs['datasheet'] if 'datasheet' in kwargs else ""
    description = "SMD capacitor, aluminum electrolytic"
    tags = 'capacitor electrolytic'
    if name[:2] == "C_":
        description += " nonpolar"
        tags += " nonpolar"
    if 'extra_description' in kwargs:
        description += ", " + kwargs['extra_description']

    # ensure all provided dimensions are fully toleranced
    device_dimensions = {
        'body_length': TolerancedSize.fromYaml(kwargs, base_name='body_length'),
        'body_width': TolerancedSize.fromYaml(kwargs, base_name='body_width'),
        'body_height': TolerancedSize.fromYaml(kwargs, base_name='body_height'),
        'body_diameter': TolerancedSize.fromYaml(kwargs, base_name='body_diameter')
    }
    
    # for ease of use, capture nominal body and pad sizes
    body_size = {
        'length': device_dimensions['body_length'].nominal,
        'width': device_dimensions['body_width'].nominal,
        'height': device_dimensions['body_height'].nominal,
        'diameter': device_dimensions['body_diameter'].nominal
    }

    description += ", " + str(body_size['diameter']) + "x" + str(body_size['height']) + "mm"
    kicad_mod.setDescription(description + datasheet)
    kicad_mod.setTags(tags)
    kicad_mod.setAttribute('smd')

    # set general values
    text_offset_y = body_size['width'] / 2.0 + configuration['courtyard_offset']['default'] + 0.8

    #silkscreen REF**
    silk_text_size = configuration['references'][0]['size']
    silk_text_thickness = silk_text_size[0]*configuration['references'][0]['fontwidth']
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, -text_offset_y], layer='F.SilkS', size=[silk_text_size[0], silk_text_size[1]], thickness= silk_text_thickness))
    #fab value
    fab_text_size = configuration['values'][0]['size']
    fab_text_thickness = fab_text_size[0]*configuration['values'][0]['fontwidth']
    kicad_mod.append(Text(type='value', text=name, at=[0, text_offset_y], layer='F.Fab', size=[fab_text_size[0], fab_text_size[1]], thickness= fab_text_thickness))
    #fab REF**
    fab_text_size = body_size['diameter']/5.0
    fab_text_size = min(fab_text_size, configuration['references'][1]['size_max'][0])
    fab_text_size = max(fab_text_size, configuration['references'][1]['size_min'][0])
    fab_text_thickness = fab_text_size*configuration['references'][1]['thickness_factor']
    kicad_mod.append(Text(type='user', text='%R', at=[0, 0], layer='F.Fab', size=[fab_text_size, fab_text_size], thickness= fab_text_thickness))

    # create pads
    # all pads have these properties
    pad_params = {'type': Pad.TYPE_SMT, 'layers': Pad.LAYERS_SMT, 'shape': Pad.SHAPE_RECT}
    
    # prefer IPC-7351C compliant rounded rectangle pads
    if not configuration['force_rectangle_pads']:
        pad_params['shape'] = Pad.SHAPE_ROUNDRECT
        pad_params['radius_ratio'] = 0.25
        pad_params['maximum_radius'] = 0.25

    # prefer calculating pads from lead dimensions per IPC
    # fall back to using pad sizes directly if necessary
    if ('lead_length' in kwargs) and ('lead_width' in kwargs) and ('lead_spacing' in kwargs):
        # gather IPC data (unique parameters for >= 10mm tall caps)
        ipc_density_suffix = '' if body_size['height'] < 10 else '_10mm'
        ipc_density = configuration['ipc_density']
        ipc_data = ipc_defintions['ipc_spec_capae_crystal'][ipc_density + ipc_density_suffix]
        ipc_round_base = ipc_defintions['ipc_spec_capae_crystal']['round_base']
        
        manf_tol = {
            'F': configuration.get('manufacturing_tolerance', 0.1),
            'P': configuration.get('placement_tolerance', 0.05)
        }
        
        # # fully tolerance lead dimensions; leads are dimensioned like SOIC so use gullwing calculator
        device_dimensions['lead_width'] = TolerancedSize.fromYaml(kwargs, base_name='lead_width')
        device_dimensions['lead_spacing'] = TolerancedSize.fromYaml(kwargs, base_name='lead_spacing')
        device_dimensions['lead_length'] = TolerancedSize.fromYaml(kwargs, base_name='lead_length')
        device_dimensions['lead_outside'] = TolerancedSize(maximum =
            device_dimensions['lead_spacing'].maximum +
            device_dimensions.get('lead_length').maximum * 2,
            minimum = device_dimensions['lead_spacing'].minimum +
            device_dimensions.get('lead_length').minimum * 2)
        
        Gmin, Zmax, Xmax = ipc_gull_wing(ipc_data, ipc_round_base, manf_tol,
                device_dimensions['lead_width'], device_dimensions['lead_outside'],
                lead_len=device_dimensions.get('lead_length'))
        
        pad_params['size'] = [(Zmax - Gmin) / 2.0, Xmax]

        x_pad_spacing = (Zmax + Gmin) / 4.0
    elif ('pad_length' in kwargs) and ('pad_width' in kwargs) and ('pad_spacing' in kwargs):
        x_pad_spacing = kwargs['pad_spacing'] / 2.0 + kwargs['pad_length'] / 2.0
        pad_params['size'] = [kwargs['pad_length'], kwargs['pad_width']]
    else:
        raise KeyError("Provide all three 'pad' or 'lead' properties ('_spacing', '_length', and '_width')")

    kicad_mod.append(Pad(number=1, at=[-x_pad_spacing, 0], **pad_params))
    kicad_mod.append(Pad(number=2, at=[x_pad_spacing, 0], **pad_params))
    
    # create fabrication layer
    fab_x = body_size['length'] / 2.0
    fab_y = body_size['width'] / 2.0

    if kwargs['pin1_chamfer'] == 'auto':
        fab_edge = min(fab_x/2.0, fab_y/2.0, configuration['fab_pin1_marker_length'])
    else:
        fab_edge = kwargs['pin1_chamfer']
    fab_x_edge = fab_x - fab_edge
    fab_y_edge = fab_y - fab_edge
    kicad_mod.append(Line(start=[fab_x, -fab_y], end=[fab_x, fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[-fab_x_edge, -fab_y], end=[fab_x, -fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[-fab_x_edge, fab_y], end=[fab_x, fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    if fab_edge > 0:
        kicad_mod.append(Line(start=[-fab_x, -fab_y_edge], end=[-fab_x, fab_y_edge], layer='F.Fab', width=configuration['fab_line_width']))
        kicad_mod.append(Line(start=[-fab_x, -fab_y_edge], end=[-fab_x_edge, -fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[-fab_x, fab_y_edge], end=[-fab_x_edge, fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Circle(center=[0, 0], radius=body_size['diameter']/2.0, layer='F.Fab', width=configuration['fab_line_width']))


    #fab polarity marker for polarized caps
    if name[:2].upper() == "CP":
        fab_pol_size = body_size['diameter']/10.0
        fab_pol_wing = fab_pol_size/2.0
        fab_pol_distance = body_size['diameter']/2.0 - fab_pol_wing - configuration['fab_line_width']
        fab_pol_pos_y = fab_text_size/2.0 + configuration['silk_pad_clearance'] + fab_pol_size
        fab_pol_pos_x = math.sqrt(fab_pol_distance*fab_pol_distance-fab_pol_pos_y*fab_pol_pos_y)
        fab_pol_pos_x = -fab_pol_pos_x
        fab_pol_pos_y = -fab_pol_pos_y
        kicad_mod.append(Line(start=[fab_pol_pos_x-fab_pol_wing, fab_pol_pos_y], end=[fab_pol_pos_x+fab_pol_wing, fab_pol_pos_y], 
            layer='F.Fab', width=configuration['fab_line_width']))
        kicad_mod.append(Line(start=[fab_pol_pos_x, fab_pol_pos_y-fab_pol_wing], end=[fab_pol_pos_x, fab_pol_pos_y+fab_pol_wing], 
            layer='F.Fab', width=configuration['fab_line_width']))


    # create silkscreen
    fab_to_silk_offset = configuration['silk_fab_offset']
    silk_x = body_size['length'] / 2.0 + fab_to_silk_offset
    silk_y = body_size['width'] / 2.0 + fab_to_silk_offset
    silk_y_start = pad_params['size'][1] / 2.0 + configuration['silk_pad_clearance'] + configuration['silk_line_width']/2.0
    silk_45deg_offset = fab_to_silk_offset*math.tan(math.radians(22.5))
    silk_x_edge = fab_x - fab_edge + silk_45deg_offset
    silk_y_edge = fab_y - fab_edge + silk_45deg_offset

    kicad_mod.append(Line(start=[silk_x, silk_y], end=[silk_x, silk_y_start], layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[silk_x, -silk_y], end=[silk_x, -silk_y_start], layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[-silk_x_edge, -silk_y], end=[silk_x, -silk_y], layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[-silk_x_edge, silk_y], end=[silk_x, silk_y], layer='F.SilkS', width=configuration['silk_line_width']))

    if silk_y_edge > silk_y_start:
        kicad_mod.append(Line(start=[-silk_x, silk_y_edge], end=[-silk_x, silk_y_start], layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[-silk_x, -silk_y_edge], end=[-silk_x, -silk_y_start], layer='F.SilkS', width=configuration['silk_line_width']))

        kicad_mod.append(Line(start=[-silk_x, -silk_y_edge], end=[-silk_x_edge, -silk_y], layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[-silk_x, silk_y_edge], end=[-silk_x_edge, silk_y], layer='F.SilkS', width=configuration['silk_line_width']))
    else:
        silk_x_cut = silk_x - (silk_y_start - silk_y_edge) # because of the 45 degree edge we can user a simple apporach
        silk_y_edge_cut = silk_y_start

        kicad_mod.append(Line(start=[-silk_x_cut, -silk_y_edge_cut], end=[-silk_x_edge, -silk_y], layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[-silk_x_cut, silk_y_edge_cut], end=[-silk_x_edge, silk_y], layer='F.SilkS', width=configuration['silk_line_width']))

    #silk polarity marker
    if name[:2].upper() == "CP":
        silk_pol_size = body_size['diameter']/8.0
        silk_pol_wing = silk_pol_size/2.0
        silk_pol_pos_y = silk_y_start + silk_pol_size
        silk_pol_pos_x = silk_x + silk_pol_wing + configuration['silk_line_width']*2
        silk_pol_pos_x = -silk_pol_pos_x
        silk_pol_pos_y = -silk_pol_pos_y
        kicad_mod.append(Line(start=[silk_pol_pos_x-silk_pol_wing, silk_pol_pos_y], end=[silk_pol_pos_x+silk_pol_wing, silk_pol_pos_y], 
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[silk_pol_pos_x, silk_pol_pos_y-silk_pol_wing], end=[silk_pol_pos_x, silk_pol_pos_y+silk_pol_wing], 
            layer='F.SilkS', width=configuration['silk_line_width']))

    # create courtyard
    courtyard_offset = configuration['courtyard_offset']['default']
    courtyard_x = body_size['length'] / 2.0 + courtyard_offset
    courtyard_y = body_size['width'] / 2.0 + courtyard_offset
    courtyard_pad_x = x_pad_spacing + pad_params['size'][0] / 2.0 + courtyard_offset
    courtyard_pad_y = pad_params['size'][1] / 2.0 + courtyard_offset
    courtyard_45deg_offset = courtyard_offset*math.tan(math.radians(22.5))
    courtyard_x_edge = fab_x - fab_edge + courtyard_45deg_offset
    courtyard_y_edge = fab_y - fab_edge + courtyard_45deg_offset
    courtyard_x_lower_edge = courtyard_x
    if courtyard_y_edge < courtyard_pad_y:
        courtyard_x_lower_edge = courtyard_x_lower_edge - courtyard_pad_y + courtyard_y_edge
        courtyard_y_edge = courtyard_pad_y
    #rounding
    courtyard_x = float(format(courtyard_x, ".2f"))
    courtyard_y = float(format(courtyard_y, ".2f"))
    courtyard_pad_x = float(format(courtyard_pad_x, ".2f"))
    courtyard_pad_y = float(format(courtyard_pad_y, ".2f"))
    courtyard_x_edge = float(format(courtyard_x_edge, ".2f"))
    courtyard_y_edge = float(format(courtyard_y_edge, ".2f"))
    courtyard_x_lower_edge = float(format(courtyard_x_lower_edge, ".2f"))

    # drawing courtyard
    kicad_mod.append(Line(start=[courtyard_x, -courtyard_y], end=[courtyard_x, -courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[courtyard_x, -courtyard_pad_y], end=[courtyard_pad_x, -courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[courtyard_pad_x, -courtyard_pad_y], end=[courtyard_pad_x, courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[courtyard_pad_x, courtyard_pad_y], end=[courtyard_x, courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[courtyard_x, courtyard_pad_y], end=[courtyard_x, courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))

    kicad_mod.append(Line(start=[-courtyard_x_edge, courtyard_y], end=[courtyard_x, courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[-courtyard_x_edge, -courtyard_y], end=[courtyard_x, -courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    if fab_edge > 0:
        kicad_mod.append(Line(start=[-courtyard_x_lower_edge, courtyard_y_edge], end=[-courtyard_x_edge, courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
        kicad_mod.append(Line(start=[-courtyard_x_lower_edge, -courtyard_y_edge], end=[-courtyard_x_edge, -courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    if courtyard_y_edge > courtyard_pad_y:
        kicad_mod.append(Line(start=[-courtyard_x, -courtyard_y_edge], end=[-courtyard_x, -courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
        kicad_mod.append(Line(start=[-courtyard_x, courtyard_pad_y], end=[-courtyard_x, courtyard_y_edge], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[-courtyard_x_lower_edge, -courtyard_pad_y], end=[-courtyard_pad_x, -courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[-courtyard_pad_x, -courtyard_pad_y], end=[-courtyard_pad_x, courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[-courtyard_pad_x, courtyard_pad_y], end=[-courtyard_x_lower_edge, courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))

    lib_name ='Capacitor_SMD'
    # add model
    modelname = name.replace("_HandSoldering", "")
    kicad_mod.append(Model(filename="{model_prefix:s}{lib_name:s}.3dshapes/{name:s}.wrl".format(model_prefix=configuration['3d_model_prefix'], lib_name=lib_name, name=modelname),
                            at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    # write file
    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)

    filename = '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=name)
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse *.kicad_mod.yml file(s) and create matching footprints')
    parser.add_argument('files', metavar='file', type=str, nargs='+', help='yml-files to parse')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../SMD_chip_package_rlc-etc/config_KLCv3.0.yaml')
    parser.add_argument('--ipc_definition', type=str, nargs='?', help='the IPC definition file', default='ipc7351B_capae_crystal.yaml')
    parser.add_argument('--ipc_density', type=str, nargs='?', help='the IPC desnity', default='nominal')
    parser.add_argument('--force_rectangle_pads', action='store_true', help='Force the generation of rectangle pads instead of rounded rectangle (KiCad 4.x compatibility.)')
    #parser.add_argument('-v', '--verbose', help='show more information when creating footprint', action='store_true')
    # TODO: allow writing into sub file
    
    args = parser.parse_args()
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
    
    ipc_doc = args.ipc_definition
    with open(ipc_doc, 'r') as ipc_stream:
        try:
            ipc_defintions = yaml.safe_load(ipc_stream)
        except yaml.YAMLError as exc:
            print(exc)

    configuration['ipc_density'] = args.ipc_density
    configuration['force_rectangle_pads'] = args.force_rectangle_pads
    
    for filepath in args.files:
        with open(filepath, 'r') as stream:
            try:
                yaml_parsed = yaml.safe_load(stream)
                for footprint in yaml_parsed:
                    print("generate {name}.kicad_mod".format(name=footprint))
                    create_footprint(footprint, configuration , **yaml_parsed.get(footprint))
            except yaml.YAMLError as exc:
                print(exc)
