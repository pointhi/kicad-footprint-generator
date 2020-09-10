#!/usr/bin/env python

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2017 by @SchrodingersGat
# (C) 2017 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

from types import GeneratorType
from KicadModTree.nodes.base.Pad import *
from KicadModTree.nodes.specialized.ChamferedPad import *
from KicadModTree.nodes.Node import Node

from KicadModTree.util.paramUtil import *


class PadArray(Node):
    r"""Add a row of Pads

    Simplifies the handling of pads which are rendered in a specific form

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *start* (``Vector2D``) --
          start edge of the pad array
        * *center* (``Vector2D``) --
          center pad array around specific point
        * *pincount* (``int``) --
          number of pads to render
        * *spacing* (``Vector2D``, ``float``) --
          offset between rendered pads
        * *x_spacing* (``float``) --
          x offset between rendered pads
        * *y_spacing* (``float``) --
          y offset between rendered pads
        * *initial* (``int``) --
          name of the first pad
        * *increment* (``int, function(previous_number)``) --
          declare how the name of the follow up is calculated
        * *type* (``Pad.TYPE_THT``, ``Pad.TYPE_SMT``, ``Pad.TYPE_CONNECT``, ``Pad.TYPE_NPTH``) --
          type of the pad
        * *shape* (``Pad.SHAPE_CIRCLE``, ``Pad.SHAPE_OVAL``, ``Pad.SHAPE_RECT``, ``Pad.SHAPE_TRAPEZE``, ...) --
          shape of the pad
        * *rotation* (``float``) --
          rotation of the pad
        * *size* (``float``, ``Vector2D``) --
          size of the pad
        * *offset* (``Vector2D``) --
          offset of the pad
        * *drill* (``float``, ``Vector2D``) --
          drill-size of the pad
        * *solder_paste_margin_ratio* (``float``) --
          solder paste margin ratio of the pad
        * *layers* (``Pad.LAYERS_SMT``, ``Pad.LAYERS_THT``, ``Pad.LAYERS_NPTH``) --
          layers on which are used for the pad
        * *chamfer_corner_selection_first* (``[bool, bool, bool, bool]``)
          Select which corner should be chamfered for the first pad. (default: None)
        * *chamfer_corner_selection_last* (``[bool, bool, bool, bool]``)
          Select which corner should be chamfered for the last pad. (default: None)
        * *chamfer_size* (``float``, ``Vector2D``) --
          size for the chamfer used for the end pads. (default: None)

        * *end_pads_size_reduction* (``dict with keys x-,x+,y-,y+``) --
          size is reduced on the given side. (size reduced plus center moved.)
        * *tht_pad1_shape* (``Pad.SHAPE_RECT``, ``Pad.SHAPE_ROUNDRECT``, ...) --
          shape for marking pad 1 for through hole components. (deafult: ``Pad.SHAPE_ROUNDRECT``)
        * *tht_pad1_id* (``int, string``) --
          pad number used for "pin 1" (default: 1)
        * *hidden_pins* (``int, Vector1D``) --
          pin number(s) to be skipped; a footprint with hidden pins has missing pads and matching pin numbers
        * *deleted_pins* (``int, Vector1D``) --
          pin locations(s) to be skipped; a footprint with deleted pins has pads missing but no missing pin numbers"


    :Example:

    >>> from KicadModTree import *
    >>> PadArray(pincount=10, spacing=[1,-1], center=[0,0], initial=5, increment=2,
    ...          type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[1,2], layers=Pad.LAYERS_SMT)
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self._initPincount(**kwargs)
        self._initIncrement(**kwargs)
        self._initInitialNumber(**kwargs)
        self._initSpacing(**kwargs)
        self._initStartingPosition(**kwargs)
        self.virtual_childs = self._createPads(**kwargs)

    # How many pads in the array
    def _initPincount(self, **kwargs):
        if not kwargs.get('pincount'):
            raise KeyError('pincount not declared (like "pincount=10")')
        self.pincount = kwargs.get('pincount')
        if type(self.pincount) is not int or self.pincount <= 0:
            raise ValueError('{pc} is an invalid value for pincount'.format(pc=self.pincount))

        if kwargs.get('hidden_pins') and kwargs.get('deleted_pins'):
            raise KeyError('hidden pins and deleted pins cannot be used together')

        self.exclude_pin_list = []
        if kwargs.get('hidden_pins'):
            # exclude_pin_list is for pads being removed based on pad number
            # deleted pins are filtered out later by pad location (not number)
            self.exclude_pin_list = kwargs.get('hidden_pins')

            if type(self.exclude_pin_list) not in [list, tuple]:
                raise TypeError('exclude pin list must be specified like "exclude_pin_list=[0,1]"')
            elif any([type(i) not in [int] for i in self.exclude_pin_list]):
                raise ValueError('exclude pin list must be integer value')

    # Where to start the aray
    def _initStartingPosition(self, **kwargs):
        """
        can use the 'start' argument to start a pad array at a given position
        OR
        can use the 'center' argument to center the array around the given position
        """
        self.startingPosition = [0, 0]

        # Start takes priority
        if kwargs.get('start'):
            self.startingPosition = kwargs.get('start')
            if type(self.startingPosition) not in [list, tuple] or not len(self.startingPosition) == 2:
                raise ValueError('array starting position "start" must be given as an list of length two')
            if any([type(i) not in [int, float] for i in self.startingPosition]):
                raise ValueError('array starting coordinates must be numerical')
        elif kwargs.get('center'):
            center = kwargs.get('center')

            if type(center) not in [list, tuple] or not len(center) == 2:
                raise ValueError('array center position "center" must be given as a list of length two')
            if any([type(i) not in [int, float] for i in center]):
                raise ValueError('array center coordinates must be numerical')

            # Now calculate the desired starting position of the array
            self.startingPosition[0] = center[0] - (self.pincount - 1) * self.spacing[0] / 2.
            self.startingPosition[1] = center[1] - (self.pincount - 1) * self.spacing[1] / 2.

    # What number to start with?
    def _initInitialNumber(self, **kwargs):
        self.initialPin = kwargs.get('initial', 1)
        if self.initialPin == "":
            self.increment = 0
        elif type(self.initialPin) is not int or self.initialPin < 1:
            if not callable(self.increment):
                raise ValueError('{pn} is not a valid starting pin number if increment is not a function'
                                 .format(pn=self.initialPin))

    # Pin incrementing
    def _initIncrement(self, **kwargs):
        self.increment = kwargs.get('increment', 1)

    # Pad spacing
    def _initSpacing(self, **kwargs):
        """
        spacing can be given as:
        spacing = [1,2] # high priority
        x_spacing = 1
        y_spacing = 2
        """

        self.spacing = [0, 0]  # [x, y]

        if kwargs.get('spacing'):
            self.spacing = kwargs.get('spacing')
            if type(self.spacing) not in [list, tuple]:
                raise TypeError('spacing must be specified like "spacing=[0,1]"')
            elif len(self.spacing) is not 2:
                raise ValueError('spacing must be supplied as x,y pair')
            elif any([type(i) not in [int, float] for i in self.spacing]):
                raise ValueError('spacing must be numerical value')
            # if 'spacing' is specified, ignore x_spacing and y_spacing
            return

        if kwargs.get('x_spacing'):
            self.spacing[0] = kwargs.get('x_spacing')
            if type(self.spacing[0]) not in [int, float]:
                raise ValueError('x_spacing must be supplied as numerical value')

        if kwargs.get('y_spacing'):
            self.spacing[1] = kwargs.get('y_spacing')
            if type(self.spacing[1]) not in [int, float]:
                raise ValueError('y_spacing must be supplied as numerical value')

        if all([i == 0 for i in self.spacing]):
            raise ValueError('pad spacing ({sp}) must be non-zero'.format(sp=self.spacing))

    def _createPads(self, **kwargs):

        pads = []

        x_start, y_start = self.startingPosition
        x_spacing, y_spacing = self.spacing

        padShape = kwargs.get('shape')

        # Special case, increment = 0
        # this can be used for creating an array with all the same pad number
        if self.increment == 0:
            pad_numbers = [self.initialPin] * self.pincount
        elif type(self.increment) == int:
            pad_numbers = range(self.initialPin, self.initialPin + (self.pincount * self.increment), self.increment)
        elif callable(self.increment):
            pad_numbers = [self.initialPin]
            for idx in range(1, self.pincount):
                pad_numbers.append(self.increment(pad_numbers[-1]))
        elif type(self.increment) == GeneratorType:
            pad_numbers = [next(self.increment) for i in range(self.pincount)]
        else:
            raise TypeError("Wrong type for increment. It must be either a int, callable or generator.")

        end_pad_params = copy(kwargs)
        if kwargs.get('end_pads_size_reduction'):
            size_reduction = kwargs['end_pads_size_reduction']
            end_pad_params['size'] = toVectorUseCopyIfNumber(kwargs.get('size'), low_limit=0)

            delta_size = Vector2D(
                size_reduction.get('x+', 0) + size_reduction.get('x-', 0),
                size_reduction.get('y+', 0) + size_reduction.get('y-', 0)
                )

            end_pad_params['size'] -= delta_size

            delta_pos = Vector2D(
                -size_reduction.get('x+', 0) + size_reduction.get('x-', 0),
                -size_reduction.get('y+', 0) + size_reduction.get('y-', 0)
                )/2
        else:
            delta_pos = Vector2D(0, 0)

        for i, number in enumerate(pad_numbers):
            includePad = True

            # deleted pins are filtered by pad/pin position (they are 'None' in pad_numbers list)
            if type(number) not in [int, str]:
                includePad = False

            # hidden pins are filtered out by pad number (index of pad_numbers list)
            if not kwargs.get('deleted_pins'):
                if type(self.initialPin) == 'int':
                    includePad = (self.initialPin + i) not in self.exclude_pin_list
                else:
                    includePad = number not in self.exclude_pin_list

            if includePad:
                current_pad_pos = Vector2D(
                    x_start + i * x_spacing,
                    y_start + i * y_spacing
                    )
                current_pad_params = copy(kwargs)
                if i == 0 or i == len(pad_numbers)-1:
                    current_pad_pos += delta_pos
                    current_pad_params = end_pad_params
                if kwargs.get('type') == Pad.TYPE_THT and number == kwargs.get('tht_pad1_id', 1):
                    current_pad_params['shape'] = kwargs.get('tht_pad1_shape', Pad.SHAPE_ROUNDRECT)
                    if 'radius_ratio' not in current_pad_params:
                        current_pad_params['radius_ratio'] = 0.25
                    if 'maximum_radius' not in current_pad_params:
                        current_pad_params['maximum_radius'] = 0.25
                else:
                    current_pad_params['shape'] = padShape
                if kwargs.get('chamfer_size'):
                    if i == 0 and 'chamfer_corner_selection_first' in kwargs:
                        pads.append(
                            ChamferedPad(
                                number=number, at=current_pad_pos,
                                corner_selection=kwargs.get('chamfer_corner_selection_first'),
                                **current_pad_params
                                ))
                        continue
                    if i == len(pad_numbers)-1 and 'chamfer_corner_selection_last' in kwargs:
                        pads.append(
                            ChamferedPad(
                                number=number, at=current_pad_pos,
                                corner_selection=kwargs.get('chamfer_corner_selection_last'),
                                **current_pad_params
                                ))
                        continue
                pads.append(Pad(number=number, at=current_pad_pos, **current_pad_params))

        return pads

    def getVirtualChilds(self):
        return self.virtual_childs
