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
from math import sqrt


class Vector2D(object):
    r"""Representation of a 2D Vector in space

    :Example:

    >>> from KicadModTree import *
    >>> Vector2D(0, 0)
    >>> Vector2D([0, 0])
    >>> Vector2D((0, 0))
    >>> Vector2D({'x': 0, 'y':0})
    >>> Vector2D(Vector2D(0, 0))
    """
    def __init__(self, coordinates=None, y=None):
        # parse constructor
        if coordinates is None:
            coordinates = {}
        elif type(coordinates) in [int, float]:
            if y is not None:
                coordinates = [coordinates, y]
            else:
                raise TypeError('you have to give x and y coordinate')
        elif isinstance(coordinates, Vector2D):
            # convert Vector2D as well as Vector3D to dict
            coordinates = coordinates.__dict__()

        # parse vectors with format: Vector2D({'x':0, 'y':0})
        if type(coordinates) is dict:
            self.x = float(coordinates.get('x', 0.))
            self.y = float(coordinates.get('y', 0.))
            return

        # parse vectors with format: Vector2D([0, 0]) or Vector2D((0, 0))
        if type(coordinates) in [list, tuple]:
            if len(coordinates) == 2:
                self.x = float(coordinates[0])
                self.y = float(coordinates[1])
                return
            else:
                raise TypeError('invalid list size (2 elements expected)')

        raise TypeError('invalid parameters given')

    def round_to(self, base):
        r"""Round to a specific base (like it's required for a grid)

        :param base: base we want to round to
        :return: rounded point

        >>> from KicadModTree import *
        >>> Vector2D(0.1234, 0.5678).round_to(0.01)
        """
        if base == 0:
            return self

        return Vector2D({'x': round(self.x / base) * base,
                        'y': round(self.y / base) * base})

    def distance_to(self, value):
        r"""Distance between this and another point

        :param value: the other point
        :return: distance between self and other point
        """
        other = Vector2D.__arithmetic_parse(value)
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    @staticmethod
    def __arithmetic_parse(value):
        if isinstance(value, Vector2D):
            return value
        elif type(value) in [int, float]:
            return Vector2D([value, value])
        else:
            return Vector2D(value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, value):
        other = Vector2D.__arithmetic_parse(value)

        return Vector2D({'x': self.x + other.x,
                        'y': self.y + other.y})

    def __sub__(self, value):
        other = Vector2D.__arithmetic_parse(value)

        return Vector2D({'x': self.x - other.x,
                        'y': self.y - other.y})

    def __mul__(self, value):
        other = Vector2D.__arithmetic_parse(value)

        return Vector2D({'x': self.x * other.x,
                        'y': self.y * other.y})

    def __div__(self, value):
        other = Vector2D.__arithmetic_parse(value)

        return Vector2D({'x': self.x / other.x,
                        'y': self.y / other.y})

    def __truediv__(self, obj):
        return self.__div__(obj)

    def __dict__(self):
        return {'x': self.x, 'y': self.y}

    def render(self, formatcode):
        warnings.warn(
            "render is deprecated, read values directly instead",
            DeprecationWarning
        )
        return formatcode.format(x=formatFloat(self.x),
                                 y=formatFloat(self.y))

    def __repr__(self):
        return "Vector2D (x={x}, y={y})".format(**self.__dict__())

    def __str__(self):
        return "(x={x}, y={y})".format(**self.__dict__())

    def __getitem__(self, item):
        if item == 0 or item == 'x':
            return self.x
        if item == 1 or item == 'y':
            return self.y

        raise IndexError('Index {} is out of range'.format(item))

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y


class Vector3D(Vector2D):
    r"""Representation of a 3D Vector in space

    :Example:

    >>> from KicadModTree import *
    >>> Vector3D(0, 0, 0)
    >>> Vector3D([0, 0, 0])
    >>> Vector3D((0, 0, 0))
    >>> Vector3D({'x': 0, 'y':0, 'z':0})
    >>> Vector3D(Vector2D(0, 0))
    >>> Vector3D(Vector3D(0, 0, 0))
    """

    def __init__(self, coordinates=None, y=None, z=None):
        # we don't need a super constructor here

        # parse constructor
        if coordinates is None:
            coordinates = {}
        elif type(coordinates) in [int, float]:
            if y is not None:
                if z is not None:
                    coordinates = [coordinates, y, z]
                else:
                    coordinates = [coordinates, y]
            else:
                raise TypeError('you have to give at least x and y coordinate')
        elif isinstance(coordinates, Vector2D):
            # convert Vector2D as well as Vector3D to dict
            coordinates = coordinates.__dict__()

        # parse vectors with format: Vector2D({'x':0, 'y':0})
        if type(coordinates) is dict:
            self.x = float(coordinates.get('x', 0.))
            self.y = float(coordinates.get('y', 0.))
            self.z = float(coordinates.get('z', 0.))
            return

        # parse vectors with format: Vector3D([0, 0]), Vector3D([0, 0, 0]) or Vector3D((0, 0)), Vector3D((0, 0, 0))
        if type(coordinates) in [list, tuple]:
            if len(coordinates) >= 2:
                self.x = float(coordinates[0])
                self.y = float(coordinates[1])
            else:
                raise TypeError('invalid list size (to small)')

            if len(coordinates) == 3:
                self.z = float(coordinates[2])
            else:
                self.z = 0.

            if len(coordinates) > 3:
                raise TypeError('invalid list size (to big)')

        else:
            raise TypeError('dict or list type required')

    def round_to(self, base):
        r"""Round to a specific base (like it's required for a grid)

        :param base: base we want to round to
        :return: rounded point

        >>> from KicadModTree import *
        >>> Vector3D(0.123, 0.456, 0.789).round_to(0.01)
        """
        if base == 0:
            return self

        return Vector3D({'x': round(self.x / base) * base,
                        'y': round(self.y / base) * base,
                        'z': round(self.z / base) * base})

    @staticmethod
    def __arithmetic_parse(value):
        if isinstance(value, Vector3D):
            return value
        elif type(value) in [int, float]:
            return Vector3D([value, value, value])
        else:
            return Vector3D(value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, value):
        other = Vector3D.__arithmetic_parse(value)

        return Vector3D({'x': self.x + other.x,
                        'y': self.y + other.y,
                        'z': self.z + other.z})

    def __sub__(self, value):
        other = Vector3D.__arithmetic_parse(value)

        return Vector3D({'x': self.x - other.x,
                        'y': self.y - other.y,
                        'z': self.z - other.z})

    def __mul__(self, value):
        other = Vector3D.__arithmetic_parse(value)

        return Vector3D({'x': self.x * other.x,
                        'y': self.y * other.y,
                        'z': self.z * other.z})

    def __div__(self, value):
        other = Vector3D.__arithmetic_parse(value)

        return Vector3D({'x': self.x / other.x,
                        'y': self.y / other.y,
                        'z': self.z / other.z})

    def __truediv__(self, obj):
        return self.__div__(obj)

    def __dict__(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def render(self, formatcode):
        warnings.warn(
            "render is deprecated, read values directly instead",
            DeprecationWarning
        )
        return formatcode.format(x=formatFloat(self.x),
                                 y=formatFloat(self.y),
                                 z=formatFloat(self.z))

    def __repr__(self):
        return "Vector3D (x={x}, y={y}, z={z})".format(**self.__dict__())

    def __str__(self):
        return "(x={x}, y={y}, z={z})".format(**self.__dict__())

    def __getitem__(self, item):
        if item == 0 or item == 'x':
            return self.x
        if item == 1 or item == 'y':
            return self.y
        if item == 2 or item == 'z':
            return self.z

        raise IndexError('Index {} is out of range'.format(item))

    def __len__(self):
        return 3

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
