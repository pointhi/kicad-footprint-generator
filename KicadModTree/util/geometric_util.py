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
from KicadModTree.nodes.base import *
from KicadModTree.Vector import *


class BaseNodeIntersection():
    @staticmethod
    def intersectTwoNodes(*nodes):
        if len(nodes) < 2 or len(nodes) > 3:
            raise KeyError("intersectTwoNodes expects two node objects or a node and two vectors")

        circles = []
        lines = []
        vectors = []

        for n in nodes:
            if type(n) is Circle:
                circles.append(n)
            elif type(n) is Arc:
                circles.append(Circle(center=n.center_pos, radius=n.getRadius()))
            elif type(n) is Line:
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
            return None

        return Vector2D.from_homogeneous(ip)

    @staticmethod
    def intersectLineWithCircle(line, circle):
        # from http://mathworld.wolfram.com/Circle-LineIntersection.html
        # Equations are for circle center on (0, 0) so we translate everything
        # to the orign (well the line anyways as we do only need the radius of the circle)
        lt = Line(start=line.start_pos, end=line.end_pos).translate(-circle.center_pos)

        d = lt.end_pos - lt.start_pos
        dr = math.hypot(d.x, d.y)
        D = lt.start_pos.x*lt.end_pos.y - lt.end_pos.x*lt.start_pos.y

        discriminant = circle.radius**2 * dr**2 - D**2
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
