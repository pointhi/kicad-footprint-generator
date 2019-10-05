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
from KicadModTree.util.geometric_util import geometricCircle, BaseNodeIntersection


class Circle(Node, geometricCircle):
    r"""Add a Circle to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *center* (``Vector2D``) --
          center of the circle
        * *radius* (``float``) --
          radius of the circle
        * *layer* (``str``) --
          layer on which the circle is drawn (default: 'F.SilkS')
        * *width* (``float``) --
          width of the circle line (default: None, which means auto detection)

    :Example:

    >>> from KicadModTree import *
    >>> Circle(center=[0, 0], radius=1.5, layer='F.SilkS')
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        geometricCircle.__init__(self, Vector2D(kwargs['center']), float(kwargs['radius']))

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.width = kwargs.get('width')

    def rotate(self, angle, origin=(0, 0), use_degrees=True):
        r""" Rotate circle around given origin

        :params:
            * *angle* (``float``)
                rotation angle
            * *origin* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        self.center_pos.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        return self

    def translate(self, distance_vector):
        r""" Translate circle

        :params:
            * *distance_vector* (``Vector2D``)
                2D vector defining by how much and in what direction to translate.
        """

        self.center_pos += distance_vector
        return self

    def cut(self, *other):
        raise NotImplemented("cut for circles not yet implemented")

    def getRadius(self):
        return self.radius

    def calculateBoundingBox(self):
        min_x = self.center_pos.x-self.radius
        min_y = self.center_pos.y-self.radius
        max_x = self.center_pos.x+self.radius
        max_y = self.center_pos.y+self.radius

        return Node.calculateBoundingBox({'min': ParseXY(min_x, min_y), 'max': ParseXY(max_x, max_y)})

    def _getRenderTreeText(self):
        render_strings = ['fp_circle']
        render_strings.append(self.center_pos.render('(center {x} {y})'))
        render_strings.append(self.end_pos.render('(end {x} {y})'))
        render_strings.append('(layer {layer})'.format(layer=self.layer))
        render_strings.append('(width {width})'.format(width=self.width))

        render_text = Node._getRenderTreeText(self)
        render_text += ' ({})'.format(' '.join(render_strings))

        return render_text
