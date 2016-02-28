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

from .kicad_util import formatFloat


class Point(object):
    def __init__(self, coordinates=None):
        if coordinates is None:
            coordinates = {}

        if isinstance(coordinates, Point):
            self.x = coordinates.x
            self.y = coordinates.y
            self.z = coordinates.z
            self.r = coordinates.r
            return

        if type(coordinates) is not dict:
            raise TypeError('dict type required')

        self.x = float(coordinates.get('x', 0))
        self.y = float(coordinates.get('y', 0))
        self.z = float(coordinates.get('z', 0))
        self.r = float(coordinates.get('r', 0))


    def render(self, formatcode):
        return formatcode.format(x=formatFloat(self.x)
                                ,y=formatFloat(self.y)
                                ,z=formatFloat(self.z)
                                ,r=formatFloat(self.r))


    def __dict__(self):
        return {'x':self.x, 'y':self.y, 'z':self.z, 'r':self.r}


    def __str__(self):
        return self.render("Point(x={x}, y={y}, z={z}, r={r})")


class PointXY(Point):
    def __init__(self, coordinates):
        if type(coordinates) is dict:
            Point.__init__(self, coordinates)
        elif type(coordinates) is list or type(coordinates) is tuple:
            Point.__init__(self)
            if len(coordinates) == 2:
                self.x = coordinates[0]
                self.y = coordinates[1]
            else:
                raise TypeError('invalid list size')
        else:
            raise TypeError('dict or list type required')


class PointXYR(Point):
    def __init__(self, coordinates):
        if type(coordinates) is dict or isinstance(coordinates, Point):
            Point.__init__(self, coordinates)
        elif type(coordinates) is list or type(coordinates) is tuple:
            Point.__init__(self)
            if len(coordinates) == 3:
                self.x = coordinates[0]
                self.y = coordinates[1]
                self.r = coordinates[2]
            else:
                raise TypeError('invalid list size')
        else:
            raise TypeError('dict or list type required')


class PointXYZ(Point):
    def __init__(self, coordinates):
        if type(coordinates) is dict or isinstance(coordinates, Point):
            Point.__init__(self, coordinates)
        elif type(coordinates) is list or type(coordinates) is tuple:
            Point.__init__(self)
            if len(coordinates) == 3:
                self.x = coordinates[0]
                self.y = coordinates[1]
                self.z = coordinates[2]
            else:
                raise TypeError('invalid list size')
        else:
            raise TypeError('dict or list type required')
