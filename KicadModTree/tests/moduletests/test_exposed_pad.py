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
  (pad "" smd rect (at 0 1) (size 2.1 2.1) (layers F.Mask))
  (pad 3 smd rect (at 0 1) (size 2.1 3) (layers F.Cu))
  (pad "" smd rect (at -0.49 0.34) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at 0.49 0.34) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at -0.49 1) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at 0.49 1) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at -0.49 1.66) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at 0.49 1.66) (size 0.85 0.56) (layers F.Paste))
  (pad 3 thru_hole circle (at -0.75 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.75 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 1) (size 2.1 3) (layers B.Cu))
)"""


class ExposedPadTests(unittest.TestCase):

    def testSimpleExposedPad(self):
        kicad_mod = Footprint("round_rect_test")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="round_rect_test", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, at=[0, 1], size=[2.1, 3],
            mask_size=[2.1, 2.1], paste_layout=[2, 3], via_layout=[3, 2]
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(result, RESULT_ROUNDRECT_FP)
