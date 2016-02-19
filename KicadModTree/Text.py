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
from .util import lispString


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
        render_strings1 = ['fp_text']
        render_strings1.append(lispString(self.type))
        render_strings1.append(lispString(self.text))

        at_real_position = self.getRealPosition(self.at)
        if at_real_position.r:
            render_strings1.append(at_real_position.render('(at {x} {y} {r})'))
        else:
            render_strings1.append(at_real_position.render('(at {x} {y})'))

        render_strings1.append('(layer {layer})'.format(layer=self.layer))

        render_strings_font = ['font']
        render_strings_font.append(self.size.render('(size {x} {y})'))
        render_strings_font.append('(thickness {thickness})'.format(thickness=self.thickness))

        render_strings2 = ['effects']
        render_strings2.append('({})'.format(' '.join(render_strings_font)))

        render_list = ["({str1}\r\n{str2}\r\n)".format(str1=' '.join(render_strings1)
                                                      ,str2='({})'.format(' '.join(render_strings2)))]

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

        render_string = ['type: "{}"'.format(self.type)]
        render_string.append('text: "{}"'.format(self.text))
        render_string.append('at: {}'.format(self.at.render('(at {x} {y})')))
        render_string.append('layer: {}'.format(self.layer))
        render_string.append('size: {}'.format(self.size.render('(size {x} {y})')))
        render_string.append('thickness: {}'.format(self.thickness))
        render_text += " [{}]".format(", ".join(render_string))

        return render_text
