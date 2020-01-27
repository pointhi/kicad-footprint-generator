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
        * *via_tented* (VIA_TENTED, VIA_TENTED_TOP_ONLY, VIA_TENTED_BOTTOM_ONLY, VIA_NOT_TENTED) --
          Determines which side of the thermal vias is covered in soldermask.
          On the top only vias outside the defined mask area can be covered in soldermask.
          default: VIA_TENTED
        * *min_annular_ring* (``float``) --
          Anullar ring for thermal vias. (default: 0.15)
        * *bottom_pad_Layers* (``[layer string]``) --
          Select layers for the bottom pad (default: [B.Cu]) --
          Ignored if no thermal vias are added.
          If None or empty no pad is added.
        * *bottom_pad_min_size* (``float``, ``Vector2D``) --
          Minimum size for bottom pad. default: (0,0)
          Ignored if no bottom pad given.
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

        * *radius_ratio* (``float``) --
          The radius ratio of the main pads.
        * *maximum_radius* (``float``) --
          The maximum radius for the main pads.
          If the radius produced by the radius_ratio parameter for the pad would
          exceed the maximum radius, the ratio is reduced to limit the radius.
        * *round_radius_exact* (``float``) --
          Set an exact round radius for the main pads.

        * *paste_radius_ratio* (``float``) --
          The radius ratio of the paste pads.
        * *paste_maximum_radius* (``float``) --
          The maximum radius for the paste pads.
          If the radius produced by the paste_radius_ratio parameter for the paste pad would
          exceed the maximum radius, the ratio is reduced to limit the radius.
        * *paste_round_radius_exact* (``float``) --
          Set an exact round radius for the paste pads.

        * *kicad4_compatible* (``bool``) --
          Makes sure the resulting pad is compatible with kicad 4. default False
    """

    VIA_TENTED = 'all'
    VIA_TENTED_TOP_ONLY = 'top'
    VIA_TENTED_BOTTOM_ONLY = 'bottom'
    VIA_NOT_TENTED = 'none'

    def __init__(self, **kwargs):
        Node.__init__(self)
        self.at = Vector2D(kwargs.get('at', [0, 0]))
        self.size_round_base = kwargs.get('size_round_base', 0.01)
        self.grid_round_base = kwargs.get('grid_round_base', 0.01)

        self.round_radius_handler = RoundRadiusHandler(default_radius_ratio=0, **kwargs)

        self.kicad4_compatible = kwargs.get('kicad4_compatible', False)
        self.paste_round_radius_handler = RoundRadiusHandler(
                radius_ratio=kwargs.get('paste_radius_ratio', 0),
                maximum_radius=kwargs.get('paste_maximum_radius', None),
                round_radius_exact=kwargs.get('paste_round_radius_exact', None),
                kicad4_compatible=self.kicad4_compatible
            )

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

    def setViaLayout(self, layout):
        self.has_vias = True
        self.via_layout = toIntArray(layout, min_value=0)
        if self.via_layout[0] == 0 or self.via_layout[1] == 0:
            self.has_vias = False
        return self.has_vias

    def __initViaGrid(self, **kwargs):
        nx = self.via_layout[0]-1
        ny = self.via_layout[1]-1

        self.via_grid = kwargs.get('via_grid')
        if self.via_grid is not None:
            self.via_grid = toVectorUseCopyIfNumber(self.via_grid, low_limit=self.via_size)
        else:
            self.via_grid = Vector2D([
                    (self.size.x-self.via_size)/(nx if nx > 0 else 1),
                    (self.size.y-self.via_size)/(ny if ny > 0 else 1)
                ])

        self.via_grid = self.via_grid.round_to(kwargs.get('grid_round_base', 0))

    def _initThermalVias(self, **kwargs):
        if not self.setViaLayout(kwargs.get('via_layout', [0, 0])):
            return

        self.via_drill = kwargs.get('via_drill', 0.3)
        self.via_size = self.via_drill + 2*kwargs.get('min_annular_ring', 0.15)
        self.__initViaGrid(**kwargs)
        self.via_tented = kwargs.get('via_tented', ExposedPad.VIA_TENTED)

        self.bottom_pad_Layers = kwargs.get('bottom_pad_Layers', ['B.Cu'])

        self.add_bottom_pad = True
        if self.bottom_pad_Layers is None or len(self.bottom_pad_Layers) == 0:
            self.add_bottom_pad = False
        else:
            bottom_pad_min_size = toVectorUseCopyIfNumber(kwargs.get('bottom_pad_min_size', [0, 0]))
            self.bottom_size = Vector2D([
                    max((self.via_layout[0]-1)*self.via_grid[0]+self.via_size, bottom_pad_min_size[0]),
                    max((self.via_layout[1]-1)*self.via_grid[1]+self.via_size, bottom_pad_min_size[1])
                ])

    def __viasInMaskCount(self, idx):
        r""" Determine the number of vias within the soldermask area

        :param idx: (``int``) --
           determines if the x or y direction is used.
        """
        if (self.via_layout[idx]-1)*self.via_grid[idx] <= self.paste_area_size[idx]:
            return self.via_layout[idx]
        else:
            return int(self.paste_area_size[idx]//(self.via_grid[idx]))

    def _initPasteForAvoidingVias(self, **kwargs):
        self.via_clarance = kwargs.get('via_paste_clarance', 0.05)

        # check get against none to allow the caller to use None as the sign to ignore these.
        if kwargs.get('paste_between_vias') is not None\
                or kwargs.get('paste_rings_outside')is not None:
            self.paste_between_vias = toIntArray(kwargs.get('paste_between_vias', [0, 0]), min_value=0)
            self.paste_rings_outside = toIntArray(kwargs.get('paste_rings_outside', [0, 0]), min_value=0)
        else:
            default = [l-1 for l in self.via_layout]
            layout = kwargs.get('paste_layout')
            if layout is None:
                # alows initializing with 'paste_layout=None' to force default value
                layout = default
            self.paste_layout = toIntArray(layout)

            # int(floor(paste_count/(vias_in_mask-1)))
            self.paste_between_vias = [p//(v-1) if v > 1 else p//v
                                       for p, v in zip(self.paste_layout, self.vias_in_mask)]
            inner_count = [(v-1)*p for v, p in zip(self.vias_in_mask, self.paste_between_vias)]
            self.paste_rings_outside = [(p-i)//2 for p, i in zip(self.paste_layout, inner_count)]

    def _initPaste(self, **kwargs):
        self.paste_avoid_via = kwargs.get('paste_avoid_via', False)
        self.paste_reduction = sqrt(kwargs.get('paste_coverage', 0.65))

        self.paste_area_size = Vector2D([min(m, c) for m, c in zip(self.mask_size, self.size)])
        if self.has_vias:
            self.vias_in_mask = [self.__viasInMaskCount(i) for i in range(2)]

        if not self.has_vias or not all(self.vias_in_mask):
            self.paste_avoid_via = False

        if self.has_vias and self.paste_avoid_via:
            self._initPasteForAvoidingVias(**kwargs)
        else:
            self.paste_layout = toIntArray(kwargs.get('paste_layout', [1, 1]))

    def __createPasteIgnoreVia(self):
        nx = self.paste_layout[0]
        ny = self.paste_layout[1]

        sx = self.paste_area_size.x
        sy = self.paste_area_size.y

        paste_size = Vector2D([sx*self.paste_reduction/nx, sy*self.paste_reduction/ny])\
            .round_to(self.size_round_base)

        dx = (sx - paste_size[0]*nx)/(nx)
        dy = (sy - paste_size[1]*ny)/(ny)

        paste_grid = Vector2D(
                    [paste_size[0]+dx, paste_size[1]+dy]
                ).round_to(self.grid_round_base)

        return [ChamferedPadGrid(
                    number="", type=Pad.TYPE_SMT,
                    center=self.at, size=paste_size, layers=['F.Paste'],
                    chamfer_size=0, chamfer_selection=0,
                    pincount=self.paste_layout, grid=paste_grid,
                    round_radius_handler=self.paste_round_radius_handler
                    )]

    @staticmethod
    def __createPasteGrids(original, grid, count, center):
        r""" Helper function for creating grids of ChamferedPadGrid sections

        :param original: (``ChamferedPadGrid``) --
           This instance will be shallow copied to create a grid.
        :param grid: (``float``, ``Vector2D``) --
           The spacing between instances
        :param count: (``int``, ``[int, int]``) --
           Determines how many copies will be created in x and y direction.
           If only one number is given, both directions use the same count.
        :parma center: (``float``, ``Vector2D``) --
           Center of the resulting grid of grids.
        """
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
                pincount=self.paste_between_vias, grid=self.inner_grid,
                round_radius_handler=self.paste_round_radius_handler
                )

        if not self.kicad4_compatible:
            pad.chamferAvoidCircle(
                        center=self.via_grid/2, diameter=self.via_drill,
                        clearance=self.via_clarance)

        count = [self.vias_in_mask[0]-1, self.vias_in_mask[1]-1]
        return ExposedPad.__createPasteGrids(
                    original=pad, grid=self.via_grid, count=count, center=self.at
                    )

    def __createPasteOutsideX(self):
        pads = []
        corner = ChamferSelPadGrid(
                    {ChamferSelPadGrid.TOP_RIGHT: 1,
                     ChamferSelPadGrid.BOTTOM_RIGHT: 1
                     })
        x = self.top_left_via[0]-self.ring_size[0]/2
        y = self.at[1]-(self.via_layout[1]-2)/2*self.via_grid[1]

        pad_side = ChamferedPadGrid(
            number="", type=Pad.TYPE_SMT,
            center=[x, y],
            size=[self.outer_size[0], self.inner_size[1]],
            layers=['F.Paste'],
            chamfer_size=0, chamfer_selection=corner,
            pincount=[self.paste_rings_outside[0], self.paste_between_vias[1]],
            grid=[self.outer_paste_grid[0], self.inner_grid[1]],
            round_radius_handler=self.paste_round_radius_handler
            )

        if not self.kicad4_compatible:
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
        return pads

    def __createPasteOutsideY(self):
        pads = []
        corner = ChamferSelPadGrid(
                    {ChamferSelPadGrid.BOTTOM_LEFT: 1,
                     ChamferSelPadGrid.BOTTOM_RIGHT: 1
                     })

        x = self.at[0]-(self.via_layout[0]-2)/2*self.via_grid[0]
        y = self.top_left_via[1]-self.ring_size[1]/2

        pad_side = ChamferedPadGrid(
            number="", type=Pad.TYPE_SMT,
            center=[x, y],
            size=[self.inner_size[0], self.outer_size[1]],
            layers=['F.Paste'],
            chamfer_size=0, chamfer_selection=corner,
            pincount=[self.paste_between_vias[0], self.paste_rings_outside[1]],
            grid=[self.inner_grid[0], self.outer_paste_grid[1]],
            round_radius_handler=self.paste_round_radius_handler
            )

        if not self.kicad4_compatible:
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
        return pads

    def __createPasteOutsideCorners(self):
        pads = []
        left = self.top_left_via[0]-self.ring_size[0]/2
        top = self.top_left_via[1]-self.ring_size[1]/2
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
            center=[left, top], size=self.outer_size, layers=['F.Paste'],
            chamfer_size=0, chamfer_selection=0,
            pincount=self.paste_rings_outside,
            grid=self.outer_paste_grid,
            round_radius_handler=self.paste_round_radius_handler
            )

        if not self.kicad4_compatible:
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

    def __createPasteAvoidViasOutside(self):
        self.ring_size = (self.paste_area_size-(Vector2D(self.vias_in_mask)-1)*self.via_grid)/2
        self.outer_paste_grid = Vector2D([s/p if p != 0 else s
                                          for s, p in zip(self.ring_size, self.paste_rings_outside)])
        self.outer_size = self.outer_paste_grid*self.paste_reduction

        pads = []
        if self.paste_rings_outside[0] and self.inner_count[1] > 0:
            pads.extend(self.__createPasteOutsideX())

        if self.paste_rings_outside[1] and self.inner_count[0]:
            pads.extend(self.__createPasteOutsideY())

        if all(self.paste_rings_outside):
            pads.extend(self.__createPasteOutsideCorners())

        return pads

    def __createPaste(self):
        pads = []
        if self.has_vias:
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

    def __createMainPad(self):
        pads = []
        if self.size == self.mask_size:
            layers_main = ['F.Cu', 'F.Mask']
        else:
            layers_main = ['F.Cu']
            pads.append(Pad(
                number="", at=self.at, size=self.mask_size,
                shape=Pad.SHAPE_ROUNDRECT, type=Pad.TYPE_SMT, layers=['F.Mask'],
                round_radius_handler=self.round_radius_handler
            ))

        pads.append(Pad(
            number=self.number, at=self.at, size=self.size,
            shape=Pad.SHAPE_ROUNDRECT, type=Pad.TYPE_SMT, layers=layers_main,
            round_radius_handler=self.round_radius_handler
        ))

        return pads

    def __createVias(self):
        via_layers = ['*.Cu']
        if self.via_tented == ExposedPad.VIA_NOT_TENTED or self.via_tented == ExposedPad.VIA_TENTED_BOTTOM_ONLY:
            via_layers.append('F.Mask')
        if self.via_tented == ExposedPad.VIA_NOT_TENTED or self.via_tented == ExposedPad.VIA_TENTED_TOP_ONLY:
            via_layers.append('B.Mask')

        pads = []
        cy = -((self.via_layout[1]-1)*self.via_grid[1])/2 + self.at.y
        for i in range(self.via_layout[1]):
            pads.append(
                PadArray(center=[self.at.x, cy], initial=self.number,
                         increment=0, pincount=self.via_layout[0],
                         x_spacing=self.via_grid[0], size=self.via_size,
                         type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                         drill=self.via_drill, layers=via_layers
                         ))
            cy += self.via_grid[1]

        if self.add_bottom_pad:
            pads.append(Pad(
                number=self.number, at=self.at, size=self.bottom_size,
                shape=Pad.SHAPE_ROUNDRECT, type=Pad.TYPE_SMT,
                layers=self.bottom_pad_Layers,
                round_radius_handler=self.round_radius_handler
            ))

        return pads

    def getVirtualChilds(self):
        # traceback.print_stack()
        if self.has_vias:
            self.round_radius_handler.limitMaxRadius(self.via_size/2)

        pads = []
        pads += self.__createMainPad()
        if self.has_vias:
            pads += self.__createVias()
        pads += self.__createPaste()
        return pads

    def getRoundRadius(self):
        return self.round_radius_handler.getRoundRadius(min(self.size))
