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

import math

from .Point import *
from .Node import Node


class Rotation(Node):
    '''
    Apply rotation to the child tree
    '''
    def __init__(self, r):
        Node.__init__(self)
        self.rotation = r # in degree


    def getRealPosition(self, coordinate):
        parsed_coordinate = Point(coordinate)

        phi = self.rotation*math.pi/180
        rotation_coordinate = {'x': parsed_coordinate.x*math.cos(phi) + parsed_coordinate.y*math.sin(phi)
                              ,'y': -parsed_coordinate.x*math.sin(phi) + parsed_coordinate.y*math.cos(phi)
                              ,'r': parsed_coordinate.r + self.rotation}

        if not self._parent:
            return rotation_coordinate
        else:
            return self._parent.getRealPosition(rotation_coordinate)


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [r: {r}]".format(r=self.rotation)

        return render_text
