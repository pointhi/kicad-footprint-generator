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
        self.at = Point(kwargs['at'])
        self.rotation = kwargs.get('rotation', 0)

        self.layer = kwargs['layer']
        self.size = Point(kwargs.get('size', [1,1]))
        self.thickness = kwargs.get('thickness', 0.15)


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

        render_string = ['type: "{}"'.format(self.type)]
        render_string.append('text: "{}"'.format(self.text))
        render_string.append('at: {}'.format(self.at.render('(at {x} {y})')))
        render_string.append('layer: {}'.format(self.layer))
        render_string.append('size: {}'.format(self.size.render('(size {x} {y})')))
        render_string.append('thickness: {}'.format(self.thickness))
        render_text += " [{}]".format(", ".join(render_string))

        return render_text
