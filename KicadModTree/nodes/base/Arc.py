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
import math


class Arc(Node):
    r"""Add an Arc to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *center* (``Vector2D``) --
          center of arc
        * *start* (``Vector2D``) --
          start point of arc
        * *midpoint* (``Vector2D``) --
          alternative to start point
          point is on arc and defines point of equal distance to both arc ends
          arcs of this form are given as midpoint, center plus angle
        * *end* (``Vector2D``) --
          alternative to angle
          arcs of this form are given as start, end and center
        * *angle* (``float``) --
          angle of arc
        * *layer* (``str``) --
          layer on which the arc is drawn (default: 'F.SilkS')
        * *width* (``float``) --
          width of the arc line (default: None, which means auto detection)

    :Example:

    >>> from KicadModTree import *
    >>> Arc(center=[0, 0], start=[-1, 0], angle=180, layer='F.SilkS')
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self._initArcParams(**kwargs)

        self.layer = kwargs.get('layer', 'F.SilkS')
        self.width = kwargs.get('width')

    def _initAngle(self, angle):
        self.angle = angle % (2*360)
        if self.angle > 360:
            self.angle -= 2*360

    def _initArcParams(self, **kwargs):
        if 'center' in kwargs:
            if 'angle' in kwargs:
                self._initFromCenterAndAngle(**kwargs)
            elif 'end' in kwargs:
                self._initFromCenterAndEnd(**kwargs)
            else:
                raise KeyError('Arcs defined with center point must define either an angle or endpoint')
        else:
            raise NotImplementedError('3 point arcs are not implemented, center is always required.')

    def _initFromCenterAndAngle(self, **kwargs):
        self.center_pos = Vector2D(kwargs['center'])
        self._initAngle(kwargs['angle'])

        if 'start' in kwargs:
            self.start_pos = Vector2D(kwargs['start'])
        elif 'midpoint' in kwargs:
            mp_r, mp_a = Vector2D(kwargs['midpoint']).to_polar(
                origin=self.center_pos, use_degrees=True)

            self.start_pos = Vector2D.from_polar(
                radius=mp_r, angle=mp_a-self.angle/2,
                origin=self.center_pos, use_degrees=True)
        else:
            raise KeyError('Arcs defined with center and angle must either define the start or midpoint.')

    def _initFromCenterAndEnd(self, **kwargs):
        self.center_pos = Vector2D(kwargs['center'])
        if 'start' in kwargs:
            self.start_pos = Vector2D(kwargs['start'])
            sp_r, sp_a = self.start_pos.to_polar(
                origin=self.center_pos, use_degrees=True)
            ep_r, ep_a = Vector2D(kwargs['end']).to_polar(
                origin=self.center_pos, use_degrees=True)

            if abs(sp_r - ep_r) > 1e-7:
                warnings.warn(
                    """Start and end point are not an same arc.
                    Extended line from center to end point used to determine angle."""
                )
            # print("sr: {} sa: {} -- er: {} ea: {}".format(sp_r, sp_a, ep_r, ep_a))
            self._initAngle(ep_a - sp_a)

            if kwargs.get('long_way', False):
                if abs(self.angle) < 180:
                    self.angle = -math.copysign((360-abs(self.angle)), self.angle)
                if self.angle == -180:
                    self.angle = 180
            else:
                if abs(self.angle) > 180:
                    self.angle = -math.copysign((abs(self.angle) - 360), self.angle)
                if self.angle == 180:
                    self.angle = -180
        else:
            raise KeyError('Arcs defined with center and endpoint must define the start point.')

    def rotate(self, angle, origin=(0, 0), use_degrees=True):
        self.center_pos.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        self.start_pos.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        return self

    def calculateBoundingBox(self):
        # TODO: finish implementation
        min_x = min(self.start_pos.x, self._calulateEndPos().x)
        min_y = min(self.start_pos.x, self._calulateEndPos().y)
        max_x = max(self.start_pos.x, self._calulateEndPos().x)
        max_y = max(self.start_pos.x, self._calulateEndPos().y)

        '''
        for angle in range(4):
            float_angle = angle * math.pi/2.

            start_angle = _calculateStartAngle(self)
            end_angle = start_angle + math.radians(self.angle)

            # TODO: +- pi border
            if float_angle < start_angle:
                continue
            if float_angle > end_angle:
                continue

            print("TODO: add angle side: {1}".format(float_angle))
        '''

        return Node.calculateBoundingBox({'min': Vector2D((min_x, min_y)), 'max': Vector2D((max_x, max_y))})

    def _calulateEndPos(self):
        radius, angle = self.start_pos.to_polar(
            origin=self.center, use_degrees=True)

        return Vector2D.from_polar(
            radius=radius, angle=angle+self.angle,
            origin=self.center, use_degrees=True)

    def _getRenderTreeText(self):
        render_strings = ['fp_arc']
        render_strings.append(self.center_pos.render('(center {x} {y})'))
        render_strings.append(self.start_pos.render('(start {x} {y})'))
        render_strings.append('(angle {angle})'.format(angle=self.angle))
        render_strings.append('(layer {layer})'.format(layer=self.layer))
        render_strings.append('(width {width})'.format(width=self.width))

        render_text = Node._getRenderTreeText(self)
        render_text += ' ({})'.format(' '.join(render_strings))

        return render_text
