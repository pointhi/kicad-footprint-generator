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
        * *offset* (``Point``, ``float``) --
          offset of the rect line to the specified one
        * *chamfers* (``list`` of ``dict`` ) --
          one or more chamfer instructions

    :Example:

    >>> from KicadModTree import *
    >>> RectLine(start=[-3, -2], end=[3, 2], layer='F.SilkS')
    >>> RectLine(start=[-3, -2], end=[3, 2], layer='F.SilkS', chamfers=[{'corner': 'all', 'size': 1.5}])
    >>> RectLine(start=[-3, -2], end=[3, 2], layer='F.SilkS', chamfers=[{'corner': 'topleft', 'size': 1.5}, {'corner': 'topright', 'size': 0.5}])
    """

    def __init__(self, **kwargs):
        self.start_pos = Point(kwargs['start'])
        self.end_pos = Point(kwargs['end'])

        # If specified, one or more corners can be chamfered at 45 degrees
        # Name of corner and size of chamfer for that corner are key:value pairs in a dict
        # Argument is list of one or more dicts
        c_list = kwargs.get('chamfers') if kwargs.get('chamfers') else []
        self.chamfers = []
        for c in c_list:
            try:
                if 'corner' in c.keys() and 'size' in c.keys():
                    self.chamfers.append(c)
            except Exception as e:
                # print(e)
                pass

        # If specifed, an 'offset' can be applied to the RectLine.
        # For example, creating a border around a given Rect of a specified size
        # offset for the rect line
        offset = [0, 0]
        if kwargs.get('offset'):
            # Has an offset / inset been specified?
            if type(kwargs['offset']) in [int, float]:
                offset[0] = offset[1] = kwargs['offset']
            elif type(kwargs['offset']) in [list, tuple] and len(kwargs['offset']) == 2:
                # Ensure that all offset params are numerical
                if all([type(i) in [int, float] for i in kwargs['offset']]):
                    offset = kwargs['offset']

        # For the offset and chamfer to work properly, start-pos must be top-left, and end-pos must be bottom-right
        x1 = min(self.start_pos.x, self.end_pos.x)
        x2 = max(self.start_pos.x, self.end_pos.x)
        y1 = min(self.start_pos.y, self.end_pos.y)
        y2 = max(self.start_pos.y, self.end_pos.y)

        # Put the offset (if any) back in
        self.start_pos.x = x1 - offset[0]
        self.start_pos.y = y1 - offset[1]
        self.end_pos.x = x2 + offset[0]
        self.end_pos.y = y2 + offset[1]
        
        # Work out intermediate positions on each side to use later when drawing corners or chamfers
        JOG = 0.001  # avoid coincident intermediate points on non-chamfered sides
        self.top_left_mid_pos = Point([self.start_pos.x + JOG, self.start_pos.y])
        self.top_right_mid_pos = Point([self.end_pos.x - JOG, self.start_pos.y])
        self.bottom_left_mid_pos = Point([self.start_pos.x + JOG, self.end_pos.y])
        self.bottom_right_mid_pos = Point([self.end_pos.x - JOG, self.end_pos.y])
        self.left_top_mid_pos = Point([self.start_pos.x, self.start_pos.y + JOG])
        self.left_bottom_mid_pos = Point([self.start_pos.x, self.end_pos.y - JOG])
        self.right_top_mid_pos = Point([self.end_pos.x, self.start_pos.y + JOG])
        self.right_bottom_mid_pos = Point([self.end_pos.x, self.end_pos.y - JOG])

        # Set the positions of the corners
        self.top_left_pos = Point([self.start_pos.x, self.start_pos.y])
        self.top_right_pos = Point([self.end_pos.x, self.start_pos.y])
        self.bottom_left_pos = Point([self.start_pos.x, self.end_pos.y])
        self.bottom_right_pos = Point([self.end_pos.x, self.end_pos.y])

        for c in self.chamfers:
            # Need to shift chamfered edges so they maintain constant distance from non-offset line
            # tan(22.5) = 0.414 works correctly when chamfer is at 45 degrees (same  and Y offset), 
            # and still looks OK when X and Y offsets are different
            try:
                x_delta = c['size'] + 0.414 * offset[0]
                y_delta = c['size'] + 0.414 * offset[1]
                if c['corner'] == 'topleft':
                    self.top_left_pos.x = self.start_pos.x + (x_delta) / 2.0
                    self.top_left_pos.y = self.start_pos.y + (y_delta) / 2.0
                    self.top_left_mid_pos.x = self.start_pos.x + (x_delta)
                    self.left_top_mid_pos.y = self.start_pos.y + (y_delta)
                elif c['corner'] == 'topright':
                    self.top_right_pos.x = self.end_pos.x - (x_delta) / 2.0
                    self.top_right_pos.y = self.start_pos.y + (y_delta) / 2.0
                    self.top_right_mid_pos.x = self.end_pos.x - (x_delta)
                    self.right_top_mid_pos.y = self.start_pos.y + (y_delta)
                elif c['corner'] == 'bottomleft':
                    self.bottom_left_pos.x = self.start_pos.x + (x_delta) / 2.0
                    self.bottom_left_pos.y = self.end_pos.y - (y_delta) / 2.0
                    self.bottom_left_mid_pos.x = self.start_pos.x + (x_delta)
                    self.left_bottom_mid_pos.y = self.end_pos.y - (y_delta)
                elif c['corner'] == 'bottomright':
                    self.bottom_right_pos.x = self.end_pos.x - (x_delta) / 2.0
                    self.bottom_right_pos.y = self.end_pos.y - (y_delta) / 2.0
                    self.bottom_right_mid_pos.x = self.end_pos.x - (x_delta)
                    self.right_bottom_mid_pos.y = self.end_pos.y - (y_delta)
                elif c['corner'] == 'all':
                    self.chamfers.append({'corner': 'topleft', 'size': c['size']})
                    self.chamfers.append({'corner': 'topright', 'size': c['size']})
                    self.chamfers.append({'corner': 'bottomleft', 'size': c['size']})
                    self.chamfers.append({'corner': 'bottomright', 'size': c['size']})
                else:
                    pass
            except Exception as e:
                # print(e)
                pass

        polygone_line = [
                         {'x': self.top_left_pos.x, 'y': self.top_left_pos.y},
                         {'x': self.top_left_mid_pos.x, 'y': self.top_left_mid_pos.y},
                         {'x': self.top_right_mid_pos.x, 'y': self.top_right_mid_pos.y},
                         {'x': self.top_right_pos.x, 'y': self.top_right_pos.y},
                         {'x': self.right_top_mid_pos.x, 'y': self.right_top_mid_pos.y},
                         {'x': self.right_bottom_mid_pos.x, 'y': self.right_bottom_mid_pos.y},
                         {'x': self.bottom_right_pos.x, 'y': self.bottom_right_pos.y},
                         {'x': self.bottom_right_mid_pos.x, 'y': self.bottom_right_mid_pos.y},
                         {'x': self.bottom_left_mid_pos.x, 'y': self.bottom_left_mid_pos.y},
                         {'x': self.bottom_left_pos.x, 'y': self.bottom_left_pos.y},
                         {'x': self.left_bottom_mid_pos.x, 'y': self.left_bottom_mid_pos.y},
                         {'x': self.left_top_mid_pos.x, 'y': self.left_top_mid_pos.y},
                         {'x': self.top_left_pos.x, 'y': self.top_left_pos.y} ]

        PolygoneLine.__init__(self, polygone=polygone_line, layer=kwargs['layer'], width=kwargs['width'])

    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [start: [x: {sx}, y: {sy}] end: [x: {ex}, y: {ey}]]".format(sx=self.start_pos.x,
                                                                                     sy=self.start_pos.y,
                                                                                     ex=self.end_pos.x,
                                                                                     ey=self.end_pos.y)
        return render_text

