from __future__ import division

import sys, os
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
from KicadModTree import *  # NOQA
from pad_number_generators import get_generator

def add_dual_or_quad_pad_border(kicad_mod, configuration, pad_details, device_params):
    pad_shape_details = {}
    pad_shape_details['shape'] = Pad.SHAPE_ROUNDRECT
    pad_shape_details['radius_ratio'] = configuration.get('round_rect_radius_ratio', 0)
    if 'round_rect_max_radius' in configuration:
        pad_shape_details['maximum_radius'] = configuration['round_rect_max_radius']

    if 'exclude_pin_list' in device_params:
        pad_shape_details['exclude_pin_list'] = device_params['exclude_pin_list']

    if device_params['num_pins_x'] == 0:
        radius = add_dual_pad_border_y(kicad_mod, pad_details, device_params, pad_shape_details)
    elif device_params['num_pins_y'] == 0:
        radius = add_dual_pad_border_x(kicad_mod, pad_details, device_params, pad_shape_details)
    else:
        radius = add_quad_pad_border(
            kicad_mod, pad_details, device_params, pad_shape_details,
            configuration.get('kicad4_compatible', False))

    return radius


def add_dual_pad_border_y(kicad_mod, pad_details, device_params, pad_shape_details):
    init = 1
    increment = get_generator(device_params)

    pa = PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_y'],
            x_spacing=0, y_spacing=device_params['pitch'],
            increment=increment,
            **pad_details['left'], **pad_shape_details,
            )
    kicad_mod.append(pa)
    init += device_params['num_pins_y']
    kicad_mod.append(PadArray(
        initial= init,
        type=Pad.TYPE_SMT,
        layers=Pad.LAYERS_SMT,
        pincount=device_params['num_pins_y'],
        x_spacing=0, y_spacing=-device_params['pitch'],
        increment=increment,
        **pad_details['right'], **pad_shape_details,
        )
    )

    pads = pa.getVirtualChilds()
    pad = pads[0]
    return pad.getRoundRadius()


def add_dual_pad_border_x(kicad_mod, pad_details, device_params, pad_shape_details):
    #for devices with clockwise numbering
    init = 1
    increment = get_generator(device_params)

    pa = PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_x'],
            y_spacing=0, x_spacing=device_params['pitch'],
            increment=increment,
            **pad_details['top'], **pad_shape_details,
    )
    kicad_mod.append(pa)
    init += device_params['num_pins_x']
    kicad_mod.append(PadArray(
        initial= init,
        type=Pad.TYPE_SMT,
        layers=Pad.LAYERS_SMT,
        pincount=device_params['num_pins_x'],
        y_spacing=0, x_spacing=-device_params['pitch'],
        increment=increment,
        **pad_details['bottom'], **pad_shape_details,
        )
    )

    pads = pa.getVirtualChilds()
    pad = pads[0]
    return pad.getRoundRadius()

def add_quad_pad_border(kicad_mod, pad_details, device_params, pad_shape_details, kicad4_compatible):

    chamfer_size = device_params.get('chamfer_edge_pins', 0)

    pad_size_red = device_params.get('edge_heel_reduction', 0)
    if kicad4_compatible:
        chamfer_size = 0
        pad_size_red += device_params.get('chamfer_edge_pins', 0)


    init = 1
    corner_first = CornerSelection({CornerSelection.TOP_RIGHT: True})
    corner_last = CornerSelection({CornerSelection.BOTTOM_RIGHT: True})
    pad_size_reduction = {'x+': pad_size_red} if pad_size_red > 0 else None
    increment = get_generator(device_params)

    pa = PadArray(
            initial= init,
            type=Pad.TYPE_SMT,
            layers=Pad.LAYERS_SMT,
            pincount=device_params['num_pins_y'],
            x_spacing=0, y_spacing=device_params['pitch'],
            chamfer_size=chamfer_size,
            chamfer_corner_selection_first=corner_first,
            chamfer_corner_selection_last=corner_last,
            end_pads_size_reduction = pad_size_reduction,
            increment=increment,
            **pad_details['left'], **pad_shape_details,
            )
    kicad_mod.append(pa)

    init += device_params['num_pins_y']
    corner_first = copy(corner_first).rotateCCW()
    corner_last = copy(corner_last).rotateCCW()
    pad_size_reduction = {'y-': pad_size_red} if pad_size_red > 0 else None

    kicad_mod.append(PadArray(
        initial= init,
        type=Pad.TYPE_SMT,
        layers=Pad.LAYERS_SMT,
        pincount=device_params['num_pins_x'],
        y_spacing=0, x_spacing=device_params['pitch'],
        chamfer_size=chamfer_size,
        chamfer_corner_selection_first=corner_first,
        chamfer_corner_selection_last=corner_last,
        end_pads_size_reduction = pad_size_reduction,
        increment=increment,
        **pad_details['bottom'], **pad_shape_details,
        )
    )

    init += device_params['num_pins_x']
    corner_first = copy(corner_first).rotateCCW()
    corner_last = copy(corner_last).rotateCCW()
    pad_size_reduction = {'x-': pad_size_red} if pad_size_red > 0 else None

    kicad_mod.append(PadArray(
        initial= init,
        type=Pad.TYPE_SMT,
        layers=Pad.LAYERS_SMT,
        pincount=device_params['num_pins_y'],
        x_spacing=0, y_spacing=-device_params['pitch'],
        chamfer_size=chamfer_size,
        chamfer_corner_selection_first=corner_first,
        chamfer_corner_selection_last=corner_last,
        end_pads_size_reduction = pad_size_reduction,
        increment=increment,
        **pad_details['right'], **pad_shape_details,
        )
    )

    init += device_params['num_pins_y']
    corner_first = copy(corner_first).rotateCCW()
    corner_last = copy(corner_last).rotateCCW()
    pad_size_reduction = {'y+': pad_size_red} if pad_size_red > 0 else None

    kicad_mod.append(PadArray(
        initial= init,
        type=Pad.TYPE_SMT,
        layers=Pad.LAYERS_SMT,
        pincount=device_params['num_pins_x'],
        y_spacing=0, x_spacing=-device_params['pitch'],
        chamfer_size=chamfer_size,
        chamfer_corner_selection_first=corner_first,
        chamfer_corner_selection_last=corner_last,
        end_pads_size_reduction = pad_size_reduction,
        increment=increment,
        **pad_details['top'], **pad_shape_details,
        )
    )

    pads = pa.getVirtualChilds()
    pad = pads[0]
    return pad.getRoundRadius()
