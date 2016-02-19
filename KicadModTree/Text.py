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


class Text(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.type = kwargs['type']
        self.text = kwargs['text']
        self.at = PointXY(kwargs['at'])

        self.layer = kwargs['layer']
        self.size = PointXY(kwargs.get('size', [1,1]))
        self.thickness = kwargs.get('thickness', 0.15)


    def renderList(self):
        at_real_position = self.getRealPosition(self.at)
        if at_real_position.r:
            at_string = at_real_position.render('(at {x} {y} {r})')
        else:
            at_string = at_real_position.render('(at {x} {y})')

        render_string = "(fp_text {type} {text} {at} (layer {layer})\r\n".format(type=self.type
                                                                                ,text=self.text
                                                                                ,at=at_string
                                                                                ,layer=self.layer)
        render_string += "  (effects (font {size} (thickness {thickness})))\r\n".format(size=self.size.render('(size {x} {y})')
                                                                                       ,thickness=self.thickness)
        render_string += ")"

        render_list = [render_string]

        render_list.extend(Node.renderList(self))
        return render_list


    def calculateOutline(self):
        width = len(self.text)*self.size['x']
        height = self.size['y']

        min_x = self.at[x]-width/2.
        min_y = self.at[y]-height/2.
        max_x = self.at[x]+width/2.
        max_y = self.at[y]+height/2.

        return Node.calculateOutline({'min':Point(min_x, min_y), 'max':Point(max_x, max_y)})


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [type: {type}, text: {text}, at: {at}, layer: {layer}, size: {size}, thickness: {thickness}]".format(type=self.type
                                                                                                                             ,text=self.text
                                                                                                                             ,at=self.at.render('(at {x} {y})')
                                                                                                                             ,layer=self.layer
                                                                                                                             ,size=self.size.render('(size {x} {y})')
                                                                                                                             ,thickness=self.thickness)

        return render_text
