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
        self.start_pos = ParseXY(kwargs['start'])
        self.end_pos = ParseXY(kwargs['end'])
        self.angle = kwargs['angle']

        self.layer = kwargs['layer']
        self.width = kwargs['width']


    def renderList(self):
        render_list = ["(fp_arc {start} {end} (angle {angle}) (layer {layer}) (width {width}))".format(start=self.getRealPosition(self.start_pos).render('(center {x} {y})')
                                                                                                      ,end=self.getRealPosition(self.end_pos).render('(end {x} {y})')
                                                                                                      ,angle=self.angle
                                                                                                      ,layer=self.layer
                                                                                                      ,width=self.width)]
        render_list.extend(Node.renderList(self))
        return render_list


    def calculateOutline(self):
        min_x = min(self.start_pos.x, self.end_pos.x)
        min_y = min(self.start_pos.y, self.end_pos.y)
        max_x = max(self.start_pos.x, self.end_pos.x)
        max_y = max(self.start_pos.y, self.end_pos.y)

        return Node.calculateOutline({'min':parse_coordinate_xy((min_x, min_y)), 'max':parse_coordinate_xy((max_x, max_y))})


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " (fp_arc {start} {end} (angle {angle}) (layer {layer}) (width {width}))".format(start=self.start_pos.render('(center {x} {y})')
                                                                                                       ,end=self.end_pos.render('(end {x} {y})')
                                                                                                       ,angle=self.angle
                                                                                                       ,layer=self.layer
                                                                                                       ,width=self.width)

        return render_text
