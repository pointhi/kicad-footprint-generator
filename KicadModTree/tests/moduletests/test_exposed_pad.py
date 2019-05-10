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
# (C) 2018 by Rene Poeschl, github @poeschlr

import unittest

from KicadModTree import *

RESULT_SIMPLE_EP_FP = """(module simple_exposed (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value simple_exposed (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "" smd rect (at 0 1) (size 2.1 2.1) (layers F.Mask))
  (pad 3 smd rect (at 0 1) (size 2.1 3) (layers F.Cu))
  (pad 3 thru_hole circle (at -0.75 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.75 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 1) (size 2.1 3) (layers B.Cu))
  (pad "" smd rect (at -0.525 0.3) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at -0.525 1) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at -0.525 1.7) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at 0.525 0.3) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at 0.525 1) (size 0.85 0.56) (layers F.Paste))
  (pad "" smd rect (at 0.525 1.7) (size 0.85 0.56) (layers F.Paste))
)"""

RESULT_SIMPLE_EP_NO_ROUNDING_FP = """(module simple_exposed (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value simple_exposed (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "" smd rect (at 0 1) (size 2.1 2.1) (layers F.Mask))
  (pad 3 smd rect (at 0 1) (size 2.1 3) (layers F.Cu))
  (pad 3 thru_hole circle (at -0.75 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 -0.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.75 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.75 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 1) (size 2.1 3) (layers B.Cu))
  (pad "" smd rect (at -0.525 0.3) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at -0.525 1) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at -0.525 1.7) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at 0.525 0.3) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at 0.525 1) (size 0.846537 0.564358) (layers F.Paste))
  (pad "" smd rect (at 0.525 1.7) (size 0.846537 0.564358) (layers F.Paste))
)"""

RESULT_MINIMAL_EP_SPECIFICATION = """(module simple_exposed (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value simple_exposed (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 2.1 3) (layers F.Cu F.Mask))
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
  (pad "" smd rect (at -0.525 -0.75) (size 0.85 1.21) (layers F.Paste))
  (pad "" smd rect (at -0.525 0.75) (size 0.85 1.21) (layers F.Paste))
  (pad "" smd rect (at 0.525 -0.75) (size 0.85 1.21) (layers F.Paste))
  (pad "" smd rect (at 0.525 0.75) (size 0.85 1.21) (layers F.Paste))
)"""

RESULT_EP_PASTE_GEN_INNER = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 5 5) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at -2.2 -2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.2 -2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -2.2 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.2 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 0) (size 5 5) (layers B.Cu))
  (pad "" smd custom (at -1.466667 -1.466667) (size 1.230653 1.230653) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.671855 -0.511969) (xy -0.511969 -0.671855) (xy 0.671855 -0.671855) (xy 0.671855 0.671855)
         (xy -0.671855 0.671855)) (width 0))
    ))
  (pad "" smd rect (at -1.466667 0) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd custom (at -1.466667 1.466667) (size 1.230653 1.230653) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.671855 -0.671855) (xy 0.671855 -0.671855) (xy 0.671855 0.671855) (xy -0.511969 0.671855)
         (xy -0.671855 0.511969)) (width 0))
    ))
  (pad "" smd rect (at 0 -1.466667) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd rect (at 0 0) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd rect (at 0 1.466667) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd custom (at 1.466667 -1.466667) (size 1.230653 1.230653) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.671855 -0.671855) (xy 0.511969 -0.671855) (xy 0.671855 -0.511969) (xy 0.671855 0.671855)
         (xy -0.671855 0.671855)) (width 0))
    ))
  (pad "" smd rect (at 1.466667 0) (size 1.34371 1.34371) (layers F.Paste))
  (pad "" smd custom (at 1.466667 1.466667) (size 1.230653 1.230653) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.671855 -0.671855) (xy 0.671855 -0.671855) (xy 0.671855 0.511969) (xy 0.511969 0.671855)
         (xy -0.671855 0.671855)) (width 0))
    ))
)"""

RESULT_EP_PASTE_GEN_INNER2 = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 5 5) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at -2.2 -2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.733333 -2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.733333 -2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.2 -2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -2.2 -0.733333) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.733333 -0.733333) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.733333 -0.733333) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.2 -0.733333) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -2.2 0.733333) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.733333 0.733333) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.733333 0.733333) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.2 0.733333) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -2.2 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -0.733333 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0.733333 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.2 2.2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 0) (size 5 5) (layers B.Cu))
  (pad "" smd custom (at -1.833333 -1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.833333 -1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at -1.1 -1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.1 -1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.833333 -0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.833333 0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at -1.1 -0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.1 0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.833333 1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.833333 1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at -1.1 1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -1.1 1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.366667 -1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.366667 -1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at 0.366667 -1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 0.366667 -1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.366667 -0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.366667 0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at 0.366667 -0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 0.366667 0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.366667 1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at -0.366667 1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at 0.366667 1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 0.366667 1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1 -1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1 -1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at 1.833333 -1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.833333 -1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1 -0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1 0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at 1.833333 -0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.833333 0.366667) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1 1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.155863) (xy -0.155863 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.1 1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.294628) (xy -0.155863 0.294628)
         (xy -0.294628 0.155863)) (width 0))
    ))
  (pad "" smd custom (at 1.833333 1.1) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.155863 -0.294628) (xy 0.294628 -0.155863) (xy 0.294628 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
  (pad "" smd custom (at 1.833333 1.833333) (size 0.491134 0.491134) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.294628 -0.294628) (xy 0.294628 -0.294628) (xy 0.294628 0.155863) (xy 0.155863 0.294628)
         (xy -0.294628 0.294628)) (width 0))
    ))
)"""

RESULT_EP_PASTE_GEN_INNER_AND_OUTHER = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 7 5) (size 12 8) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at 4 3) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 7 3) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 10 3) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 4 5) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 7 5) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 10 5) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 4 7) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 7 7) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 10 7) (size 0.8 0.8) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 7 5) (size 6.8 4.8) (layers B.Cu))
  (pad "" smd custom (at 4.75 3.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 4.75 4.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd custom (at 6.25 3.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 6.25 4.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 4.75 5.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 4.75 6.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd custom (at 6.25 5.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 6.25 6.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 7.75 3.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 7.75 4.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd custom (at 9.25 3.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 9.25 4.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 7.75 5.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 7.75 6.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd custom (at 9.25 5.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 9.25 6.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 1.75 3.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 1.75 4.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 3.25 3.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 3.25 4.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 1.75 5.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 1.75 6.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 3.25 5.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 3.25 6.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 10.75 3.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 10.75 4.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd rect (at 12.25 3.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 12.25 4.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 10.75 5.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 10.75 6.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd rect (at 12.25 5.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 12.25 6.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 4.75 1.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 4.75 2.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd rect (at 6.25 1.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 6.25 2.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 7.75 1.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 7.75 2.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd rect (at 9.25 1.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 9.25 2.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd custom (at 4.75 7.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 4.75 8.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 6.25 7.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 6.25 8.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 7.75 7.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 7.75 8.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 9.25 7.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 9.25 8.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 1.75 1.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 1.75 2.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 3.25 1.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 3.25 2.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.05682) (xy 0.265985 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 1.75 7.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 1.75 8.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 3.25 7.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.265985 -0.41833) (xy 0.627495 -0.05682) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 3.25 8.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 10.75 1.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 10.75 2.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833) (xy -0.265985 0.41833)
         (xy -0.627495 0.05682)) (width 0))
    ))
  (pad "" smd rect (at 12.25 1.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 12.25 2.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd custom (at 10.75 7.5) (size 0.581034 0.581034) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.627495 -0.05682) (xy -0.265985 -0.41833) (xy 0.627495 -0.41833) (xy 0.627495 0.41833)
         (xy -0.627495 0.41833)) (width 0))
    ))
  (pad "" smd rect (at 10.75 8.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 12.25 7.5) (size 1.25499 0.83666) (layers F.Paste))
  (pad "" smd rect (at 12.25 8.5) (size 1.25499 0.83666) (layers F.Paste))
)"""

RESULT_EP_PASTE_GEN_INNER_ONLY_Y_AND_OUTHER = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 3 5) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at 0 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 0) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 0) (size 0.6 4.6) (layers B.Cu))
  (pad "" smd rect (at -1.125 -1.5) (size 0.604669 0.806226) (layers F.Paste))
  (pad "" smd rect (at -1.125 -0.5) (size 0.604669 0.806226) (layers F.Paste))
  (pad "" smd custom (at -0.375 -1.5) (size 0.424561 0.424561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.403113) (xy 0.047623 -0.403113) (xy 0.302335 -0.148401) (xy 0.302335 0.403113)
         (xy -0.302335 0.403113)) (width 0))
    ))
  (pad "" smd custom (at -0.375 -0.5) (size 0.424561 0.424561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.403113) (xy 0.302335 -0.403113) (xy 0.302335 0.148401) (xy 0.047623 0.403113)
         (xy -0.302335 0.403113)) (width 0))
    ))
  (pad "" smd rect (at -1.125 0.5) (size 0.604669 0.806226) (layers F.Paste))
  (pad "" smd rect (at -1.125 1.5) (size 0.604669 0.806226) (layers F.Paste))
  (pad "" smd custom (at -0.375 0.5) (size 0.424561 0.424561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.403113) (xy 0.047623 -0.403113) (xy 0.302335 -0.148401) (xy 0.302335 0.403113)
         (xy -0.302335 0.403113)) (width 0))
    ))
  (pad "" smd custom (at -0.375 1.5) (size 0.424561 0.424561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.403113) (xy 0.302335 -0.403113) (xy 0.302335 0.148401) (xy 0.047623 0.403113)
         (xy -0.302335 0.403113)) (width 0))
    ))
  (pad "" smd custom (at 0.375 -1.5) (size 0.424561 0.424561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.148401) (xy -0.047623 -0.403113) (xy 0.302335 -0.403113) (xy 0.302335 0.403113)
         (xy -0.302335 0.403113)) (width 0))
    ))
  (pad "" smd custom (at 0.375 -0.5) (size 0.424561 0.424561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.403113) (xy 0.302335 -0.403113) (xy 0.302335 0.403113) (xy -0.047623 0.403113)
         (xy -0.302335 0.148401)) (width 0))
    ))
  (pad "" smd rect (at 1.125 -1.5) (size 0.604669 0.806226) (layers F.Paste))
  (pad "" smd rect (at 1.125 -0.5) (size 0.604669 0.806226) (layers F.Paste))
  (pad "" smd custom (at 0.375 0.5) (size 0.424561 0.424561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.148401) (xy -0.047623 -0.403113) (xy 0.302335 -0.403113) (xy 0.302335 0.403113)
         (xy -0.302335 0.403113)) (width 0))
    ))
  (pad "" smd custom (at 0.375 1.5) (size 0.424561 0.424561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.403113) (xy 0.302335 -0.403113) (xy 0.302335 0.403113) (xy -0.047623 0.403113)
         (xy -0.302335 0.148401)) (width 0))
    ))
  (pad "" smd rect (at 1.125 0.5) (size 0.604669 0.806226) (layers F.Paste))
  (pad "" smd rect (at 1.125 1.5) (size 0.604669 0.806226) (layers F.Paste))
  (pad "" smd rect (at -1.125 -2.25) (size 0.604669 0.403113) (layers F.Paste))
  (pad "" smd custom (at -0.375 -2.25) (size 0.18875 0.18875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.201556) (xy 0.302335 -0.201556) (xy 0.302335 -0.101599) (xy -0.000821 0.201556)
         (xy -0.302335 0.201556)) (width 0))
    ))
  (pad "" smd rect (at -1.125 2.25) (size 0.604669 0.403113) (layers F.Paste))
  (pad "" smd custom (at -0.375 2.25) (size 0.18875 0.18875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.201556) (xy -0.000821 -0.201556) (xy 0.302335 0.101599) (xy 0.302335 0.201556)
         (xy -0.302335 0.201556)) (width 0))
    ))
  (pad "" smd custom (at 0.375 -2.25) (size 0.18875 0.18875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 -0.201556) (xy 0.302335 -0.201556) (xy 0.302335 0.201556) (xy 0.000821 0.201556)
         (xy -0.302335 -0.101599)) (width 0))
    ))
  (pad "" smd rect (at 1.125 -2.25) (size 0.604669 0.403113) (layers F.Paste))
  (pad "" smd custom (at 0.375 2.25) (size 0.18875 0.18875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.302335 0.101599) (xy 0.000821 -0.201556) (xy 0.302335 -0.201556) (xy 0.302335 0.201556)
         (xy -0.302335 0.201556)) (width 0))
    ))
  (pad "" smd rect (at 1.125 2.25) (size 0.604669 0.403113) (layers F.Paste))
)"""

RESULT_EP_PASTE_GEN_INNER_ONLY_X_AND_OUTHER = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 4 3) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at -1 0) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 0 0) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 1 0) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 0) (size 2.6 0.6) (layers B.Cu))
  (pad "" smd rect (at -0.75 -1.125) (size 0.403113 0.604669) (layers F.Paste))
  (pad "" smd custom (at -0.75 -0.375) (size 0.33875 0.33875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.201556 -0.302335) (xy 0.201556 -0.302335) (xy 0.201556 0.302335) (xy -0.110533 0.302335)
         (xy -0.201556 0.211312)) (width 0))
    ))
  (pad "" smd rect (at -0.25 -1.125) (size 0.403113 0.604669) (layers F.Paste))
  (pad "" smd custom (at -0.25 -0.375) (size 0.33875 0.33875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.201556 -0.302335) (xy 0.201556 -0.302335) (xy 0.201556 0.211312) (xy 0.110533 0.302335)
         (xy -0.201556 0.302335)) (width 0))
    ))
  (pad "" smd rect (at 0.25 -1.125) (size 0.403113 0.604669) (layers F.Paste))
  (pad "" smd custom (at 0.25 -0.375) (size 0.33875 0.33875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.201556 -0.302335) (xy 0.201556 -0.302335) (xy 0.201556 0.302335) (xy -0.110533 0.302335)
         (xy -0.201556 0.211312)) (width 0))
    ))
  (pad "" smd rect (at 0.75 -1.125) (size 0.403113 0.604669) (layers F.Paste))
  (pad "" smd custom (at 0.75 -0.375) (size 0.33875 0.33875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.201556 -0.302335) (xy 0.201556 -0.302335) (xy 0.201556 0.211312) (xy 0.110533 0.302335)
         (xy -0.201556 0.302335)) (width 0))
    ))
  (pad "" smd custom (at -0.75 0.375) (size 0.33875 0.33875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.201556 -0.211312) (xy -0.110533 -0.302335) (xy 0.201556 -0.302335) (xy 0.201556 0.302335)
         (xy -0.201556 0.302335)) (width 0))
    ))
  (pad "" smd rect (at -0.75 1.125) (size 0.403113 0.604669) (layers F.Paste))
  (pad "" smd custom (at -0.25 0.375) (size 0.33875 0.33875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.201556 -0.302335) (xy 0.110533 -0.302335) (xy 0.201556 -0.211312) (xy 0.201556 0.302335)
         (xy -0.201556 0.302335)) (width 0))
    ))
  (pad "" smd rect (at -0.25 1.125) (size 0.403113 0.604669) (layers F.Paste))
  (pad "" smd custom (at 0.25 0.375) (size 0.33875 0.33875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.201556 -0.211312) (xy -0.110533 -0.302335) (xy 0.201556 -0.302335) (xy 0.201556 0.302335)
         (xy -0.201556 0.302335)) (width 0))
    ))
  (pad "" smd rect (at 0.25 1.125) (size 0.403113 0.604669) (layers F.Paste))
  (pad "" smd custom (at 0.75 0.375) (size 0.33875 0.33875) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.201556 -0.302335) (xy 0.110533 -0.302335) (xy 0.201556 -0.211312) (xy 0.201556 0.302335)
         (xy -0.201556 0.302335)) (width 0))
    ))
  (pad "" smd rect (at 0.75 1.125) (size 0.403113 0.604669) (layers F.Paste))
  (pad "" smd rect (at -1.5 -1.125) (size 0.806226 0.604669) (layers F.Paste))
  (pad "" smd custom (at -1.5 -0.375) (size 0.574561 0.574561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.403113 -0.302335) (xy 0.403113 -0.302335) (xy 0.403113 0.259755) (xy 0.360533 0.302335)
         (xy -0.403113 0.302335)) (width 0))
    ))
  (pad "" smd custom (at -1.5 0.375) (size 0.574561 0.574561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.403113 -0.302335) (xy 0.360533 -0.302335) (xy 0.403113 -0.259755) (xy 0.403113 0.302335)
         (xy -0.403113 0.302335)) (width 0))
    ))
  (pad "" smd rect (at -1.5 1.125) (size 0.806226 0.604669) (layers F.Paste))
  (pad "" smd rect (at 1.5 -1.125) (size 0.806226 0.604669) (layers F.Paste))
  (pad "" smd custom (at 1.5 -0.375) (size 0.574561 0.574561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.403113 -0.302335) (xy 0.403113 -0.302335) (xy 0.403113 0.302335) (xy -0.360533 0.302335)
         (xy -0.403113 0.259755)) (width 0))
    ))
  (pad "" smd custom (at 1.5 0.375) (size 0.574561 0.574561) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.403113 -0.259755) (xy -0.360533 -0.302335) (xy 0.403113 -0.302335) (xy 0.403113 0.302335)
         (xy -0.403113 0.302335)) (width 0))
    ))
  (pad "" smd rect (at 1.5 1.125) (size 0.806226 0.604669) (layers F.Paste))
)"""

RESULT_EP_PASTE_GEN_ONLY_OUTHER = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at 0 0) (size 2 2) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at 0 0) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 0) (size 0.6 0.6) (layers B.Cu))
  (pad "" smd custom (at -0.5 -0.5) (size 0.743245 0.743245) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.403113 -0.403113) (xy 0.403113 -0.403113) (xy 0.403113 0.314044) (xy 0.314044 0.403113)
         (xy -0.403113 0.403113)) (width 0))
    ))
  (pad "" smd custom (at -0.5 0.5) (size 0.743245 0.743245) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.403113 -0.403113) (xy 0.314044 -0.403113) (xy 0.403113 -0.314044) (xy 0.403113 0.403113)
         (xy -0.403113 0.403113)) (width 0))
    ))
  (pad "" smd custom (at 0.5 -0.5) (size 0.743245 0.743245) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.403113 -0.403113) (xy 0.403113 -0.403113) (xy 0.403113 0.403113) (xy -0.314044 0.403113)
         (xy -0.403113 0.314044)) (width 0))
    ))
  (pad "" smd custom (at 0.5 0.5) (size 0.743245 0.743245) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.403113 -0.314044) (xy -0.314044 -0.403113) (xy 0.403113 -0.403113) (xy 0.403113 0.403113)
         (xy -0.403113 0.403113)) (width 0))
    ))
)"""

RESULT_EP_BOTTOM_PAD = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at -2 -2) (size 2 2) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at -2 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad "" smd rect (at -2 -2) (size 1.61 1.61) (layers F.Paste))
  (pad 3 smd rect (at 2 -2) (size 2 2) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at 2 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 2 -2) (size 3 3) (layers B.Cu B.Mask))
  (pad "" smd rect (at 2 -2) (size 1.61 1.61) (layers F.Paste))
)"""

RESULT_EP_4x4 = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 33 smd rect (at 0 0) (size 3.55 3.55) (layers F.Cu F.Mask))
  (pad 33 thru_hole circle (at -1 -1) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 thru_hole circle (at 0 -1) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 thru_hole circle (at 1 -1) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 thru_hole circle (at -1 0) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 thru_hole circle (at 0 0) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 thru_hole circle (at 1 0) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 thru_hole circle (at -1 1) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 thru_hole circle (at 0 1) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 thru_hole circle (at 1 1) (size 0.5 0.5) (drill 0.2) (layers *.Cu))
  (pad 33 smd rect (at 0 0) (size 2.5 2.5) (layers B.Cu))
  (pad "" smd custom (at -0.5 -0.5) (size 0.733981 0.733981) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.387298 -0.329859) (xy -0.329859 -0.387298) (xy 0.329859 -0.387298) (xy 0.387298 -0.329859)
         (xy 0.387298 0.329859) (xy 0.329859 0.387298) (xy -0.329859 0.387298) (xy -0.387298 0.329859)) (width 0))
    ))
  (pad "" smd custom (at -0.5 0.5) (size 0.733981 0.733981) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.387298 -0.329859) (xy -0.329859 -0.387298) (xy 0.329859 -0.387298) (xy 0.387298 -0.329859)
         (xy 0.387298 0.329859) (xy 0.329859 0.387298) (xy -0.329859 0.387298) (xy -0.387298 0.329859)) (width 0))
    ))
  (pad "" smd custom (at 0.5 -0.5) (size 0.733981 0.733981) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.387298 -0.329859) (xy -0.329859 -0.387298) (xy 0.329859 -0.387298) (xy 0.387298 -0.329859)
         (xy 0.387298 0.329859) (xy 0.329859 0.387298) (xy -0.329859 0.387298) (xy -0.387298 0.329859)) (width 0))
    ))
  (pad "" smd custom (at 0.5 0.5) (size 0.733981 0.733981) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.387298 -0.329859) (xy -0.329859 -0.387298) (xy 0.329859 -0.387298) (xy 0.387298 -0.329859)
         (xy 0.387298 0.329859) (xy 0.329859 0.387298) (xy -0.329859 0.387298) (xy -0.387298 0.329859)) (width 0))
    ))
  (pad "" smd custom (at -1.3875 -0.5) (size 0.541766 0.541766) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.300156 -0.387298) (xy 0.217359 -0.387298) (xy 0.300156 -0.304501) (xy 0.300156 0.304501)
         (xy 0.217359 0.387298) (xy -0.300156 0.387298)) (width 0))
    ))
  (pad "" smd custom (at -1.3875 0.5) (size 0.541766 0.541766) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.300156 -0.387298) (xy 0.217359 -0.387298) (xy 0.300156 -0.304501) (xy 0.300156 0.304501)
         (xy 0.217359 0.387298) (xy -0.300156 0.387298)) (width 0))
    ))
  (pad "" smd custom (at 1.3875 -0.5) (size 0.541766 0.541766) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.300156 -0.304501) (xy -0.217359 -0.387298) (xy 0.300156 -0.387298) (xy 0.300156 0.387298)
         (xy -0.217359 0.387298) (xy -0.300156 0.304501)) (width 0))
    ))
  (pad "" smd custom (at 1.3875 0.5) (size 0.541766 0.541766) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.300156 -0.304501) (xy -0.217359 -0.387298) (xy 0.300156 -0.387298) (xy 0.300156 0.387298)
         (xy -0.217359 0.387298) (xy -0.300156 0.304501)) (width 0))
    ))
  (pad "" smd custom (at -0.5 -1.3875) (size 0.541766 0.541766) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.387298 -0.300156) (xy 0.387298 -0.300156) (xy 0.387298 0.217359) (xy 0.304501 0.300156)
         (xy -0.304501 0.300156) (xy -0.387298 0.217359)) (width 0))
    ))
  (pad "" smd custom (at 0.5 -1.3875) (size 0.541766 0.541766) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.387298 -0.300156) (xy 0.387298 -0.300156) (xy 0.387298 0.217359) (xy 0.304501 0.300156)
         (xy -0.304501 0.300156) (xy -0.387298 0.217359)) (width 0))
    ))
  (pad "" smd custom (at -0.5 1.3875) (size 0.541766 0.541766) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.387298 -0.217359) (xy -0.304501 -0.300156) (xy 0.304501 -0.300156) (xy 0.387298 -0.217359)
         (xy 0.387298 0.300156) (xy -0.387298 0.300156)) (width 0))
    ))
  (pad "" smd custom (at 0.5 1.3875) (size 0.541766 0.541766) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.387298 -0.217359) (xy -0.304501 -0.300156) (xy 0.304501 -0.300156) (xy 0.387298 -0.217359)
         (xy 0.387298 0.300156) (xy -0.387298 0.300156)) (width 0))
    ))
  (pad "" smd custom (at -1.3875 -1.3875) (size 0.523835 0.523835) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.300156 -0.300156) (xy 0.300156 -0.300156) (xy 0.300156 0.192001) (xy 0.192001 0.300156)
         (xy -0.300156 0.300156)) (width 0))
    ))
  (pad "" smd custom (at -1.3875 1.3875) (size 0.523835 0.523835) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.300156 -0.300156) (xy 0.192001 -0.300156) (xy 0.300156 -0.192001) (xy 0.300156 0.300156)
         (xy -0.300156 0.300156)) (width 0))
    ))
  (pad "" smd custom (at 1.3875 -1.3875) (size 0.523835 0.523835) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.300156 -0.300156) (xy 0.300156 -0.300156) (xy 0.300156 0.300156) (xy -0.192001 0.300156)
         (xy -0.300156 0.192001)) (width 0))
    ))
  (pad "" smd custom (at 1.3875 1.3875) (size 0.523835 0.523835) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.300156 -0.192001) (xy -0.192001 -0.300156) (xy 0.300156 -0.300156) (xy 0.300156 0.300156)
         (xy -0.300156 0.300156)) (width 0))
    ))
)"""

RESULT_EP_AUTOGEN_EDGECASE_1 = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad 3 smd rect (at -2 -2) (size 2 2) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at -2.7 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at -1.3 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at -2 -2) (size 2 0.6) (layers B.Cu))
  (pad "" smd custom (at -2 -2.5) (size 0.770649 0.770649) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.564358 -0.403113) (xy 0.564358 -0.403113) (xy 0.564358 0.352799) (xy 0.514044 0.403113)
         (xy -0.514044 0.403113) (xy -0.564358 0.352799)) (width 0))
    ))
  (pad "" smd custom (at -2 -1.5) (size 0.770649 0.770649) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.564358 -0.352799) (xy -0.514044 -0.403113) (xy 0.514044 -0.403113) (xy 0.564358 -0.352799)
         (xy 0.564358 0.403113) (xy -0.564358 0.403113)) (width 0))
    ))
  (pad 3 smd rect (at 2 -2) (size 2 2) (layers F.Cu F.Mask))
  (pad 3 thru_hole circle (at 1.3 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 2.7 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 2 -2) (size 2 0.6) (layers B.Cu))
  (pad "" smd custom (at 2 -2.5) (size 0.770649 0.770649) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.564358 -0.403113) (xy 0.564358 -0.403113) (xy 0.564358 0.352799) (xy 0.514044 0.403113)
         (xy -0.514044 0.403113) (xy -0.564358 0.352799)) (width 0))
    ))
  (pad "" smd custom (at 2 -1.5) (size 0.770649 0.770649) (layers F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -0.564358 -0.352799) (xy -0.514044 -0.403113) (xy 0.514044 -0.403113) (xy 0.564358 -0.352799)
         (xy 0.564358 0.403113) (xy -0.564358 0.403113)) (width 0))
    ))
  (pad "" smd rect (at 0 3) (size 2 2) (layers F.Mask))
  (pad 3 smd rect (at 0 3) (size 3 3) (layers F.Cu))
  (pad 3 thru_hole circle (at -1.2 3) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 1.2 3) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 0 3) (size 3 0.6) (layers B.Cu))
  (pad "" smd rect (at 0 2.5) (size 1.61 0.81) (layers F.Paste))
  (pad "" smd rect (at 0 3.5) (size 1.61 0.81) (layers F.Paste))
)"""

RESULT_EP_VIA_TENTING = """(module exposed_paste_autogen (layer F.Cu) (tedit 0)
  (descr "A example footprint")
  (tags example)
  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value exposed_paste_autogen (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "" smd rect (at -2 -2) (size 2 2) (layers F.Mask))
  (pad 3 smd rect (at -2 -2) (size 3 3) (layers F.Cu))
  (pad 3 thru_hole circle (at -3.2 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu F.Mask B.Mask))
  (pad 3 thru_hole circle (at -0.8 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu F.Mask B.Mask))
  (pad 3 smd rect (at -2 -2) (size 3 0.6) (layers B.Cu))
  (pad "" smd rect (at -2 -2.5) (size 1.61 0.81) (layers F.Paste))
  (pad "" smd rect (at -2 -1.5) (size 1.61 0.81) (layers F.Paste))
  (pad "" smd rect (at 2 -2) (size 2 2) (layers F.Mask))
  (pad 3 smd rect (at 2 -2) (size 3 3) (layers F.Cu))
  (pad 3 thru_hole circle (at 0.8 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu F.Mask))
  (pad 3 thru_hole circle (at 3.2 -2) (size 0.6 0.6) (drill 0.3) (layers *.Cu F.Mask))
  (pad 3 smd rect (at 2 -2) (size 3 0.6) (layers B.Cu))
  (pad "" smd rect (at 2 -2.5) (size 1.61 0.81) (layers F.Paste))
  (pad "" smd rect (at 2 -1.5) (size 1.61 0.81) (layers F.Paste))
  (pad "" smd rect (at -2 2) (size 2 2) (layers F.Mask))
  (pad 3 smd rect (at -2 2) (size 3 3) (layers F.Cu))
  (pad 3 thru_hole circle (at -3.2 2) (size 0.6 0.6) (drill 0.3) (layers *.Cu B.Mask))
  (pad 3 thru_hole circle (at -0.8 2) (size 0.6 0.6) (drill 0.3) (layers *.Cu B.Mask))
  (pad 3 smd rect (at -2 2) (size 3 0.6) (layers B.Cu))
  (pad "" smd rect (at -2 1.5) (size 1.61 0.81) (layers F.Paste))
  (pad "" smd rect (at -2 2.5) (size 1.61 0.81) (layers F.Paste))
  (pad "" smd rect (at 2 2) (size 2 2) (layers F.Mask))
  (pad 3 smd rect (at 2 2) (size 3 3) (layers F.Cu))
  (pad 3 thru_hole circle (at 0.8 2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 thru_hole circle (at 3.2 2) (size 0.6 0.6) (drill 0.3) (layers *.Cu))
  (pad 3 smd rect (at 2 2) (size 3 0.6) (layers B.Cu))
  (pad "" smd rect (at 2 1.5) (size 1.61 0.81) (layers F.Paste))
  (pad "" smd rect (at 2 2.5) (size 1.61 0.81) (layers F.Paste))
)"""


class ExposedPadTests(unittest.TestCase):

    def testSimpleExposedPad(self):
        kicad_mod = Footprint("simple_exposed")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="simple_exposed", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, at=[0, 1], size=[2.1, 3],
            mask_size=[2.1, 2.1], paste_layout=[2, 3], via_layout=[3, 2]
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_SIMPLE_EP_FP)

    def testSimpleExposedPadNoRounding(self):
        kicad_mod = Footprint("simple_exposed")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="simple_exposed", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, at=[0, 1], size=[2.1, 3],
            mask_size=[2.1, 2.1], paste_layout=[2, 3], via_layout=[3, 2],
            grid_round_base=None, size_round_base=0
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_SIMPLE_EP_NO_ROUNDING_FP)

    def testSimpleExposedMinimal(self):
        kicad_mod = Footprint("simple_exposed")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="simple_exposed", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[2.1, 3], paste_layout=2, via_layout=3
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_MINIMAL_EP_SPECIFICATION)

    def testExposedPasteAutogenInner(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[5, 5], paste_layout=3, via_layout=2,
            paste_avoid_via=True
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_PASTE_GEN_INNER)

    def testExposedPasteAutogenInner2(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[5, 5], paste_layout=6, via_layout=4,
            paste_avoid_via=True, paste_coverage=0.5
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep1.kicad_mod')
        self.assertEqual(result, RESULT_EP_PASTE_GEN_INNER2)

    def testExposedPasteAutogenInnerAndOuther(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[12, 8], paste_between_vias=2,
            paste_rings_outside=2, via_layout=3,
            paste_avoid_via=True, paste_coverage=0.7, via_grid=[3, 2],
            via_paste_clarance=0.25, min_annular_ring=0.25, at=[7, 5]
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_PASTE_GEN_INNER_AND_OUTHER)

    def testExposedPasteAutogenInnerYonlyAndOuther(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[3, 5], paste_between_vias=2, paste_rings_outside=[2, 1], via_layout=[1, 3],
            paste_avoid_via=True, paste_coverage=0.65, via_grid=2, via_paste_clarance=0.15
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_PASTE_GEN_INNER_ONLY_Y_AND_OUTHER)

    def testExposedPasteAutogenInnerXonlyAndOuther(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[4, 3], paste_between_vias=2, paste_rings_outside=[1, 2], via_layout=[3, 1],
            paste_avoid_via=True, paste_coverage=0.65, via_grid=1, via_paste_clarance=0.0
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_PASTE_GEN_INNER_ONLY_X_AND_OUTHER)

    def testExposedPasteAutogenOnlyOuther(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[2, 2], paste_between_vias=0, paste_rings_outside=[1, 1], via_layout=[1, 1],
            paste_avoid_via=True, paste_coverage=0.65, via_grid=1.5
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_PASTE_GEN_ONLY_OUTHER)

    def testExposedPasteBottomPadTests(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[2, 2], via_layout=[1, 1], at=[-2, -2],
            paste_coverage=0.65, via_grid=1, bottom_pad_Layers=None
            ))

        kicad_mod.append(ExposedPad(
            number=3, size=[2, 2], via_layout=[1, 1], at=[2, -2],
            paste_coverage=0.65, via_grid=1, bottom_pad_Layers=['B.Cu', 'B.Mask'],
            bottom_pad_min_size=[3, 3]
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_BOTTOM_PAD)

    def testExposed4x4paste(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=33, size=[3.55, 3.55],
            paste_layout=[3, 3],
            paste_between_vias=1,
            paste_rings_outside=1,
            paste_coverage=0.6,
            via_layout=[3, 3],
            via_drill=0.2,
            via_grid=[1, 1],
            paste_avoid_via=True,
            via_paste_clarance=0.1,
            min_annular_ring=0.15,
            bottom_pad_min_size=[0, 0]
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_4x4)

    def testExposedPadEdgeCase1(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[2, 2], via_layout=[2, 1], at=[-2, -2],
            paste_coverage=0.65, paste_layout=[1, 2],
            paste_avoid_via=True
            ))

        kicad_mod.append(ExposedPad(
            number=3, size=[2, 2], via_layout=[2, 1], at=[2, -2],
            paste_coverage=0.65, paste_layout=[1, 2],
            paste_avoid_via=True
            ))

        kicad_mod.append(ExposedPad(
            number=3, size=[3, 3], via_layout=[2, 1], at=[0, 3],
            paste_coverage=0.65, paste_layout=[1, 2], mask_size=[2, 2],
            paste_avoid_via=True
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_AUTOGEN_EDGECASE_1)

    def testExposedPasteViaTented(self):
        kicad_mod = Footprint("exposed_paste_autogen")

        kicad_mod.setDescription("A example footprint")
        kicad_mod.setTags("example")

        kicad_mod.append(Text(type='reference', text='REF**', at=[0, 0], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text="exposed_paste_autogen", at=[0, 0], layer='F.Fab'))

        kicad_mod.append(ExposedPad(
            number=3, size=[3, 3], via_layout=[2, 1], at=[-2, -2],
            paste_coverage=0.65, paste_layout=[1, 2], mask_size=[2, 2],
            paste_avoid_via=True, via_tented=ExposedPad.VIA_NOT_TENTED
            ))

        kicad_mod.append(ExposedPad(
            number=3, size=[3, 3], via_layout=[2, 1], at=[2, -2],
            paste_coverage=0.65, paste_layout=[1, 2], mask_size=[2, 2],
            paste_avoid_via=True, via_tented=ExposedPad.VIA_TENTED_BOTTOM_ONLY
            ))

        kicad_mod.append(ExposedPad(
            number=3, size=[3, 3], via_layout=[2, 1], at=[-2, 2],
            paste_coverage=0.65, paste_layout=[1, 2], mask_size=[2, 2],
            paste_avoid_via=True, via_tented=ExposedPad.VIA_TENTED_TOP_ONLY
            ))

        kicad_mod.append(ExposedPad(
            number=3, size=[3, 3], via_layout=[2, 1], at=[2, 2],
            paste_coverage=0.65, paste_layout=[1, 2], mask_size=[2, 2],
            paste_avoid_via=True, via_tented=ExposedPad.VIA_TENTED
            ))

        file_handler = KicadFileHandler(kicad_mod)
        result = file_handler.serialize(timestamp=0)
        # file_handler.writeFile('test_ep.kicad_mod')
        self.assertEqual(result, RESULT_EP_VIA_TENTING)
