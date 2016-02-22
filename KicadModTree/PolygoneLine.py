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
from .Line import Line


class PolygoneLine(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.polygone_line = kwargs['polygone']

        self.layer = kwargs['layer']
        self.width = kwargs['width']

        self.virtual_childs = self._createChildNodes(self.polygone_line)


    def _createChildNodes(self, polygone_line):
        nodes = []

        for line_start, line_end in zip(polygone_line, polygone_line[1:]):
            nodes.append(Line(start=line_start, end=line_end, layer=self.layer, width=self.width))

        return nodes


    def getVirtualChilds(self):
        return self.virtual_childs


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " ["

        node_strings = []
        for node in self.polygone_line:
            node_position = Point(node)
            node_strings.append("[x: {x}, y: {y}]".format(x=node_position.x
                                                         ,y=node_position.y))

        if len(node_strings) <= 6:
            render_text += " ,".join(node_strings)
        else:
            # display only a few nodes of the beginning and the end of the polygone line
            render_text += " ,".join(node_strings[:3])
            render_text += " ,... ,"
            render_text += " ,".join(node_strings[-3:])

        render_text += "]"

        return render_text
