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
from __future__ import division
from KicadModTree.Vector import *
from KicadModTree.nodes.base.Polygon import *
from KicadModTree.nodes.base.Pad import Pad


class CornerSelection():
    r"""Class for handling chamfer selection
        :param chamfer_select:
            * A list of bools do directly set the corners
              (top left, top right, bottom right, bottom left)
            * A dict with keys 'tl', 'tr', 'br', 'bl'
            * A list of strings (available as constants in this class)
            * The integer 1 means all corners
            * The integer 0 means no corners
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
        self.top_left = value
        self.bottom_left = value

    def setTop(self, value=1):
        self.top_left = value
        self.top_right = value

    def setRight(self, value=1):
        self.top_right = value
        self.bottom_right = value

    def setBottom(self, value=1):
        self.bottom_left = value
        self.bottom_right = value

    def isAnySelected(self):
        for v in self:
            if v:
                return True
        return False

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
            self.top_left = value
        elif item in [1, CornerSelection.TOP_RIGHT]:
            self.top_right = value
        elif item in [2, CornerSelection.BOTTOM_RIGHT]:
            self.bottom_right = value
        elif item in [3, CornerSelection.BOTTOM_LEFT]:
            self.bottom_left = value
        else:
            raise IndexError('Index {} is out of range'.format(item))

    def __dict__(self):
        return {
            CornerSelection.TOP_LEFT: self.top_left,
            CornerSelection.TOP_RIGHT: self.top_right,
            CornerSelection.BOTTOM_RIGHT: self.bottom_right,
            CornerSelection.BOTTOM_LEFT: self.bottom_left
            }

    def __str__(self):
        return str(self.__dict__())


class ChamferedPad(Node):
    r"""Add a ChamferedPad to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad (default: \"\")
        * *type* (``Pad.TYPE_THT``, ``Pad.TYPE_SMT``, ``Pad.TYPE_CONNECT``, ``Pad.TYPE_NPTH``) --
          type of the pad
        * *at* (``Vector``) --
          center position of the pad
        * *rotation* (``float``) --
          rotation of the pad
        * *size* (``float``, ``Vector``) --
          size of the pad
        * *offset* (``Vector``) --
          offset of the pad
        * *drill* (``float``, ``Vector``) --
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
        * *chamfer_size* (``float``, ``Vector``) --
          Size of the chamfer.
        * *x_mirror* (``[int, float](mirror offset)``) --
          mirror x direction around offset "point"
        * *y_mirror* (``[int, float](mirror offset)``) --
          mirror y direction around offset "point"
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self._initSize(**kwargs)
        self._initPad(**kwargs)

    def _initSize(self, **kwargs):
        if not kwargs.get('size'):
            raise KeyError('pad size not declared (like "size=[1,1]")')
        if type(kwargs.get('size')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.size = Vector2D([kwargs.get('size'), kwargs.get('size')])
        else:
            self.size = Vector2D(kwargs.get('size'))

    def _initPad(self, **kwargs):
        if 'chamfer_size' not in kwargs:
            raise KeyError('chamfer size is required for chamfered pads (like "chamfer_size=[1,1]")')
        if 'corner_selection' not in kwargs:
            raise KeyError('corner selection is required for chamfered pads (like "corner_selection=[1,0,0,0]")')

        corner_selection = CornerSelection(kwargs.get('corner_selection'))

        if type(kwargs.get('chamfer_size')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.chamfer_size = Vector2D([kwargs.get('chamfer_size'), kwargs.get('chamfer_size')])
        else:
            self.chamfer_size = Vector2D(kwargs.get('chamfer_size'))

        if corner_selection.isAnySelected() and self.chamfer_size[0] > 0 and self.chamfer_size[1] > 0:
            outside = Vector2D(self.size.x/2, self.size.y/2)

            inside = [Vector2D(outside.x, outside.y-self.chamfer_size.y),
                      Vector2D(outside.x-self.chamfer_size.x, outside.y)
                      ]

            points = []
            corner_vectors = [
                Vector2D(-1, -1), Vector2D(1, -1), Vector2D(1, 1), Vector2D(-1, 1)
                ]
            for i in range(4):
                if corner_selection[i]:
                    points.append(corner_vectors[i]*inside[i % 2])
                    points.append(corner_vectors[i]*inside[(i+1) % 2])
                else:
                    points.append(corner_vectors[i]*outside)
            kwargs2 = {}
            if 'x_mirror' in kwargs:
                kwargs2['x_mirror'] = kwargs['x_mirror']
            if 'y_mirror' in kwargs:
                kwargs2['y_mirror'] = kwargs['y_mirror']
            primitives = [Polygon(nodes=points, **kwargs2)]
            kwargs['size'] = min(self.size.x, self.size.y)-sqrt(self.chamfer_size[0]**2+self.chamfer_size[1]**2)
            kwargs['shape'] = Pad.SHAPE_CUSTOM
            self.pad = Pad(primitives=primitives, **kwargs)
        else:
            kwargs['shape'] = Pad.SHAPE_RECT
            self.pad = Pad(**kwargs)

    def getVirtualChilds(self):
        return [self.pad]
