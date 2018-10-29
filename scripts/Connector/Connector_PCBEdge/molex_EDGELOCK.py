#!/usr/bin/env python3

import sys
import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))

from KicadModTree import *

padNum = 6
datasheet = "https://www.molex.com/pdm_docs/sd/2008900106_sd.pdf"
footprint_name = "molex_EDGELOCK_" + str(padNum) + "-CKT"

leftSpaceWidth = 2.2
rightSpaceWidth = 1.4
spaceHeight = 7.1
centerSpaceHeight = 4.2
centerSpaceWidth = 0.85
centerCardWidth = 5.4
edgeToHoleBottom = 5.25
holeWidth = 2.8
holeHeight = 3.05
edgeToPadBottom = 0.9
edgeToPadTop = spaceHeight
padWidth = 1.0
padHeight = edgeToPadTop - edgeToPadBottom
padToPad = 2.0
padCenterToSpaceSide = 1.1
datasheetCDiffB = 0.3
datasheetBtoHousingLeft = 1.9
datasheetBtoHousingRight = 1.0

datasheetC = centerCardWidth + centerSpaceWidth * 2 + padCenterToSpaceSide * 4 + (padNum - 2) * padToPad

datasheetB = datasheetC + datasheetCDiffB
housingWidth = datasheetB + datasheetBtoHousingLeft + datasheetBtoHousingRight
housingHeight = 20.8
edgeToHousingTop = edgeToHoleBottom + holeHeight

f = Footprint(footprint_name)
f.setDescription(datasheet)
f.setTags("Connector PCBEdge molex EDGELOCK")
f.setAttribute("smd")
f.append(Model(filename="${KISYS3DMOD}/Connector_PCBEdge.3dshapes/" + footprint_name + ".wrl",
               at=[0.0, 0.0, 0.0],
               scale=[1.0, 1.0, 1.0],
               rotate=[0.0, 0.0, 0.0]))

s = [1.0, 1.0]
sFabRef = [0.7, 0.7]

t1 = 0.1
t2 = 0.15

wCrtYd = 0.05
wFab = 0.1
wSilkS = 0.12
wCut = wSilkS
crtYd = 0.3
silkClearance = 0.2
bevelLength = 1.0

xCenter = 0.0
xFabRight = housingWidth / 2
xSilkRight = xFabRight + silkClearance
xRightCrtYd = xSilkRight + crtYd

xLeftCrtYd = - xRightCrtYd
xFabLeft = -xFabRight
xSilkLeft = -xSilkRight

xOffset = (datasheetBtoHousingLeft - datasheetBtoHousingRight) / 2
xFabRight -= xOffset
xSilkRight -= xOffset
xRightCrtYd -= xOffset
xLeftCrtYd -= xOffset
xFabLeft -= xOffset
xSilkLeft -= xOffset

yCenter = 0.0

yFabBottom = housingHeight / 2
yFabTop = -yFabBottom
yEdge = yFabTop + edgeToHousingTop
ySilkBottom = yEdge - spaceHeight
yBottomCrtYd = yEdge

ySilkTop = yFabTop - silkClearance
yTopCrtYd = ySilkTop - crtYd

yValue = yFabBottom + 1.25
yRef = yFabTop - 1.25

yOffset = yEdge - edgeToPadBottom - padHeight / 2
yFabBottom -= yOffset
yFabTop -= yOffset
yEdge -= yOffset
ySilkBottom -= yOffset
yBottomCrtYd -= yOffset
ySilkTop -= yOffset
yTopCrtYd -= yOffset
yValue -= yOffset
yRef -= yOffset

f.append(Text(type="reference", text="REF**", at=[xCenter, yRef],
              layer="F.SilkS", size=s, thickness=t2))
f.append(Text(type="value", text=footprint_name, at=[xCenter, yValue],
              layer="F.Fab", size=s, thickness=t2))
f.append(Text(type="user", text="%R", at=[xCenter, yCenter],
              layer="F.Fab", size=sFabRef, thickness=t1))

f.append(RectLine(start=[xLeftCrtYd, yTopCrtYd],
                  end=[xRightCrtYd, yBottomCrtYd],
                  layer="F.CrtYd", width=wCrtYd))

f.append(PolygoneLine(polygone=[[xFabRight, yFabTop],
                                [xFabRight, yFabBottom],
                                [xFabLeft, yFabBottom],
                                [xFabLeft, yFabTop + bevelLength],
                                [xFabLeft + bevelLength, yFabTop],
                                [xFabRight, yFabTop]],
                      layer="F.Fab", width=wFab))

f.append(PolygoneLine(polygone=[[xSilkLeft, ySilkBottom],
                                [xSilkLeft, ySilkTop + bevelLength],
                                [xSilkLeft + bevelLength, ySilkTop],
                                [xSilkRight, ySilkTop],
                                [xSilkRight, ySilkBottom]],
                      layer="F.SilkS", width=wSilkS))

padShape = Pad.SHAPE_ROUNDRECT
radiusRatio = 0.2
padSize = [padWidth, padHeight]
yPad = yEdge - edgeToPadBottom - padHeight / 2
xPadLeft = xFabLeft + datasheetBtoHousingLeft + padCenterToSpaceSide + datasheetCDiffB / 2

for i in range(0, padNum):
    x = xPadLeft + padToPad * i
    if (i >= padNum/2):
        x += centerCardWidth + centerSpaceWidth * 2 + padCenterToSpaceSide * 2 - padToPad
    f.append(Pad(number=i+1, type=Pad.TYPE_SMT, shape=padShape,
                 at=[x, yPad], size=padSize, layers=Pad.LAYERS_SMT,
                 radius_ratio=radiusRatio))

padCardWidth = padToPad * (padNum / 2 - 1) + padCenterToSpaceSide * 2
xSpaceLeftRight = xFabLeft + datasheetBtoHousingLeft + datasheetCDiffB / 2
xSpaceCneterLeftLeft = xSpaceLeftRight + padCardWidth
xSpaceCneterRightLeft = xSpaceCneterLeftLeft + centerSpaceWidth + centerCardWidth
xSpaceRightLeft = xSpaceCneterRightLeft + centerSpaceWidth + padCardWidth
f.append(PolygoneLine(polygone=[[xSpaceLeftRight - leftSpaceWidth, yEdge],
                                [xSpaceLeftRight - leftSpaceWidth, yEdge - spaceHeight],
                                [xSpaceLeftRight, yEdge - spaceHeight],
                                [xSpaceLeftRight, yEdge],
                                [xSpaceCneterLeftLeft, yEdge],
                                [xSpaceCneterLeftLeft, yEdge - centerSpaceHeight],
                                [xSpaceCneterLeftLeft + centerSpaceWidth, yEdge - centerSpaceHeight],
                                [xSpaceCneterLeftLeft + centerSpaceWidth, yEdge],
                                [xSpaceCneterRightLeft, yEdge],
                                [xSpaceCneterRightLeft, yEdge - centerSpaceHeight],
                                [xSpaceCneterRightLeft + centerSpaceWidth, yEdge - centerSpaceHeight],
                                [xSpaceCneterRightLeft + centerSpaceWidth, yEdge],
                                [xSpaceRightLeft, yEdge],
                                [xSpaceRightLeft, yEdge - spaceHeight],
                                [xSpaceRightLeft + rightSpaceWidth, yEdge - spaceHeight],
                                [xSpaceRightLeft + rightSpaceWidth, yEdge]],
         layer="Edge.Cuts", width=wCut))

xHoleLeft = xSpaceCneterLeftLeft + centerSpaceWidth + (centerCardWidth - holeWidth) / 2
yHoleBottom = yEdge - edgeToHoleBottom
f.append(PolygoneLine(polygone=[[xHoleLeft, yHoleBottom],
                                [xHoleLeft + holeWidth, yHoleBottom],
                                [xHoleLeft + holeWidth, yHoleBottom - holeHeight],
                                [xHoleLeft, yHoleBottom - holeHeight],
                                [xHoleLeft, yHoleBottom]],
         layer="Edge.Cuts", width=wCut))

file_handler = KicadFileHandler(f)
file_handler.writeFile(footprint_name + ".kicad_mod")
