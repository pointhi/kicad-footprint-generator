import sys
import os
import argparse
import yaml
import math

from copy import deepcopy

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))
from KicadModTree import *  # NOQA
from KicadModTree.util.geometric_util import geometricLine, geometricCircle
from KicadModTree.util.paramUtil import round_to

 # load parent path of tools
sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))
from footprint_text_fields import addTextFields

DEFAULT_MIN_PAD_DRILL_INC = 0.2
DEFAULT_PAD_DRILL_INC_FACTOR = 1.25
DEFAULT_RELIEF_DRILL_INC = 0.5

FOOTPRINT_TYPES = {
    'plain':{
        'name': '',
        'description': '',
        'tag': '',
        'relief_count': 0
    },
    'relief':{
        'name': '_Relief',
        'description': ' with feed through strain relief',
        'tag': ' strain-relief',
        'relief_count': 1
    },
    'relief2x':{
        'name': '_Relief2x',
        'description': ' with double feed through strain relief',
        'tag': ' double-strain-relief',
        'relief_count': 2
    }
}

def bend_radius(wire_def):
    return wire_def['outer_diameter'] * 3

def fp_name_gen(wire_def, fp_type, pincount, pitch):
    if 'area' in wire_def:
        size_code = '{:g}sqmm'.format(wire_def['area'])

    return 'SolderWire-{}_1x{:02d}{}_D{:g}mm_OD{:g}mm{}'.format(
                    size_code, pincount,
                    '' if pincount == 1 else '_P{:g}mm'.format(pitch),
                    wire_def['diameter'], wire_def['outer_diameter'], fp_type
                )

def description_gen(wire_def, fp_type, pincount, pitch):
    if 'area' in wire_def:
        size_code = '{:g} mm²'.format(wire_def['area'])

    d1 = 'for a single {size:s} wire' if pincount == 1 else 'for {count:d} times {size:s} wires'

    return (
        'Soldered wire connection{}, {}, '
        '{} insulation, '
        'conductor diameter {:g}mm, outer diameter {:g}mm, '
        'size source {}, '
        'bend radius 3 times outer diameter, '
        'generated with kicad-footprint-generator'
        .format(
                fp_type, d1.format(count=pincount, size=size_code),
                wire_def['insulation'],
                wire_def['diameter'], wire_def['outer_diameter'],
                wire_def['source']
            )
    )

def tag_gen(wire_def, fp_type, pincount, pitch):
    if 'area' in wire_def:
        size_code = '{:g}sqmm'.format(wire_def['area'])

    return 'connector wire {}{}'.format(size_code, fp_type)

def make_fp(wire_def, fp_type, pincount, configuration):
    crtyd_off= configuration['courtyard_offset']['connector']
    silk_pad_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    pad_drill = max(wire_def['diameter'] + configuration['min_pad_drill_inc'],
                    wire_def['diameter'] * configuration['pad_drill_factor'])
    pad_drill = round_to(pad_drill, 0.05)
    pad_size = max(pad_drill + 1, wire_def['outer_diameter'])

    npth_drill = wire_def['outer_diameter'] + configuration['relief_drill_inc']
    npth_drill = round_to(npth_drill, 0.05)
    npth_offset = bend_radius(wire_def)*2

    pitch = max(2*wire_def['outer_diameter'], pad_size+2, npth_drill+2)

    fp_name = fp_name_gen(wire_def, fp_type['name'], pincount, pitch)

    kicad_mod = Footprint(fp_name)
    kicad_mod.setDescription(description_gen(wire_def, fp_type['description'], pincount, pitch))

    kicad_mod.setTags(tag_gen(wire_def, fp_type['tag'], pincount, pitch))

    kicad_mod.setAttribute('virtual')

    prototype = Translation(0, 0)
    kicad_mod.append(PadArray(
            initial=1, increment=1, pincount=pincount,
            type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
            start=(0, 0), spacing=(pitch, 0),
            drill=pad_drill, size=pad_size,
            radius_ratio=0.25, maximum_radius=0.25,
            layers=Pad.LAYERS_THT
        ))

    for i in range(fp_type['relief_count']):
        prototype.append(Pad(
                number='', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                at=(0, (i+1)*npth_offset), drill=npth_drill, size=npth_drill,
                layers=Pad.LAYERS_NPTH
            ))

    ######################### Fab Graphic ###############################
    for i in range(fp_type['relief_count']+1):
        prototype.append(Circle(
                center=(0, i*npth_offset), radius=wire_def['outer_diameter']/2,
                layer='F.Fab', width=configuration['fab_line_width']
            ))

    # wire on top side
    if fp_type['relief_count']>0:
        for i in range((fp_type['relief_count']+1)//2):
            sy = 2*i * npth_offset
            ey = (2*i+1) * npth_offset
            prototype.append(Line(
                    start=(-wire_def['outer_diameter']/2, sy),
                    end=(-wire_def['outer_diameter']/2, ey),
                    layer='F.Fab', width=configuration['fab_line_width']
                ))
            prototype.append(Line(
                    start=(wire_def['outer_diameter']/2, sy),
                    end=(wire_def['outer_diameter']/2, ey),
                    layer='F.Fab', width=configuration['fab_line_width']
                ))

    if fp_type['relief_count']>1:
        for i in range(fp_type['relief_count']):
            prototype.append(Circle(
                    center=(0, (i+1)*npth_offset), radius=wire_def['outer_diameter']/2,
                    layer='B.Fab', width=configuration['fab_line_width']
                ))
        for i in range((fp_type['relief_count'])//2):
            sy = (2*i+1) * npth_offset
            ey = (2*i+2) * npth_offset
            prototype.append(Line(
                    start=(-wire_def['outer_diameter']/2, sy),
                    end=(-wire_def['outer_diameter']/2, ey),
                    layer='B.Fab', width=configuration['fab_line_width']
                ))
            prototype.append(Line(
                    start=(wire_def['outer_diameter']/2, sy),
                    end=(wire_def['outer_diameter']/2, ey),
                    layer='B.Fab', width=configuration['fab_line_width']
                ))

    ######################### Silk Graphic ##############################

    silk_x = wire_def['outer_diameter']/2 + configuration['silk_fab_offset']

    silk_helper_line = geometricLine(start=(silk_x, 0), end=(silk_x, npth_offset))\
        .cut(geometricCircle(center=(0,0), radius=(npth_drill/2 + silk_pad_off)))[1]

    silk_y_rel_npth = silk_helper_line.start_pos['x']

    if fp_type['relief_count']>0:
        if silk_x > pad_size/2 + silk_pad_off:
            top = 0
        else:
            top = pad_size/2 + silk_pad_off

        bottom = npth_offset - silk_y_rel_npth
        prototype.append(Line(
                start=(silk_x, top), end=(silk_x, bottom),
                layer='F.SilkS', width=configuration['silk_line_width']
            ))
        prototype.append(Line(
                start=(-silk_x, top), end=(-silk_x, bottom),
                layer='F.SilkS', width=configuration['silk_line_width']
            ))

    if fp_type['relief_count']>1:
        for i in range(fp_type['relief_count']-1):
            layer = 'F.SilkS' if i%2 == 1 else 'B.SilkS'

            top = (i+1)*npth_offset + silk_y_rel_npth
            bottom = (i+2)*npth_offset - silk_y_rel_npth

            prototype.append(Line(
                    start=(silk_x, top), end=(silk_x, bottom),
                    layer=layer, width=configuration['silk_line_width']
                ))
            prototype.append(Line(
                    start=(-silk_x, top), end=(-silk_x, bottom),
                    layer=layer, width=configuration['silk_line_width']
                ))

    ########################## Courtyard ################################

    crtyd_x = max(pad_size, npth_drill)/2 + crtyd_off
    crtyd_top = -max(pad_size, wire_def['outer_diameter'])/2 - crtyd_off
    crtyd_top_main = crtyd_top
    if fp_type['relief_count'] == 0:
        crtyd_bottom = -crtyd_top
        crtyd_bottom_main = crtyd_bottom
    else:
        crtyd_bottom = npth_offset + npth_drill/2 + crtyd_off
        crtyd_bottom_main = npth_offset*fp_type['relief_count'] + npth_drill/2 + crtyd_off

    layer = 'F.CrtYd'
    prototype.append(RectLine(
            start=Vector2D(-crtyd_x, crtyd_top).round_to(configuration['courtyard_grid']),
            end=Vector2D(crtyd_x, crtyd_bottom).round_to(configuration['courtyard_grid']),
            layer=layer, width=configuration['courtyard_line_width']
        ))

    if fp_type['relief_count']>0:
        i = fp_type['relief_count']
        layer = 'B.CrtYd' if i%2 == 1 else 'F.CrtYd'

        crtyd_top = (i)*npth_offset - (npth_drill/2 + crtyd_off)
        crtyd_bottom = (i)*npth_offset + npth_drill/2 + crtyd_off

        prototype.append(RectLine(
                start=Vector2D(-crtyd_x, crtyd_top).round_to(configuration['courtyard_grid']),
                end=Vector2D(crtyd_x, crtyd_bottom).round_to(configuration['courtyard_grid']),
                layer=layer, width=configuration['courtyard_line_width']
            ))

    if fp_type['relief_count']>1:
        for i in range(fp_type['relief_count']-1):
            layer = 'F.CrtYd' if i%2 == 1 else 'B.CrtYd'

            crtyd_top = (i+1)*npth_offset - (npth_drill/2 + crtyd_off)
            crtyd_bottom = (i+2)*npth_offset + npth_drill/2 + crtyd_off

            prototype.append(RectLine(
                    start=Vector2D(-crtyd_x, crtyd_top).round_to(configuration['courtyard_grid']),
                    end=Vector2D(crtyd_x, crtyd_bottom).round_to(configuration['courtyard_grid']),
                    layer=layer, width=configuration['courtyard_line_width']
                ))


    ######################### Text Fields ###############################
    center_x = (pincount-1)*pitch/2

    y1 = -wire_def['outer_diameter']/2
    y2 = wire_def['outer_diameter']/2 + (npth_offset if fp_type['relief_count'] > 0 else 0)

    if pincount%2 == 0 and fp_type['relief_count'] == 0:
        y1 = crtyd_top_main
        y2 = crtyd_bottom_main

    addTextFields(
        kicad_mod=kicad_mod, configuration=configuration,
        body_edges={
            'left':center_x - wire_def['outer_diameter']/2,
            'right':center_x + wire_def['outer_diameter']/2,
            'top':y1,
            'bottom':y2
            },
        courtyard={'top':crtyd_top_main, 'bottom':crtyd_bottom_main},
        fp_name=fp_name, text_y_inside_position='center',
        allow_rotation=True
        )

    ##################### Output and 3d model ############################
    for i in range(pincount):
        prototype.offset_x = i*pitch
        kicad_mod.append(deepcopy(prototype))

    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = 'Connector_Wire'
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=fp_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir):
        #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)

    filename = '{outdir:s}{fp_name:s}.kicad_mod'\
            .format(outdir=output_dir, fp_name=fp_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

def make_for_wire(wire_def, configuration):
    for fp_type in FOOTPRINT_TYPES:
        for i in range(6):
            make_fp(wire_def, FOOTPRINT_TYPES[fp_type], i+1, configuration)

def make_for_file(filepath, configuration):
    with open(filepath, 'r') as wire_definition:
        try:
            wires = yaml.safe_load(wire_definition)
            for w in wires:
                make_for_wire(wires[w], configuration)
        except yaml.YAMLError as exc:
            print(exc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create footprints for directly soldering wires to a PCB.'
        )
    parser.add_argument(
        'wire_def', metavar='wire_def', type=str, nargs='+',
        help='Wire definition files'
        )
    parser.add_argument(
        '--global_config', type=str, nargs='?',
        help='The config file defining how the footprint will look like. (KLC)',
        default='../../tools/global_config_files/config_KLCv3.0.yaml'
        )
    parser.add_argument(
        '--minimum_pad_drill_oversize', type=float, default=DEFAULT_MIN_PAD_DRILL_INC,
        help='Determines the minimum for how much the pads PTH drill is increased compared to conductor diameter.'
        )
    parser.add_argument(
        '--pad_drill_factor', type=float, default=DEFAULT_PAD_DRILL_INC_FACTOR,
        help='Determines the multiplicator for pad drill size compared to conductor diameter'
        )
    parser.add_argument(
        '--relief_drill_oversize', type=float, default=DEFAULT_RELIEF_DRILL_INC,
        help='Determines how much the relief NPTH drill is increased compared to outer diameter.'
        )

    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    configuration['pad_drill_factor'] = args.pad_drill_factor
    configuration['min_pad_drill_inc'] = args.minimum_pad_drill_oversize
    configuration['relief_drill_inc'] = args.relief_drill_oversize

    for filepath in args.wire_def:
        make_for_file(filepath, configuration)
