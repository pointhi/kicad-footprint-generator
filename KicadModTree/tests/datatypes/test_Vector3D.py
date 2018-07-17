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

import unittest

from KicadModTree.Vector import *


class Vector3DTests(unittest.TestCase):

    def test_init(self):
        p1 = Vector3D([1, 2, 3])
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)
        self.assertEqual(p1.z, 3)

        p1_xy = Vector3D([1, 2])
        self.assertEqual(p1_xy.x, 1)
        self.assertEqual(p1_xy.y, 2)
        self.assertEqual(p1_xy.z, 0)

        p2 = Vector3D((4, 5, 6))
        self.assertEqual(p2.x, 4)
        self.assertEqual(p2.y, 5)
        self.assertEqual(p2.z, 6)

        p2_xy = Vector3D((4, 5))
        self.assertEqual(p2_xy.x, 4)
        self.assertEqual(p2_xy.y, 5)
        self.assertEqual(p2_xy.z, 0)

        p3 = Vector3D({'x': 7, 'y': 8, 'z': 9})
        self.assertEqual(p3.x, 7)
        self.assertEqual(p3.y, 8)
        self.assertEqual(p3.z, 9)

        p3_xy = Vector3D({'x': 7, 'y': 8})
        self.assertEqual(p3_xy.x, 7)
        self.assertEqual(p3_xy.y, 8)
        self.assertEqual(p3_xy.z, 0)

        p3_empty = Vector3D({})
        self.assertEqual(p3_empty.x, 0)
        self.assertEqual(p3_empty.y, 0)
        self.assertEqual(p3_empty.z, 0)

        p4 = Vector3D(p1)
        self.assertEqual(p4.x, 1)
        self.assertEqual(p4.y, 2)
        self.assertEqual(p4.z, 3)

        p5 = Vector3D(1, 2, 3)
        self.assertEqual(p5.x, 1)
        self.assertEqual(p5.y, 2)
        self.assertEqual(p5.z, 3)

        p5_xy = Vector3D(1, 2)
        self.assertEqual(p5_xy.x, 1)
        self.assertEqual(p5_xy.y, 2)
        self.assertEqual(p5_xy.z, 0)

        # TODO: test float datatype
        # TODO: invalid type tests
        # TODO: tests if int is always converted to float

    def test_round_to(self):
        p1 = Vector3D([1.234, 5.678, 9.012]).round_to(0)
        self.assertAlmostEqual(p1.x, 1.234)
        self.assertAlmostEqual(p1.y, 5.678)
        self.assertAlmostEqual(p1.z, 9.012)

        p2 = Vector3D([1.234, 5.678, 9.012]).round_to(0.1)
        self.assertAlmostEqual(p2.x, 1.2)
        self.assertAlmostEqual(p2.y, 5.7)
        self.assertAlmostEqual(p2.z, 9)

        p3 = Vector3D([1.234, 5.678, 9.012]).round_to(0.01)
        self.assertAlmostEqual(p3.x, 1.23)
        self.assertAlmostEqual(p3.y, 5.68)
        self.assertAlmostEqual(p3.z, 9.01)

        p4 = Vector3D([1.234, 5.678, 9.012]).round_to(0.001)
        self.assertAlmostEqual(p4.x, 1.234)
        self.assertAlmostEqual(p4.y, 5.678)
        self.assertAlmostEqual(p4.z, 9.012)

        p5 = Vector3D([1.234, 5.678, 9.012]).round_to(0.0001)
        self.assertAlmostEqual(p5.x, 1.234)
        self.assertAlmostEqual(p5.y, 5.678)
        self.assertAlmostEqual(p5.z, 9.012)

    def test_add(self):
        p1 = Vector3D([1, 2, 3])
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

    def test_sub(self):
        p1 = Vector3D([1, 2, 3])
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

    def test_mul(self):
        p1 = Vector3D([1, 2, 3])
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
        self.assertEqual(p5.z, 0)

        # TODO: invalid type tests

    def test_div(self):
        p1 = Vector3D([1, 2, 3])
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

        # TODO: division by zero tests
        # TODO: invalid type tests
