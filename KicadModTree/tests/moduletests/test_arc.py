import unittest
import math
from KicadModTree import *

RESULT_kx90DEG = """(module test (layer F.Cu) (tedit 0)
  (fp_arc (start 0 0) (end 1 0) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 -1.2) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -1.4 0) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 1.6) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 2 0) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 2.2) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -2.4 0) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 -2.6) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 3 0) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 -3.2) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -3.4 0) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 3.6) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 4 0) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 4.2) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -4.4 0) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 -4.6) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 5 0) (angle 270) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 -5.2) (angle 270) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -5.4 0) (angle 270) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 0 5.6) (angle 270) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 6 0) (angle -180) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -6.2 0) (angle -180) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 6.6 0) (angle 180) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -6.8 0) (angle 180) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 4.949747 -4.949747) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -5.091169 -5.091169) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -5.23259 5.23259) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 5.374012 5.374012) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 5.656854 5.656854) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end 5.798276 -5.798276) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -5.939697 -5.939697) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start 0 0) (end -6.081118 6.081118) (angle -90) (layer F.SilkS) (width 0.12))
)"""

RESULT_kx90DEG_45deg = """(module test (layer F.Cu) (tedit 0)
  (fp_arc (start -5 5) (end -4.292893 5.707107) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -4.151472 4.151472) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -5.989949 4.010051) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -6.131371 6.131371) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -3.585786 6.414214) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -6.555635 6.555635) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -6.697056 3.302944) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -3.161522 3.161522) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -2.87868 7.12132) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -2.737258 2.737258) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -7.404163 2.595837) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -7.545584 7.545584) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -2.171573 7.828427) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -7.969848 7.969848) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -8.11127 1.88873) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -1.747309 1.747309) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -1.464466 8.535534) (angle 270) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -1.323045 1.323045) (angle 270) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -8.818377 1.181623) (angle 270) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -8.959798 8.959798) (angle 270) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -0.757359 9.242641) (angle -180) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -9.384062 0.615938) (angle -180) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -0.333095 9.666905) (angle 180) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -9.808326 0.191674) (angle 180) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end 2 5) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -5 -2.2) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -12.4 5) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -5 12.6) (angle 90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -5 13) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end 3.2 5) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -5 -3.4) (angle -90) (layer F.SilkS) (width 0.12))
  (fp_arc (start -5 5) (end -13.6 5) (angle -90) (layer F.SilkS) (width 0.12))
)"""


class ArcTests(unittest.TestCase):

    def testArcsKx90deg(self):
        kicad_mod = Footprint("test")

        center = Vector2D(0, 0)
        kicad_mod.append(
            Arc(center=center, start=Vector2D(1, 0), angle=-90))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, -1.2), angle=-90))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(-1.4, 0), angle=-90))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, 1.6), angle=-90))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(2, 0), angle=90))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, 2.2), angle=90))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(-2.4, 0), angle=90))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, -2.6), angle=90))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(3, 0), end=Vector2D(0, -3)))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, -3.2), end=Vector2D(-3.2, 0)))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(-3.4, 0), end=Vector2D(0, 3.4)))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, 3.6), end=Vector2D(3.6, 0)))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(4, 0), end=Vector2D(0, 4)))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, 4.2), end=Vector2D(-4.2, 0)))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(-4.4, 0), end=Vector2D(0, -4.4)))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, -4.6), end=Vector2D(4.6, 0)))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(5, 0), end=Vector2D(0, -5),
                long_way=True))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, -5.2), end=Vector2D(-5.2, 0),
                long_way=True))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(-5.4, 0), end=Vector2D(0, 5.4),
                long_way=True))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(0, 5.6), end=Vector2D(5.6, 0),
                long_way=True))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(6, 0), end=Vector2D(-6, 0)))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(-6.2, 0), end=Vector2D(6.2, 0)))

        kicad_mod.append(
            Arc(center=center, start=Vector2D(6.6, 0), end=Vector2D(-6.6, 0),
                long_way=True))
        kicad_mod.append(
            Arc(center=center, start=Vector2D(-6.8, 0), end=Vector2D(6.8, 0),
                long_way=True))

        kicad_mod.append(
            Arc(center=center, midpoint=Vector2D(7, 0), angle=90))
        kicad_mod.append(
            Arc(center=center, midpoint=Vector2D(0, -7.2), angle=90))
        kicad_mod.append(
            Arc(center=center, midpoint=Vector2D(-7.4, 0), angle=90))
        kicad_mod.append(
            Arc(center=center, midpoint=Vector2D(0, 7.6), angle=90))

        kicad_mod.append(
            Arc(center=center, midpoint=Vector2D(8, 0), angle=-90))
        kicad_mod.append(
            Arc(center=center, midpoint=Vector2D(0, -8.2), angle=-90))
        kicad_mod.append(
            Arc(center=center, midpoint=Vector2D(-8.4, 0), angle=-90))
        kicad_mod.append(
            Arc(center=center, midpoint=Vector2D(0, 8.6), angle=-90))

        file_handler = KicadFileHandler(kicad_mod)
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_kx90DEG)
        # file_handler.writeFile('test_arc4.kicad_mod')

    def testArcsKx90degOffsetRotated(self):
        kicad_mod = Footprint("test")

        center = Vector2D(-5, 5)
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(1, 0)+center).rotate(45, origin=center),
              angle=-90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, -1.2)+center).rotate(45, origin=center),
              angle=-90
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(-1.4, 0)+center).rotate(45, origin=center),
              angle=-90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, 1.6)+center).rotate(45, origin=center),
              angle=-90
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(2, 0)+center).rotate(45, origin=center),
              angle=90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, 2.2)+center).rotate(45, origin=center),
              angle=90
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(-2.4, 0)+center).rotate(45, origin=center),
              angle=90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, -2.6)+center).rotate(45, origin=center),
              angle=90
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(3, 0)+center).rotate(45, origin=center),
              end=(Vector2D(0, -3)+center).rotate(45, origin=center)
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, -3.2)+center).rotate(45, origin=center),
              end=(Vector2D(-3.2, 0)+center).rotate(45, origin=center)
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(-3.4, 0)+center).rotate(45, origin=center),
              end=(Vector2D(0, 3.4)+center).rotate(45, origin=center)
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, 3.6)+center).rotate(45, origin=center),
              end=(Vector2D(3.6, 0)+center).rotate(45, origin=center)
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(4, 0)+center).rotate(45, origin=center),
              end=(Vector2D(0, 4)+center).rotate(45, origin=center)
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, 4.2)+center).rotate(45, origin=center),
              end=(Vector2D(-4.2, 0)+center).rotate(45, origin=center)
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(-4.4, 0)+center).rotate(45, origin=center),
              end=(Vector2D(0, -4.4)+center).rotate(45, origin=center)
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, -4.6)+center).rotate(45, origin=center),
              end=(Vector2D(4.6, 0)+center).rotate(45, origin=center)
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(5, 0)+center).rotate(45, origin=center),
              end=(Vector2D(0, -5)+center).rotate(45, origin=center),
              long_way=True
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, -5.2)+center).rotate(45, origin=center),
              end=(Vector2D(-5.2, 0)+center).rotate(45, origin=center),
              long_way=True
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(-5.4, 0)+center).rotate(45, origin=center),
              end=(Vector2D(0, 5.4)+center).rotate(45, origin=center),
              long_way=True
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(0, 5.6)+center).rotate(45, origin=center),
              end=(Vector2D(5.6, 0)+center).rotate(45, origin=center),
              long_way=True
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(6, 0)+center).rotate(45, origin=center),
              end=(Vector2D(-6, 0)+center).rotate(45, origin=center)
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(-6.2, 0)+center).rotate(45, origin=center),
              end=(Vector2D(6.2, 0)+center).rotate(45, origin=center)
              ))

        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(6.6, 0)+center).rotate(45, origin=center),
              end=(Vector2D(-6.6, 0)+center).rotate(45, origin=center),
              long_way=True
              ))
        kicad_mod.append(
          Arc(
              center=center,
              start=(Vector2D(-6.8, 0)+center).rotate(45, origin=center),
              end=(Vector2D(6.8, 0)+center).rotate(45, origin=center),
              long_way=True
              ))

        kicad_mod.append(
          Arc(
              center=center,
              midpoint=(Vector2D(7, 0)+center).rotate(45, origin=center),
              angle=90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              midpoint=(Vector2D(0, -7.2)+center).rotate(45, origin=center),
              angle=90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              midpoint=(Vector2D(-7.4, 0)+center).rotate(45, origin=center),
              angle=90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              midpoint=(Vector2D(0, 7.6)+center).rotate(45, origin=center),
              angle=90
              ))

        kicad_mod.append(
          Arc(
              center=center,
              midpoint=(Vector2D(8, 0)+center).rotate(45, origin=center),
              angle=-90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              midpoint=(Vector2D(0, -8.2)+center).rotate(45, origin=center),
              angle=-90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              midpoint=(Vector2D(-8.4, 0)+center).rotate(45, origin=center),
              angle=-90
              ))
        kicad_mod.append(
          Arc(
              center=center,
              midpoint=(Vector2D(0, 8.6)+center).rotate(45, origin=center),
              angle=-90
              ))

        file_handler = KicadFileHandler(kicad_mod)
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_kx90DEG_45deg)
        # file_handler.writeFile('test_arc5.kicad_mod')
