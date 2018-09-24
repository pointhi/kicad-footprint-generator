#!/usr/bin/env python3

import sys
import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", ".."))

from KicadModTree import *

datasheet = "https://www.rohm.com/datasheet/SMLVN6RGB1U"
footprint_name = "LED_SMLVN6"
pkgWidth = 3.1
pkgHeight = 2.8
padXSpacing = 2.7
padYSpacing = 0.95
padWidth = 0.8
padHeight = 0.5
pads_clockwise = True

# desc = str(pkgWidth) + "mm x " + str(pkgHeight) + "mm SMLV6 LED, "

f = Footprint(footprint_name)
f.setDescription(datasheet)
f.setTags("LED SMLVN6")
f.setAttribute("smd")
f.append(Model(filename="${KISYS3DMOD}/LED_SMD.3dshapes/" + footprint_name + ".wrl",
               at=[0.0, 0.0, 0.0],
               scale=[1.0, 1.0, 1.0],
               rotate=[0.0, 0.0, 0.0]))

p = [padWidth, padHeight]
s = [1.0, 1.0]
sFabRef = [0.5, 0.5]

t1 = 0.075
t2 = 0.15

wCrtYd = 0.05
wFab = 0.1
wSilkS = 0.12
crtYd = 0.25
silkClearance = 0.2

xCenter = 0.0
xPadRight = padXSpacing / 2
xFabRight = pkgWidth / 2
xSilkRight = xPadRight + padWidth / 2 + silkClearance
xRightCrtYd = xSilkRight + crtYd

xLeftCrtYd = -xRightCrtYd
xSilkLeft = -xSilkRight
xPadLeft = -xPadRight
xFabLeft = -xFabRight
xChamfer = xFabLeft + 1.0

yCenter = 0.0
yPadBottom = padYSpacing
yFabBottom = pkgHeight / 2
ySilkBottom = max(yFabBottom + 0.1,
                  yPadBottom + padHeight / 2 + silkClearance)
yBottomCrtYd = ySilkBottom + crtYd

yTopCrtYd = -yBottomCrtYd
ySilkTop = -ySilkBottom
yFabTop = -yFabBottom
yPadTop = -yPadBottom
yChamfer = yFabTop + 1

yValue = yFabBottom + 1.25
yRef = yFabTop - 1.25

f.append(Text(type="reference", text="REF**", at=[xCenter, yRef],
              layer="F.SilkS", size=s, thickness=t2))
f.append(Text(type="value", text=footprint_name, at=[xCenter, yValue],
              layer="F.Fab", size=s, thickness=t2))
f.append(Text(type="user", text="%R", at=[xCenter, yCenter],
              layer="F.Fab", size=sFabRef, thickness=t1))

f.append(RectLine(start=[xLeftCrtYd, yTopCrtYd],
                  end=[xRightCrtYd, yBottomCrtYd],
                  layer="F.CrtYd", width=wCrtYd))

f.append(Line(start=[xChamfer, yFabTop],
              end=[xFabLeft, yChamfer],
              layer="F.Fab", width=wFab))
f.append(RectLine(start=[xFabLeft, yFabTop],
                  end=[xFabRight, yFabBottom],
                  layer="F.Fab", width=wFab))

f.append(PolygoneLine(polygone=[[xSilkLeft, yPadTop],
                                [xSilkLeft, ySilkTop],
                                [xSilkRight, ySilkTop]],
                      layer="F.SilkS", width=wSilkS))
f.append(Line(start=[xSilkLeft, ySilkBottom],
              end=[xSilkRight, ySilkBottom],
              layer="F.SilkS", width=wSilkS))

if pads_clockwise:
    pads = ["1", "2", "3", "4", "5", "6"]
else:
    pads = ["1", "6", "2", "5", "3", "4"]

f.append(Pad(number=pads[0], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
             at=[xPadLeft, yPadTop], size=p, layers=Pad.LAYERS_SMT))
f.append(Pad(number=pads[1], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
             at=[xPadRight, yPadTop], size=p, layers=Pad.LAYERS_SMT))
f.append(Pad(number=pads[2], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
             at=[xPadLeft, yCenter], size=p, layers=Pad.LAYERS_SMT))
f.append(Pad(number=pads[3], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
             at=[xPadRight, yCenter], size=p, layers=Pad.LAYERS_SMT))
f.append(Pad(number=pads[4], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
             at=[xPadRight, yPadBottom], size=p, layers=Pad.LAYERS_SMT))
f.append(Pad(number=pads[5], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
             at=[xPadLeft, yPadBottom], size=p, layers=Pad.LAYERS_SMT))

file_handler = KicadFileHandler(f)
file_handler.writeFile(footprint_name + ".kicad_mod")
