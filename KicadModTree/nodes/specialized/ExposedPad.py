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
# (C) 2017 by @SchrodingersGat
# (C) 2017 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

from __future__ import division

from KicadModTree.nodes.base.Pad import *
from KicadModTree.nodes.specialized.PadArray import *
from KicadModTree.nodes.Node import Node
from math import sqrt
from builtins import round


class ExposedPad(Node):
    r"""Add an exposed pad

    Complete with correct paste, mask and via handling

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad
        * *at* (``Point``) --
          center the exposed pad around this point (default: 0,0)
        * *size* (``float``, ``Point``) --
          size of the pad
        * *solder_mask_margin* (``float``) --
          solder mask margin of the pad (default: 0)
          Only used if mask_size is not specified.
        * *mask_size* (``float``, ``Point``) --
          size of the mask cutout (If not given, mask will be part of the main pad)
        * *paste_layout* (``int``, [``int``, ``int``]) --
          paste layout specification.
          How many pads in x and y direction.
          If only a single integer given, x and y direction use the same count.
        * *paste_coverage* (``float``) --
          how much of the mask free area is covered with paste. (default: 0.65)
        * *via_layout* (``int``, [``int``, ``int``]) --
          thermal via layout specification.
          How many vias in x and y direction.
          If only a single integer given, x and y direction use the same count.
          default: no vias added
        * *via_grid* (``int``, [``int``, ``int``]) --
          thermal via grid specification.
          Grid used for thermal vias in x and y direction.
          If only a single integer given, x and y direction use the same count.
          If none is given then the via grid will be automatically calculated
          to have them distributed across the main pad.
        * *via_drill* (``float``) --
          via drill diameter (default: 0.3)
        * *min_annular_ring* (``float``) --
          Anullar ring for thermal vias. (default: 0.15)
        * *bottom_pad_Layers* (``[layer string]``) --
          Select layers for the bottom pad (default: [B.Cu])
          Ignored if no thermal vias are added.
          If None or empty no pad is added.
        * *paste_avoid_via* (``bool``) --
          Should paste be generated to specifically avoid vias? (default: false)
        * *grid_round_base* (``float``) --
          Base used for rounding calculated grids (default: 0.01)
          0 means no rounding
        * *size_round_base* (``float``) --
          Base used for rounding calculated sizes (default: 0.01)
          0 means no rounding
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self.at = Vector2D(kwargs.get('at', [0, 0]))

        self._initNumber(**kwargs)
        self._initSize(**kwargs)
        self._initThermalVias(**kwargs)
        self._initPaste(**kwargs)

        self.virtual_childs = self._createPads(**kwargs)

    def _initNumber(self, **kwargs):
        if not kwargs.get('number'):
            raise KeyError('pad number for exposed pad not declared (like "number=9")')
        self.number = kwargs.get('number')

    def _initSize(self, **kwargs):
        if not kwargs.get('size'):
            raise KeyError('pad size not declared (like "size=[1,1]")')
        if type(kwargs.get('size')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.size = Vector2D([kwargs.get('size'), kwargs.get('size')])
        else:
            self.size = Vector2D(kwargs.get('size'))

        if not kwargs.get('mask_size'):
            self.mask_size = self.size
        elif type(kwargs.get('mask_size')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.mask_size = Vector2D([kwargs.get('mask_size'), kwargs.get('mask_size')])
        else:
            self.mask_size = Vector2D(kwargs.get('mask_size'))

    def _initThermalVias(self, **kwargs):
        if 'via_layout' not in kwargs:
            self.has_vias = False
            return

        self.has_vias = True

        if type(kwargs.get('via_layout')) is int:
            # when the attribute is a simple number, use it for x and y
            self.via_layout = [kwargs.get('via_layout'), kwargs.get('via_layout')]
        else:
            self.via_layout = kwargs.get('via_layout')

        self.via_drill = kwargs.get('via_drill', 0.3)
        self.via_size = self.via_drill + 2*kwargs.get('min_annular_ring', 0.15)

        nx = self.via_layout[0]-1
        ny = self.via_layout[1]-1
        if 'via_grid' in kwargs:
            if type(kwargs.get('via_grid')) is int:
                # when the attribute is a simple number, use it for x and y
                self.via_grid = [kwargs.get('via_grid'), kwargs.get('via_grid')]
            else:
                self.via_grid = kwargs.get('via_grid')
        else:
            self.via_grid = [
                    (self.size.x-self.via_size)/(nx if nx > 0 else 1),
                    (self.size.y-self.via_size)/(ny if ny > 0 else 1)
                ]

        self.via_grid = ExposedPad.__roundToBase(
            self.via_grid, kwargs.get('grid_round_base', 0.01)
            )

        self.bottom_pad_Layers = kwargs.get('bottom_pad_Layers', ['B.Cu'])

        self.add_bottom_pad = True
        if self.bottom_pad_Layers is None or len(self.bottom_pad_Layers) == 0:
            self.add_bottom_pad = False

        if self.add_bottom_pad:
            self.bottom_size = [
                    nx*self.via_grid[0]+self.via_size,
                    ny*self.via_grid[1]+self.via_size
                ]

    def _initPaste(self, **kwargs):
        self.paste_avoid_via = kwargs.get('paste_avoid_via', False)
        if self.has_vias and self.paste_avoid_via:
            raise NotImplementedError('Managing paste for pads for avoiding thermal vias not yet implemented.')

        c = sqrt(kwargs.get('paste_coverage', 0.65))

        if not kwargs.get('paste_layout'):
            self.paste_layout = [1, 1]
        if type(kwargs.get('paste_layout')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.paste_layout = [kwargs.get('paste_layout'), kwargs.get('paste_layout')]
        else:
            self.paste_layout = kwargs.get('paste_layout')

        nx = self.paste_layout[0]
        ny = self.paste_layout[1]

        sx = self.mask_size.x
        sy = self.mask_size.y

        self.paste_size = ExposedPad.__roundToBase(
                [sx*c/nx, sy*c/ny],
                kwargs.get('size_round_base', 0.01)
            )

        dx = (sx - self.paste_size[0]*nx)/(nx+1)
        dy = (sy - self.paste_size[1]*ny)/(ny+1)

        self.paste_grid = ExposedPad.__roundToBase(
                [self.paste_size[0]+dx, self.paste_size[1]+dy],
                kwargs.get('grid_round_base', 0.01)
            )

    def _createPads(self, **kwargs):
        pads = []
        if self.size == self.mask_size:
            layers_main = ['F.Cu', 'F.Mask']
        else:
            layers_main = ['F.Cu']
            pads.append(Pad(
                number="", at=self.at, size=self.mask_size,
                shape=Pad.SHAPE_RECT, type=Pad.TYPE_SMT, layers=['F.Mask']
            ))

        pads.append(Pad(
            number=self.number, at=self.at, size=self.size,
            shape=Pad.SHAPE_RECT, type=Pad.TYPE_SMT, layers=layers_main
        ))

        cy = -((self.paste_layout[1]-1)*self.paste_grid[1])/2 + self.at.y
        for i in range(self.paste_layout[1]):
            pads.append(
                PadArray(center=[self.at.x, cy],
                         initial="", increment=0, pincount=self.paste_layout[0],
                         x_spacing=self.paste_grid[0], size=self.paste_size,
                         type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                         layers=['F.Paste']
                         ))
            cy += self.paste_grid[1]

        if self.has_vias:
            cy = -((self.via_layout[1]-1)*self.via_grid[1])/2 + self.at.y
            for i in range(self.via_layout[1]):
                pads.append(
                    PadArray(center=[self.at.x, cy], initial=self.number,
                             increment=0, pincount=self.via_layout[0],
                             x_spacing=self.via_grid[0], size=self.via_size,
                             type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                             drill=self.via_drill, layers=['*.Cu']
                             ))
                cy += self.via_grid[1]

            if self.add_bottom_pad:
                pads.append(Pad(
                    number=self.number, at=self.at, size=self.bottom_size,
                    shape=Pad.SHAPE_RECT, type=Pad.TYPE_SMT,
                    layers=self.bottom_pad_Layers
                ))

        return pads

    @staticmethod
    def __roundToBase(value, base):
        if base is None or base == 0:
            return value

        if type(value) in [float, int]:
            return round(value/base)*base

        return [round(x/base)*base for x in value]

    def getVirtualChilds(self):
        return self.virtual_childs
