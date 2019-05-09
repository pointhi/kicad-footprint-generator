import unittest

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

class ArcTests(unittest.TestCase):

    def testArcsKx90deg(self):
        kicad_mod = Footprint("test")

        kicad_mod.append(Arc(center=(0, 0), start=(1, 0), angle=-90))
        kicad_mod.append(Arc(center=(0, 0), start=(0, -1.2), angle=-90))

        kicad_mod.append(Arc(center=(0, 0), start=(-1.4, 0), angle=-90))
        kicad_mod.append(Arc(center=(0, 0), start=(0, 1.6), angle=-90))

        kicad_mod.append(Arc(center=(0, 0), start=(2, 0), angle=90))
        kicad_mod.append(Arc(center=(0, 0), start=(0, 2.2), angle=90))

        kicad_mod.append(Arc(center=(0, 0), start=(-2.4, 0), angle=90))
        kicad_mod.append(Arc(center=(0, 0), start=(0, -2.6), angle=90))

        kicad_mod.append(Arc(center=(0, 0), start=(3, 0), end=(0, -3)))
        kicad_mod.append(Arc(center=(0, 0), start=(0, -3.2), end=(-3.2, 0)))

        kicad_mod.append(Arc(center=(0, 0), start=(-3.4, 0), end=(0, 3.4)))
        kicad_mod.append(Arc(center=(0, 0), start=(0, 3.6), end=(3.6, 0)))

        kicad_mod.append(Arc(center=(0, 0), start=(4, 0), end=(0, 4)))
        kicad_mod.append(Arc(center=(0, 0), start=(0, 4.2), end=(-4.2, 0)))

        kicad_mod.append(Arc(center=(0, 0), start=(-4.4, 0), end=(0, -4.4)))
        kicad_mod.append(Arc(center=(0, 0), start=(0, -4.6), end=(4.6, 0)))

        kicad_mod.append(Arc(center=(0, 0), start=(5, 0), end=(0, -5), long_way=True))
        kicad_mod.append(Arc(center=(0, 0), start=(0, -5.2), end=(-5.2, 0), long_way=True))

        kicad_mod.append(Arc(center=(0, 0), start=(-5.4, 0), end=(0, 5.4), long_way=True))
        kicad_mod.append(Arc(center=(0, 0), start=(0, 5.6), end=(5.6, 0), long_way=True))


        kicad_mod.append(Arc(center=(0, 0), start=(6, 0), end=(-6, 0)))
        kicad_mod.append(Arc(center=(0, 0), start=(-6.2, 0), end=(6.2, 0)))

        kicad_mod.append(Arc(center=(0, 0), start=(6.6, 0), end=(-6.6, 0), long_way=True))
        kicad_mod.append(Arc(center=(0, 0), start=(-6.8, 0), end=(6.8, 0), long_way=True))

        kicad_mod.append(Arc(center=(0, 0), midpoint=(7, 0), angle=90))
        kicad_mod.append(Arc(center=(0, 0), midpoint=(0, -7.2), angle=90))
        kicad_mod.append(Arc(center=(0, 0), midpoint=(-7.4, 0), angle=90))
        kicad_mod.append(Arc(center=(0, 0), midpoint=(0, 7.6), angle=90))

        kicad_mod.append(Arc(center=(0, 0), midpoint=(8, 0), angle=-90))
        kicad_mod.append(Arc(center=(0, 0), midpoint=(0, -8.2), angle=-90))
        kicad_mod.append(Arc(center=(0, 0), midpoint=(-8.4, 0), angle=-90))
        kicad_mod.append(Arc(center=(0, 0), midpoint=(0, 8.6), angle=-90))

        file_handler = KicadFileHandler(kicad_mod)
        self.assertEqual(file_handler.serialize(timestamp=0), RESULT_kx90DEG)
        #file_handler.writeFile('test_arc.kicad_mod')
