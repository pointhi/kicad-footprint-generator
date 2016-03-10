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


class Model(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.filename = kwargs['filename']
        self.at = Point(kwargs['at'])
        self.scale = Point(kwargs['scale'])
        self.rotate = Point(kwargs['rotate'])


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [filename: {filename}, at: {at}, scale: {scale}, rotate: {rotate}]".format(filename=self.filename
                                                                                                   ,at=self.at.render('(xyz {x}  {y} {z})')
                                                                                                   ,scale=self.scale.render('(xyz {x}  {y} {z})')
                                                                                                   ,rotate=self.rotate.render('(xyz {x}  {y} {z})'))

        return render_text
