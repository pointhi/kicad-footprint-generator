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
from KicadModTree.util.geometric_util import geometricLine, BaseNodeIntersection


class Line(Node, geometricLine):
    r"""Add a Line to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *start* (``Vector2D``) --
          start point of the line
        * *end* (``Vector2D``) --
          end point of the line
        * *layer* (``str``) --
          layer on which the line is drawn (default: 'F.SilkS')
        * *width* (``float``) --
          width of the line (default: None, which means auto detection)

    :Example:

    >>> from KicadModTree import *
    >>> Line(start=[1, 0], end=[-1, 0], layer='F.SilkS')
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        if 'geometry' in kwargs:
            geometry = kwargs['geometry']
            geometricLine.__init__(self, geometry.start_pos, geometry.end_pos)
        else:
            geometricLine.__init__(
                self,
                start=Vector2D(kwargs['start']),
                end=Vector2D(kwargs['end'])
                )

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.width = kwargs.get('width')

    def copyReplaceGeometry(self, geometry):
        return Line(
            start=geometry.start_pos, end=geometry.end_pos,
            layer=self.layer, width=self.width
            )

    def copy(self):
        return Line(
            start=self.start_pos, end=self.end_pos,
            layer=self.layer, width=self.width
            )

    def cut(self, *other):
        r""" cut line with given other element

        :params:
            * *other* (``Line``, ``Circle``, ``Arc``)
                cut the element on any intersection with the given geometric element
        """
        result = []
        glines = geometricLine.cut(self, *other)
        for g in glines:
            result.append(self.copyReplaceGeometry(g))

        return result

    def _getRenderTreeText(self):
        render_strings = ['fp_line']
        render_strings.append(self.start_pos.render('(start {x} {y})'))
        render_strings.append(self.end_pos.render('(end {x} {y})'))
        render_strings.append('(layer {layer})'.format(layer=self.layer))
        render_strings.append('(width {width})'.format(width=self.width))

        render_text = Node._getRenderTreeText(self)
        render_text += ' ({})'.format(' '.join(render_strings))

        return render_text

    def calculateBoundingBox(self):
        render_start_pos = self.getRealPosition(self.start_pos)
        render_end_pos = self.getRealPosition(self.end_pos)

        min_x = min([render_start_pos.x, render_end_pos.x])
        min_y = min([render_start_pos.y, render_end_pos.y])
        max_x = max([render_start_pos.x, render_end_pos.x])
        max_y = max([render_start_pos.y, render_end_pos.y])

        return Node.calculateBoundingBox({'min': Vector2D(min_x, min_y), 'max': Vector2D(max_x, max_y)})
