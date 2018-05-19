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
from .PolygoneLine import PolygoneLine


class RectLine(PolygoneLine):
    r"""Add a Rect to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *start* (``Vector2D``) --
          start edge of the rect
        * *end* (``Vector2D``) --
          end edge of the rect
        * *layer* (``str``) --
          layer on which the rect is drawn
        * *width* (``float``) --
          width of the outer line (default: None, which means auto detection)
        * *offset* (``Vector2D``, ``float``) --
          offset of the rect line to the specified one

    :Example:

    >>> from KicadModTree import *
    >>> RectLine(start=[-3, -2], end=[3, 2], layer='F.SilkS')
    """

    def __init__(self, **kwargs):
        self.start_pos = Vector2D(kwargs['start'])
        self.end_pos = Vector2D(kwargs['end'])

        # If specifed, an 'offset' can be applied to the RectLine.
        # For example, creating a border around a given Rect of a specified size
        if kwargs.get('offset'):
            # offset for the rect line
            # e.g. for creating a rectLine 0.5mm LARGER than the given rect, or similar
            offset = [0, 0]

            # Has an offset / inset been specified?
            if type(kwargs['offset']) in [int, float]:
                offset[0] = offset[1] = kwargs['offset']
            elif type(kwargs['offset']) in [list, tuple] and len(kwargs['offset']) == 2:
                # Ensure that all offset params are numerical
                if all([type(i) in [int, float] for i in kwargs['offset']]):
                    offset = kwargs['offset']

            # For the offset to work properly, start-pos must be top-left, and end-pos must be bottom-right
            x1 = min(self.start_pos.x, self.end_pos.x)
            x2 = max(self.start_pos.x, self.end_pos.x)

            y1 = min(self.start_pos.y, self.end_pos.y)
            y2 = max(self.start_pos.y, self.end_pos.y)

            # Put the offset back in
            self.start_pos.x = x1 - offset[0]
            self.start_pos.y = y1 - offset[1]

            self.end_pos.x = x2 + offset[0]
            self.end_pos.y = y2 + offset[1]

        polygone_line = [{'x': self.start_pos.x, 'y': self.start_pos.y},
                         {'x': self.start_pos.x, 'y': self.end_pos.y},
                         {'x': self.end_pos.x, 'y': self.end_pos.y},
                         {'x': self.end_pos.x, 'y': self.start_pos.y},
                         {'x': self.start_pos.x, 'y': self.start_pos.y}]

        PolygoneLine.__init__(self, polygone=polygone_line, layer=kwargs['layer'], width=kwargs.get('width'))

    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [start: [x: {sx}, y: {sy}] end: [x: {ex}, y: {ey}]]".format(sx=self.start_pos.x,
                                                                                     sy=self.start_pos.y,
                                                                                     ex=self.end_pos.x,
                                                                                     ey=self.end_pos.y)

        return render_text
