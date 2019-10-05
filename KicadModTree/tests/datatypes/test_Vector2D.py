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
# (C) 2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import unittest
import math
from KicadModTree.Vector import *


class Vector2DTests(unittest.TestCase):

    def test_init(self):
        p1 = Vector2D([1, 2])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)

        p2 = Vector2D((4, 5))
        self.assertEqual(p2.x, 4)
        self.assertEqual(p2.y, 5)

        p3 = Vector2D({'x': 7, 'y': 8})
        self.assertEqual(p3.x, 7)
        self.assertEqual(p3.y, 8)

        p3_empty = Vector2D({})
        self.assertEqual(p3_empty.x, 0)
        self.assertEqual(p3_empty.y, 0)

        p4 = Vector2D(p1)
        self.assertEqual(p4.x, 1)
        self.assertEqual(p4.y, 2)

        p5 = Vector2D(1, 2)
        self.assertEqual(p5.x, 1)
        self.assertEqual(p5.y, 2)

        # TODO: test float datatype
        # TODO: invalid type tests
        # TODO: tests if int is always converted to float

    def test_round_to(self):
        p1 = Vector2D([1.234, 5.678]).round_to(0)
        self.assertAlmostEqual(p1.x, 1.234)
        self.assertAlmostEqual(p1.y, 5.678)

        p2 = Vector2D([1.234, 5.678]).round_to(0.1)
        self.assertAlmostEqual(p2.x, 1.2)
        self.assertAlmostEqual(p2.y, 5.7)

        p3 = Vector2D([1.234, 5.678]).round_to(0.01)
        self.assertAlmostEqual(p3.x, 1.23)
        self.assertAlmostEqual(p3.y, 5.68)

        p4 = Vector2D([1.234, 5.678]).round_to(0.001)
        self.assertAlmostEqual(p4.x, 1.234)
        self.assertAlmostEqual(p4.y, 5.678)

        p5 = Vector2D([1.234, 5.678]).round_to(0.0001)
        self.assertAlmostEqual(p5.x, 1.234)
        self.assertAlmostEqual(p5.y, 5.678)

    def test_add(self):
        p1 = Vector2D([1, 2])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)

        p2 = p1 + 5
        self.assertEqual(p2.x, 6)
        self.assertEqual(p2.y, 7)

        p3 = p1 + (-5)
        self.assertEqual(p3.x, -4)
        self.assertEqual(p3.y, -3)

        p4 = p1 + [4, 2]
        self.assertEqual(p4.x, 5)
        self.assertEqual(p4.y, 4)

        p5 = p1 + [-5, -3]
        self.assertEqual(p5.x, -4)
        self.assertEqual(p5.y, -1)

        # TODO: invalid type tests

    def test_sub(self):
        p1 = Vector2D([1, 2])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)

        p2 = p1 - 5
        self.assertEqual(p2.x, -4)
        self.assertEqual(p2.y, -3)

        p3 = p1 - (-5)
        self.assertEqual(p3.x, 6)
        self.assertEqual(p3.y, 7)

        p4 = p1 - [4, 2]
        self.assertEqual(p4.x, -3)
        self.assertEqual(p4.y, 0)

        p5 = p1 - [-5, -3]
        self.assertEqual(p5.x, 6)
        self.assertEqual(p5.y, 5)

        # TODO: invalid type tests

    def test_mul(self):
        p1 = Vector2D([1, 2])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)

        p2 = p1 * 5
        self.assertEqual(p2.x, 5)
        self.assertEqual(p2.y, 10)

        p3 = p1 * (-5)
        self.assertEqual(p3.x, -5)
        self.assertEqual(p3.y, -10)

        p4 = p1 * [4, 5]
        self.assertEqual(p4.x, 4)
        self.assertEqual(p4.y, 10)

        p5 = p1 * [-5, -3]
        self.assertEqual(p5.x, -5)
        self.assertEqual(p5.y, -6)

        # TODO: invalid type tests

    def test_div(self):
        p1 = Vector2D([1, 2])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)

        p2 = p1 / 5
        self.assertEqual(p2.x, 0.2)
        self.assertEqual(p2.y, 0.4)

        p3 = p1 / (-5)
        self.assertEqual(p3.x, -0.2)
        self.assertEqual(p3.y, -0.4)

        p4 = p1 / [4, 5]
        self.assertEqual(p4.x, 0.25)
        self.assertEqual(p4.y, 0.4)

        p5 = p1 / [-5, -2]
        self.assertEqual(p5.x, -0.2)
        self.assertEqual(p5.y, -1)

        # TODO: division by zero tests
        # TODO: invalid type tests

    def test_polar(self):
        p1 = Vector2D.from_polar(math.sqrt(2), 45, use_degrees=True)
        self.assertAlmostEqual(p1.x, 1)
        self.assertAlmostEqual(p1.y, 1)

        p1 = Vector2D.from_polar(2, -90, use_degrees=True, origin=(6, 1))
        self.assertAlmostEqual(p1.x, 6)
        self.assertAlmostEqual(p1.y, -1)

        r, a = p1.to_polar(use_degrees=True, origin=(6, 1))
        self.assertAlmostEqual(r, 2)
        self.assertAlmostEqual(a, -90)

        p1.rotate(90, use_degrees=True, origin=(6, 1))
        self.assertAlmostEqual(p1.x, 8)
        self.assertAlmostEqual(p1.y, 1)

        p1 = Vector2D.from_polar(math.sqrt(2), 135, use_degrees=True)
        self.assertAlmostEqual(p1.x, -1)
        self.assertAlmostEqual(p1.y, 1)

        p1.rotate(90, use_degrees=True)
        self.assertAlmostEqual(p1.x, -1)
        self.assertAlmostEqual(p1.y, -1)

        r, a = p1.to_polar(use_degrees=True)
        self.assertAlmostEqual(r, math.sqrt(2))
        self.assertAlmostEqual(a, -135)
