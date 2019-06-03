#!/usr/bin/env python3

import sys
import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))

from KicadModTree import *

padNums = [2, 4, 6, 8]
datasheet = "https://www.molex.com/pdm_docs/sd/2008900106_sd.pdf"

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
largerR = 0.4
smallerR = 0.2
chamferLength = 0.5
chamferComment = "Chamfer 30 degree " + str(chamferLength) + " mm"

housingHeight = 20.8

for padNum in padNums:
    footprint_name = "molex_EDGELOCK_" + str(padNum) + "-CKT"
    datasheetC = centerCardWidth + centerSpaceWidth * 2 + padCenterToSpaceSide * 4 + (padNum - 2) * padToPad

    datasheetB = datasheetC + datasheetCDiffB
    housingWidth = datasheetB + datasheetBtoHousingLeft + datasheetBtoHousingRight
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
                                    [xSpaceLeftRight - leftSpaceWidth, yEdge - spaceHeight + largerR]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xSpaceLeftRight - leftSpaceWidth + largerR, yEdge - spaceHeight + largerR],
                 start=[xSpaceLeftRight - leftSpaceWidth, yEdge - spaceHeight + largerR],
                 angle=90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceLeftRight - leftSpaceWidth + largerR, yEdge - spaceHeight],
                                    [xSpaceLeftRight - largerR, yEdge - spaceHeight]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xSpaceLeftRight - largerR, yEdge - spaceHeight + largerR],
                 start=[xSpaceLeftRight - largerR, yEdge - spaceHeight],
                 angle=90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceLeftRight, yEdge - spaceHeight + largerR],
                                    [xSpaceLeftRight, yEdge],
                                    [xSpaceCneterLeftLeft, yEdge],
                                    [xSpaceCneterLeftLeft, yEdge - centerSpaceHeight + smallerR]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xSpaceCneterLeftLeft + smallerR, yEdge - centerSpaceHeight + smallerR],
                 start=[xSpaceCneterLeftLeft, yEdge - centerSpaceHeight + smallerR],
                 angle=90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceCneterLeftLeft + smallerR, yEdge - centerSpaceHeight],
                                    [xSpaceCneterLeftLeft + centerSpaceWidth - smallerR, yEdge - centerSpaceHeight]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xSpaceCneterLeftLeft + centerSpaceWidth - smallerR, yEdge - centerSpaceHeight + smallerR],
                 start=[xSpaceCneterLeftLeft + centerSpaceWidth - smallerR, yEdge - centerSpaceHeight],
                 angle=90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceCneterLeftLeft + centerSpaceWidth, yEdge - centerSpaceHeight + smallerR],
                                    [xSpaceCneterLeftLeft + centerSpaceWidth, yEdge],
                                    [xSpaceCneterRightLeft, yEdge],
                                    [xSpaceCneterRightLeft, yEdge - centerSpaceHeight + smallerR]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xSpaceCneterRightLeft + smallerR, yEdge - centerSpaceHeight + smallerR],
                 start=[xSpaceCneterRightLeft, yEdge - centerSpaceHeight + smallerR],
                 angle=90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceCneterRightLeft + smallerR, yEdge - centerSpaceHeight],
                                    [xSpaceCneterRightLeft + centerSpaceWidth - smallerR, yEdge - centerSpaceHeight]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xSpaceCneterRightLeft + centerSpaceWidth - smallerR, yEdge - centerSpaceHeight + smallerR],
                 start=[xSpaceCneterRightLeft + centerSpaceWidth - smallerR, yEdge - centerSpaceHeight],
                 angle=90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceCneterRightLeft + centerSpaceWidth, yEdge - centerSpaceHeight + smallerR],
                                    [xSpaceCneterRightLeft + centerSpaceWidth, yEdge],
                                    [xSpaceRightLeft, yEdge],
                                    [xSpaceRightLeft, yEdge - spaceHeight + largerR]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xSpaceRightLeft + largerR, yEdge - spaceHeight + largerR],
                 start=[xSpaceRightLeft, yEdge - spaceHeight + largerR],
                 angle=90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceRightLeft + largerR, yEdge - spaceHeight],
                                    [xSpaceRightLeft + rightSpaceWidth - largerR, yEdge - spaceHeight]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xSpaceRightLeft + rightSpaceWidth - largerR, yEdge - spaceHeight + largerR],
                 start=[xSpaceRightLeft + rightSpaceWidth - largerR, yEdge - spaceHeight],
                 angle=90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceRightLeft + rightSpaceWidth, yEdge - spaceHeight + largerR],
                                    [xSpaceRightLeft + rightSpaceWidth, yEdge]],
             layer="Edge.Cuts", width=wCut))

    xHoleLeft = xSpaceCneterLeftLeft + centerSpaceWidth + (centerCardWidth - holeWidth) / 2
    yHoleBottom = yEdge - edgeToHoleBottom
    f.append(Arc(center=[xHoleLeft + largerR, yHoleBottom - largerR],
                 start=[xHoleLeft, yHoleBottom - largerR],
                 angle=-90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xHoleLeft + largerR, yHoleBottom],
                                    [xHoleLeft + holeWidth - largerR, yHoleBottom]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xHoleLeft + holeWidth - largerR, yHoleBottom - largerR],
                 start=[xHoleLeft + holeWidth - largerR, yHoleBottom],
                 angle=-90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xHoleLeft + holeWidth, yHoleBottom - largerR],
                                    [xHoleLeft + holeWidth, yHoleBottom - holeHeight + largerR]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xHoleLeft + holeWidth - largerR, yHoleBottom - holeHeight + largerR],
                 start=[xHoleLeft + holeWidth, yHoleBottom - holeHeight + largerR],
                 angle=-90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xHoleLeft + holeWidth - largerR, yHoleBottom - holeHeight],
                                    [xHoleLeft + largerR, yHoleBottom - holeHeight]],
             layer="Edge.Cuts", width=wCut))
    f.append(Arc(center=[xHoleLeft + largerR, yHoleBottom - holeHeight + largerR],
                 start=[xHoleLeft + largerR, yHoleBottom - holeHeight],
                 angle=-90.0, layer="Edge.Cuts", width=wCut))
    f.append(PolygoneLine(polygone=[[xHoleLeft, yHoleBottom - holeHeight + largerR],
                                    [xHoleLeft, yHoleBottom - largerR]],
             layer="Edge.Cuts", width=wCut))

    f.append(PolygoneLine(polygone=[[xSpaceLeftRight, yEdge - chamferLength],
                                    [xSpaceCneterLeftLeft, yEdge - chamferLength]],
             layer="Dwgs.User", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceCneterLeftLeft + centerSpaceWidth, yEdge - chamferLength],
                                    [xSpaceCneterRightLeft, yEdge - chamferLength]],
             layer="Dwgs.User", width=wCut))
    f.append(PolygoneLine(polygone=[[xSpaceCneterRightLeft + centerSpaceWidth, yEdge - chamferLength],
                                    [xSpaceRightLeft, yEdge - chamferLength]],
             layer="Dwgs.User", width=wCut))
    f.append(Text(type="user", text=chamferComment, at=[xCenter, yEdge + sFabRef[0]],
                  layer="Cmts.User", size=sFabRef, thickness=t2))

    file_handler = KicadFileHandler(f)
    file_handler.writeFile(footprint_name + ".kicad_mod")
