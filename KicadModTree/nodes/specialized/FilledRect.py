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
from KicadModTree.nodes.specialized import RectLine
from KicadModTree.nodes.specialized import RectFill


class FilledRect(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.start_pos = Point(kwargs['start'])
        self.end_pos = Point(kwargs['end'])

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.width = kwargs.get('width', 0.15) # TODO: better variation to get line width

        rect_line = RectLine(**kwargs)
        rect_line._parent = self

        rect_fill = RectFill(**kwargs)
        rect_fill._parent = self

        self.virtual_childs = [rect_line, rect_fill]


    def getVirtualChilds(self):
        return self.virtual_childs


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [start: [x: {sx}, y: {sy}] end: [x: {ex}, y: {ey}]]".format(sx=self.start_pos.x
                                                                                    ,sy=self.start_pos.y
                                                                                    ,ex=self.end_pos.x
                                                                                    ,ey=self.end_pos.y)

        return render_text
