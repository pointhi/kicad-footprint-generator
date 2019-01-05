#!/usr/bin/env python3

import sys
import os
import re

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))

lib_name = "Package_DFN_QFN"

from KicadModTree import *

def qfn(args):
    footprint_name = args["name"]
    desc = args["description"]

    pkgWidth = args["pkg_width"]
    pkgHeight = args["pkg_height"]

    pitch = args["pitch"]
    nVertPads = args["n_vert_pads"]
    nHorzPads = args["n_horz_pads"]
    padWidth = args["pad_width"]
    padHeight = args["pad_height"]
    padHDistance = args["pad_h_distance"]
    padVDistance = args["pad_v_distance"]

    cornerPads = args["corner_pads"]
    cornerPadSize = args["corner_pad_size"]
    cornerPadHDistance = args["corner_pad_h_distance"]
    cornerPadVDistance = args["corner_pad_v_distance"]

    centerPad = args["center_pad"]
    centerPadWidth = args["center_pad_width"]
    centerPadHeight = args["center_pad_height"]
    centerPadHDiv = args["center_pad_h_div"]
    centerPadVDiv = args["center_pad_v_div"]
    pasteMarginRatio = args["paste_margin_ratio"]

    thermalVias = args["thermal_vias"]
    viaSize = args["via_size"]

    pat = re.compile('_ThermalVias')
    model = pat.sub("", footprint_name)

    f = Footprint(footprint_name)
    f.setDescription(desc)
    f.setTags("QFN " + str(pitch))
    f.setAttribute("smd")
    f.append(Model(filename="${KISYS3DMOD}/Package_DFN_QFN.3dshapes/" + model + ".wrl",
                   at=[0.0, 0.0, 0.0],
                   scale=[1.0, 1.0, 1.0],
                   rotate=[0.0, 0.0, 0.0]))

    d = [viaSize, viaSize]

    p1 = [viaSize + 0.3, viaSize + 0.3]
    p2 = [padWidth, padHeight]
    p3 = [cornerPadSize, cornerPadSize]

    s1 = [0.65, 0.65]
    s2 = [1.0, 1.0]

    t1 = 0.125
    t2 = 0.15

    wCrtYd = 0.05
    wFab = 0.10
    wSilkS = 0.12

    padShape = Pad.SHAPE_RECT

    chamfer = min(1.0, 0.25*min(pkgWidth, pkgHeight))
    silkOffset = 0.125
    crtYd = 0.25
    silkClearance = 0.2 + wSilkS / 2
    bottomPadMargin = 0.5

    xCenter = 0.0
    xLeftFab = xCenter - pkgWidth / 2
    xRightFab = xCenter + pkgWidth / 2
    xChamferFab = xLeftFab + chamfer
    xPadLeft = xCenter - (padHDistance / 2)
    xPadRight = xCenter + (padHDistance / 2)
    xLeftCrtYd = xPadLeft - (padWidth / 2 + crtYd)
    xRightCrtYd = xPadRight + (padWidth / 2 + crtYd)

    yCenter = 0.0
    yTopFab = yCenter - pkgHeight / 2
    yBottomFab = yCenter + pkgHeight / 2
    yChamferFab = yTopFab + chamfer
    yPadTop = yCenter - (padVDistance / 2)
    yPadBottom = yCenter + (padVDistance / 2)
    yTopCrtYd = yPadTop - (padWidth / 2 + crtYd)
    yBottomCrtYd = yPadBottom + (padWidth / 2 + crtYd)
    yRef = yTopCrtYd - 0.75
    yValue = yBottomCrtYd + 0.75

    if cornerPads:
        hDist = (cornerPadHDistance + cornerPadSize) / 2 + silkClearance
        vDist = (cornerPadVDistance + cornerPadSize) / 2 + silkClearance
        xLeftSilk = xCenter - hDist
        xRightSilk = xCenter + hDist
        yTopSilk = yCenter - vDist
        yBottomSilk = yCenter + vDist
    else:
        xLeftSilk = xLeftFab - silkOffset
        xRightSilk = xRightFab + silkOffset
        yTopSilk = yTopFab - silkOffset
        yBottomSilk = yBottomFab + silkOffset

    h2 = (pitch * (nHorzPads - 1) + padHeight) / 2 + silkClearance
    v2 = (pitch * (nVertPads - 1) + padHeight) / 2 + silkClearance
    xLeft2Silk = xCenter - h2
    xRight2Silk = xCenter + h2
    yTop2Silk = yCenter - v2
    yBottom2Silk = yCenter + v2

    # Text
    f.append(Text(type="reference", text="REF**", at=[xCenter, yRef],
                  layer="F.SilkS", size=s2, thickness=t2))
    f.append(Text(type="value", text=footprint_name, at=[xCenter, yValue],
                  layer="F.Fab", size=s2, thickness=t2))
    f.append(Text(type="user", text="%R", at=[xCenter, yCenter],
                  layer="F.Fab", size=s1, thickness=t1))

    # Fab
    f.append(PolygoneLine(polygone=[[xRightFab, yBottomFab],
                                    [xLeftFab, yBottomFab],
                                    [xLeftFab, yChamferFab],
                                    [xChamferFab, yTopFab],
                                    [xRightFab, yTopFab],
                                    [xRightFab, yBottomFab]],
                          layer="F.Fab", width=wFab))

    # Courtyard
    f.append(RectLine(start=[xLeftCrtYd, yTopCrtYd],
                      end=[xRightCrtYd, yBottomCrtYd],
                      layer="F.CrtYd", width=wCrtYd))

    # Silk
    f.append(PolygoneLine(polygone=[[xRight2Silk, yTopSilk],
                                    [xRightSilk, yTopSilk],
                                    [xRightSilk, yTop2Silk]],
                          layer="F.SilkS", width=wSilkS))
    f.append(PolygoneLine(polygone=[[xLeft2Silk, yBottomSilk],
                                    [xLeftSilk, yBottomSilk],
                                    [xLeftSilk, yBottom2Silk]],
                          layer="F.SilkS", width=wSilkS))
    f.append(PolygoneLine(polygone=[[xRight2Silk, yBottomSilk],
                                    [xRightSilk, yBottomSilk],
                                    [xRightSilk, yBottom2Silk]],
                          layer="F.SilkS", width=wSilkS))
    f.append(Line(start=[xLeftSilk, yTopSilk],
                  end=[xLeft2Silk, yTopSilk],
                  layer="F.SilkS", width=wSilkS))

    # Pads
    def padStart(n):
        return (n-1) * pitch / 2

    padNo = 1

    if cornerPads:
        f.append(Pad(number=str(padNo), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                     at=[xCenter - cornerPadHDistance / 2,
                         yCenter - cornerPadVDistance / 2],
                     size=p3, layers=Pad.LAYERS_SMT))
        padNo = padNo + 1

    for i in range(0, nVertPads):
        y = yCenter - padStart(nVertPads) + i * pitch
        f.append(Pad(number=str(padNo), type=Pad.TYPE_SMT, shape=padShape,
                     at=[xPadLeft, y], size=p2, layers=Pad.LAYERS_SMT))
        padNo = padNo + 1

    if cornerPads:
        f.append(Pad(number=str(padNo), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                     at=[xCenter - cornerPadHDistance / 2,
                         yCenter + cornerPadVDistance / 2],
                     size=p3, layers=Pad.LAYERS_SMT))
        padNo = padNo + 1

    for i in range(0, nHorzPads):
        x = xCenter - padStart(nHorzPads) + i * pitch
        f.append(Pad(number=str(padNo), type=Pad.TYPE_SMT, shape=padShape,
                     rotation=90.0,
                     at=[x, yPadBottom], size=p2, layers=Pad.LAYERS_SMT))
        padNo = padNo + 1

    if cornerPads:
        f.append(Pad(number=str(padNo), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                     at=[xCenter + cornerPadHDistance / 2,
                         yCenter + cornerPadVDistance / 2],
                     size=p3, layers=Pad.LAYERS_SMT))
        padNo = padNo + 1

    for i in range(0, nVertPads):
        y = yCenter + padStart(nVertPads) - i * pitch
        f.append(Pad(number=str(padNo), type=Pad.TYPE_SMT, shape=padShape,
                     at=[xPadRight, y], size=p2, layers=Pad.LAYERS_SMT))
        padNo = padNo + 1

    if cornerPads:
        f.append(Pad(number=str(padNo), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                     at=[xCenter + cornerPadHDistance / 2,
                         yCenter - cornerPadVDistance / 2],
                     size=p3, layers=Pad.LAYERS_SMT))
        padNo = padNo + 1

    for i in range(0, nHorzPads):
        x = xCenter + padStart(nHorzPads) - i * pitch
        f.append(Pad(number=str(padNo), type=Pad.TYPE_SMT, shape=padShape,
                     rotation=90.0,
                     at=[x, yPadTop], size=p2, layers=Pad.LAYERS_SMT))
        padNo = padNo + 1

    if centerPad:
        if thermalVias:
            f.append(Pad(number=str(padNo),
                         type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                         at=[xCenter, yCenter],
                         size=[centerPadWidth + 2 * bottomPadMargin,
                               centerPadHeight + 2 * bottomPadMargin],
                         layers=["B.Cu"]))

        f.append(Pad(number=str(padNo),
                     type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                     at=[xCenter, yCenter],
                     size=[centerPadWidth, centerPadHeight],
                     layers=["F.Cu", "F.Mask"]))

        subPadWidth = centerPadWidth / centerPadHDiv
        subPadHeight = centerPadHeight / centerPadVDiv
        subPadStartX = xCenter - (centerPadHDiv - 1) * subPadWidth / 2
        subPadStartY = yCenter - (centerPadVDiv - 1) * subPadHeight / 2

        pasteRatio = 1 + 2 * pasteMarginRatio

        for i in range(0, centerPadHDiv):
            x = subPadStartX + i * subPadWidth
            for j in range(0, centerPadVDiv):
                y = subPadStartY + j * subPadHeight
                f.append(Pad(number="", type=Pad.TYPE_SMT,
                             shape=Pad.SHAPE_RECT,
                             at=[x, y],
                             size=[subPadWidth * pasteRatio, subPadHeight * pasteRatio],
                             layers=["F.Paste"]))

        if thermalVias:
            nHVias = 2 * centerPadHDiv - 1
            nVVias = 2 * centerPadVDiv - 1
            viaHSpace = centerPadWidth / (nHVias + 1)
            viaVSpace = centerPadHeight / (nVVias + 1)
            viaStartX = xCenter - (nHVias - 1) * viaHSpace / 2
            viaStartY = yCenter - (nVVias - 1) * viaVSpace / 2

            for i in range(0, nHVias):
                x = viaStartX + i * viaHSpace
                for j in range(0, nVVias):
                    y = viaStartY + j * viaVSpace
                    if i % 2 == 1 or j % 2 == 1:
                        f.append(Pad(number=str(padNo), type=Pad.TYPE_THT,
                                     shape=Pad.SHAPE_CIRCLE, at=[x, y], size=p1,
                                     layers=["*.Cu"], drill=d))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(f)
    file_handler.writeFile(filename)


if __name__ == '__main__':
    parser = ModArgparser(qfn)
    # the root node of .yml files is parsed as name
    parser.add_parameter("name", type=str, required=True)
    parser.add_parameter("description", type=str, required=True)
    parser.add_parameter("pkg_width", type=float, required=True)
    parser.add_parameter("pkg_height", type=float, required=True)
    parser.add_parameter("pitch", type=float, required=False, default=0.5)
    parser.add_parameter("n_vert_pads", type=int, required=True)
    parser.add_parameter("n_horz_pads", type=int, required=True)
    parser.add_parameter("pad_width", type=float, required=False, default=0.9)
    parser.add_parameter("pad_height", type=float, required=False, default=0.3)
    parser.add_parameter("pad_h_distance", type=float, required=True)
    parser.add_parameter("pad_v_distance", type=float, required=True)
    parser.add_parameter("corner_pads", type=bool, required=False, default=False)
    parser.add_parameter("corner_pad_size", type=float, required=False, default=0.3)
    parser.add_parameter("corner_pad_h_distance", type=float, required=False, default=2.5)
    parser.add_parameter("corner_pad_v_distance", type=float, required=False, default=2.5)
    parser.add_parameter("center_pad", type=bool, required=False, default=False)
    parser.add_parameter("center_pad_width", type=float, required=False, default=1.8)
    parser.add_parameter("center_pad_height", type=float, required=False, default=1.8)
    parser.add_parameter("center_pad_h_div", type=int, required=False, default=2)
    parser.add_parameter("center_pad_v_div", type=int, required=False, default=2)
    parser.add_parameter("paste_margin_ratio", type=float, required=False, default=-0.2)
    parser.add_parameter("thermal_vias", type=bool, required=False, default=False)
    parser.add_parameter("via_size", type=float, required=False, default=0.3)

    # now run our script which handles the whole part of parsing the files
    parser.run()
