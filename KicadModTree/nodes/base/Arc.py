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

from KicadModTree.Vector import *
from KicadModTree.nodes.Node import Node
import math
from KicadModTree.util.geometric_util import geometricArc, BaseNodeIntersection


class Arc(Node, geometricArc):
    r"""Add an Arc to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *geometry* (``geometricArc``)
          alternative to using geometric parameters
        * *center* (``Vector2D``) --
          center of arc
        * *start* (``Vector2D``) --
          start point of arc
        * *midpoint* (``Vector2D``) --
          alternative to start point
          point is on arc and defines point of equal distance to both arc ends
          arcs of this form are given as midpoint, center plus angle
        * *end* (``Vector2D``) --
          alternative to angle
          arcs of this form are given as start, end and center
        * *angle* (``float``) --
          angle of arc
        * *layer* (``str``) --
          layer on which the arc is drawn (default: 'F.SilkS')
        * *width* (``float``) --
          width of the arc line (default: None, which means auto detection)

    :Example:

    >>> from KicadModTree import *
    >>> Arc(center=[0, 0], start=[-1, 0], angle=180, layer='F.SilkS')
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        geometricArc.__init__(self, **kwargs)

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.width = kwargs.get('width')

    def copyReplaceGeometry(self, geometry):
        return Arc(geometry=geometry, layer=self.layer, width=self.width)

    def copy(self):
        return Arc(
            center=self.center_pos, start=self.start_pos, angle=self.angle,
            layer=self.layer, width=self.width
            )

    def cut(self, *other):
        r""" cut line with given other element

        :params:
            * *other* (``Line``, ``Circle``, ``Arc``)
                cut the element on any intersection with the given geometric element
        """
        result = []
        garcs = geometricArc.cut(self, *other)
        for g in garcs:
            result.append(self.copyReplaceGeometry(g))

        return result

    def calculateBoundingBox(self):
        # TODO: finish implementation
        min_x = min(self.start_pos.x, self._calulateEndPos().x)
        min_y = min(self.start_pos.x, self._calulateEndPos().y)
        max_x = max(self.start_pos.x, self._calulateEndPos().x)
        max_y = max(self.start_pos.x, self._calulateEndPos().y)

        '''
        for angle in range(4):
            float_angle = angle * math.pi/2.

            start_angle = _calculateStartAngle(self)
            end_angle = start_angle + math.radians(self.angle)

            # TODO: +- pi border
            if float_angle < start_angle:
                continue
            if float_angle > end_angle:
                continue

            print("TODO: add angle side: {1}".format(float_angle))
        '''

        return Node.calculateBoundingBox({'min': Vector2D((min_x, min_y)), 'max': Vector2D((max_x, max_y))})

    def _getRenderTreeText(self):
        render_strings = ['fp_arc']
        render_strings.append(self.center_pos.render('(center {x} {y})'))
        render_strings.append(self.start_pos.render('(start {x} {y})'))
        render_strings.append('(angle {angle})'.format(angle=self.angle))
        render_strings.append('(layer {layer})'.format(layer=self.layer))
        render_strings.append('(width {width})'.format(width=self.width))

        render_text = Node._getRenderTreeText(self)
        render_text += ' ({})'.format(' '.join(render_strings))

        return render_text
