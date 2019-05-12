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
# (C) 2016-2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import math
from KicadModTree.Vector import *
import copy


class geometricLine():
    r""" Handle the geometric side of lines

    :params:
        * *start* (``Vector2D``) --
          start point of the line
        * *end* (``Vector2D``) --
          end point of the line
    """

    def __init__(self, start, end):
        self.start_pos = start
        self.end_pos = end

    def rotate(self, angle, origin=(0, 0), use_degrees=True):
        r""" Rotate around given origin

        :params:
            * *angle* (``float``)
                rotation angle
            * *orign* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        self.start_pos.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        self.end_pos.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        return self

    def translate(self, distance_vector):
        r""" Translate

        :params:
            * *distance_vector* (``Vector2D``)
                2D vector defining by how much and in what direction to translate.
        """

        self.start_pos += distance_vector
        self.end_pos += distance_vector
        return self

    def isPointOnSelf(self, point, tolerance=1e-7):
        r""" is the given point on this line

        :params:
            * *point* (``Vector2D``)
                The point to be checked
            * *tolerance* (``float``)
                tolerance used to determine if the point is on the element
                default: 1e-7
        """

        ll, la = (self.end_pos - self.start_pos).to_polar()
        pl, pa = (point - self.start_pos).to_polar()
        return abs(la - pa) < tolerance and pl <= ll

    def sortPointsRelativeToStart(self, points):
        r""" sort given points releative to start point

        :params:
            * *points* (``[Vector2D]``)
                itterable of points
        """

        if len(points) < 2:
            return points

        if len(points) > 2:
            raise NotImplementedError("Sorting for more than 2 points not supported")

        if self.start_pos.distance_to(points[0]) < self.start_pos.distance_to(points[1]):
            return points
        else:
            return [points[1], points[0]]

    def cut(self, *other):
        r""" cut line with given other element

        :params:
            * *other* (``Line``, ``Circle``, ``Arc``)
                cut the element on any intersection with the given geometric element
        """

        ip = BaseNodeIntersection.intersectTwoNodes(self, *other)
        cp = []
        for p in ip:
            if self.isPointOnSelf(p):
                cp.append(p)

        sp = self.sortPointsRelativeToStart(cp)
        sp.insert(0, self.start_pos)
        sp.append(self.end_pos)

        r = []
        for i in range(len(sp)-1):
            r.append(geometricLine(start=sp[i], end=sp[i+1]))

        return r

    def to_homogeneous(self):
        r""" Get homogeneous representation of the line
        """
        p1 = self.start_pos.to_homogeneous()
        p2 = self.end_pos.to_homogeneous()
        return p1.cross_product(p2)

    def __iter__(self):
        yield self.start_pos
        yield self.end_pos

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0 or key == 'start':
            return self.start_pos
        if key == 1 or key == 'end':
            return self.end_pos

        raise IndexError('Index {} is out of range'.format(key))

    def __setitem__(self, key, item):
        if key == 0 or key == 'start':
            self.start_pos = item
        elif key == 1 or key == 'end':
            self.end_pos = item
        else:
            raise IndexError('Index {} is out of range'.format(key))


class geometricCircle():
    r"""Handle the geometric side of circles

    :params:
        * *center* (``Vector2D``) --
          center of the circle
        * *radius* (``float``) --
          radius of the circle
    """

    def __init__(self, center, radius):
        self.center_pos = center
        self.radius = radius

    def rotate(self, angle, origin=(0, 0), use_degrees=True):
        r""" Rotate around given origin

        :params:
            * *angle* (``float``)
                rotation angle
            * *orign* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        self.center_pos.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        return self

    def translate(self, distance_vector):
        r""" Translate

        :params:
            * *distance_vector* (``Vector2D``)
                2D vector defining by how much and in what direction to translate.
        """

        self.center_pos += distance_vector
        return self

    def isPointOnSelf(self, point, tolerance=1e-7):
        r""" is the given point on this circle

        :params:
            * *point* (``Vector2D``)
                The point to be checked
            * *tolerance* (``float``)
                tolerance used to determine if the point is on the element
                default: 1e-7
        """

        rad_p, ang_p = Vector2D(point).to_polar(orign=self.center_pos)
        return abs(self.radius - rad_p) < tolerance

    def sortPointsRelativeToStart(self, points):
        r""" sort given points releative to start point

        :params:
            * *points* (``[Vector2D]``)
                itterable of points
        """

        pass

    def cut(self, *other):
        r""" cut line with given other element

        :params:
            * *other* (``Line``, ``Circle``, ``Arc``)
                cut the element on any intersection with the given geometric element
        """

        pass

    def __iter__(self):
        yield self.center_pos

    def __len__(self):
        return 1

    def __getitem__(self, key):
        if key == 0 or key == 'center':
            return self.center_pos

        raise IndexError('Index {} is out of range'.format(key))

    def __setitem__(self, key, item):
        if key == 0 or key == 'center':
            self.center_pos = item
        else:
            raise IndexError('Index {} is out of range'.format(key))


class geometricArc():
    r""" Handle the geometric side of arcs

    :params:
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
    """

    def __init__(self, **kwargs):
        if 'center' in kwargs:
            if 'angle' in kwargs:
                self._initFromCenterAndAngle(**kwargs)
            elif 'end' in kwargs:
                self._initFromCenterAndEnd(**kwargs)
            else:
                raise KeyError('Arcs defined with center point must define either an angle or endpoint')
        else:
            raise NotImplementedError('3 point arcs are not implemented, center is always required.')

    def _initAngle(self, angle):
        self.angle = angle % (2*360)
        if self.angle > 360:
            self.angle -= 2*360

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
        r""" Rotate around given origin

        :params:
            * *angle* (``float``)
                rotation angle
            * *orign* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        self.center_pos.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        self.start_pos.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        return self

    def translate(self, distance_vector):
        r""" Translate

        :params:
            * *distance_vector* (``Vector2D``)
                2D vector defining by how much and in what direction to translate.
        """

        self.center_pos += distance_vector
        self.start_pos += distance_vector
        return self

    def getRadius(self):
        r, a = (self.start_pos - self.center_pos).to_polar()
        return r

    def isPointOnSelf(self, point, tolerance=1e-7):
        r""" is the given point on this arc

        :params:
            * *point* (``Vector2D``)
                The point to be checked
            * *tolerance* (``float``)
                tolerance used to determine if the point is on the element
                default: 1e-7
        """

        rad_p, ang_p = Vector2D(point).to_polar(orign=self.center_pos)
        rad_s, ang_s = self.start_pos.to_polar(orign=self.center_pos)
        ang_e = ang_s + self.angle

        raise NotImplementedError("Not yet done")
        return abs(rad_s - rad_p) < tolerance

    def sortPointsRelativeToStart(self, points):
        r""" sort given points releative to start point

        :params:
            * *points* (``[Vector2D]``)
                itterable of points
        """

        pass

    def cut(self, *other):
        r""" cut line with given other element

        :params:
            * *other* (``Line``, ``Circle``, ``Arc``)
                cut the element on any intersection with the given geometric element
        """

        pass

    def __iter__(self):
        yield self.center_pos
        yield self.start_pos

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0 or key == 'center':
            return self.center_pos
        if key == 1 or key == 'start':
            return self.start_pos

        raise IndexError('Index {} is out of range'.format(key))

    def __setitem__(self, key, item):
        if key == 0 or key == 'center':
            self.center_pos = item
        if key == 1 or key == 'start':
            return self.start_pos
        else:
            raise IndexError('Index {} is out of range'.format(key))


class BaseNodeIntersection():
    @staticmethod
    def intersectTwoNodes(*nodes):
        import KicadModTree.nodes.base.Line
        if len(nodes) < 2 or len(nodes) > 3:
            raise KeyError("intersectTwoNodes expects two node objects or a node and two vectors")

        circles = []
        lines = []
        vectors = []

        for n in nodes:
            if hasattr(n, 'getRadius') and hasattr(n, 'center_pos'):
                circles.append(n)
            elif hasattr(n, 'end_pos') and hasattr(n, 'start_pos'):
                lines.append(n)
            else:
                vectors.append(n)

        if len(vectors) == 2:
            lines.append(Line(start=vectors[0], end=vectors[1]))

        if len(lines) == 2:
            return BaseNodeIntersection.intersectTwoLines(*lines)
        if len(circles) == 2:
            raise NotImplementedError('intersection between circles is not supported')
        if len(lines) == 1 and len(circles) == 1:
            return BaseNodeIntersection.intersectLineWithCircle(lines[0], circles[0])

        raise NotImplementedError('unsupported combination of parameter types')

    @staticmethod
    def intersectTwoLines(line1, line2):
        # we use homogeneous coordinates here.
        l1 = line1.to_homogeneous()
        l2 = line2.to_homogeneous()

        ip = l1.cross_product(l2)
        if ip.z == 0:
            return []

        return [Vector2D.from_homogeneous(ip)]

    @staticmethod
    def intersectLineWithCircle(line, circle):
        # from http://mathworld.wolfram.com/Circle-LineIntersection.html
        # Equations are for circle center on (0, 0) so we translate everything
        # to the orign (well the line anyways as we do only need the radius of the circle)
        lt = copy.copy(line).translate(-circle.center_pos)

        d = lt.end_pos - lt.start_pos
        dr = math.hypot(d.x, d.y)
        D = lt.start_pos.x*lt.end_pos.y - lt.end_pos.x*lt.start_pos.y

        discriminant = circle.getRadius()**2 * dr**2 - D**2
        intersection = []
        if discriminant < 0:
            return intersection

        def calcPoint(x):
            return Vector2D({
                'x': (D*d.y + x*math.copysign(1, d.y)*d.x*math.sqrt(discriminant))/dr**2,
                'y': (-D*d.x + x*abs(d.y)*math.sqrt(discriminant))/dr**2
                }) + circle.center_pos

        intersection.append(calcPoint(1))
        if discriminant == 0:
            return intersection

        intersection.append(calcPoint(-1))
        return intersection
