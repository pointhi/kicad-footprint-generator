#!/usr/bin/env python

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

#
# This module (canvas.py) contains wrapper classes and methods for parts
# of the KicadModTree primitives.
# They provide "turtle style" drawing using relative moves in order
# to simplify the math involved in calculating and keeping track of vertex coordinates.
# They also introduce the concept of canvases for drawing the different layers, this
# to simplify drawing and provide functionality such as transparent grid align
# and method chaining.
# A canvas is somewhat similar to a workplane in CadQuery which is
# often used for creating KiCad 3D models.
#
# (C) 2017 by Terje Io, <http://github.com/terjeio>

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\..")

from KicadModTree.nodes.base import Line, Circle, Text, Pad
from KicadModTree.nodes.specialized import RectFill

class Layer:

    _DEFAULT_LINE_WIDTHS = {'F.SilkS': 0.12,
                            'B.SilkS': 0.12,
                            'F.Fab':   0.1,
                            'B.Fab':   0.1,
                            'F.CrtYd': 0.05,
                            'B.CrtYd': 0.05}

    _DEFAULT_LINE_WIDTH       = 0.15
    _DEFAULT_TEXT_OFFSET      = 1.0
    _DEFAULT_TEXT_SIZE_MIN    = 0.25
    _DEFAULT_TEXT_SIZE_MAX    = 2.00
    _DEFAULT_GRID_CRT         = 0.05
    _DEFAULT_OFFSET_CRT       = 0.25
    _DEFAULT_MIN_PAD_DISTANCE = 0.2 # clearance?

    def __init__(self, footprint, layer='F.Fab', origin=(0,0), line_width=None, offset=None):
        self.footprint = footprint
        self.layer = layer
        self.gridspacing = None
        self.setOrigin(origin[0], origin[1])
        self.txt_size = [1.0] * 2
        self.setTextDefaults()
        self.setTextSize(1.0)
        self.txt_offset = self._DEFAULT_TEXT_OFFSET
        if offset == None and layer.split('.')[1] == 'CrtYd':
            offset = self._DEFAULT_OFFSET_CRT
        if offset != None:
            self.offset = offset
        self.auto_offset = offset == None
        self.goHome()
        self.setLineWidth(self._DEFAULT_LINE_WIDTHS.get(layer, self._DEFAULT_LINE_WIDTH) if line_width == None else line_width)
        if layer.split('.')[1] == 'CrtYd':
            self.setGridSpacing(self._DEFAULT_GRID_CRT)

    @staticmethod        
    def getBevel(width, height):
        return min(1.0, min(width, height) * 0.25)

    def setOrigin(self, x, y):
        self.origin = (self._align(x), self._align(y))
        self.goHome()
        return self

    def getOrigin(self):
        return self.origin

    def setLineWidth(self, width):
        self.line_width = width
        if self.auto_offset:
            self.offset = self.line_width / 2.0
        return self

    def setTextDefaults(self, max_size=None, min_size=None):
        if max_size == None and min_size == None:
            self.text_size_min = self._DEFAULT_TEXT_SIZE_MIN
            self.text_size_max = self._DEFAULT_TEXT_SIZE_MAX
        else:
            if max_size != None:
                self.text_size_max = round(max_size, 2)
            if min_size != None:
                self.text_size_min = round(min_size, 2)
        return self    

    def setTextSize(self, height, width=None, thickness=None):
        height = round(height, 2)
        self.txt_size[0] = min(max(height, self.text_size_min), self.text_size_max)
        self.txt_size[1] = min(max(height if width == None else round(width, 2), self.text_size_min), self.text_size_max)
        self.txt_thickness = round(self.txt_size[0] * 0.15 if thickness == None else thickness, 2)
        return self

    def setGridSpacing(self, grid):
        self.gridspacing = grid
        if self.gridspacing != None:
            self.alignToGrid()
        return self

    def getPadOffsetH(self, pad, offset=None):
        return (pad[0] + self.line_width) / 2.0 + (self._DEFAULT_MIN_PAD_DISTANCE if offset == None else offset)

    def getPadOffsetV(self, pad, offset=None):
        return (pad[1] + self.line_width) / 2.0 + (self._DEFAULT_MIN_PAD_DISTANCE if offset == None else offset)

    def goHome(self):
        self.x = self.origin[0]
        self.y = self.origin[1]
        return self

    def goto(self, x, y):
        self.x = self._align(x)
        self.y = self._align(y)
        return self

    def jump(self, x, y):
        self.x += self._align(x)
        self.y += self._align(y)
        return self

    def _align(self, value):
        return value if self.gridspacing == None\
                      else (math.ceil(value / self.gridspacing) * self.gridspacing if value > 0.0 else math.floor(value / self.gridspacing) * self.gridspacing)

    def alignToGrid(self):
        self.x = self._align(self.x)
        self.y = self._align(self.y)
        self.setOrigin(self._align(self.origin[0]), self._align(self.origin[1]))
        return self

    def to(self, x, y, draw=True):
        x = self._align(x)
        y = self._align(y)
        if draw:
            self.footprint.append(Line(start=[self.x, self.y], end=[self.x + x, self.y + y], layer=self.layer, width=self.line_width))
        self.x += x
        self.y += y
        return self

    def left(self, distance, draw=True):
        distance = self._align(distance)
        if draw:
            self.footprint.append(Line(start=[self.x, self.y], end=[self.x - distance, self.y], layer=self.layer, width=self.line_width))
        self.x -= distance
        return self

    def right(self, distance, draw=True):
        distance = self._align(distance)
        if draw:
            self.footprint.append(Line(start=[self.x, self.y], end=[self.x + distance, self.y], layer=self.layer, width=self.line_width))
        self.x += distance
        return self

    def up(self, distance, draw=True):
        distance = self._align(distance)
        if draw:
            self.footprint.append(Line(start=[self.x, self.y], end=[self.x , self.y - distance], layer=self.layer, width=self.line_width))
        self.y -= distance
        return self

    def down(self, distance, draw=True):
        distance = self._align(distance)
        if draw:
            self.footprint.append(Line(start=[self.x, self.y], end=[self.x , self.y + distance], layer=self.layer, width=self.line_width))
        self.y += distance
        return self

    def circle(self, radius, filled=False):
        if filled:
            line_width = radius / 3.0 + self.line_width / 2.0
            r = line_width / 2.0
            while r < radius:
                self.footprint.append(Circle(center=[self.x, self.y], radius=r, layer=self.layer, width=line_width))        
                r += line_width - self.line_width / 2.0
        else:
            self.footprint.append(Circle(center=[self.x, self.y], radius=radius, layer=self.layer, width=self.line_width))
        return self
   
    def fillrect(self, w, h):
        x = self.x
        y = self.y
        w = self._align(w)
        h = self._align(h)
        self.jump(self._align(-w / 2.0), self._align(-h / 2.0))
        self.footprint.append(RectFill(start=[x, y], end=[w + x, h + y], layer=self.layer))
        self.x = x
        self.y = y
        return self

    def rect(self, w, h, bevel=(0.0, 0.0, 0.0, 0.0), draw=(True, True, True, True), origin='center'):

        x = self.x
        y = self.y
        w = self._align(w)
        h = self._align(h)

        if origin == 'center':
            self.jump(self._align(-w / 2.0), self._align(-h / 2.0))

        if bevel[0] != 0.0:
            self.jump(bevel[0], 0.0)

        self.right(w - bevel[0] - bevel[1], draw[0])

        if bevel[1] != 0.0:
            self.to(bevel[1], bevel[1])

        self.down(h - bevel[1] - bevel[2], draw[1])

        if bevel[2] != 0.0:
            self.to(-bevel[2], bevel[2])

        self.left(w - bevel[3] - bevel[2], draw[2])

        if bevel[3] != 0.0:
            self.to(-bevel[3], -bevel[3])

        self.up(h - bevel[3] - bevel[0], draw[3])

        if bevel[0] != 0.0:
            self.to(bevel[0], -bevel[0])

        self.x = x
        self.y = y

        return self

    def text(self, type, text, rotation=0):
        self.footprint.append(Text(type=type, text=text, at=[self.x, self.y], rotation=rotation, layer=self.layer, size=self.txt_size, thickness=self.txt_thickness))
        return self



class PadLayer:

    def __init__(self, footprint, size, type, shape, shape_first=None, drill=None, layers=None, x_offset=0.0, y_offset=0.0):
        self.footprint = footprint
        self.type = type
        self.layers = layers
        self.shape = shape
        self.shape_first = shape if shape_first == None else shape_first
        self.size = size
        self.drill = 0.5 if drill == None and type == Pad.TYPE_SMT else drill
        self.x_offset = x_offset
        self.y_offset = y_offset
        self._init_layers(layers)
        self.p = 1
        self.last_pad = None

    def _init_layers(self, layers):

        if layers == None:
            if self.type == Pad.TYPE_SMT:
                layers = Pad.LAYERS_SMT
            elif self.type == Pad.TYPE_THT:
                layers = Pad.LAYERS_THT

        self.layers=layers

    def add(self, x, y, number=None, x_offset=None, y_offset=None):

        if number == None:
            number = self.p
            self.p += 1

        if x_offset == None:
            x_offset = self.x_offset

        if y_offset == None:
            y_offset = self.y_offset

        self.last_pad = Pad(number=number, type=self.type,
                            shape=self.shape_first if number == 1 else self.shape,
                            at=[x + x_offset, y + y_offset],
                            size=self.size, drill=self.drill, layers=self.layers)
        self.footprint.append(self.last_pad)
        return self

    def getLast(self):
        return self.last_pad

### EOF ###
