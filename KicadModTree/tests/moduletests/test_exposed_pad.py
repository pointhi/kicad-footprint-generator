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

RESULT_SIMPLE_EP_FP = """(module round_rect_test (layer F.Cu) (tedit 0)
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

RESULT_SIMPLE_EP_NO_ROUNDING_FP = """(module round_rect_test (layer F.Cu) (tedit 0)
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
  (pad "" smd rect (at -0.49109 0.33391) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at 0.49109 0.33391) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at -0.49109 1) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at 0.49109 1) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at -0.49109 1.66609) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at 0.49109 1.66609) (size 0.846537 0.564358) (layers F.Paste))
  (pad 3 thru_hole circle (at -0.75 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.75 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 1) (size 2.1 3) (layers B.Cu))
)"""

RESULT_MINIMAL_EP_SPECIFICATION = """(module round_rect_test (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value round_rect_test (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 2.1 3) (layers F.Cu F.Mask))
  (pad "" smd rect (at -0.49 -0.7) (size 0.85 1.21) (layers F.Paste))
  (pad "" smd rect (at 0.49 -0.7) (size 0.85 1.21) (layers F.Paste))
  (pad "" smd rect (at -0.49 0.7) (size 0.85 1.21) (layers F.Paste))
  (pad "" smd rect (at 0.49 0.7) (size 0.85 1.21) (layers F.Paste))
  (pad 3 thru_hole circle (at -0.75 -1.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 -1.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 -1.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.75 0) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 0) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 0) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.75 1.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 1.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 1.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 0) (size 2.1 3) (layers B.Cu))
)"""

RESULT_EP_PASTE_GEN_INNER = """(module round_rect_test (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value round_rect_test (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 5 5) (layers F.Cu F.Mask))
  (pad "" smd custom (at -1.466667 -1.466667) (size 1.117597 1.117597) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.671855 -0.511969) (xy -0.511969 -0.671855) (xy 0.671855 -0.671855) (xy 0.671855 0.671855)
         (xy -0.671855 0.671855)) (width 0))
    ))
  (pad "" smd rect (at -1.466667 0) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd custom (at -1.466667 1.466667) (size 1.117597 1.117597) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.671855 -0.671855) (xy 0.671855 -0.671855) (xy 0.671855 0.671855) (xy -0.511969 0.671855)
         (xy -0.671855 0.511969)) (width 0))
    ))
  (pad "" smd rect (at 0 -1.466667) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd rect (at 0 0) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd rect (at 0 1.466667) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd custom (at 1.466667 -1.466667) (size 1.117597 1.117597) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.671855 -0.671855) (xy 0.511969 -0.671855) (xy 0.671855 -0.511969) (xy 0.671855 0.671855)
         (xy -0.671855 0.671855)) (width 0))
    ))
  (pad "" smd rect (at 1.466667 0) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd custom (at 1.466667 1.466667) (size 1.117597 1.117597) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.671855 -0.671855) (xy 0.671855 -0.671855) (xy 0.671855 0.511969) (xy 0.511969 0.671855)
         (xy -0.671855 0.671855)) (width 0))
    ))
  (pad 3 thru_hole circle (at -2.2 -2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.2 -2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -2.2 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.2 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 0) (size 5 5) (layers B.Cu))
)"""

RESULT_EP_PASTE_GEN_INNER2 = """(module EP_PasteGen2 (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value EP_PasteGen2 (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 5 5) (layers F.Cu F.Mask))
  (pad "" smd custom (at -1.8375 -1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.8375 -1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at -1.8375 -0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.8375 0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at -1.8375 1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.8375 1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at -1.1025 -1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.1025 -1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.1025 -0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.1025 0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.1025 1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.1025 1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.3675 -1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.3675 -1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at -0.3675 -0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.3675 0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at -0.3675 1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.3675 1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at 0.3675 -1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 0.3675 -1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 0.3675 -0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 0.3675 0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 0.3675 1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 0.3675 1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1025 -1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1025 -1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at 1.1025 -0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1025 0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at 1.1025 1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.157529) (xy -0.157529 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1025 1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.157529 0.294628)
         (xy -0.294628 0.157529)) (width 0))
    ))
  (pad "" smd custom (at 1.8375 -1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.8375 -1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.8375 -0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.8375 0.3675) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.8375 1.1025) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.157529 -0.294628) (xy 0.294628 -0.157529) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.8375 1.8375) (size 0.395369 0.395369) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.157529) (xy 0.157529 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad 3 thru_hole circle (at -2.205 -2.205) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.735 -2.205) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.735 -2.205) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.205 -2.205) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -2.205 -0.735) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.735 -0.735) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.735 -0.735) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.205 -0.735) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -2.205 0.735) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.735 0.735) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.735 0.735) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.205 0.735) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -2.205 2.205) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.735 2.205) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.735 2.205) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.205 2.205) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 0) (size 5.01 5.01) (layers B.Cu))
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
        file_handler.writeFile('test1.kicad_mod')
        self.assertEqual(result, RESULT_SIMPLE_EP_FP)

    def testSimpleExposedPadNoRounding(self):
        kicad_mod = Footprint("round_rect_test")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="round_rect_test", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, at=[0, 1], size=[2.1, 3],
            mask_size=[2.1, 2.1], paste_layout=[2, 3], via_layout=[3, 2],
            grid_round_base=None, size_round_base=0
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(result, RESULT_SIMPLE_EP_NO_ROUNDING_FP)

    def testSimpleExposedMinimal(self):
        kicad_mod = Footprint("round_rect_test")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="round_rect_test", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[2.1, 3], paste_layout=2, via_layout=3
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(result, RESULT_MINIMAL_EP_SPECIFICATION)

    def testExposedPasteAutogenInner(self):
        kicad_mod = Footprint("round_rect_test")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="round_rect_test", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[5, 5], paste_layout=3, via_layout=2,
            paste_avoid_via=True
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        file_handler.writeFile('test.kicad_mod')
        self.assertEqual(result, RESULT_EP_PASTE_GEN_INNER)

    def testExposedPasteAutogenInner2(self):
        kicad_mod = Footprint("EP_PasteGen2")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="EP_PasteGen2", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[5, 5], paste_layout=6, via_layout=4,
            paste_avoid_via=True, paste_coverage=0.5
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(result, RESULT_EP_PASTE_GEN_INNER2)
