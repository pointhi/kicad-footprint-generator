'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.

(C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
'''

from KicadModTree.Point import *
from KicadModTree.nodes.Node import Node
import math


class Arc(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.center_pos = Point(kwargs['center'])
        self.start_pos = Point(kwargs['start'])
        self.angle = kwargs['angle']

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.width = kwargs.get('width')

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

        return Node.calculateBoundingBox({'min': Point((min_x, min_y)), 'max': Point((max_x, max_y))})

    def _calulateEndPos(self):
        radius = self._calculateRadius()

        angle = self._calculateStartAngle() + math.radians(self.angle)

        return Point(math.sin(angle)*radius, math.cos(angle)*radius)

    def _calculateRadius(self):
        x_size = self.start_pos.x - self.center_pos.x
        y_size = self.start_pos.y - self.center_pos.y

        return math.sqrt(math.pow(x_size, 2) + math.pow(y_size, 2))

    def _calculateStartAngle(self):
        x_size = self.start_pos.x - self.center_pos.x
        y_size = self.start_pos.y - self.center_pos.y

        return math.atan2(y_size, x_size)

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
