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

import warnings

from KicadModTree.util.kicad_util import formatFloat
from KicadModTree.Vector import *
from math import sqrt


class Point2D(Vector2D):
    def __init__(self, coordinates=None, y=None):
        Vector2D.__init__(self, coordinates, y)
        warnings.warn(
            "Point2D is deprecated, use Vector2D instead",
            DeprecationWarning
        )


class Point3D(Vector3D):
    def __init__(self, coordinates=None, y=None, z=None):
        Vector3D.__init__(self, coordinates, y, z)
        warnings.warn(
            "Point3D is deprecated, use Vector3D instead",
            DeprecationWarning
        )


class Point(Vector3D):
    def __init__(self, coordinates=None, y=None, z=None):
        Vector3D.__init__(self, coordinates, y, z)
        warnings.warn(
            "Point is deprecated, use Vector2D or Vector3D instead",
            DeprecationWarning
        )
