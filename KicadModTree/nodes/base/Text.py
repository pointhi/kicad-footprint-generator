# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

from KicadModTree.Point import *
from KicadModTree.nodes.Node import Node


class Text(Node):
    r"""Add a Line to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *type* (``str``) --
          type of text
        * *text* (``str``) --
          text which is been visualized
        * *at* (``Point``) --
          position of text
        * *rotation* (``float``) --
          rotation of text (default: 0)
        * *layer* (``str``) --
          layer on which the text is drawn (default: 'F.SilkS')
        * *size* (``Point``) --
          size of the text (default: [1, 1])
        * *thickness* (``float``) --
          thickness of the text (default: 0.15)
        * *hide* (``bool``) --
          hide text (default: False)

    :Example:

    >>> from KicadModTree import *
    >>> Text(type='reference', text='REF**', at=[0, -3], layer='F.SilkS')
    >>> Text(type='value', text="footprint name", at=[0, 3], layer='F.Fab')
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self.type = kwargs['type']
        self.text = kwargs['text']
        self.at = Point(kwargs['at'])
        self.rotation = kwargs.get('rotation', 0)

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.size = Point(kwargs.get('size', [1, 1]))
        self.thickness = kwargs.get('thickness', 0.15)

        self.hide = kwargs.get('hide', False)

    def calculateBoundingBox(self):
        width = len(self.text)*self.size['x']
        height = self.size['y']

        min_x = self.at[x]-width/2.
        min_y = self.at[y]-height/2.
        max_x = self.at[x]+width/2.
        max_y = self.at[y]+height/2.

        return Node.calculateBoundingBox({'min': Point(min_x, min_y), 'max': Point(max_x, max_y)})

    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)

        render_string = ['type: "{}"'.format(self.type),
                         'text: "{}"'.format(self.text),
                         'at: {}'.format(self.at.render('(at {x} {y})')),
                         'layer: {}'.format(self.layer),
                         'size: {}'.format(self.size.render('(size {x} {y})')),
                         'thickness: {}'.format(self.thickness)]

        render_text += " [{}]".format(", ".join(render_string))

        return render_text
