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
# (C) 2018 by Rene Poeschl, github @poeschlr

import warnings

from KicadModTree.Vector import Vector2D
from KicadModTree.nodes.Node import Node


class PolygonPoints(object):
    r"""Representation of multiple points for creating polygons

    :Keyword Arguments:
        * *nodes* (``list(Point)``) --
          2D points describing the "polygon"
        * *polygone* (``list(Point)``) --
          alternative naming for the nodes parameter for backwards compatibility.
        * *x_mirror* (``[int, float](mirror offset)``) --
          mirror x direction around offset "point"
        * *y_mirror* (``[int, float](mirror offset)``) --
          mirror y direction around offset "point"

    :Example:

    >>> from KicadModTree import *
    >>> PolyPoint([(0, 0),(1, 0)])
    >>> PolyPoint([{'x': 0, 'y':0}, {'x': 1, 'y':0}])
    """
    def __init__(self, **kwargs):
        self._initMirror(**kwargs)
        self._initNodes(**kwargs)

    def _initNodes(self, **kwargs):
        self.nodes = []
        if 'nodes' in kwargs:
            for n in kwargs['nodes']:
                self.nodes.append(Vector2D(n))
            if 'polygone' in kwargs:
                raise KeyError('Use of "nodes" and "polygone" parameter at the same time is not supported.')
        elif 'polygone' in kwargs:
            warnings.warn(
                "polygone argument is deprecated, use nodes instead",
                DeprecationWarning
            )
            for n in kwargs['polygone']:
                self.nodes.append(Vector2D(n))
        else:
            raise KeyError('Either "nodes" or "polygone" parameter is required for creating a PolyPoint instance.')

        for point in self.nodes:
            if self.mirror[0] is not None:
                point.x = 2 * self.mirror[0] - point.x
            if self.mirror[1] is not None:
                point.y = 2 * self.mirror[1] - point.y

    def _initMirror(self, **kwargs):
        self.mirror = [None, None]
        if 'x_mirror' in kwargs and type(kwargs['x_mirror']) in [float, int]:
            self.mirror[0] = kwargs['x_mirror']
        if 'y_mirror' in kwargs and type(kwargs['y_mirror']) in [float, int]:
            self.mirror[1] = kwargs['y_mirror']

    def calculateBoundingBox(self):
        min = max = self.getRealPosition(self.nodes[0])

        for n in self.nodes:
            min.x = min([min.x, n.x])
            min.y = min([min.y, n.y])
            max.x = max([max.x, n.x])
            max.y = max([max.y, n.y])

        return Node.calculateBoundingBox({'min': min, 'max': max})

    def findNearestPoints(self, other):
        r""" Find the nearest points for two polygons

        Find the two points for both polygons that are nearest to each other.


        :param other: the polygon points of the other polygon
        :return: a tuble with the indexes of the two points
                 (pint in self, point in other)
        """

        min_distance = self[0].distance_to(other[0])
        pi = 0
        pj = 0
        for i in range(len(self)):
            for j in range(len(other)):
                d = self[i].distance_to(other[j])
                if d < min_distance:
                    pi = i
                    pj = j
                    min_distance = d

        return (pi, pj)

    def getPoints(self):
        r""" get the points contained within self

        :return: the array of points contained within this instance
        """
        return self.nodes

    def cut(self, other):
        r""" Cut other polygon points from self

        As kicad has no native support for cuting one polygon from the other,
        the cut is done by connecting the nearest points of the two polygons
        with two lines on top of each other.

        This function assumes that the other polygon is fully within this one.
        It also assumes that connecting the two nearest points creates a valid
        polygon. (There are no geometry checks)

        :param other: the polygon points that are cut from this polygon
        """

        warnings.warn(
            "No geometry checks are implement for cutting polygons.\n"
            "Make sure the second polygon is fully inside the main polygon\n"
            "Check resulting polygon carefully.",
            Warning
        )
        idx_self, idx_other = self.findNearestPoints(other)

        self.nodes.insert(idx_self+1, self[idx_self])
        for i in range(len(other)):
            self.nodes.insert(idx_self+1, other[(i+idx_other) % len(other)])

        self.nodes.insert(idx_self+1, other[idx_other])

    def rotate(self, angle, origin=(0, 0), use_degrees=True):
        r""" Rotate points around given origin

        :params:
            * *angle* (``float``)
                rotation angle
            * *origin* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        for p in self.nodes:
            p.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        return self

    def translate(self, distance_vector):
        r""" Translate points

        :params:
            * *distance_vector* (``Vector2D``)
                2D vector defining by how much and in what direction to translate.
        """

        for p in self.nodes:
            p += distance_vector
        return self

    def __copy__(self):
        return PolygonPoints(nodes=self.nodes)

    def __iter__(self):
        for n in self.nodes:
            yield n

    def __getitem__(self, idx):
        return self.nodes[idx]

    def __len__(self):
        return len(self.nodes)
