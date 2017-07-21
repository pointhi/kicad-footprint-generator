#!/usr/bin/env python3

import sys
import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", ".."))

from KicadModTree import *

# based on TerminalBlock_Pheonix_PT-3.5mm_2pol.kicad_mod
def terminal_block(args):
    footprint_name = args["name"]
    drillHole = [args["hole_size"], args["hole_size"]]
    padSize = [args["pad_size"], args["pad_size"]]
    pitch = args["pad_spacing"]
    ways = args["ways"]
    yTop = -args["back_depth"]
    yBottom = args["front_depth"]
    courtyard = args["courtyard"]

    textSize = [1.0, 1.0]

    wSilkscreen = 0.12
    wFab = 0.1
    wCourtyard = 0.05
    wText = 0.15

    xLeft = -(pitch / 2)
    xRight = xLeft + pitch * ways
    xMiddle = (xLeft + xRight) / 2

    yFirstLine = yBottom - 1.5
    ySecondLine = yBottom - 0.4

    yRef = yTop - 1.2
    yValue = yBottom + 1.5
    yMiddle = (yTop + yBottom) / 2

    xLeftCourtyard = xLeft - courtyard
    xRightCourtyard = xRight + courtyard

    yTopCourtyard = yTop - courtyard
    yBottomCourtyard = yBottom + courtyard

    xPad1 = 0.0
    xPad2 = pitch

    yPad = 0.0

    indOff = wFab + 2 * wSilkscreen
    indLen = pitch / 2

    # Create footprint
    f = Footprint(footprint_name)
    f.setDescription(str(ways) + "-way " + str(pitch) +
                     "mm pitch terminal block, " + args['datasheet'])
    f.setTags("screw terminal block")

    # Text
    f.append(Text(type="reference",
                  text="REF**",
                  at=[xMiddle, yRef],
                  rotation=0.0,
                  layer="F.SilkS",
                  size=textSize,
                  thickness=wText,
                  hide=False))
    f.append(Text(type="user",
                  text="%R",
                  at=[xMiddle, yMiddle],
                  rotation=0.0,
                  layer="F.Fab",
                  size=textSize,
                  thickness=wText,
                  hide=False))
    f.append(Text(type="value",
                  text=footprint_name,
                  at=[xMiddle, yValue],
                  rotation=0.0,
                  layer="F.Fab",
                  size=textSize,
                  thickness=wText,
                  hide=False))

    # Courtyard
    f.append(RectLine(start=[xLeftCourtyard, yTopCourtyard],
                      end=[xRightCourtyard, yBottomCourtyard],
                      layer="F.CrtYd",
                      width=wCourtyard))

    def draw_outline(o, l, w):
        # horizontal lines
        f.append(Line(start=[xLeft-o, yFirstLine],
                      end=[xRight+o, yFirstLine],
                      layer=l,
                      width=w))
        f.append(Line(start=[xLeft-o, ySecondLine],
                      end=[xRight+o, ySecondLine],
                      layer=l,
                      width=w))
        # three sides
        f.append(PolygoneLine(polygone=[[xLeft-o, yBottom+o],
                                        [xLeft-o, yTop-o],
                                        [xRight+o, yTop-o],
                                        [xRight+o, yBottom+o]],
                              layer=l,
                              width=w))
        # little vertical lines
        for i in range(1, ways):
            x = xLeft + i * pitch
            f.append(Line(start=[x, ySecondLine],
                          end=[x, yBottom],
                          layer=l,
                          width=w))
        # pin 1 indicator (in same place on fab and silkscreen layers
        f.append(PolygoneLine(polygone=[[xLeft - indOff, yBottom - indLen],
                                        [xLeft - indOff, yBottom + indOff],
                                        [xLeft + indLen, yBottom + indOff]],
                              layer=l,
                              width=w))

    # Fab layer
    draw_outline(0, "F.Fab", wFab)

    # Silkscreen
    draw_outline(wFab, "F.SilkS", wSilkscreen)

    # Pads
    for pad in range(0, ways):
        s = Pad.SHAPE_RECT if pad == 0 else Pad.SHAPE_CIRCLE
        f.append(Pad(number=str(pad+1),
                     type=Pad.TYPE_THT,
                     shape=s,
                     at=[xPad1 + pad * pitch, yPad],
                     rotation=0.0,
                     size=padSize,
                     layers=Pad.LAYERS_THT,
                     drill=drillHole))

    # 3D Model
    model = "${KISYS3DMOD}/Connectors_Terminal_Blocks.3dshapes/" + footprint_name + ".wrl"
    f.append(Model(filename=model,
                   at=[0, 0, 0],
                   scale=[1, 1, 1],
                   rotate=[0, 0, 0]))

    # Write footprint
    file_handler = KicadFileHandler(f)
    file_handler.writeFile(footprint_name + ".kicad_mod")


if __name__ == '__main__':
    parser = ModArgparser(terminal_block)
    # the root node of .yml files is parsed as name
    parser.add_parameter("name", type=str, required=True)
    parser.add_parameter("datasheet", type=str, required=False)
    parser.add_parameter("ways", type=int, required=False, default=2)
    parser.add_parameter("courtyard", type=float, required=False, default=0.5)
    parser.add_parameter("hole_size", type=float, required=False, default=1.2)
    parser.add_parameter("pad_size", type=float, required=False, default=2.4)
    parser.add_parameter("pad_spacing", type=float, required=False, default=3.5)
    # distance from pads to front (side with screws on it)
    parser.add_parameter("front_depth", type=float, required=False, default=4.5)
    # distance from pads to back
    parser.add_parameter("back_depth", type=float, required=False, default=3.1)

    # now run our script which handles the whole part of parsing the files
    parser.run()
