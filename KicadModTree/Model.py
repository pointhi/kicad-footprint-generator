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


class Model(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.filename = kwargs['filename']
        self.at = PointXYZ(kwargs['at'])
        self.scale = PointXYZ(kwargs['scale'])
        self.rotate = PointXYZ(kwargs['rotate'])


    def renderList(self):
        render_string = "(model {filename}\n".format(filename=self.filename)
        render_string += "  (at {at})\n".format(at=self.at.render('(xyz {x}  {y} {z})')) # TODO: apply position from parent nodes (missing z)
        render_string += "  (scale {scale})\n".format(scale=self.scale.render('(xyz {x}  {y} {z})')) # TODO: apply scale from parent nodes
        render_string += "  (rotate {rotate})\n".format(rotate=self.rotate.render('(xyz {x}  {y} {z})')) # TODO: apply rotation from parent nodes
        render_string += ")"

        render_list = [render_string]

        render_list.extend(Node.renderList(self))
        return render_list


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [filename: {filename}, at: {at}, scale: {scale}, rotate: {rotate}]".format(filename=self.filename
                                                                                                   ,at=self.at.render('(xyz {x}  {y} {z})')
                                                                                                   ,scale=self.scale.render('(xyz {x}  {y} {z})')
                                                                                                   ,rotate=self.rotate.render('(xyz {x}  {y} {z})'))

        return render_text
