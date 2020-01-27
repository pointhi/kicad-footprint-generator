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
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
# (C) 2018 by Rene Poeschl, github @poeschlr
from __future__ import division

from copy import copy
from KicadModTree.util.paramUtil import *
from KicadModTree.Vector import *
from KicadModTree.nodes.base.Polygon import *
from KicadModTree.nodes.base.Pad import Pad, RoundRadiusHandler
from math import sqrt


class CornerSelection():
    r"""Class for handling chamfer selection
        :param chamfer_select:
            * A list of bools do directly set the corners
              (top left, top right, bottom right, bottom left)
            * A dict with keys (constands see below)
            * The integer 1 means all corners
            * The integer 0 means no corners

        :constants:
            * CornerSelection.TOP_LEFT
            * CornerSelection.TOP_RIGHT
            * CornerSelection.BOTTOM_RIGHT
            * CornerSelection.BOTTOM_LEFT
    """

    TOP_LEFT = 'tl'
    TOP_RIGHT = 'tr'
    BOTTOM_RIGHT = 'br'
    BOTTOM_LEFT = 'bl'

    def __init__(self, chamfer_select):
        self.top_left = False
        self.top_right = False
        self.bottom_right = False
        self.bottom_left = False

        if chamfer_select == 1:
            self.selectAll()
            return

        if chamfer_select == 0:
            return

        if type(chamfer_select) is dict:
            for key in chamfer_select:
                self[key] = bool(chamfer_select[key])
        else:
            for i, value in enumerate(chamfer_select):
                self[i] = bool(value)

    def selectAll(self):
        for i in range(len(self)):
            self[i] = True

    def clearAll(self):
        for i in range(len(self)):
            self[i] = False

    def setLeft(self, value=1):
        self.top_left = bool(value)
        self.bottom_left = bool(value)

    def setTop(self, value=1):
        self.top_left = bool(value)
        self.top_right = bool(value)

    def setRight(self, value=1):
        self.top_right = bool(value)
        self.bottom_right = bool(value)

    def setBottom(self, value=1):
        self.bottom_left = bool(value)
        self.bottom_right = bool(value)

    def isAnySelected(self):
        for v in self:
            if v:
                return True
        return False

    def rotateCW(self):
        top_left_old = self.top_left

        self.top_left = self.bottom_left
        self.bottom_left = self.bottom_right
        self.bottom_right = self.top_right
        self.top_right = top_left_old
        return self

    def rotateCCW(self):
        top_left_old = self.top_left

        self.top_left = self.top_right
        self.top_right = self.bottom_right
        self.bottom_right = self.bottom_left
        self.bottom_left = top_left_old
        return self

    def __or__(self, other):
        return CornerSelection([s or o for s, o in zip(self, other)])

    def __ior__(self, other):
        for i in range(len(self)):
            self[i] |= other[i]
        return self

    def __and__(self, other):
        return CornerSelection([s and o for s, o in zip(self, other)])

    def __iand__(self, other):
        for i in range(len(self)):
            self[i] &= other[i]
        return self

    def __len__(self):
        return 4

    def __iter__(self):
        yield self.top_left
        yield self.top_right
        yield self.bottom_right
        yield self.bottom_left

    def __getitem__(self, item):
        if item in [0, CornerSelection.TOP_LEFT]:
            return self.top_left
        if item in [1, CornerSelection.TOP_RIGHT]:
            return self.top_right
        if item in [2, CornerSelection.BOTTOM_RIGHT]:
            return self.bottom_right
        if item in [3, CornerSelection.BOTTOM_LEFT]:
            return self.bottom_left

        raise IndexError('Index {} is out of range'.format(item))

    def __setitem__(self, item, value):
        if item in [0, CornerSelection.TOP_LEFT]:
            self.top_left = bool(value)
        elif item in [1, CornerSelection.TOP_RIGHT]:
            self.top_right = bool(value)
        elif item in [2, CornerSelection.BOTTOM_RIGHT]:
            self.bottom_right = bool(value)
        elif item in [3, CornerSelection.BOTTOM_LEFT]:
            self.bottom_left = bool(value)
        else:
            raise IndexError('Index {} is out of range'.format(item))

    def to_dict(self):
        return {
            CornerSelection.TOP_LEFT: self.top_left,
            CornerSelection.TOP_RIGHT: self.top_right,
            CornerSelection.BOTTOM_RIGHT: self.bottom_right,
            CornerSelection.BOTTOM_LEFT: self.bottom_left
            }

    def __str__(self):
        return str(self.to_dict())


class ChamferedPad(Node):
    r"""Add a ChamferedPad to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad (default: \"\")
        * *type* (``Pad.TYPE_THT``, ``Pad.TYPE_SMT``, ``Pad.TYPE_CONNECT``, ``Pad.TYPE_NPTH``) --
          type of the pad
        * *at* (``Vector2D``) --
          center position of the pad
        * *rotation* (``float``) --
          rotation of the pad
        * *size* (``float``, ``Vector2D``) --
          size of the pad
        * *offset* (``Vector2D``) --
          offset of the pad
        * *drill* (``float``, ``Vector2D``) --
          drill-size of the pad
        * *solder_paste_margin_ratio* (``float``) --
          solder paste margin ratio of the pad (default: 0)
        * *solder_paste_margin* (``float``) --
          solder paste margin of the pad (default: 0)
        * *solder_mask_margin* (``float``) --
          solder mask margin of the pad (default: 0)
        * *layers* (``Pad.LAYERS_SMT``, ``Pad.LAYERS_THT``, ``Pad.LAYERS_NPTH``) --
          layers on which are used for the pad
        * *corner_selection* (``CornerSelection``) --
          Select which corner(s) to chamfer. (top left, top right, bottom right, bottom left)
        * *chamfer_size* (``float``, ``Vector2D``) --
          Size of the chamfer.
        * *x_mirror* (``[int, float](mirror offset)``) --
          mirror x direction around offset "point"
        * *y_mirror* (``[int, float](mirror offset)``) --
          mirror y direction around offset "point"

        * *radius_ratio* (``float``) --
          The radius ratio of the rounded rectangle.
          (default 0 for backwards compatibility)
        * *maximum_radius* (``float``) --
          The maximum radius for the rounded rectangle.
          If the radius produced by the radius_ratio parameter for the pad would
          exceed the maximum radius, the ratio is reduced to limit the radius.
          (This is useful for IPC-7351C compliance as it suggests 25% ratio with limit 0.25mm)
        * *round_radius_exact* (``float``) --
          Set an exact round radius for a pad.
        * *round_radius_handler* (``RoundRadiusHandler``) --
          An instance of the RoundRadiusHandler class
          If this is given then all other round radius specifiers are ignored
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self._initPosition(**kwargs)
        self._initSize(**kwargs)
        self._initMirror(**kwargs)
        self._initPadSettings(**kwargs)

        self.pad = self._generatePad()

    def _initSize(self, **kwargs):
        if not kwargs.get('size'):
            raise KeyError('pad size not declared (like "size=[1,1]")')
        self.size = toVectorUseCopyIfNumber(kwargs.get('size'), low_limit=0)

    def _initPosition(self, **kwargs):
        if 'at' not in kwargs:
            raise KeyError('center position not declared (like "at=[0,0]")')
        self.at = Vector2D(kwargs.get('at'))

    def _initMirror(self, **kwargs):
        self.mirror = {}
        if 'x_mirror' in kwargs and type(kwargs['x_mirror']) in [float, int]:
            self.mirror['x_mirror'] = kwargs['x_mirror']
        if 'y_mirror' in kwargs and type(kwargs['y_mirror']) in [float, int]:
            self.mirror['y_mirror'] = kwargs['y_mirror']

    def _initPadSettings(self, **kwargs):
        if 'corner_selection' not in kwargs:
            raise KeyError('corner selection is required for chamfered pads (like "corner_selection=[1,0,0,0]")')

        self.corner_selection = CornerSelection(kwargs.get('corner_selection'))

        if 'chamfer_size' not in kwargs:
            self.chamfer_size = Vector2D(0, 0)
        else:
            self.chamfer_size = toVectorUseCopyIfNumber(
                kwargs.get('chamfer_size'), low_limit=0, must_be_larger=False)

        if('round_radius_handler' in kwargs):
            self.round_radius_handler = kwargs['round_radius_handler']
        else:
            # default radius ration 0 for backwards compatibility
            self.round_radius_handler = RoundRadiusHandler(default_radius_ratio=0, **kwargs)

        self.padargs = copy(kwargs)
        self.padargs.pop('size', None)
        self.padargs.pop('shape', None)
        self.padargs.pop('at', None)
        self.padargs.pop('round_radius_handler', None)

    def _generatePad(self):
        if self.chamfer_size[0] >= self.size[0] or self.chamfer_size[1] >= self.size[1]:
            raise ValueError('Chamfer size ({}) too large for given pad size ({})'.format(self.chamfer_size, self.size))

        is_chamfered = False
        if self.corner_selection.isAnySelected() and self.chamfer_size[0] > 0 and self.chamfer_size[1] > 0:
            is_chamfered = True

        radius = self.round_radius_handler.getRoundRadius(min(self.size))

        if is_chamfered:
            outside = Vector2D(self.size.x/2, self.size.y/2)

            inside = [Vector2D(outside.x, outside.y-self.chamfer_size.y),
                      Vector2D(outside.x-self.chamfer_size.x, outside.y)
                      ]

            polygon_width = 0
            if self.round_radius_handler.roundingRequested():
                if self.chamfer_size[0] != self.chamfer_size[1]:
                    raise NotImplementedError(
                            'Rounded chamfered pads are only supported for 45 degree chamfers.'
                            ' Chamfer {}'.format(self.chamfer_size)
                            )
                # We prefer the use of rounded rectangle over chamfered pads.
                r_chamfer = self.chamfer_size[0] + sqrt(2)*self.chamfer_size[0]/2
                if radius >= r_chamfer:
                    is_chamfered = False
                elif radius > 0:
                    shortest_sidlength = min(min(self.size-self.chamfer_size), self.chamfer_size[0]*sqrt(2))
                    if radius > shortest_sidlength/2:
                        radius = shortest_sidlength/2
                    polygon_width = radius*2
                    outside -= radius
                    inside[0].y -= radius*(2/sqrt(2)-1)
                    inside[0].x -= radius
                    inside[1].x -= radius*(2/sqrt(2)-1)
                    inside[1].y -= radius

        if is_chamfered:
            points = []
            corner_vectors = [
                Vector2D(-1, -1), Vector2D(1, -1), Vector2D(1, 1), Vector2D(-1, 1)
                ]
            for i in range(4):
                if self.corner_selection[i]:
                    points.append(corner_vectors[i]*inside[i % 2])
                    points.append(corner_vectors[i]*inside[(i+1) % 2])
                else:
                    points.append(corner_vectors[i]*outside)

            primitives = [Polygon(nodes=points, width=polygon_width, **self.mirror)]
            # TODO make size calculation more resilient
            size = min(self.size.x, self.size.y)-max(self.chamfer_size[0], self.chamfer_size[1])/sqrt(2)
            if size <= 0:
                raise ValueError('Anchor pad size calculation failed.'
                                 'Chamfer size ({}) to large for given pad size ({})'
                                 .format(self.size, self.chamfer_size))
            return Pad(primitives=primitives, at=self.at,
                       shape=Pad.SHAPE_CUSTOM, size=size, **self.padargs)
        else:
            return Pad(
                    at=self.at, shape=Pad.SHAPE_ROUNDRECT, size=self.size,
                    round_radius_handler=self.round_radius_handler, **self.padargs
                )

    def chamferAvoidCircle(self, center, diameter, clearance=0):
        r""" set the chamfer such that the pad avoids a cricle located at near corner.

        :param center: (``Vector2D``) --
           The center of the circle ot avoid
        :param diameter: (``float``, ``Vector2D``) --
           The diameter of the circle. If Vector2D given only x direction is used.
        :param clearance: (``float``) --
           Additional clearance around circle. default:0
        """

        relative_center = Vector2D(center) - self.at
        # pad and circle are symetric so we do not care which corner the
        # reference circle is located at.
        #  -> move it to bottom right to get only positive relative coordinates.
        relative_center = Vector2D([abs(v) for v in relative_center])
        d = diameter if type(diameter) in [float, int] else diameter.x

        # Where should the chamfer be if the center of the reference circle
        # would be in line with the pad edges
        # (meaning exactly at the bottome right corner)
        reference_point = relative_center - sqrt(2)*(clearance+d/2)
        self.chamfer_size = self.size/2 - reference_point

        # compensate for reference circles not placed exactly at the corner
        edge_to_center = relative_center - self.size/2
        self.chamfer_size -= [edge_to_center.y, edge_to_center.x]
        self.chamfer_size = Vector2D([x if x > 0 else 0 for x in self.chamfer_size])

        self.pad = self._generatePad()
        return self.chamfer_size

    def getVirtualChilds(self):
        return [self.pad]

    def getRoundRadius(self):
        return self.pad.getRoundRadius()
