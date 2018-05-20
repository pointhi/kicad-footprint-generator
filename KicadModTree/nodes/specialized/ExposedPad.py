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
# (C) 2018 by Rene Poeschl, github @poeschlr

from __future__ import division

from KicadModTree.util.paramUtil import *
from KicadModTree.nodes.base.Pad import *
from KicadModTree.nodes.specialized.ChamferedPadGrid import *
from KicadModTree.nodes.specialized.PadArray import *
from KicadModTree.nodes.Node import Node
from math import sqrt, floor
from copy import copy
import traceback


class ExposedPad(Node):
    r"""Add an exposed pad

    Complete with correct paste, mask and via handling

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad
        * *at* (``Vector2D``) --
          center the exposed pad around this point (default: 0,0)
        * *size* (``float``, ``Vector2D``) --
          size of the pad
        * *solder_mask_margin* (``float``) --
          solder mask margin of the pad (default: 0)
          Only used if mask_size is not specified.
        * *mask_size* (``float``, ``Vector2D``) --
          size of the mask cutout (If not given, mask will be part of the main pad)

        * *paste_layout* (``int``, ``[int, int]``) --
          paste layout specification.
          How many pads in x and y direction.
          If only a single integer given, x and y direction use the same count.
        * *paste_between_vias* (``int``, ``[int, int]``)
          Alternative for paste_layout with more controll.
          This defines how many pads will be between 4 vias in x and y direction.
          If only a single integer given, x and y direction use the same count.
        * *paste_rings_outside* (``int``, ``[int, int]``)
          Alternative for paste_layout with more controll.
          Defines the number of rings outside of the vias in x and y direction.
          If only a single integer given, x and y direction use the same count.
        * *paste_coverage* (``float``) --
          how much of the mask free area is covered with paste. (default: 0.65)

        * *via_layout* (``int``, ``[int, int]``) --
          thermal via layout specification.
          How many vias in x and y direction.
          If only a single integer given, x and y direction use the same count.
          default: no vias added
        * *via_grid* (``int``, ``Vector2D``) --
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
          Paste automatically generated to avoid vias (default: false)
        * *via_paste_clarance* (``float``)
          Clearance between paste and via drills (default: 0.05)
          Only used if paste_avoid_via is set.

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
        self.size_round_base = kwargs.get('size_round_base', 0.01)
        self.grid_round_base = kwargs.get('grid_round_base', 0.01)

        self._initNumber(**kwargs)
        self._initSize(**kwargs)
        self._initThermalVias(**kwargs)
        self._initPaste(**kwargs)

    def _initNumber(self, **kwargs):
        if not kwargs.get('number'):
            raise KeyError('pad number for exposed pad not declared (like "number=9")')
        self.number = kwargs.get('number')

    def _initSize(self, **kwargs):
        if not kwargs.get('size'):
            raise KeyError('pad size not declared (like "size=[1,1]")')
        self.size = toVectorUseCopyIfNumber(kwargs.get('size'))

        if not kwargs.get('mask_size'):
            self.mask_size = self.size
        else:
            self.mask_size = toVectorUseCopyIfNumber(kwargs.get('mask_size'))

    def _initThermalVias(self, **kwargs):
        if 'via_layout' not in kwargs:
            self.has_vias = False
            return

        self.has_vias = True
        self.via_layout = toIntArray(kwargs.get('via_layout'))

        self.via_drill = kwargs.get('via_drill', 0.3)
        self.via_size = self.via_drill + 2*kwargs.get('min_annular_ring', 0.15)

        nx = self.via_layout[0]-1
        ny = self.via_layout[1]-1
        if 'via_grid' in kwargs:
            self.via_grid = toVectorUseCopyIfNumber(kwargs.get('via_grid'), low_limit=self.via_size)
        else:
            self.via_grid = Vector2D([
                    (self.size.x-self.via_size)/(nx if nx > 0 else 1),
                    (self.size.y-self.via_size)/(ny if ny > 0 else 1)
                ])

        self.via_grid = self.via_grid.round_to(kwargs.get('grid_round_base', 0.01))

        self.bottom_pad_Layers = kwargs.get('bottom_pad_Layers', ['B.Cu'])

        self.add_bottom_pad = True
        if self.bottom_pad_Layers is None or len(self.bottom_pad_Layers) == 0:
            self.add_bottom_pad = False

        if self.add_bottom_pad:
            self.bottom_size = [
                    nx*self.via_grid[0]+self.via_size,
                    ny*self.via_grid[1]+self.via_size
                ]

    def __viasInMaskCount(self, idx):
        if (self.via_layout[idx]-1)*self.via_grid[idx] <= self.paste_area_size[idx]:
            return self.via_layout[idx]
        else:
            return self.paste_area_size[idx]//(self.via_grid[idx]-1)

    def _initPaste(self, **kwargs):
        self.paste_avoid_via = kwargs.get('paste_avoid_via', False)
        self.paste_reduction = sqrt(kwargs.get('paste_coverage', 0.65))

        self.paste_area_size = Vector2D([min(m, c) for m, c in zip(self.mask_size, self.size)])
        self.vias_in_mask = [self.__viasInMaskCount(i) for i in range(2)]

        if self.has_vias and self.paste_avoid_via:
            self.via_clarance = kwargs.get('via_paste_clarance', 0.05)

            if 'paste_between_vias' in kwargs or 'paste_rings_outside' in kwargs:
                self.paste_between_vias = toIntArray(kwargs.get('paste_between_vias', [0, 0]), min_value=0)
                self.paste_rings_outside = toIntArray(kwargs.get('paste_rings_outside', [0, 0]), min_value=0)
            else:
                default = [l-1 for l in self.via_layout]
                self.paste_layout = toIntArray(kwargs.get('paste_layout', default))

                # int(floor(paste_count/(vias_in_mask-1)))
                self.paste_between_vias = [p//(v-1) for p, v in zip(self.paste_layout, self.vias_in_mask)]
                inner_count = [(v-1)*p for v, p in zip(self.vias_in_mask, self.paste_between_vias)]
                self.paste_rings_outside = [p-i for p, i in zip(self.paste_layout, inner_count)]
        else:
            self.paste_layout = toIntArray(kwargs.get('paste_layout', [1, 1]))

    def __createPasteIgnoreVia(self):
        nx = self.paste_layout[0]
        ny = self.paste_layout[1]

        sx = self.paste_area_size.x
        sy = self.paste_area_size.y

        paste_size = Vector2D([sx*self.paste_reduction/nx, sy*self.paste_reduction/ny])\
            .round_to(self.size_round_base)

        dx = (sx - paste_size[0]*nx)/(nx+1)
        dy = (sy - paste_size[1]*ny)/(ny+1)

        paste_grid = Vector2D(
                    [paste_size[0]+dx, paste_size[1]+dy]
                ).round_to(self.grid_round_base)

        return [ChamferedPadGrid(
                    number="", type=Pad.TYPE_SMT,
                    center=self.at, size=paste_size, layers=['F.Paste'],
                    chamfer_size=0, chamfer_selection=0,
                    pincount=self.paste_layout, grid=paste_grid
                    )]

    @staticmethod
    def __createPasteGrids(original, grid, count, center):
        pads = []
        top_left = Vector2D(center)-Vector2D(grid)*(Vector2D(count)-1)/2
        for idx_x in range(count[0]):
            x = top_left[0]+idx_x*grid[0]
            for idx_y in range(count[1]):
                y = top_left[1]+idx_y*grid[1]
                pads.append(copy(original))
                pads[-1].center = Vector2D(x, y)
        return pads

    def __createPasteAvoidViasInside(self):
        top_left_area = self.top_left_via+self.via_grid/2
        self.inner_grid = self.via_grid/Vector2D(self.paste_between_vias)

        if any(self.paste_rings_outside):
            self.inner_size = self.via_grid/Vector2D(self.paste_between_vias)*self.paste_reduction
        else:
            # inner_grid = mask_size/(inner_count)
            self.inner_size = self.paste_area_size/(self.inner_count)*self.paste_reduction

        corner = ChamferSelPadGrid(0)
        corner.setCorners()
        pad = ChamferedPadGrid(
                number="", type=Pad.TYPE_SMT,
                center=[0, 0], size=self.inner_size, layers=['F.Paste'],
                chamfer_size=0, chamfer_selection=corner,
                pincount=self.paste_between_vias, grid=self.inner_grid
                )
        pad.chamferAvoidCircle(
                    center=self.via_grid/2, diameter=self.via_drill,
                    clearance=self.via_clarance)

        count = [self.vias_in_mask[0]-1, self.vias_in_mask[1]-1]
        return ExposedPad.__createPasteGrids(
                    original=pad, grid=self.via_grid, count=count, center=self.at
                    )

    def __createPasteAvoidViasOutside(self):
        ring_size = (self.paste_area_size-(Vector2D(self.vias_in_mask)-1)*self.via_grid)/2
        paste_grid = ring_size/Vector2D(self.paste_rings_outside)
        outer_size = paste_grid*self.paste_reduction

        pads = []
        if self.paste_rings_outside[0] and self.inner_count[1] > 0:
            corner = ChamferSelPadGrid(
                        {ChamferSelPadGrid.TOP_RIGHT: 1,
                         ChamferSelPadGrid.BOTTOM_RIGHT: 1
                         })
            x = self.top_left_via[0]-ring_size[0]/2
            y = self.at[1]-(self.via_layout[1]-1)/2*self.via_grid[1]

            pad_side = ChamferedPadGrid(
                number="", type=Pad.TYPE_SMT,
                center=[x, y],
                size=[outer_size[0], self.inner_size[1]],
                layers=['F.Paste'],
                chamfer_size=0, chamfer_selection=corner,
                pincount=[self.paste_rings_outside[0], self.paste_between_vias[1]],
                grid=[paste_grid[0], self.inner_grid[1]]
                )

            pad_side.chamferAvoidCircle(
                        center=self.top_left_via, diameter=self.via_drill,
                        clearance=self.via_clarance)

            pads.extend(ExposedPad.__createPasteGrids(
                        original=pad_side, grid=self.via_grid,
                        count=[1, self.via_layout[1]-1],
                        center=[x, self.at['y']]
                        ))

            corner = ChamferSelPadGrid(
                        {ChamferSelPadGrid.TOP_LEFT: 1,
                         ChamferSelPadGrid.BOTTOM_LEFT: 1
                         })
            pad_side.chamfer_selection = corner

            x = 2*self.at[0]-x
            pads.extend(ExposedPad.__createPasteGrids(
                        original=pad_side, grid=self.via_grid,
                        count=[1, self.via_layout[1]-1],
                        center=[x, self.at['y']]
                        ))

        if self.paste_rings_outside[1] and self.inner_count[0]:
            corner = ChamferSelPadGrid(
                        {ChamferSelPadGrid.BOTTOM_LEFT: 1,
                         ChamferSelPadGrid.BOTTOM_RIGHT: 1
                         })

            x = self.at[0]-(self.via_layout[0]-1)/2*self.via_grid[0]
            y = self.top_left_via[1]-ring_size[1]/2

            pad_side = ChamferedPadGrid(
                number="", type=Pad.TYPE_SMT,
                center=[x, y],
                size=[self.inner_size[0], outer_size[1]],
                layers=['F.Paste'],
                chamfer_size=0, chamfer_selection=corner,
                pincount=[self.paste_between_vias[0], self.paste_rings_outside[1]],
                grid=[self.inner_grid[0], paste_grid[1]]
                )

            pad_side.chamferAvoidCircle(
                        center=self.top_left_via, diameter=self.via_drill,
                        clearance=self.via_clarance)

            pads.extend(ExposedPad.__createPasteGrids(
                        original=pad_side, grid=self.via_grid,
                        count=[self.via_layout[0]-1, 1],
                        center=[self.at['x'], y]
                        ))

            corner = ChamferSelPadGrid(
                        {ChamferSelPadGrid.TOP_LEFT: 1,
                         ChamferSelPadGrid.TOP_RIGHT: 1
                         })
            pad_side.chamfer_selection = corner

            y = 2*self.at[1]-y
            pads.extend(ExposedPad.__createPasteGrids(
                        original=pad_side, grid=self.via_grid,
                        count=[self.via_layout[0]-1, 1],
                        center=[self.at['x'], y]
                        ))

        if all(self.paste_rings_outside):
            left = self.top_left_via[0]-ring_size[0]/2
            top = self.top_left_via[1]-ring_size[1]/2
            corner = [
                [
                    {ChamferSelPadGrid.BOTTOM_RIGHT: 1},
                    {ChamferSelPadGrid.TOP_RIGHT: 1}
                    ],
                [
                    {ChamferSelPadGrid.BOTTOM_LEFT: 1},
                    {ChamferSelPadGrid.TOP_LEFT: 1}
                    ]
                ]
            pad_side = ChamferedPadGrid(
                number="", type=Pad.TYPE_SMT,
                center=[left, top], size=outer_size, layers=['F.Paste'],
                chamfer_size=0, chamfer_selection=0,
                pincount=self.paste_rings_outside,
                grid=paste_grid
                )
            pad_side.chamferAvoidCircle(
                        center=self.top_left_via, diameter=self.via_drill,
                        clearance=self.via_clarance)
            for idx_x in range(2):
                for idx_y in range(2):
                    x = left if idx_x == 0 else 2*self.at[0]-left
                    y = top if idx_y == 0 else 2*self.at[1]-top
                    pad_side.center = Vector2D(x, y)
                    pad_side.chamfer_selection = ChamferSelPadGrid(corner[idx_x][idx_y])
                    pads.append(copy(pad_side))

        return pads

    def __createMainPad(self):
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

        return pads

    def __createVias(self):
        pads = []
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

    def __createPaste(self):
        pads = []
        self.top_left_via = -(Vector2D(self.vias_in_mask)-1)*self.via_grid/2+self.at

        if self.has_vias and self.paste_avoid_via:
            self.inner_count = (Vector2D(self.vias_in_mask)-1)*Vector2D(self.paste_between_vias)

            if all(self.vias_in_mask) and all(self.paste_between_vias):
                pads += self.__createPasteAvoidViasInside()
            if any(self.paste_rings_outside):
                pads += self.__createPasteAvoidViasOutside()
        else:
            pads += self.__createPasteIgnoreVia()

        return pads

    def getVirtualChilds(self):
        # traceback.print_stack()
        pads = []
        pads += self.__createMainPad()
        if self.has_vias:
            pads += self.__createVias()
        pads += self.__createPaste()
        return pads
