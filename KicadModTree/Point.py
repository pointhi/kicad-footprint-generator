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

from KicadModTree.util.kicad_util import formatFloat


class Point(object):
    def __init__(self, coordinates=None):
        if coordinates is None:
            coordinates = {}

        if isinstance(coordinates, Point):
            self.x = coordinates.x
            self.y = coordinates.y
            self.z = coordinates.z
            return

        if type(coordinates) is dict:
            self.x = float(coordinates.get('x', 0))
            self.y = float(coordinates.get('y', 0))
            self.z = float(coordinates.get('z', 0))

        elif type(coordinates) is list or type(coordinates) is tuple:
            if len(coordinates) >= 2:
                self.x = coordinates[0]
                self.y = coordinates[1]
            else:
                raise TypeError('invalid list size (to small)')

            if len(coordinates) == 3:
                self.z = coordinates[2]
            else:
                self.z = 0

            if len(coordinates) > 3:
                raise TypeError('invalid list size (to big)')

        else:
            raise TypeError('dict or list type required')


    def render(self, formatcode):
        return formatcode.format(x=formatFloat(self.x)
                                ,y=formatFloat(self.y)
                                ,z=formatFloat(self.z))


    def __dict__(self):
        return {'x':self.x, 'y':self.y, 'z':self.z}


    def __str__(self):
        return self.render("Point(x={x}, y={y}, z={z}")
