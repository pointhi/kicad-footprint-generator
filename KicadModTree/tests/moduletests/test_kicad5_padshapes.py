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

from KicadModTree import *

RESULT_ROUNDRECT_FP = """(module round_rect_test (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value round_rect_test (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd roundrect (at 5 0 45) (size 1 1) (layers F.Cu F.Mask F.Paste) (roundrect_rratio 0.1))
  (pad 2 smd roundrect (at -5 0) (size 1 1) (layers F.Cu F.Mask F.Paste) (roundrect_rratio 0.5))
  (pad 1 smd roundrect (at 0 0) (size 1 1) (layers F.Cu F.Mask F.Paste) (roundrect_rratio 0))
)"""


class Kicad5PadsTests(unittest.TestCase):

    def testRoundRectPad(self):
        kicad_mod = Footprint("round_rect_test")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="round_rect_test", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[5, 0], rotation=45, size=[1, 1], layers=Pad.LAYERS_SMT,
                             radius_ratio=0.1))

        kicad_mod.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[-5, 0], size=[1, 1], layers=Pad.LAYERS_SMT,
                             radius_ratio=0.5))

        kicad_mod.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                             at=[0, 0], size=[1, 1], layers=Pad.LAYERS_SMT,
                             radius_ratio=0))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(result, RESULT_ROUNDRECT_FP)

    def testPolygonPad(self):
        kicad_mod = Footprint("round_rect_test")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="round_rect_test", at=[0, 0], layer='F.Fab'))


        kicad_mod.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                             at=[0, 0], size=[1, 1], layers=Pad.LAYERS_SMT,
                             primitives=[Polygon(nodes=[(-1, -1), (2, -1), (1, 1), (-1, 2)])]
                             ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test.kicad_mod')
        # self.assertEqual(result, RESULT_ROUNDRECT_FP)
