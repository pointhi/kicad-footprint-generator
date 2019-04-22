#!/usr/bin/env python3

'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
'''

import sys
import os
#sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
from math import sqrt
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "Micro-Fit_3.0"
series_long = 'Micro-Fit 3.0 Connector System'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 2

variant_params = {
    'solder_mounting':{
        'mount_pins': 'solder',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/430450218_sd.pdf',
        'C_minus_B': 11.2,
        'part_code': "43045-{n:02}18",
        'alternative_codes': [
            "43045-{n:02}19",
            "43045-{n:02}20"
            ]
        },
    'retention_pin':{
        'mount_pins': 'npth',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/430450217_sd.pdf',
        'C_minus_B': 4.3,
        'part_code': "43045-{n:02}15",
        'alternative_codes': [
            "43045-{n:02}16",
            "43045-{n:02}17"
            ]
        }
}

pins_per_row_range = range(1,13)
pitch = 3.0


pad_size = [1.27, 2.54]
pitch_y = 6.86 + pad_size[1]

mount_pad_size = [3.43, 1.65]
mount_drill = 2.41

def generate_one_footprint(pins_per_row, variant, configuration):
    is_solder_mp = variant_params[variant]['mount_pins'] == 'solder'

    mpn = variant_params[variant]['part_code'].format(n=pins_per_row*2)
    alt_mpn = [code.format(n=pins_per_row*2) for code in variant_params[variant]['alternative_codes']]

    # handle arguments
    mp_name = ""
    if is_solder_mp:
        mp_name = "-1MP"
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = mp_name,
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s} (compatible alternatives: {:s}), {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, ', '.join(alt_mpn), pins_per_row, variant_params[variant]['datasheet']))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    kicad_mod.setAttribute('smd')

    ########################## Dimensions ##############################
    B = (pins_per_row-1)*pitch
    A = B + 6.65
    C = B + variant_params[variant]['C_minus_B']

    pad_row_1_y = -pitch_y/2
    pad_row_2_y = pad_row_1_y + pitch_y
    pad1_x = -B/2

    mount_pad_x = C/2 - (mount_pad_size[0]/2 if is_solder_mp else 0)
    mount_pad_y = pad_row_1_y + pitch_y/2

    tab_w = 1.4
    tab_l = 1.4

    body_edge={
        'left': -A/2,
        'right': A/2,
        'bottom': 3.43
        }
    body_edge['top'] = body_edge['bottom'] - 6.87

    chamfer={'x': 1.2, 'y': 0.63}
    y_top_min = body_edge['bottom'] - 7.37

    bounding_box={
        'left': -C/2 if is_solder_mp else body_edge['left'],
        'right': C/2 if is_solder_mp else body_edge['right'],
        'top': pad_row_1_y - pad_size[1]/2,
        'bottom': pad_row_2_y + pad_size[1]/2
    }

    ############################# Pads ##################################
    if is_solder_mp:
        #
        # Add solder nails
        #
        kicad_mod.append(Pad(at=[-mount_pad_x, mount_pad_y], number=configuration['mounting_pad_number'],
            type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=mount_pad_size,
            layers=Pad.LAYERS_SMT))
        kicad_mod.append(Pad(at=[mount_pad_x, mount_pad_y], number=configuration['mounting_pad_number'],
            type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=mount_pad_size,
            layers=Pad.LAYERS_SMT))
    else:
        kicad_mod.append(Pad(at=[-mount_pad_x, mount_pad_y], number="",
            type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=mount_drill,
            drill=mount_drill, layers=Pad.LAYERS_NPTH))
        kicad_mod.append(Pad(at=[mount_pad_x, mount_pad_y], number="",
            type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=mount_drill,
            drill=mount_drill, layers=Pad.LAYERS_NPTH))

    #
    # Add pads
    #
    kicad_mod.append(PadArray(start=[pad1_x, pad_row_1_y], initial=1,
        pincount=pins_per_row, increment=1,  x_spacing=pitch, size=pad_size,
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))
    kicad_mod.append(PadArray(start=[pad1_x, pad_row_2_y], initial=pins_per_row+1,
        pincount=pins_per_row, increment=1, x_spacing=pitch, size=pad_size,
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))


    ######################## Fabrication Layer ###########################
    main_body_poly= [
        {'x': body_edge['left'] + chamfer['x'], 'y': body_edge['top']},
        {'x': body_edge['left'] + chamfer['x'], 'y': y_top_min},
        {'x': body_edge['left'], 'y': y_top_min},
        {'x': body_edge['left'], 'y': body_edge['bottom']},
        {'x': body_edge['right'], 'y': body_edge['bottom']},
        {'x': body_edge['right'], 'y': y_top_min},
        {'x': body_edge['right'] - chamfer['x'], 'y': y_top_min},
        {'x': body_edge['right'] - chamfer['x'], 'y': body_edge['top']},
        {'x': body_edge['left'] + chamfer['x'], 'y': body_edge['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=main_body_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    kicad_mod.append(Line(
        start={
            'x': body_edge['left'],
            'y': body_edge['top'] + chamfer['y']
        },
        end={
            'x': body_edge['left'] + chamfer['x'],
            'y': body_edge['top']
        },
        width=configuration['fab_line_width'], layer="F.Fab"
        ))

    kicad_mod.append(Line(
        start={
            'x': body_edge['right'],
            'y': body_edge['top'] + chamfer['y']
        },
        end={
            'x': body_edge['right'] - chamfer['x'],
            'y': body_edge['top']
        },
        width=configuration['fab_line_width'], layer="F.Fab"
        ))


    tab_poly = [
        {'x': -tab_l/2, 'y': body_edge['bottom']},
        {'x': -tab_l/2, 'y': body_edge['bottom'] + tab_w},
        {'x': tab_l/2, 'y': body_edge['bottom'] + tab_w},
        {'x': tab_l/2, 'y': body_edge['bottom']},
    ]
    kicad_mod.append(PolygoneLine(polygone=tab_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    p1m_sl = 1
    p1m_poly = tab_poly = [
        {'x': pad1_x - p1m_sl/2, 'y': body_edge['top']},
        {'x': pad1_x, 'y': body_edge['top'] + p1m_sl/sqrt(2)},
        {'x': pad1_x + p1m_sl/2, 'y': body_edge['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=tab_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    ############################ SilkS ##################################
    # Top left corner

    silk_pad_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    xp1_left = pad1_x - pad_size[0]/2 - silk_pad_off
    ymp_top = mount_pad_y - mount_pad_size[1]/2 - silk_pad_off
    ymp_bottom = mount_pad_y + mount_pad_size[1]/2 + silk_pad_off
    xpn_right = pad1_x + B + pad_size[0]/2 + silk_pad_off
    off = configuration['silk_fab_offset']

    poly_s_bl = [
        {'x': body_edge['left'] - off, 'y': ymp_bottom},
        {'x': body_edge['left'] - off, 'y': body_edge['bottom'] + off},
        {'x': xp1_left, 'y': body_edge['bottom'] + off}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_s_bl,
        width=configuration['silk_line_width'], layer="F.SilkS"))

    poly_s_br = [
        {'x': body_edge['right'] + off, 'y': ymp_bottom},
        {'x': body_edge['right'] + off, 'y': body_edge['bottom'] + off},
        {'x': xpn_right, 'y': body_edge['bottom'] + off}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_s_br,
        width=configuration['silk_line_width'], layer="F.SilkS"))

    poly_s_tl = [
        {'x': body_edge['left'] - off, 'y': ymp_top},
        {'x': body_edge['left'] - off, 'y': y_top_min - off},
        {'x': body_edge['left'] + chamfer['x'] + off, 'y': y_top_min - off},
        {'x': body_edge['left'] + chamfer['x'] + off, 'y': body_edge['top'] - off},
        {'x': xp1_left, 'y': body_edge['top'] - off},
        {'x': xp1_left, 'y': bounding_box['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_s_tl,
        width=configuration['silk_line_width'], layer="F.SilkS"))

    poly_s_br = [
        {'x': body_edge['right'] + off, 'y': ymp_top},
        {'x': body_edge['right'] + off, 'y': y_top_min - off},
        {'x': body_edge['right'] - chamfer['x'] - off, 'y': y_top_min - off},
        {'x': body_edge['right'] - chamfer['x'] - off, 'y': body_edge['top'] - off},
        {'x': xpn_right, 'y': body_edge['top'] - off}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_s_br,
        width=configuration['silk_line_width'], layer="F.SilkS"))

    ############################ CrtYd ##################################
    CrtYd_offset = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']

    cy_top = roundToBase(bounding_box['top'] - CrtYd_offset, CrtYd_grid)
    cy_body_top = roundToBase(y_top_min - CrtYd_offset, CrtYd_grid)
    cy_mp_top = roundToBase(mount_pad_y - mount_pad_size[1]/2 - CrtYd_offset, CrtYd_grid)
    cy_mp_bottom = roundToBase(mount_pad_y + mount_pad_size[1]/2 + CrtYd_offset, CrtYd_grid)
    cy_body_bottom = roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)
    cy_bottom = roundToBase(bounding_box['bottom'] + CrtYd_offset, CrtYd_grid)

    cy_left = roundToBase(bounding_box['left'] - CrtYd_offset, CrtYd_grid)
    cy_body_left = roundToBase(body_edge['left'] - CrtYd_offset, CrtYd_grid)
    cy_pad_left = roundToBase(pad1_x - pad_size[0]/2 - CrtYd_offset, CrtYd_grid)
    cy_pad_right = roundToBase(pad1_x + B + pad_size[0]/2 + CrtYd_offset, CrtYd_grid)
    cy_body_right = roundToBase(body_edge['right'] + CrtYd_offset, CrtYd_grid)
    cy_right = roundToBase(bounding_box['right'] + CrtYd_offset, CrtYd_grid)

    CrtYd_poly_t = [
        {'x': pad1_x + B/2, 'y':cy_top},
        {'x': cy_pad_left, 'y':cy_top},
        {'x': cy_pad_left, 'y':cy_body_top},
        {'x': cy_body_left, 'y':cy_body_top}
        ]
    CrtYd_poly_m = [
        {'x': cy_body_left, 'y':cy_mp_top},
        {'x': cy_left, 'y':cy_mp_top},
        {'x': cy_left, 'y':cy_mp_bottom},
        {'x': cy_body_left, 'y':cy_mp_bottom}
        ]
    CrtYd_poly_b = [
        {'x': cy_body_left, 'y':cy_body_bottom},
        {'x': cy_pad_left, 'y':cy_body_bottom},
        {'x': cy_pad_left, 'y':cy_bottom},
        {'x': pad1_x+B/2, 'y':cy_bottom}
    ]
    CrtYd_poly = CrtYd_poly_t
    if is_solder_mp:
        CrtYd_poly.extend(CrtYd_poly_m)
    CrtYd_poly.extend(CrtYd_poly_b)

    kicad_mod.append(PolygoneLine(polygone=CrtYd_poly,
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    kicad_mod.append(PolygoneLine(polygone=CrtYd_poly,
        layer='F.CrtYd', width=configuration['courtyard_line_width'],
        x_mirror= 0.00000001 if pad1_x+B/2 == 0 else pad1_x+B/2))
    ######################### Text Fields ###############################


    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy_top, 'bottom':cy_bottom}, fp_name=footprint_name, text_y_inside_position='bottom')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../conn_config_KLCv3.yaml')
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
    for variant in variant_params:
        for pins_per_row in pins_per_row_range:
            generate_one_footprint(pins_per_row, variant, configuration)
