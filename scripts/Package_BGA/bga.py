#!/usr/bin/env python3

import math
import os
import sys
import argparse
import yaml

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", ".."))

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA
sys.path.append(os.path.join(sys.path[0], "..", "tools"))  # load parent path of tools

from KicadModTree import *
import itertools
from string import ascii_uppercase

def generateFootprint(config, fp_params, fp_id):
    print('Building footprint for parameter set: {}'.format(fp_id))
    
    pkgWidth = fp_params["pkg_width"]
    pkgHeight = fp_params["pkg_height"]
    layoutX = fp_params["layout_x"]
    layoutY = fp_params["layout_y"]
    
    if "row_names" in fp_params:
        rowNames = fp_params["row_names"]
    else:
        rowNames = config['row_names']
    
    if "row_skips" in fp_params:
        rowSkips = fp_params["row_skips"]
    else:
        rowSkips = []

    # must be given pitch (equal in X and Y) or a unique pitch in both X and Y
    if "pitch" in fp_params:
        if "pitch_x" and "pitch_y" in fp_params:
            raise KeyError('{}: Either pitch or both pitch_x and pitch_y must be given.'.format(fp_id))
        else:
            pitch_string = str(fp_params["pitch"])
            pitch_x = fp_params["pitch"]
            pitch_y = fp_params["pitch"]
    else:
        if "pitch_x" and "pitch_y" in fp_params:
            pitch_string = str(fp_params["pitch_x"]) + "x" + str(fp_params["pitch_y"])
            pitch_x = fp_params["pitch_x"]
            pitch_y = fp_params["pitch_y"]
        else:
            raise KeyError('{}: Either pitch or both pitch_x and pitch_y must be given.'.format(fp_id))

    f = Footprint(fp_id)
    f.setDescription(fp_params["description"])
    f.setAttribute("smd")
    if "mask_margin" in fp_params: f.setMaskMargin(fp_params["mask_margin"])
    if "paste_margin" in fp_params: f.setPasteMargin(fp_params["paste_margin"])
    if "paste_ratio" in fp_params: f.setPasteMarginRatio(fp_params["paste_ratio"])

    s1 = [1.0, 1.0]
    s2 = [min(1.0, round(pkgWidth / 4.3, 2))] * 2

    t1 = 0.15 * s1[0]
    t2 = 0.15 * s2[0]

    padShape = Pad.SHAPE_CIRCLE
    if "pad_shape" in fp_params:
        if fp_params["pad_shape"] == "rect":
            padShape = Pad.SHAPE_RECT
        if fp_params["pad_shape"] == "roundrect":
            padShape = Pad.SHAPE_ROUNDRECT

    chamfer = min(config['fab_bevel_size_absolute'], min(pkgWidth, pkgHeight) * config['fab_bevel_size_relative'])
    
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
    xLeftFab = xCenter - pkgWidth / 2.0
    xRightFab = xCenter + pkgWidth / 2.0
    xChamferFab = xLeftFab + chamfer
    xPadLeft = xCenter - pitch_x * ((layoutX - 1) / 2.0)
    xPadRight = xCenter + pitch_x * ((layoutX - 1) / 2.0)
    xLeftCrtYd = crtYdRound(xCenter - (pkgWidth / 2.0 + crtYdOffset))
    xRightCrtYd = crtYdRound(xCenter + (pkgWidth / 2.0 + crtYdOffset))

    yCenter = 0.0
    yTopFab = yCenter - pkgHeight / 2.0
    yBottomFab = yCenter + pkgHeight / 2.0
    yChamferFab = yTopFab + chamfer
    yPadTop = yCenter - pitch_y * ((layoutY - 1) / 2.0)
    yPadBottom = yCenter + pitch_y * ((layoutY - 1) / 2.0)
    yTopCrtYd = crtYdRound(yCenter - (pkgHeight / 2.0 + crtYdOffset))
    yBottomCrtYd = crtYdRound(yCenter + (pkgHeight / 2.0 + crtYdOffset))
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
    f.append(Text(type="value", text=fp_id, at=[xCenter, yValue],
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
                         at=[xPadLeft + (col-1) * pitch_x, yPadTop + rowNum * pitch_y],
                         size=[fp_params["pad_diameter"], fp_params["pad_diameter"]],
                         layers=Pad.LAYERS_SMT, 
                         radius_ratio=config['round_rect_radius_ratio']))

    # If this looks like a CSP footprint, use the CSP 3dshapes library
    package_type = 'CSP' if 'BGA' not in fp_id and 'CSP' in fp_id else 'BGA'

    f.append(Model(filename="{}Package_{}.3dshapes/{}.wrl".format(
                  config['3d_model_prefix'], package_type, fp_id)))

    f.setTags("{} {} {}".format(package_type, balls, pitch_string))

    output_dir = 'Package_{lib_name:s}.pretty/'.format(lib_name=package_type)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename = '{outdir:s}{fp_id:s}.kicad_mod'.format(outdir=output_dir, fp_id=fp_id)
    
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
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../tools/global_config_files/config_KLCv3.0.yaml')
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
    row_names_list = [x for x in ascii_uppercase if x not in ["I", "O", "Q", "S", "X", "Z"]]
    configuration.update({'row_names': list(itertools.islice(rowNameGenerator(row_names_list), 80))})

    for filepath in args.files:
        with open(filepath, 'r') as command_stream:
            try:
                cmd_file = yaml.safe_load(command_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for pkg in cmd_file:
            generateFootprint(configuration, cmd_file[pkg], pkg)