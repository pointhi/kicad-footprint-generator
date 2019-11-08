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

from KicadModTree.Vector import *
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
        * *at* (``Vector2D``) --
          position of text
        * *rotation* (``float``) --
          rotation of text (default: 0)
        * *mirror* (``bool``) --
          mirror text (default: False)
        * *layer* (``str``) --
          layer on which the text is drawn (default: 'F.SilkS')
        * *size* (``Vector2D``) --
          size of the text (default: [1, 1])
        * *thickness* (``float``) --
          thickness of the text (default: 0.15)
        * *hide* (``bool``) --
          hide text (default: False)

    :Example:

    >>> from KicadModTree import *
    >>> Text(type='reference', text='REF**', at=[0, -3], layer='F.SilkS')
    >>> Text(type='value', text="footprint name", at=[0, 3], layer='F.Fab')
    >>> Text(type='user', text='test', at=[0, 0], layer='Cmts.User')
    """

    TYPE_REFERENCE = 'reference'
    TYPE_VALUE = 'value'
    TYPE_USER = 'user'
    _TYPES = [TYPE_REFERENCE, TYPE_VALUE, TYPE_USER]

    def __init__(self, **kwargs):
        Node.__init__(self)
        self._initType(**kwargs)

        self.text = kwargs['text']
        self.at = Vector2D(kwargs['at'])
        self.rotation = kwargs.get('rotation', 0)
        self.mirror = kwargs.get('mirror', False)

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.size = Vector2D(kwargs.get('size', [1, 1]))
        self.thickness = kwargs.get('thickness', 0.15)

        self.hide = kwargs.get('hide', False)

    def _initType(self, **kwargs):
        self.type = kwargs['type']
        if self.type not in Text._TYPES:
            raise ValueError('Illegal type selected for text field.')

    def rotate(self, angle, origin=(0, 0), use_degrees=True):
        r""" Rotate text around given origin

        :params:
            * *angle* (``float``)
                rotation angle
            * *origin* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        self.at.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        a = angle if use_degrees else math.degrees(angle)

        # subtraction because kicad text field rotation is the wrong way round
        self.rotation -= a
        return self

    def translate(self, distance_vector):
        r""" Translate text

        :params:
            * *distance_vector* (``Vector2D``)
                2D vector defining by how much and in what direction to translate.
        """

        self.at += distance_vector
        return self

    def calculateBoundingBox(self):
        width = len(self.text)*self.size['x']
        height = self.size['y']

        min_x = self.at['x']-width/2.
        min_y = self.at['y']-height/2.
        max_x = self.at['x']+width/2.
        max_y = self.at['y']+height/2.

        return Node.calculateBoundingBox({'min': Vector2D(min_x, min_y), 'max': Vector2D(max_x, max_y)})

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
