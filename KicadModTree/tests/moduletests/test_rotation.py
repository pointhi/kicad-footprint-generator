import unittest
import math
from KicadModTree import *

RESULT_rotText = """(module test_rotate (layer F.Cu) (tedit 0)
  (fp_text user -1 (at 2 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text user -1 (at 1.414214 1.414214 -45) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text user -1 (at 0 2 -90) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text user -1 (at -1.414214 1.414214 -135) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text user -1 (at -2 0 -180) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text user -1 (at -1.414214 -1.414214 -225) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text user -1 (at 0 -2 -270) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text user -1 (at 1.414214 -1.414214 -315) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
)"""

RESULT_rotLine = """(module test_rotate (layer F.Cu) (tedit 0)
  (fp_line (start 6 0) (end 7 1) (layer F.SilkS) (width 0.12))
  (fp_line (start 5.931852 0.517638) (end 6.638958 1.742383) (layer F.SilkS) (width 0.12))
  (fp_line (start 5.732051 1) (end 6.098076 2.366025) (layer F.SilkS) (width 0.12))
  (fp_line (start 5.414214 1.414214) (end 5.414214 2.828427) (layer F.SilkS) (width 0.12))
  (fp_line (start 5 1.732051) (end 4.633975 3.098076) (layer F.SilkS) (width 0.12))
  (fp_line (start 4.517638 1.931852) (end 3.810531 3.156597) (layer F.SilkS) (width 0.12))
  (fp_line (start 4 2) (end 3 3) (layer F.SilkS) (width 0.12))
  (fp_line (start 3.482362 1.931852) (end 2.257617 2.638958) (layer F.SilkS) (width 0.12))
  (fp_line (start 3 1.732051) (end 1.633975 2.098076) (layer F.SilkS) (width 0.12))
  (fp_line (start 2.585786 1.414214) (end 1.171573 1.414214) (layer F.SilkS) (width 0.12))
  (fp_line (start 2.267949 1) (end 0.901924 0.633975) (layer F.SilkS) (width 0.12))
  (fp_line (start 2.068148 0.517638) (end 0.843403 -0.189469) (layer F.SilkS) (width 0.12))
  (fp_line (start 2 0) (end 1 -1) (layer F.SilkS) (width 0.12))
  (fp_line (start 2.068148 -0.517638) (end 1.361042 -1.742383) (layer F.SilkS) (width 0.12))
  (fp_line (start 2.267949 -1) (end 1.901924 -2.366025) (layer F.SilkS) (width 0.12))
  (fp_line (start 2.585786 -1.414214) (end 2.585786 -2.828427) (layer F.SilkS) (width 0.12))
  (fp_line (start 3 -1.732051) (end 3.366025 -3.098076) (layer F.SilkS) (width 0.12))
  (fp_line (start 3.482362 -1.931852) (end 4.189469 -3.156597) (layer F.SilkS) (width 0.12))
  (fp_line (start 4 -2) (end 5 -3) (layer F.SilkS) (width 0.12))
  (fp_line (start 4.517638 -1.931852) (end 5.742383 -2.638958) (layer F.SilkS) (width 0.12))
  (fp_line (start 5 -1.732051) (end 6.366025 -2.098076) (layer F.SilkS) (width 0.12))
  (fp_line (start 5.414214 -1.414214) (end 6.828427 -1.414214) (layer F.SilkS) (width 0.12))
  (fp_line (start 5.732051 -1) (end 7.098076 -0.633975) (layer F.SilkS) (width 0.12))
  (fp_line (start 5.931852 -0.517638) (end 7.156597 0.189469) (layer F.SilkS) (width 0.12))
)"""

RESULT_rotArc = """(module test_rotate (layer F.Cu) (tedit 0)
  (fp_arc (start 6 1) (end 5.741181 0.034074) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 5.673033 1.483564) (end 5.673033 0.483564) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 5.232051 1.866025) (end 5.49087 0.9001) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 4.707107 2.12132) (end 5.207107 1.255295) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 4.133975 2.232051) (end 4.841081 1.524944) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 3.551712 2.190671) (end 4.417738 1.690671) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 3 2) (end 3.965926 1.741181) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 2.516436 1.673033) (end 3.516436 1.673033) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 2.133975 1.232051) (end 3.0999 1.49087) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 1.87868 0.707107) (end 2.744705 1.207107) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 1.767949 0.133975) (end 2.475056 0.841081) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 1.809329 -0.448288) (end 2.309329 0.417738) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 2 -1) (end 2.258819 -0.034074) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 2.326967 -1.483564) (end 2.326967 -0.483564) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 2.767949 -1.866025) (end 2.50913 -0.9001) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 3.292893 -2.12132) (end 2.792893 -1.255295) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 3.866025 -2.232051) (end 3.158919 -1.524944) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 4.448288 -2.190671) (end 3.582262 -1.690671) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 5 -2) (end 4.034074 -1.741181) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 5.483564 -1.673033) (end 4.483564 -1.673033) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 5.866025 -1.232051) (end 4.9001 -1.49087) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 6.12132 -0.707107) (end 5.255295 -1.207107) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 6.232051 -0.133975) (end 5.524944 -0.841081) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 6.190671 0.448288) (end 5.690671 -0.417738) (angle 90) (layer F.SilkS) (width 0.12))
)"""

RESULT_rotCircle = """(module test_rotate (layer F.Cu) (tedit 0)
  (fp_circle (center 6 -1) (end 7 -1) (layer F.SilkS) (width 0.12))
  (fp_circle (center 5.673033 -0.516436) (end 6.673033 -0.516436) (layer F.SilkS) (width 0.12))
  (fp_circle (center 5.232051 -0.133975) (end 6.232051 -0.133975) (layer F.SilkS) (width 0.12))
  (fp_circle (center 4.707107 0.12132) (end 5.707107 0.12132) (layer F.SilkS) (width 0.12))
  (fp_circle (center 4.133975 0.232051) (end 5.133975 0.232051) (layer F.SilkS) (width 0.12))
  (fp_circle (center 3.551712 0.190671) (end 4.551712 0.190671) (layer F.SilkS) (width 0.12))
  (fp_circle (center 3 0) (end 4 0) (layer F.SilkS) (width 0.12))
  (fp_circle (center 2.516436 -0.326967) (end 3.516436 -0.326967) (layer F.SilkS) (width 0.12))
  (fp_circle (center 2.133975 -0.767949) (end 3.133975 -0.767949) (layer F.SilkS) (width 0.12))
  (fp_circle (center 1.87868 -1.292893) (end 2.87868 -1.292893) (layer F.SilkS) (width 0.12))
  (fp_circle (center 1.767949 -1.866025) (end 2.767949 -1.866025) (layer F.SilkS) (width 0.12))
  (fp_circle (center 1.809329 -2.448288) (end 2.809329 -2.448288) (layer F.SilkS) (width 0.12))
  (fp_circle (center 2 -3) (end 3 -3) (layer F.SilkS) (width 0.12))
  (fp_circle (center 2.326967 -3.483564) (end 3.326967 -3.483564) (layer F.SilkS) (width 0.12))
  (fp_circle (center 2.767949 -3.866025) (end 3.767949 -3.866025) (layer F.SilkS) (width 0.12))
  (fp_circle (center 3.292893 -4.12132) (end 4.292893 -4.12132) (layer F.SilkS) (width 0.12))
  (fp_circle (center 3.866025 -4.232051) (end 4.866025 -4.232051) (layer F.SilkS) (width 0.12))
  (fp_circle (center 4.448288 -4.190671) (end 5.448288 -4.190671) (layer F.SilkS) (width 0.12))
  (fp_circle (center 5 -4) (end 6 -4) (layer F.SilkS) (width 0.12))
  (fp_circle (center 5.483564 -3.673033) (end 6.483564 -3.673033) (layer F.SilkS) (width 0.12))
  (fp_circle (center 5.866025 -3.232051) (end 6.866025 -3.232051) (layer F.SilkS) (width 0.12))
  (fp_circle (center 6.12132 -2.707107) (end 7.12132 -2.707107) (layer F.SilkS) (width 0.12))
  (fp_circle (center 6.232051 -2.133975) (end 7.232051 -2.133975) (layer F.SilkS) (width 0.12))
  (fp_circle (center 6.190671 -1.551712) (end 7.190671 -1.551712) (layer F.SilkS) (width 0.12))
)"""

RESULT_rotPoly = """(module test_rotate (layer F.Cu) (tedit 0)
  (fp_poly (pts (xy -1 0) (xy -1.2 0.5) (xy 0 0) (xy -1.2 -0.5)) (layer F.SilkS) (width 0.12))
  (fp_poly (pts (xy -0.575833 -3.334679) (xy -1.108846 -3.257884) (xy -0.075833 -2.468653) (xy -0.24282 -3.757884)) (layer F.SilkS) (width 0.12))
  (fp_poly (pts (xy 2.524167 -4.634679) (xy 2.191154 -5.057884) (xy 2.024167 -3.768653) (xy 3.05718 -4.557884)) (layer F.SilkS) (width 0.12))
  (fp_poly (pts (xy 5.2 -2.6) (xy 5.4 -3.1) (xy 4.2 -2.6) (xy 5.4 -2.1)) (layer F.SilkS) (width 0.12))
  (fp_poly (pts (xy 4.775833 0.734679) (xy 5.308846 0.657884) (xy 4.275833 -0.131347) (xy 4.44282 1.157884)) (layer F.SilkS) (width 0.12))
  (fp_poly (pts (xy 1.675833 2.034679) (xy 2.008846 2.457884) (xy 2.175833 1.168653) (xy 1.14282 1.957884)) (layer F.SilkS) (width 0.12))
)"""  # NOQA: E501

RESULT_rotPad = """(module test_rotate (layer F.Cu) (tedit 0)
  (pad 1 smd custom (at 0 0) (size 0.2 0.2) (layers F.Cu F.Mask F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -1 0) (xy -1.2 0.5) (xy 0 0) (xy -1.2 -0.5)) (width 0))
    ))
  (pad 2 smd custom (at 0.175 -0.303109 -60) (size 0.2 0.2) (layers F.Cu F.Mask F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -1 0) (xy -1.2 0.5) (xy 0 0) (xy -1.2 -0.5)) (width 0))
    ))
  (pad 3 smd custom (at 0.525 -0.303109 -120) (size 0.2 0.2) (layers F.Cu F.Mask F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -1 0) (xy -1.2 0.5) (xy 0 0) (xy -1.2 -0.5)) (width 0))
    ))
  (pad 4 smd custom (at 0.7 0 -180) (size 0.2 0.2) (layers F.Cu F.Mask F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -1 0) (xy -1.2 0.5) (xy 0 0) (xy -1.2 -0.5)) (width 0))
    ))
  (pad 5 smd custom (at 0.525 0.303109 -240) (size 0.2 0.2) (layers F.Cu F.Mask F.Paste)
    (options (clearance outline) (anchor circle))
    (primitives
      (gr_poly (pts
         (xy -1 0) (xy -1.2 0.5) (xy 0 0) (xy -1.2 -0.5)) (width 0))
    ))
)"""


class RotationTests(unittest.TestCase):

    def testTextRotation(self):
        kicad_mod = Footprint("test_rotate")

        center = Vector2D(0, 0)
        at = center+Vector2D(2, 0)

        for t in range(0, 360, 45):
            kicad_mod.append(
                Text(type=Text.TYPE_USER, text="-1", at=at).rotate(t, origin=center))

        file_handler = KicadFileHandler(kicad_mod)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_rotText)

    def testLineRotation(self):
        kicad_mod = Footprint("test_rotate")

        center = Vector2D(4, 0)
        start = center + Vector2D(2, 0)
        end = start + Vector2D(1, 1)

        for t in range(0, 360, 15):
            kicad_mod.append(
                Line(start=start, end=end).rotate(t, origin=center))

        file_handler = KicadFileHandler(kicad_mod)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_rotLine)

    def testArcRotation(self):
        kicad_mod = Footprint("test_rotate")

        rot_center = Vector2D(4, 0)
        mid = rot_center + Vector2D(2, 0)
        center = rot_center + Vector2D(2, 1)
        angle = 90

        for t in range(0, 360, 15):
            kicad_mod.append(
                Arc(center=center, midpoint=mid, angle=angle)
                .rotate(angle/3, origin=center)
                .rotate(t, origin=rot_center))

        file_handler = KicadFileHandler(kicad_mod)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_rotArc)

    def testCircleRotation(self):
        kicad_mod = Footprint("test_rotate")

        rot_center = Vector2D(4, -2)
        center = rot_center + Vector2D(2, 1)
        radius = 1

        for t in range(0, 360, 15):
            kicad_mod.append(
                Circle(center=center, radius=radius).rotate(t, origin=rot_center))

        file_handler = KicadFileHandler(kicad_mod)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_rotCircle)

    def testPolygonRotation(self):
        kicad_mod = Footprint("test_rotate")

        rot_center = Vector2D(2.1, -1.3)

        nodes = [(-1, 0), (-1.2, 0.5), (0, 0), (-1.2, -0.5)]

        for t in range(0, 360, 60):
            kicad_mod.append(
                Polygon(nodes=nodes).rotate(t, origin=rot_center))

        file_handler = KicadFileHandler(kicad_mod)
        # file_handler.writeFile('test.kicad_mod')
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_rotPoly)

    def testPadRotation(self):
        kicad_mod = Footprint("test_rotate")

        rot_center = Vector2D(0.35, 0)
        nodes = [(-1, 0), (-1.2, 0.5), (0, 0), (-1.2, -0.5)]
        prim = Polygon(nodes=nodes)
        i = 1
        for t in range(0, 300, 60):
            kicad_mod.append(
                Pad(
                    number=i, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                    at=[0, 0], size=[0.2, 0.2], layers=Pad.LAYERS_SMT,
                    primitives=[prim]
                    ).rotate(t, origin=rot_center))
            i += 1

        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile('test.kicad_mod')
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_rotPad)
