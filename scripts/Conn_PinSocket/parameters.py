# -*- coding: utf8 -*-
#!/usr/bin/python
#

#****************************************************************************
#*                                                                          *
#* class for generating and importing parameters for pin sockets parts      *
#*                                                                          *
#* This is part of FreeCAD & cadquery tools                                 *
#* to export generated models in STEP & VRML format.                        *
#*   Copyright (c) 2017                                                     *
#* Terje Io https://github.com/terjeio                                      *
#*                                                                          *
#* All trademarks within this guide belong to their legitimate owners.      *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Lesser General Public License (LGPL)     *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc.,                                                      *
#*   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA           *
#*                                                                          *
#****************************************************************************

import os
import yaml
from collections import namedtuple
from cq_base_parameters import PartParametersBase, PinStyle, CaseType

class params (PartParametersBase):

    Params = namedtuple("Params", [
        'num_pins',
        'num_pin_rows',
        'pin_pitch',
        'pin_style',
        'type',
        'pin1start_right'
    ])

    DParams = namedtuple("DParams", [
        'type',
        'num_pins',
        'num_pin_rows',
        'pin_pitch',
        'pin_style',
        'pin_length',
        'pin_width',
        'pin_thickness',
        'pin_drill',
        'pins_min',
        'pins_max',
        'pin1start_right',
        'pad_width',
        'pad_length',
        'pads_lp_width',
        'pins_offset',
        'body_width',
        'body_height',
        'body_length',
        'body_overlength',
        'body_offset'
    ])

    def __init__(self, parameter_file=None):
        self.devices = {}
        self.base_params = {
            #
            # E - pin rows distance
            # P - total number of pins
            # Case - case type
            #   Generic name                                        E        P  Case
                #"THT-1x1.27mm_Horizontal"       : self._make_params(1.27,    1, PinStyle.ANGLED, CaseType.THT, True),
                "THT-1x2.00mm_Horizontal"       : self._make_params(2.00,    1, PinStyle.ANGLED, CaseType.THT, True),
                "THT-1x2.54mm_Horizontal"       : self._make_params(2.54,    1, PinStyle.ANGLED, CaseType.THT, True),
                "THT-1x1.00mm_Vertical"         : self._make_params(1.00,    1, PinStyle.STRAIGHT, CaseType.THT, True),
                "THT-1x1.27mm_Vertical"         : self._make_params(1.27,    1, PinStyle.STRAIGHT, CaseType.THT, True),
                "THT-1x2.00mm_Vertical"         : self._make_params(2.00,    1, PinStyle.STRAIGHT, CaseType.THT, True),
                "THT-1x2.54mm_Vertical"         : self._make_params(2.54,    1, PinStyle.STRAIGHT, CaseType.THT, True),

                "THT-2x1.27mm_Horizontal"       : self._make_params(1.27,    2, PinStyle.ANGLED, CaseType.THT, True),
                "THT-2x2.00mm_Horizontal"       : self._make_params(2.00,    2, PinStyle.ANGLED, CaseType.THT, True),
                "THT-2x2.54mm_Horizontal"       : self._make_params(2.54,    2, PinStyle.ANGLED, CaseType.THT, True),
                "THT-2x1.27mm_Vertical"         : self._make_params(1.27,    2, PinStyle.STRAIGHT, CaseType.THT, True),
                "THT-2x2.00mm_Vertical"         : self._make_params(2.00,    2, PinStyle.STRAIGHT, CaseType.THT, True),
                "THT-2x2.54mm_Vertical"         : self._make_params(2.54,    2, PinStyle.STRAIGHT, CaseType.THT, True),

                "SMD-1x1.00mm_Vertical_Right"   : self._make_params(1.00,    1, PinStyle.STRAIGHT, CaseType.SMD, True),
                "SMD-1x1.27mm_Vertical_Right"   : self._make_params(1.27,    1, PinStyle.STRAIGHT, CaseType.SMD, True),
                "SMD-1x2.00mm_Vertical_Right"   : self._make_params(2.00,    1, PinStyle.STRAIGHT, CaseType.SMD, True),
                "SMD-1x2.54mm_Vertical_Right"   : self._make_params(2.54,    1, PinStyle.STRAIGHT, CaseType.SMD, True),

                "SMD-1x1.00mm_Vertical_Left"    : self._make_params(1.00,    1, PinStyle.STRAIGHT, CaseType.SMD, False),
                "SMD-1x1.27mm_Vertical_Left"    : self._make_params(1.27,    1, PinStyle.STRAIGHT, CaseType.SMD, False),
                "SMD-1x2.00mm_Vertical_Left"    : self._make_params(2.00,    1, PinStyle.STRAIGHT, CaseType.SMD, False),
                "SMD-1x2.54mm_Vertical_Left"    : self._make_params(2.54,    1, PinStyle.STRAIGHT, CaseType.SMD, False),

                "SMD-2x1.00mm_Vertical"         : self._make_params(1.00,    2, PinStyle.STRAIGHT, CaseType.SMD, True),
                "SMD-2x1.27mm_Vertical"         : self._make_params(1.27,    2, PinStyle.STRAIGHT, CaseType.SMD, True),
                "SMD-2x2.00mm_Vertical"         : self._make_params(2.00,    2, PinStyle.STRAIGHT, CaseType.SMD, True),
                "SMD-2x2.54mm_Vertical"         : self._make_params(2.54,    2, PinStyle.STRAIGHT, CaseType.SMD, True)
            }

        if parameter_file == None:
            parameter_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + "parameters.yaml"

        try:
            devices = yaml.load_all(open(parameter_file))
            for device in devices:
                params = self._import_params(device)
                if not params == False:
                    self.devices[device['series']] = params
                self.loaded = True
        except Exception as exception:
            self.loaded = 'Failed to load parameters: {e:s}'.format(e=exception)
            return

    def _import_params(self, device):
        if self.base_params.has_key(device['series']):
            base = self.base_params[device['series']]
            return self.DParams(
                num_pins = None,                  # to be added programmatically
                type = base.type,
                num_pin_rows = base.num_pin_rows,
                pin_pitch = base.pin_pitch,
                pin_style = base.pin_style,
                pin1start_right = base.pin1start_right,
                pin_length = device['pins']['length'],
                pin_width = device['pins']['width'],
                pin_thickness = device['pins']['thickness'],
                pins_offset = device['pins']['offset'],
                pin_drill = device['pins']['drill'],
                pins_min = int(device['pins']['min']),
                pins_max = int(device['pins']['max']),
                body_width = device['body']['width'],
                body_height = device['body']['height'],
                body_length = None, # will be calculated by the render class
                body_overlength = device['body']['overlength'],
                body_offset = device['body']['offset'],
                pad_width = device['pads']['width'],
                pad_length = device['pads']['length'],
                pads_lp_width = device['pads']['lp_width']
            )
        else:
            return False

    def _make_params(self, pin_pitch, num_pin_rows, pin_style, type, pin1start_right):
        return self.Params(
            num_pins = None,                  # to be added programmatically
            num_pin_rows = num_pin_rows,      # number of pin rows
            pin_pitch = pin_pitch,            # pin pitch
            pin_style = pin_style,            # pin style: 'Straight' or 'Angled'
            type = type,                      # part type: 'THT' or 'SMD'
            pin1start_right = pin1start_right # True if pin 1 start at right
        )

    def getAllModels(self, model_classes):

        models = {}

        # instantiate generator classes in order to make a dictionary of all variants
        for i in range(0, len(model_classes)):
            for variant in self.devices.keys():
                for pin_columns in range(self.devices[variant].pins_min, self.devices[variant].pins_max + 1):
                    params = self.devices[variant]._replace(num_pins = pin_columns * self.devices[variant].num_pin_rows)
                    model = model_classes[i](params)
                    if model.make_me:
                        models[model.makeModelName(variant)] = self.Model(variant, params, model_classes[i])

        return models

    def getSampleModels(self, model_classes):

        models = {}

        # instantiate generator classes in order to make a dictionary of all default variants
        for i in range(0, len(model_classes)):
            for variant in self.devices.keys():
                params = self.devices[variant]._replace(num_pins = 5 * self.devices[variant].num_pin_rows)
                model = model_classes[i](params)
                if model.make_me:
                    models[model.makeModelName(variant)] = self.Model(variant, params, model_classes[i])

        return models

    def getModel(self, model_class, variant):

        model = self.devices.has_key(variant)

        # instantiate generator class in order to make a dictionary entry for a single variant
        if model:
            params = self.devices[variant]._replace(num_pins = 5 * self.devices[variant].num_pin_rows)
            model = model_class(params)
            if not model.make_me:
                model = False

        return model

### EOF ###
