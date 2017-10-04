#!/usr/bin/env python3

import sys
import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", ".."))

from KicadModTree import *

def plcc4(args):
    footprint_name = args["name"]

    pkgWidth = args["pkg_width"]
    pkgHeight = args["pkg_height"]

    padXSpacing = args["pad_x_spacing"]
    padYSpacing = args["pad_y_spacing"]

    padWidth = args["pad_width"]
    padHeight = args["pad_height"]

    pads_clockwise = args["pads_clockwise"]

    desc = str(pkgWidth) + "mm x " + str(pkgHeight) + "mm PLCC4 LED, "

    f = Footprint(footprint_name)
    f.setDescription(desc + args["datasheet"])
    f.setTags("LED Cree PLCC-4")
    f.setAttribute("smd")
    f.append(Model(filename="${KISYS3DMOD}/LEDs.3dshapes/" + footprint_name + ".wrl",
                   at=[0.0, 0.0, 0.0],
                   scale=[1.0, 1.0, 1.0],
                   rotate=[0.0, 0.0, 0.0]))

    p = [padWidth, padHeight]
    r = pkgHeight * 0.4
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
    yPadBottom = padYSpacing / 2
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
    f.append(Circle(center=[xCenter, yCenter], radius=r,
                    layer="F.Fab", width=wFab))

    f.append(PolygoneLine(polygone=[[xSilkLeft, yPadTop],
                                    [xSilkLeft, ySilkTop],
                                    [xSilkRight, ySilkTop]],
                          layer="F.SilkS", width=wSilkS))
    f.append(Line(start=[xSilkLeft, ySilkBottom],
                  end=[xSilkRight, ySilkBottom],
                  layer="F.SilkS", width=wSilkS))

    if pads_clockwise:
        pads = ["1", "2", "3", "4"]
    else:
        pads = ["1", "4", "3", "2"]

    f.append(Pad(number=pads[0], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                 at=[xPadLeft, yPadTop], size=p, layers=Pad.LAYERS_SMT))
    f.append(Pad(number=pads[1], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                 at=[xPadRight, yPadTop], size=p, layers=Pad.LAYERS_SMT))
    f.append(Pad(number=pads[2], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                 at=[xPadRight, yPadBottom], size=p, layers=Pad.LAYERS_SMT))
    f.append(Pad(number=pads[3], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                 at=[xPadLeft, yPadBottom], size=p, layers=Pad.LAYERS_SMT))

    file_handler = KicadFileHandler(f)
    file_handler.writeFile(footprint_name + ".kicad_mod")


if __name__ == '__main__':
    parser = ModArgparser(plcc4)
    # the root node of .yml files is parsed as name
    parser.add_parameter("name", type=str, required=True)
    parser.add_parameter("datasheet", type=str, required=True)
    parser.add_parameter("pkg_width", type=float, required=False, default=2.0)
    parser.add_parameter("pkg_height", type=float, required=False, default=2.0)
    parser.add_parameter("pad_x_spacing", type=float, required=False, default=1.5)
    parser.add_parameter("pad_y_spacing", type=float, required=False, default=1.1)
    parser.add_parameter("pad_width", type=float, required=False, default=1.0)
    parser.add_parameter("pad_height", type=float, required=False, default=0.8)
    parser.add_parameter("pads_clockwise", type=bool, required=False, default=True)

    # now run our script which handles the whole part of parsing the files
    parser.run()
