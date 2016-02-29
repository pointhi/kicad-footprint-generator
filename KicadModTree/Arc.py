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

from .Point import *
from .Node import Node


class Arc(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.start_pos = Point(kwargs['start'])
        self.end_pos = Point(kwargs['end'])
        self.angle = kwargs['angle']

        self.layer = kwargs['layer']
        self.width = kwargs['width']


    def calculateOutline(self):
        min_x = min(self.start_pos.x, self.end_pos.x)
        min_y = min(self.start_pos.y, self.end_pos.y)
        max_x = max(self.start_pos.x, self.end_pos.x)
        max_y = max(self.start_pos.y, self.end_pos.y)

        return Node.calculateOutline({'min':Point((min_x, min_y)), 'max':Point((max_x, max_y))})


    def _getRenderTreeText(self):
        render_strings = ['fp_arc']
        render_strings.append(self.start_pos.render('(center {x} {y})'))
        render_strings.append(self.end_pos.render('(end {x} {y})'))
        render_strings.append('(angle {angle})'.format(angle=self.angle))
        render_strings.append('(layer {layer})'.format(layer=self.layer))
        render_strings.append('(width {width})'.format(width=self.width))

        render_text = Node._getRenderTreeText(self)
        render_text += ' ({})'.format(' '.join(render_strings))

        return render_text
