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
from math import sqrt, floor


class ExposedPad(Node):
    r"""Add an exposed pad

    Complete with correct paste, mask and via handling

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad
        * *at* (``Vector``) --
          center the exposed pad around this point (default: 0,0)
        * *size* (``float``, ``Vector``) --
          size of the pad
        * *solder_mask_margin* (``float``) --
          solder mask margin of the pad (default: 0)
          Only used if mask_size is not specified.
        * *mask_size* (``float``, ``Vector``) --
          size of the mask cutout (If not given, mask will be part of the main pad)
        * *paste_layout* (``int``, ``[int, int]``) --
          paste layout specification.
          How many pads in x and y direction.
          If only a single integer given, x and y direction use the same count.
        * *paste_coverage* (``float``) --
          how much of the mask free area is covered with paste. (default: 0.65)
        * *via_layout* (``int``, ``[int, int]``) --
          thermal via layout specification.
          How many vias in x and y direction.
          If only a single integer given, x and y direction use the same count.
          default: no vias added
        * *via_grid* (``int``, ``Vector``) --
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

        if type(kwargs.get('via_layout')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.via_layout = [int(kwargs.get('via_layout'))]*2
        else:
            self.via_layout = [int(x) for x in kwargs.get('via_layout')]

        self.via_drill = kwargs.get('via_drill', 0.3)
        self.via_size = self.via_drill + 2*kwargs.get('min_annular_ring', 0.15)

        nx = self.via_layout[0]-1
        ny = self.via_layout[1]-1
        if 'via_grid' in kwargs:
            if type(kwargs.get('via_grid')) is int:
                # when the attribute is a simple number, use it for x and y
                self.via_grid = Vector2D([kwargs.get('via_grid'), kwargs.get('via_grid')])
            else:
                self.via_grid = Vector2D(kwargs.get('via_grid'))
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

    @staticmethod
    def __calcPasteDetails(via_count, via_grid, drill, paste_count, mask_size,
                           copper_size, paste_reduction, via_clarance):
        r"""Calculate the paste centers relative to center of pad for one axis

        Inner paste pads are the pads inside the area determined by the
        thermal vias (inside the mask area)
        Outer pads are the ones between the outermost via still inside mask
        and mask

        : param via_count: (``int``) --
            Via count in the direction currently examined
        : param via_grid: (``float``) --
            Via grid in this direction
        : param drill: (``float``) --
            Via drill size
        : param paste_count: (``int`` or ``[int, int]``) --
            Paste count
            * if int: this is the overall count of paste pads in this direction
            * if array: the numbers stand for [inner, outher] pad count
        : param mask_siz: (``float``) --
            Soldermask size in this direction
        : param copper_size: (``float``) --
            Main copper pad size in this direction
        : param paste_reduction: (``float``) --
            Paste reduction factor for this direction (typically sqrt(paste_coverage))
        : param via_clarance: (``float``) --
            Clearance between drill and paste
        """
        paste_area_size = min(mask_size, copper_size)

        if (via_count-1)*via_grid <= paste_area_size:
            vias_in_mask = via_count
        else:
            vias_in_mask = int(floor(paste_area_size/(via_grid-1)))

        if type(paste_count) in [int, float]:
            if vias_in_mask > 1:
                paste_pads_between_two_vias = int(floor(paste_count/(vias_in_mask-1)))
                inner_count = int((vias_in_mask-1)*paste_pads_between_two_vias)
            else:
                inner_count = 0

            outer_count = int(paste_count - inner_count)
        else:
            outer_count = int(paste_count[1])
            paste_pads_between_two_vias = int(floor(paste_count[0]/(vias_in_mask-1)))
            inner_count = int((vias_in_mask-1)*paste_pads_between_two_vias)

        first_via = -(vias_in_mask-1)/2*via_grid
        paste_chamfer_to_via = sqrt(2)*(via_clarance+drill/2)

        if inner_count > 0:
            inner_grid = via_grid/(paste_pads_between_two_vias)
            if outer_count > 0:
                inner_size = paste_reduction*via_grid/(paste_pads_between_two_vias)
            else:
                # inner_grid = mask_size/(inner_count)
                inner_size = paste_reduction*mask_size/(inner_count)

            first = -(inner_count-1)*inner_grid/2

            paste_edge = first-inner_size/2
            chamfer_reference_point = first_via+paste_chamfer_to_via
            inner_chamfer = chamfer_reference_point - paste_edge

            positions = []
            for i in range(vias_in_mask-1):
                p = []
                for j in range(paste_pads_between_two_vias):
                    p.append(first+(i*paste_pads_between_two_vias+j)*inner_grid)
                positions.append(p)
            inner_pads = {
                'pos': positions,
                'size': inner_size,
                'chamfer': inner_chamfer,
                'edge_to_via': first_via - paste_edge
                }
        else:
            inner_pads = {
                'pos': []
                }

        outer_space = paste_area_size/2+first_via
        outer_per_side = outer_count//2
        if outer_per_side > 0:
            outer_grid = outer_space/(outer_per_side+1)
            first = first_via - outer_grid*outer_per_side

            outer_size = paste_reduction*outer_space/outer_per_side

            paste_edge = first+outer_size/2
            chamfer_reference_point = first_via-paste_chamfer_to_via
            outer_chamfer = chamfer_reference_point - paste_edge

            outer_pads = {
                'pos': [first+i*outer_grid for i in range(outer_per_side)],
                'size': outer_size,
                'chamfer': outer_chamfer,
                'edge_to_via': paste_edge - first_via
                }
        else:
            outer_pads = outer_pads = {
                'pos': []
                }

        return inner_pads, outer_pads

    def _initPaste(self, **kwargs):
        self.paste_avoid_via = kwargs.get('paste_avoid_via', False)
        paste_reduction = sqrt(kwargs.get('paste_coverage', 0.65))

        if self.has_vias and self.paste_avoid_via:
            via_clarance = kwargs.get('via_paste_clarance', 0.05)
            default_paste_layout = [l-1 for l in self.via_layout]

            paste_layout = kwargs.get('paste_layout', default_paste_layout)
            if type(paste_layout) in [float, int]:
                paste_layout = [paste_layout, paste_layout]

            self.gen_paste_x_inner, self.gen_paste_x_outher = ExposedPad.__calcPasteDetails(
                self.via_layout[0], self.via_grid[0], self.via_drill,
                paste_layout[0], self.mask_size.x, self.size.x,
                paste_reduction, via_clarance)

            self.gen_paste_y_inner, self.gen_paste_y_outher = ExposedPad.__calcPasteDetails(
                self.via_layout[1], self.via_grid[1], self.via_drill,
                paste_layout[1], self.mask_size.y, self.size.y,
                paste_reduction, via_clarance)
            return

        if not kwargs.get('paste_layout'):
            self.paste_layout = [1, 1]
        if type(kwargs.get('paste_layout')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.paste_layout = [int(kwargs.get('paste_layout'))]*2
        else:
            self.paste_layout = [int(x) for x in kwargs.get('paste_layout')]

        nx = self.paste_layout[0]
        ny = self.paste_layout[1]

        sx = self.mask_size.x
        sy = self.mask_size.y

        self.paste_size = Vector2D([sx*paste_reduction/nx, sy*paste_reduction/ny])\
            .round_to(kwargs.get('size_round_base', 0.01))

        dx = (sx - self.paste_size[0]*nx)/(nx+1)
        dy = (sy - self.paste_size[1]*ny)/(ny+1)

        self.paste_grid = Vector2D(
                    [self.paste_size[0]+dx, self.paste_size[1]+dy]
                ).round_to(kwargs.get('grid_round_base', 0.01))

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

        if self.has_vias and self.paste_avoid_via:
            chamfer_size_inner = [
                self.gen_paste_x_inner['chamfer']+self.gen_paste_y_inner['edge_to_via'],
                self.gen_paste_y_inner['chamfer']+self.gen_paste_x_inner['edge_to_via'],
            ]

            for posx in self.gen_paste_x_inner['pos']:
                for idx_x, x in enumerate(posx):
                    for posy in self.gen_paste_y_inner['pos']:
                        for idx_y, y in enumerate(posy):
                            corner = CornerSelection(0)
                            if chamfer_size_inner[0] > 0 and chamfer_size_inner[1] > 0:
                                if idx_x == 0 and idx_y == 0:
                                    corner[CornerSelection.TOP_LEFT] = 1
                                if idx_x == len(posx)-1 and idx_y == 0:
                                    corner[CornerSelection.TOP_RIGHT] = 1
                                if idx_x == len(posx)-1 and idx_y == len(posy)-1:
                                    corner[CornerSelection.BOTTOM_RIGHT] = 1
                                if idx_x == 0 and idx_y == len(posy)-1:
                                    corner[CornerSelection.BOTTOM_LEFT] = 1
                            if corner.isAnySelected():
                                pads.append(ChamferedPad(
                                    at=self.at+[x, y], number="",
                                    size=[self.gen_paste_x_inner['size'], self.gen_paste_y_inner['size']],
                                    corner_selection=corner,
                                    chamfer_size=chamfer_size_inner,
                                    type=Pad.TYPE_SMT, layers=['F.Paste']
                                    ))
                            else:
                                pads.append(Pad(
                                    at=self.at+[x, y], number="",
                                    size=[self.gen_paste_x_inner['size'], self.gen_paste_y_inner['size']],
                                    corner_selection=corner, shape=Pad.SHAPE_RECT,
                                    type=Pad.TYPE_SMT, layers=['F.Paste']
                                    ))

        else:
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

    def getVirtualChilds(self):
        return self.virtual_childs
