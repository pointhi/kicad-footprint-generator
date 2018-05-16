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
        * *corner_selection* (``[bool, bool, bool, bool]``) --
          Select which corner(s) to chamfer. (top left, top right, bottom right, bottom left)
        * *chamfer_size* (``float``, ``Vector``) --
          Size of the chamfer.
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self._initSize(**kwargs)

        primitives = [self.__generatePoints(**kwargs)]
        kwargs['size'] = min(self.size.x, self.size.y)
        kwargs['shape'] = Pad.SHAPE_CUSTOM
        self.pad = Pad(primitives=primitives, **kwargs)

    def _initSize(self, **kwargs):
        if not kwargs.get('size'):
            raise KeyError('pad size not declared (like "size=[1,1]")')
        if type(kwargs.get('size')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.size = Vector2D([kwargs.get('size'), kwargs.get('size')])
        else:
            self.size = Vector2D(kwargs.get('size'))

    def __generatePoints(self, **kwargs):
        if 'chamfer_size' not in kwargs:
            raise KeyError('chamfer size is required for chamfered pads (like "chamfer_size=[1,1]")')
        if 'corner_selection' not in kwargs:
            raise KeyError('corner selection is required for chamfered pads (like "corner_selection=[1,0,0,0]")')

        corner_selection = kwargs.get('corner_selection')
        if len(corner_selection) != 4:
            raise TypeError('corner selection must be an array of lenght 4')

        if type(kwargs.get('chamfer_size')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            chamfer_size = Vector2D([kwargs.get('chamfer_size'), kwargs.get('chamfer_size')])
        else:
            chamfer_size = Vector2D(kwargs.get('chamfer_size'))

        outside = Vector2D(self.size.x/2, self.size.y/2)

        inside = [Vector2D(outside.x, outside.y-chamfer_size.y),
                  Vector2D(outside.x-chamfer_size.x, outside.y)
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

        return Polygon(nodes=points)

    def getVirtualChilds(self):
        return [self.pad]
