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
'''

import unittest

from KicadModTree.Point import *


class PointTests(unittest.TestCase):

    def testInit(self):
        p1 = Point([1, 2, 3])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)
        self.assertEqual(p1.z, 3)

        p1_xy = Point([1, 2])
        self.assertEqual(p1_xy.x, 1)
        self.assertEqual(p1_xy.y, 2)
        self.assertEqual(p1_xy.z, 0)

        p2 = Point((4, 5, 6))
        self.assertEqual(p2.x, 4)
        self.assertEqual(p2.y, 5)
        self.assertEqual(p2.z, 6)

        p2_xy = Point((4, 5))
        self.assertEqual(p2_xy.x, 4)
        self.assertEqual(p2_xy.y, 5)
        self.assertEqual(p2_xy.z, 0)

        p3 = Point({'x':7, 'y':8, 'z':9})
        self.assertEqual(p3.x, 7)
        self.assertEqual(p3.y, 8)
        self.assertEqual(p3.z, 9)

        p3_xy = Point({'x':7, 'y':8})
        self.assertEqual(p3_xy.x, 7)
        self.assertEqual(p3_xy.y, 8)
        self.assertEqual(p3_xy.z, 0)

        p3_empty = Point({})
        self.assertEqual(p3_empty.x, 0)
        self.assertEqual(p3_empty.y, 0)
        self.assertEqual(p3_empty.z, 0)

        p4 = Point(p1)
        self.assertEqual(p4.x, 1)
        self.assertEqual(p4.y, 2)
        self.assertEqual(p4.z, 3)

        # TODO: test float datatype
        # TODO: invalid type tests


    def testAdd(self):
        p1 = Point([1, 2, 3])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)
        self.assertEqual(p1.z, 3)

        p2 = p1 + 5
        self.assertEqual(p2.x, 6)
        self.assertEqual(p2.y, 7)
        self.assertEqual(p2.z, 8)

        p3 = p1 + (-5)
        self.assertEqual(p3.x, -4)
        self.assertEqual(p3.y, -3)
        self.assertEqual(p3.z, -2)

        p4 = p1 + [4, 2, -2]
        self.assertEqual(p4.x, 5)
        self.assertEqual(p4.y, 4)
        self.assertEqual(p4.z, 1)

        p5 = p1 + [-5, -3]
        self.assertEqual(p5.x, -4)
        self.assertEqual(p5.y, -1)
        self.assertEqual(p5.z, 3)

        # TODO: invalid type tests


    def testSub(self):
        p1 = Point([1, 2, 3])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)
        self.assertEqual(p1.z, 3)

        p2 = p1 - 5
        self.assertEqual(p2.x, -4)
        self.assertEqual(p2.y, -3)
        self.assertEqual(p2.z, -2)

        p3 = p1 - (-5)
        self.assertEqual(p3.x, 6)
        self.assertEqual(p3.y, 7)
        self.assertEqual(p3.z, 8)

        p4 = p1 - [4, 2, -2]
        self.assertEqual(p4.x, -3)
        self.assertEqual(p4.y, 0)
        self.assertEqual(p4.z, 5)

        p5 = p1 - [-5, -3]
        self.assertEqual(p5.x, 6)
        self.assertEqual(p5.y, 5)
        self.assertEqual(p5.z, 3)

        # TODO: invalid type tests


    def testMul(self):
        p1 = Point([1, 2, 3])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)
        self.assertEqual(p1.z, 3)

        p2 = p1 * 5
        self.assertEqual(p2.x, 5)
        self.assertEqual(p2.y, 10)
        self.assertEqual(p2.z, 15)

        p3 = p1 * (-5)
        self.assertEqual(p3.x, -5)
        self.assertEqual(p3.y, -10)
        self.assertEqual(p3.z, -15)

        p4 = p1 * [4, 5, -2]
        self.assertEqual(p4.x, 4)
        self.assertEqual(p4.y, 10)
        self.assertEqual(p4.z, -6)

        p5 = p1 * [-5, -3]
        self.assertEqual(p5.x, -5)
        self.assertEqual(p5.y, -6)
        self.assertEqual(p5.z, 3)

        # TODO: invalid type tests

    def testDiv(self):
        p1 = Point([1, 2, 3])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)
        self.assertEqual(p1.z, 3)

        p2 = p1 / 5
        self.assertEqual(p2.x, 0.2)
        self.assertEqual(p2.y, 0.4)
        self.assertEqual(p2.z, 0.6)

        p3 = p1 / (-5)
        self.assertEqual(p3.x, -0.2)
        self.assertEqual(p3.y, -0.4)
        self.assertEqual(p3.z, -0.6)

        p4 = p1 / [4, 5, -2]
        self.assertEqual(p4.x, 0.25)
        self.assertEqual(p4.y, 0.4)
        self.assertEqual(p4.z, -1.5)

        p5 = p1 / [-5, -2]
        self.assertEqual(p5.x, -0.2)
        self.assertEqual(p5.y, -1)
        self.assertEqual(p5.z, 3)

        # TODO: division by zero tests
        # TODO: invalid type tests
