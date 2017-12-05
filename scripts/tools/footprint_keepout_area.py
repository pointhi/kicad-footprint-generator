# Kicad currently does not support adding keepout zones directly to footprints
# For this reason the library maintainance team decided to communicate keepouts as follows:
#  - A polygone outlining the keepout area (on layer Dwgs.User)
#  - Hatching of this area on the same layer
#  - Text on Cmts.User: KEEPOUT (with additional information if necessary)

import sys, os
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
from KicadModTree import *  # NOQA
from math import sqrt

KEEPOUT_DEFAULT_CONFIG={
    'graphical_layer':'Dwgs.User',
    'line_width': 0.1,
    'hatching_spacing': 2,
    'text':{
        'size':[1,1],
        'fontwidth':0.15,
        'position':'center',
        'layer':'Cmts.User'
    }
}
def addRectangularKeepout(kicad_mod, center, size, text='KEEPOUT', config=KEEPOUT_DEFAULT_CONFIG):
    keepout_edges={
        'left': center[0] - (size[0] / 2),
        'top': center[1] - (size[1] / 2)
    }
    keepout_edges['right'] = keepout_edges['left'] + size[0]
    keepout_edges['bottom'] = keepout_edges['top'] + size[1]
    kicad_mod.append(RectLine(
        start=[keepout_edges['left'], keepout_edges['top']],
        end=[keepout_edges['right'], keepout_edges['bottom']],
        layer=config['graphical_layer'], width=config['line_width']))

    if size[0] >= size[1]:
        rot = 0
        longer_size = size[0]
    else:
        longer_size = size[1]
        rot = 90

    fs = round(longer_size/len(text), 2)
    if fs > config['text']['size'][0]:
        size = config['text']['size']
        thickness = config['text']['fontwidth']
    else:
        size = [fs, fs]
        thickness = config['text']['fontwidth'] * fs


    kicad_mod.append(Text(type='user', text=text,
        at=center, rotation=rot,
        layer=config['text']['layer'], size=size,
        thickness=thickness))


    p1 = {'x':keepout_edges['left'], 'y':keepout_edges['top']}
    p2 = {'x':keepout_edges['left'], 'y':keepout_edges['top']}
    # 45° hatching
    step = config['hatching_spacing']
    step_x = step/sqrt(2)
    step_y = step_x

    p1_direction = 'move_right'
    p2_direction = 'move_down'

    while (1):
        if p1_direction == 'move_right':
            p1['x'] += step_x
            if p1['x'] > keepout_edges['right']:
                p1_direction = 'move_down'
                dx = keepout_edges['right'] - (p1['x'] - step_x)
                dy = step_y - dx
                p1['x'] = keepout_edges['right']
                p1['y'] += dy
        else:
            p1['y'] += step_y


        if p2_direction == 'move_down':
            p2['y'] += step_y
            if p2['y'] > keepout_edges['bottom']:
                p2_direction = 'move_right'
                dy = keepout_edges['bottom'] - (p2['y'] - step_y)
                dx = step_x - dy
                p2['x'] += dx
                p2['y'] = keepout_edges['bottom']
        else:
            p2['x'] += step_x

        if p1['y'] > keepout_edges['bottom']:
            return

        kicad_mod.append(Line(start=p1, end=p2,
            layer=config['graphical_layer'], width=config['line_width']))
