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

from KicadModTree.Point import *
from KicadModTree.nodes.Node import Node
from .PolygoneLine import PolygoneLine


class RectLine(PolygoneLine):
    r"""Add a Rect to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *start* (``Point``) --
          start edge of the rect
        * *end* (``Point``) --
          end edge of the rect
        * *layer* (``str``) --
          layer on which the rect is drawn
        * *width* (``float``) --
          width of the outer line

    :Example:

    >>> from KicadModTree import *
    >>> RectLine(start=[-3, -2], end=[3, 2], layer='F.SilkS')
    """

    def __init__(self, **kwargs):
        self.start_pos = Point(kwargs['start'])
        self.end_pos = Point(kwargs['end'])

        polygone_line = [{'x': self.start_pos.x, 'y': self.start_pos.y},
                         {'x': self.start_pos.x, 'y': self.end_pos.y},
                         {'x': self.end_pos.x, 'y': self.end_pos.y},
                         {'x': self.end_pos.x, 'y': self.start_pos.y},
                         {'x': self.start_pos.x, 'y': self.start_pos.y}]

        PolygoneLine.__init__(self,
                              polygone=polygone_line,
                              layer=kwargs.get('layer', 'F.SilkS'),
                              width=kwargs.get('width'))

    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [start: [x: {sx}, y: {sy}] end: [x: {ex}, y: {ey}]]".format(sx=self.start_pos.x,
                                                                                     sy=self.start_pos.y,
                                                                                     ex=self.end_pos.x,
                                                                                     ey=self.end_pos.y)

        return render_text
