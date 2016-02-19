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


class Pad(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.number = kwargs['number']
        self.type = kwargs['type']
        self.form = kwargs['form']
        self.at = PointXY(kwargs['at'])
        self.size = PointXY(kwargs.get('size'))
        self.drill = kwargs.get('drill')
        self.layers=kwargs['layers']


    def renderList(self):
        # TODO: rotation
        render_strings = ['pad']
        render_strings.append(lispString(self.number))
        render_strings.append(lispString(self.type))
        render_strings.append(lispString(self.form))
        render_strings.append(self.getRealPosition(self.at).render('(at {x} {y})'))
        render_strings.append(self.getRealPosition(self.size).render('(size {x} {y})'))
        render_strings.append('(drill {})'.format(self.drill))
        render_strings.append('(layers {})'.format(' '.join(self.layers)))

        render_list = ['({})'.format(' '.join(render_strings))]
        render_list.extend(Node.renderList(self))

        return render_list


    def calculateOutline(self):
        return Node.calculateOutline(self)


    def _getRenderTreeText(self):
        render_strings = ['pad']
        render_strings.append(lispString(self.number))
        render_strings.append(lispString(self.type))
        render_strings.append(lispString(self.form))
        render_strings.append(self.getRealPosition(self.at).render('(at {x} {y})'))
        render_strings.append(self.getRealPosition(self.size).render('(size {x} {y})'))
        render_strings.append('(drill {})'.format(self.drill))
        render_strings.append('(layers {})'.format(' '.join(self.layers)))

        render_text = Node._getRenderTreeText(self)
        render_text += '({})'.format(' '.join(render_strings))

        return render_text
