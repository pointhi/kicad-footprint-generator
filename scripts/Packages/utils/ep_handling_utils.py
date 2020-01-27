#!/usr/bin/env python3

from KicadModTree.nodes.base.Pad import Pad

def getEpRoundRadiusParams(device_params, configuration, pad_radius):
    pad_shape_details = {}
    pad_shape_details['shape'] = Pad.SHAPE_ROUNDRECT

    pad_shape_details['paste_radius_ratio'] = configuration['paste_radius_ratio']
    pad_shape_details['paste_maximum_radius'] = configuration['paste_maximum_radius']

    if 'EP_round_radius' in device_params:
        if type(device_params['EP_round_radius']) in [float, int]:
            pad_shape_details['round_radius_exact'] = device_params['EP_round_radius']
        elif device_params['EP_round_radius'] == "pad":
            pad_shape_details['round_radius_exact'] = pad_radius
        else:
            raise TypeError(
                    "round radius must be a number or 'pad', is {}"
                    .format(type(device_params['EP_round_radius']))
                    )
    elif 'EP_round_radius_ratio' in device_params:
        pad_shape_details['radius_ratio'] = device_params['EP_round_radius_ratio']
    elif 'EP_round_radius_ratio' in configuration:
        pad_shape_details['radius_ratio'] = configuration['EP_round_radius_ratio']
    else:
        pad_shape_details['radius_ratio'] = 0

    if 'radius_ratio' in pad_shape_details and pad_shape_details['radius_ratio'] > 0:
        if 'EP_maximum_radius' in device_params:
            pad_shape_details['maximum_radius'] = device_params['EP_maximum_radius']
        elif 'EP_maximum_radius' in configuration:
            pad_shape_details['maximum_radius'] = configuration['EP_maximum_radius']
        else:
            pad_shape_details['maximum_radius'] = 0.25

    return pad_shape_details
