# -*- coding: utf8 -*-
#!/usr/bin/python
#

#
# Parts script module for socket strip footprints for KicCad
#
# This module is built on top of the kicad-footprint-generator framework
# by Thomas Pointhuber, https://github.com/pointhi/kicad-footprint-generator
#
# This module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.

#
# (C) 2017 Terje Io, <http://github.com/terjeio>
#

# 2017-11-25

#
# parts of this code is based on work by other contributors
#

from collections import namedtuple

### use enums (Phyton 3+)

class CaseType:
    r"""A class for holding constants for part types

    .. note:: will be changed to enum when Python version allows it
    """
    THT = 'THT'
    r"""THT - trough hole part
    """
    SMD = 'SMD'
    r"""SMD - surface mounted part
    """

class PinStyle:
    r"""A class for holding constants for pin styles

    .. note:: will be changed to enum when Python version allows it
    """
    STRAIGHT = 'Straight'
    ANGLED   = 'Angled' 

###

#
# The following classes must be subclassed
#
class PartParametersBase:
    """

    .. document private functions
    .. automethod:: _make_params
    """

    Model = namedtuple("Model", [
        'variant',      # generic model name
        'params',       # parameters
        'model'         # model creator class
    ])
    """ Internally used for passing information from the base parameters to the class instance used for creating models

    .. py:attribute:: variant

        The generic name from the list of parameters

    .. py:attribute:: params

        The final parameters passed to the class instance

    .. py:attribute:: model

        The class instance itself

    """

    Params = namedtuple("Params", [
        'num_pins',
        'pin_pitch',
        'pin_style',
        'type'
    ])
    """ Basic parameters for parts, if further parameters are required this should be subclassed/overriden 

    .. note:: The existing parameters should be kept with the same name when overriden as the framework requires them

    .. py:attribute:: num_pins

        Number of pins, for parts with this is usually set to None for 

    .. py:attribute:: pin_pitch

        The final parameters passed to the class instance

    .. py:attribute:: pin_style

        The class instance itself

    .. py:attribute:: type

        The class instance itself

    """

    def __init__(self):
        self.base_params = {}

    def _make_params(self, pin_pitch, num_pin_rows, pin_style, type):
        r"""add a list of new points
        """
        return self.Params(
            num_pins = None,                # to be added programmatically
            pin_pitch = pin_pitch,          # pin pitch
            pin_style = pin_style,          # pin style: 'Straight' or 'Angled'
            type = type                     # part type: 'THT' or 'SMD'
        )

    def getAllModels(self, model_classes):
        r"""Generate model parameters for all series and variants

        Loops through all base parameters and model classes instantiating the classes and checks whether a variant should be made.
        If a variant is to be made a namedtuple is made with the index from a call to the model instance makeModelName method
        and the base parameters are copied to this. When copying the base parameters others may be added such as number of pins (num_pins). 

        .. note:: Typically this method is overriden in order to add calculated parameters like number of pins.
                  The model specific parameters are contained in the model class itself.

        :param model_classes:
            list of part creator classes inherited from :class:`cq_base_model.PartBase`
        :type  model_classes: ``list of classes``

        :rtype: ```tuple````

        """
        models = {}

        # instantiate generator classes in order to make a dictionary of all model names
        for i in range(0, len(model_classes)):
            for variant in self.base_params.keys():
                params = self.base_params[variant]
                model = model_classes[i](params)
                if model.make_me:
                    models[model.makeModelName(variant)] = self.Model(variant, params, model_classes[i])

        return models

    def getSampleModels(self, model_classes):
        r"""Generate model parameters for all series and variants

        Loops through all base parameters and model classes instantiating the classes and checks whether a variant should be made.
        If a variant is to be made a namedtuple is made with the index from a call to the model instance makeModelName method
        and the base parameters are copied to this. When copying the base parameters others may be added such as number of pins (num_pins). 

        .. note:: Typically this method is overriden in order to add calculated parameters like number of pins.
                  The model specific parameters are contained in the model class itself.

        :param model_classes:
            list of part creator classes inherited from :class:`cq_base_model.PartBase`
        :type  model_classes: ``list of classes``

        :rtype: ```tuple````

        """

        models = {}

        # instantiate generator classes in order to make a dictionary of all model names
        for i in range(0, len(model_classes)):
            for variant in self.base_params.keys():
                params = self.base_params[variant]
                model = model_classes[i](params)
                if model.make_me:
                    models[model.makeModelName(variant)] = self.Model(variant, params, model_classes[i])

        return models
