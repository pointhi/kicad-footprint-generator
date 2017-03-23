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

from KicadModTree.nodes.base.Pad import *
from KicadModTree.nodes.Node import Node


class PadArray(Node):
    r"""Add a row of Pads

    Simplifies the handling of pads which are rendered in a specific form

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *start* (``Point``) --
          start edge of the pad array
        * *center* (``Point``) --
          center pad array around specific point
        * *pincount* (``int``) --
          number of pads to render
        * *spacing* (``Point``, ``float``) --
          offset between rendered pads
        * *x_spacing* (``float``) --
          x offset between rendered pads
        * *y_spacing* (``float``) --
          y offset between rendered pads
        * *initial* (``int``) --
          name of the first pad
        * *increment* (``int``) --
          declare how the name of the follow up is calculated
        * *type* (``Pad.TYPE_THT``, ``Pad.TYPE_SMT``, ``Pad.TYPE_CONNECT``, ``Pad.TYPE_NPTH``) --
          type of the pad
        * *shape* (``Pad.SHAPE_CIRCLE``, ``Pad.SHAPE_OVAL``, ``Pad.SHAPE_RECT``, ``Pad.SHAPE_TRAPEZE``) --
          shape of the pad
        * *rotation* (``float``) --
          rotation of the pad
        * *size* (``float``, ``Point``) --
          size of the pad
        * *offset* (``Point``) --
          offset of the pad
        * *drill* (``float``, ``Point``) --
          drill-size of the pad
        * *solder_paste_margin_ratio* (``float``) --
          solder paste margin ratio of the pad
        * *layers* (``Pad.LAYERS_SMT``, ``Pad.LAYERS_THT``, ``Pad.LAYERS_NPTH``) --
          layers on which are used for the pad

    :Example:

    >>> from KicadModTree import *
    >>> PadArray(pincount=10, spacing=[1,-1], center=[0,0], initial=5, increment=2,
    ...          type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[1,2], layers=Pad.LAYERS_SMT)
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self._initPincount(**kwargs)
        self._initInitialNumber(**kwargs)
        self._initIncrement(**kwargs)
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
        if not kwargs.get('initial'):
            self.initialPin = 1
        else:
            self.initialPin = kwargs.get('initial')
            if type(self.initialPin) is not int or self.initialPin < 1:
                raise ValueError('{pn} is not a valid starting pin number'.format(pn=self.initialPin))

    # Pin incrementing
    def _initIncrement(self, **kwargs):
        if kwargs.get('increment', None) is None:
            self.increment = 1
        else:
            self.increment = kwargs.get('increment')
            if type(self.increment) is not int:
                raise ValueError('{inc} is not a valid number for pin increment'.format(inc=self.increment))

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

        else:
            pad_numbers = range(self.initialPin, self.initialPin + (self.pincount * self.increment), self.increment)

        for i, number in enumerate(pad_numbers):
            x_pad = x_start + i * x_spacing
            y_pad = y_start + i * y_spacing

            if kwargs.get('type') == Pad.TYPE_THT and number == 1:
                kwargs['shape'] = Pad.SHAPE_RECT
            else:
                kwargs['shape'] = padShape

            pads.append(Pad(number=number, at=[x_pad, y_pad], **kwargs))
        return pads

    def getVirtualChilds(self):
        return self.virtual_childs
