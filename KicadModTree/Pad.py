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
        render_list = ["(pad {number} {type} {form} {at} {size} (drill {drill}) (layers {layers}))".format(number=self.number
                                                                                                          ,type=self.type
                                                                                                          ,form=self.form
                                                                                                          ,drill=self.drill
                                                                                                          ,at=self.getRealPosition(self.at).render('(at {x} {y})')
                                                                                                          ,size=self.getRealPosition(self.size).render('(size {x} {y})')
                                                                                                          ,layers=' '.join(self.layers))]
        return render_list


    def calculateOutline(self):
        return Node.calculateOutline(self)


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " (pad {number} {type} {form} {at} {size} (drill {drill}) (layers {layers}))".format(number=self.number
                                                                                                           ,type=self.type
                                                                                                           ,form=self.form
                                                                                                           ,drill=self.drill
                                                                                                           ,at=self.getRealPosition(self.at).render('(at {x} {y})')
                                                                                                           ,size=self.getRealPosition(self.size).render('(size {x} {y})')
                                                                                                           ,layers=' '.join(self.layers))

        return render_text
