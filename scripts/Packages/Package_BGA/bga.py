#!/usr/bin/env python3

import math
import os
import sys
import argparse
import yaml

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA
sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools

from KicadModTree import *
import itertools
from string import ascii_uppercase

def generateFootprint(config, fpParams, fpId):
    print('Building footprint for parameter set: {}'.format(fpId))
    
    pkgX = fpParams["body_size_x"]
    pkgY = fpParams["body_size_y"]
    layoutX = fpParams["layout_x"]
    layoutY = fpParams["layout_y"]
    
    if "additional_tags" in fpParams:
        additionalTag = " " + fpParams["additional_tags"]
    else:
        additionalTag = ""
    
    if "row_names" in fpParams:
        rowNames = fpParams["row_names"]
    else:
        rowNames = config['row_names']
    
    if "row_skips" in fpParams:
        rowSkips = fpParams["row_skips"]
    else:
        rowSkips = []

    # must be given pitch (equal in X and Y) or a unique pitch in both X and Y
    if "pitch" in fpParams:
        if "pitch_x" and "pitch_y" in fpParams:
            raise KeyError('{}: Either pitch or both pitch_x and pitch_y must be given.'.format(fpId))
        else:
            pitchString = str(fpParams["pitch"])
            pitchX = fpParams["pitch"]
            pitchY = fpParams["pitch"]
    else:
        if "pitch_x" and "pitch_y" in fpParams:
            pitchString = str(fpParams["pitch_x"]) + "x" + str(fpParams["pitch_y"])
            pitchX = fpParams["pitch_x"]
            pitchY = fpParams["pitch_y"]
        else:
            raise KeyError('{}: Either pitch or both pitch_x and pitch_y must be given.'.format(fpId))

    f = Footprint(fpId)
    f.setAttribute("smd")
    if "mask_margin" in fpParams: f.setMaskMargin(fpParams["mask_margin"])
    if "paste_margin" in fpParams: f.setPasteMargin(fpParams["paste_margin"])
    if "paste_ratio" in fpParams: f.setPasteMarginRatio(fpParams["paste_ratio"])

    s1 = [1.0, 1.0]
    s2 = [min(1.0, round(pkgX / 4.3, 2))] * 2

    t1 = 0.15 * s1[0]
    t2 = 0.15 * s2[0]

    padShape = Pad.SHAPE_CIRCLE
    if "pad_shape" in fpParams:
        if fpParams["pad_shape"] == "rect":
            padShape = Pad.SHAPE_RECT
        if fpParams["pad_shape"] == "roundrect":
            padShape = Pad.SHAPE_ROUNDRECT

    chamfer = min(config['fab_bevel_size_absolute'], min(pkgX, pkgY) * config['fab_bevel_size_relative'])
    
    silkOffset = config['silk_fab_offset']
    crtYdOffset = config['courtyard_offset']['bga']
    
    def crtYdRound(x):
        # Round away from zero for proper courtyard calculation
        neg = x < 0
        if neg:
            x = -x
        x = math.ceil(x * 100) / 100.0
        if neg:
            x = -x
        return x

    xCenter = 0.0
    xLeftFab = xCenter - pkgX / 2.0
    xRightFab = xCenter + pkgX / 2.0
    xChamferFab = xLeftFab + chamfer
    xPadLeft = xCenter - pitchX * ((layoutX - 1) / 2.0)
    xPadRight = xCenter + pitchX * ((layoutX - 1) / 2.0)
    xLeftCrtYd = crtYdRound(xCenter - (pkgX / 2.0 + crtYdOffset))
    xRightCrtYd = crtYdRound(xCenter + (pkgX / 2.0 + crtYdOffset))

    yCenter = 0.0
    yTopFab = yCenter - pkgY / 2.0
    yBottomFab = yCenter + pkgY / 2.0
    yChamferFab = yTopFab + chamfer
    yPadTop = yCenter - pitchY * ((layoutY - 1) / 2.0)
    yPadBottom = yCenter + pitchY * ((layoutY - 1) / 2.0)
    yTopCrtYd = crtYdRound(yCenter - (pkgY / 2.0 + crtYdOffset))
    yBottomCrtYd = crtYdRound(yCenter + (pkgY / 2.0 + crtYdOffset))
    yRef = yTopFab - 1.0
    yValue = yBottomFab + 1.0

    xLeftSilk = xLeftFab - silkOffset
    xRightSilk = xRightFab + silkOffset
    xChamferSilk = xLeftSilk + chamfer
    yTopSilk = yTopFab - silkOffset
    yBottomSilk = yBottomFab + silkOffset
    yChamferSilk = yTopSilk + chamfer

    wFab = configuration['fab_line_width']
    wCrtYd = configuration['courtyard_line_width']
    wSilkS = configuration['silk_line_width']

    # Text
    f.append(Text(type="reference", text="REF**", at=[xCenter, yRef],
                  layer="F.SilkS", size=s1, thickness=t1))
    f.append(Text(type="value", text=fpId, at=[xCenter, yValue],
                  layer="F.Fab", size=s1, thickness=t1))
    f.append(Text(type="user", text="%R", at=[xCenter, yCenter],
                  layer="F.Fab", size=s2, thickness=t2))

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
    f.append(PolygoneLine(polygone=[[xChamferSilk, yTopSilk],
                                    [xRightSilk, yTopSilk],
                                    [xRightSilk, yBottomSilk],
                                    [xLeftSilk, yBottomSilk],
                                    [xLeftSilk, yChamferSilk]],
                          layer="F.SilkS", width=wSilkS))

    # Pads
    balls = layoutX * layoutY
    if rowSkips == []:
        for _ in range(layoutY):
            rowSkips.append([])
    for rowNum, row in zip(range(layoutY), rowNames):
        rowSet = set(range(1, layoutX + 1))
        for item in rowSkips[rowNum]:
            try:
                # If item is a range, remove that range
                rowSet -= set(range(*item))
                balls -= item[1] - item[0]
            except TypeError:
                # If item is an int, remove that int
                rowSet -= {item}
                balls -= 1
        for col in rowSet:
            f.append(Pad(number="{}{}".format(row, col), type=Pad.TYPE_SMT,
                         shape=padShape,
                         at=[xPadLeft + (col-1) * pitchX, yPadTop + rowNum * pitchY],
                         size=[fpParams["pad_diameter"], fpParams["pad_diameter"]],
                         layers=Pad.LAYERS_SMT, 
                         radius_ratio=config['round_rect_radius_ratio']))

    # If this looks like a CSP footprint, use the CSP 3dshapes library
    packageType = 'CSP' if 'BGA' not in fpId and 'CSP' in fpId else 'BGA'

    f.append(Model(filename="{}Package_{}.3dshapes/{}.wrl".format(
                  config['3d_model_prefix'], packageType, fpId)))

    f.setDescription("{0}, {1}x{2}mm, {3} Ball, {4}x{5} Layout, {6}mm Pitch, {7}".format(fpParams["description"], pkgY, pkgX, balls, layoutX, layoutY, pitchString, fpParams["size_source"]))
    f.setTags("{} {} {}{}".format(packageType, balls, pitchString, additionalTag))

    outputDir = 'Package_{lib_name:s}.pretty/'.format(lib_name=packageType)
    if not os.path.isdir(outputDir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(outputDir)
    filename = '{outdir:s}{fpId:s}.kicad_mod'.format(outdir=outputDir, fpId=fpId)
    
    file_handler = KicadFileHandler(f)
    file_handler.writeFile(filename)

def rowNameGenerator(seq):
    for n in itertools.count(1):
        for s in itertools.product(seq, repeat = n):
            yield ''.join(s)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files holding information about what devices should be created.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    # parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../package_config_KLCv3.yaml')

    args = parser.parse_args()
    
    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    # with open(args.series_config, 'r') as config_stream:
        # try:
            # configuration.update(yaml.safe_load(config_stream))
        # except yaml.YAMLError as exc:
            # print(exc)
    
    # generate dict of A, B .. Y, Z, AA, AB .. CY less easily-confused letters
    rowNamesList = [x for x in ascii_uppercase if x not in ["I", "O", "Q", "S", "X", "Z"]]
    configuration.update({'row_names': list(itertools.islice(rowNameGenerator(rowNamesList), 80))})

    for filepath in args.files:
        with open(filepath, 'r') as command_stream:
            try:
                cmd_file = yaml.safe_load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for pkg in cmd_file:
            generateFootprint(configuration, cmd_file[pkg], pkg)
