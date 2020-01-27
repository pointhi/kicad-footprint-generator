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
# (C) 2018 by Rene Poeschl, github @poeschlr

from __future__ import division

from KicadModTree.util.paramUtil import *
from KicadModTree.Vector import *
from KicadModTree.nodes.base.Polygon import *
from KicadModTree.nodes.specialized.ChamferedPad import *


class ChamferSelPadGrid(CornerSelection):
    r"""Class for handling chamfer selection
        :param chamfer_select:
            * A list of bools do directly set the corners
              (top left, top right, bottom right, bottom left)
            * A dict with keys (Constands see below)
            * The integer 1 means all corners and edges
            * The integer 0 means no corners, no edges

        :constants:
            * ChamferSelPadGrid.TOP_EDGE
            * ChamferSelPadGrid.RIGHT_EDGE
            * ChamferSelPadGrid.BOTTOM_EDGE
            * ChamferSelPadGrid.LEFT_EDGE
            * Plus all constands inherited from CornerSelection

    """

    TOP_EDGE = "t"
    RIGHT_EDGE = "r"
    BOTTOM_EDGE = "b"
    LEFT_EDGE = "l"

    def __init__(self, chamfer_select):
        self.top_edge = False
        self.right_edge = False
        self.bottom_edge = False
        self.left_edge = False

        if chamfer_select == 1:
            self.selectAll()
            CornerSelection.__init__(self, 1)
            return

        if chamfer_select == 0:
            CornerSelection.__init__(self, 0)
            return

        if type(chamfer_select) is dict:
            CornerSelection.__init__(self, chamfer_select)
            for key in chamfer_select:
                self[key] = bool(chamfer_select[key])
        else:
            for i, value in enumerate(chamfer_select):
                self[i] = bool(value)

    def setLeft(self, value=1):
        CornerSelection.setLeft(self, value)
        self.left_edge = bool(value)

    def setTop(self, value=1):
        CornerSelection.setTop(self, value)
        self.top_edge = bool(value)

    def setRight(self, value=1):
        CornerSelection.setRight(self, value)
        self.right_edge = bool(value)

    def setBottom(self, value=1):
        CornerSelection.setBottom(self, value)
        self.bottom_edge = bool(value)

    def setCorners(self, value=1):
        self.top_left = bool(value)
        self.top_right = bool(value)
        self.bottom_right = bool(value)
        self.bottom_left = bool(value)

    def setEdges(self, value=1):
        self.top_edge = bool(value)
        self.right_edge = bool(value)
        self.bottom_edge = bool(value)
        self.left_edge = bool(value)

    def __len__(self):
        return 8

    def __iter__(self):
        for v in CornerSelection.__iter__(self):
            yield v
        yield self.top_edge
        yield self.right_edge
        yield self.bottom_edge
        yield self.left_edge

    def __getitem__(self, item):
        if item in [4, ChamferSelPadGrid.TOP_EDGE]:
            return self.top_edge
        if item in [5, ChamferSelPadGrid.RIGHT_EDGE]:
            return self.right_edge
        if item in [6, ChamferSelPadGrid.BOTTOM_EDGE]:
            return self.bottom_edge
        if item in [7, ChamferSelPadGrid.LEFT_EDGE]:
            return self.left_edge
        return CornerSelection.__getitem__(self, item)

    def __setitem__(self, item, value):
        if item in [4, ChamferSelPadGrid.TOP_EDGE]:
            self.top_edge = bool(value)
        elif item in [5, ChamferSelPadGrid.RIGHT_EDGE]:
            self.right_edge = bool(value)
        elif item in [6, ChamferSelPadGrid.BOTTOM_EDGE]:
            self.bottom_edge = bool(value)
        elif item in [7, ChamferSelPadGrid.LEFT_EDGE]:
            self.left_edge = bool(value)
        else:
            CornerSelection.__setitem__(self, item, value)

    def to_dict(self):
        result = CornerSelection.to_dict(self)
        result.update({
            ChamferSelPadGrid.TOP_EDGE: self.top_edge,
            ChamferSelPadGrid.RIGHT_EDGE: self.right_edge,
            ChamferSelPadGrid.BOTTOM_EDGE: self.bottom_edge,
            ChamferSelPadGrid.LEFT_EDGE: self.left_edge
            })
        return result


class ChamferedPadGrid(Node):
    r"""Add a ChamferedPad to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad (default: \"\")
        * *center* (``Vector2D``) --
          center position of the pad grid
        * *size* (``float``, ``Vector2D``) --
          size of the pads
        * *pincount* (``int``, ``[int, int]``)
          Pad count in x and y direction.
          If only one integer is given, it will be used for both directions.
        * *grid* (``float``, ``Vector2D``)
          Pad grid in x and y direction.
          If only one float is given, it will be used for both directions.

        * *solder_paste_margin_ratio* (``float``) --
          solder paste margin ratio of the pad (default: 0)
        * *solder_paste_margin* (``float``) --
          solder paste margin of the pad (default: 0)
        * *solder_mask_margin* (``float``) --
          solder mask margin of the pad (default: 0)

        * *layers* (``Pad.LAYERS_SMT``, ``Pad.LAYERS_THT``, ``Pad.LAYERS_NPTH``) --
          layers on which are used for the pad
        * *chamfer_selection* (``ChamferSelPadGrid``) --
          Select which corner and edge pads to chamfer.
        * *chamfer_size* (``float``, ``Vector2D``) --
          Size of the chamfer.
        * *x_mirror* (``[int, float](mirror offset)``) --
          mirror x direction around offset "point"
        * *y_mirror* (``[int, float](mirror offset)``) --
          mirror y direction around offset "point"

        * *radius_ratio* (``float``) --
          The radius ratio of the rounded rectangle.
          (default 0 for backwards compatibility)
        * *maximum_radius* (``float``) --
          The maximum radius for the rounded rectangle.
          If the radius produced by the radius_ratio parameter for the pad would
          exceed the maximum radius, the ratio is reduced to limit the radius.
          (This is useful for IPC-7351C compliance as it suggests 25% ratio with limit 0.25mm)
        * *round_radius_exact* (``float``) --
          Set an exact round radius for a pad.
        * *round_radius_handler* (``RoundRadiusHandler``) --
          An instance of the RoundRadiusHandler class
          If this is given then all other round radius specifiers are ignored
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        if len(kwargs) == 0:
            return

        self.number = kwargs.get('number', "")
        self.center = Vector2D(kwargs.get('center', [0, 0]))

        self._initSize(**kwargs)
        self._initCount(**kwargs)
        self._initGrid(**kwargs)
        self._initPadSettings(**kwargs)

    def _initCount(self, **kwargs):
        if 'pincount' not in kwargs:
            raise KeyError('pincount not declared (like "pincount=10")')

        self.pincount = toIntArray(kwargs['pincount'])

    def _initSize(self, **kwargs):
        if 'size' not in kwargs:
            raise KeyError('size not declared (like "size=[1, 2]")')

        self.size = toVectorUseCopyIfNumber(kwargs['size'], low_limit=0)

    def _initGrid(self, **kwargs):
        if 'grid' not in kwargs:
            raise KeyError('grid not declared (like "grid=[1, 2]")')

        self.grid = toVectorUseCopyIfNumber(kwargs['grid'], low_limit=self.size)

    def _initPadSettings(self, **kwargs):
        if 'chamfer_selection' not in kwargs:
            raise KeyError('chamfer selection is required for chamfered pads (like "chamfer_selection=[1,0,0,0]")')

        self.chamfer_selection = ChamferSelPadGrid(kwargs.get('chamfer_selection'))

        if 'chamfer_size' not in kwargs:
            self.chamfer_size = Vector2D(0, 0)
        else:
            self.chamfer_size = toVectorUseCopyIfNumber(
                kwargs.get('chamfer_size'), low_limit=0, must_be_larger=False)

        if('round_radius_handler' in kwargs):
            self.round_radius_handler = kwargs['round_radius_handler']
        else:
            # default radius ration 0 for backwards compatibility
            self.round_radius_handler = RoundRadiusHandler(default_radius_ratio=0, **kwargs)

        self.padargs = copy(kwargs)
        self.padargs.pop('size', None)
        self.padargs.pop('number', None)
        self.padargs.pop('at', None)
        self.padargs.pop('chamfer_size', None)
        self.padargs.pop('round_radius_handler', None)

    def chamferAvoidCircle(self, center, diameter, clearance=0):
        r""" set the chamfer such that the pad avoids a cricle located at near corner.

        :param center: (``Vector2D``) --
           The center of the circle ot avoid
        :param diameter: (``float``, ``Vector2D``) --
           The diameter of the circle. If Vector2D given only x direction is used.
        :param clearance: (``float``) --
           Additional clearance around circle. default:0
        """
        relative_center = Vector2D(center) - self.center

        left = -self.grid['x']*(self.pincount[0]-1)/2
        top = -self.grid['y']*(self.pincount[1]-1)/2

        nearest_x = left
        nearest_y = top

        min_dist_x = abs(relative_center['x']-nearest_x)
        min_dist_y = abs(relative_center['y']-nearest_y)

        for i in range(self.pincount[0]):
            x = left+i*self.grid['x']
            dx = abs(x-relative_center['x'])
            if dx < min_dist_x:
                min_dist_x = dx
                nearest_x = x

        for i in range(self.pincount[1]):
            y = top+i*self.grid['y']
            dy = abs(y-relative_center['y'])
            if dy < min_dist_y:
                min_dist_y = dy
                nearest_y = y

        temp_pad = ChamferedPad(
            at=[nearest_x, nearest_y], size=self.size,
            type=Pad.TYPE_SMT, layers=['F.Cu'], corner_selection=1
        )
        self.chamfer_size = temp_pad.chamferAvoidCircle(
            center=relative_center, diameter=diameter, clearance=clearance)
        return self.chamfer_size

    def __padCornerSelection(self, idx_x, idx_y):
        corner = CornerSelection(0)
        if idx_x == 0:
            if idx_y == 0:
                if self.chamfer_selection[ChamferSelPadGrid.TOP_LEFT]:
                    corner[CornerSelection.TOP_LEFT] = True
                if self.chamfer_selection[ChamferSelPadGrid.LEFT_EDGE]:
                    corner[CornerSelection.BOTTOM_LEFT] = True
            if idx_y == self.pincount[1]-1:
                if self.chamfer_selection[ChamferSelPadGrid.BOTTOM_LEFT]:
                    corner[CornerSelection.BOTTOM_LEFT] = True
                if self.chamfer_selection[ChamferSelPadGrid.LEFT_EDGE]:
                    corner[CornerSelection.TOP_LEFT] = True
            if idx_y != 0 and idx_y != self.pincount[1]-1:
                if self.chamfer_selection[ChamferSelPadGrid.LEFT_EDGE]:
                    corner.setLeft()
        if idx_x == self.pincount[0]-1:
            if idx_y == 0:
                if self.chamfer_selection[ChamferSelPadGrid.TOP_RIGHT]:
                    corner[CornerSelection.TOP_RIGHT] = True
                if self.chamfer_selection[ChamferSelPadGrid.RIGHT_EDGE]:
                    corner[CornerSelection.BOTTOM_RIGHT] = True
            if idx_y == self.pincount[1]-1:
                if self.chamfer_selection[ChamferSelPadGrid.BOTTOM_RIGHT]:
                    corner[CornerSelection.BOTTOM_RIGHT] = True
                if self.chamfer_selection[ChamferSelPadGrid.RIGHT_EDGE]:
                    corner[CornerSelection.TOP_RIGHT] = True
            if idx_y != 0 and idx_y != self.pincount[1]-1:
                if self.chamfer_selection[ChamferSelPadGrid.RIGHT_EDGE]:
                    corner.setRight()
        if idx_x != 0 and idx_x != self.pincount[0]-1:
            if idx_y == 0:
                if self.chamfer_selection[ChamferSelPadGrid.TOP_EDGE]:
                    corner.setTop()
            if idx_y == self.pincount[1]-1:
                if self.chamfer_selection[ChamferSelPadGrid.BOTTOM_EDGE]:
                    corner.setBottom()
        return corner

    def _generatePads(self):
        left = -self.grid['x']*(self.pincount[0]-1)/2+self.center['x']
        top = -self.grid['y']*(self.pincount[1]-1)/2+self.center['y']

        pads = []
        for idx_x in range(self.pincount[0]):
            x = left+idx_x*self.grid['x']
            for idx_y in range(self.pincount[1]):
                y = top+idx_y*self.grid['y']
                corner = self.__padCornerSelection(idx_x, idx_y)
                pads.append(ChamferedPad(
                    at=[x, y], number=self.number, size=self.size,
                    chamfer_size=self.chamfer_size,
                    corner_selection=corner,
                    round_radius_handler=self.round_radius_handler,
                    **self.padargs
                    ))
        return pads

    def getVirtualChilds(self):
        return self._generatePads()

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone
