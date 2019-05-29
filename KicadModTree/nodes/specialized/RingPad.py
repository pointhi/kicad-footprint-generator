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

from copy import copy
from KicadModTree.nodes.Node import Node
from KicadModTree.util.paramUtil import *
from KicadModTree.util.geometric_util import geometricArc, geometricLine, BaseNodeIntersection
from KicadModTree.Vector import *
from KicadModTree.nodes.base.Pad import Pad
from KicadModTree.nodes.base.Circle import Circle
from KicadModTree.nodes.base.Arc import Arc
from KicadModTree.nodes.base.Line import Line
from math import sqrt, sin, cos, pi, ceil


class RingPadPrimitive(Node):
    r"""Add a RingPad to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
      * *radius*: (``float``) --
        middle radius of the ring
      * *width*: (``float``) --
        width of the ring (outer radius - inner radius)
      * *at*: (``Vector2D``) --
        position of the center
      * *layers*: (``Pad.Layers``) --
        layers used for creating the pad
      * *number* (``int``, ``str``) --
        number/name of the pad (default: \"\")
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self.at = Vector2D(kwargs.get('at', (0, 0)))
        self.radius = float(kwargs['radius'])
        self.width = float(kwargs['width'])
        self.layers = kwargs['layers']
        self.number = kwargs.get('number', "")

    def copy(self):
        return RingPadPrimitive(
                    at=self.at, radius=self.radius,
                    width=self.width, layers=self.layers,
                    number=self.number
                    )

    def getVirtualChilds(self):
        return [Pad(number=self.number,
                    type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                    at=(self.at+Vector2D(self.radius, 0)),
                    size=self.width, layers=self.layers,
                    primitives=[Circle(
                        center=(-self.radius, 0),
                        radius=self.radius,
                        width=self.width
                        )]
                    )]


class ArcPadPrimitive(Node):
    r"""Add a RingPad to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad (default: \"\")
        * *width* (``float``) --
          width of the pad
        * *layers* (``Pad.Layers``) --
          layers on which are used for the pad
        * *round_radius_ratio* (``float``) --
          round radius.
          default: 25\% of ring width
        * *max_round_radius* (``float``) --
          maximum round radius, default: 0.25
          Use none to ignore
        * *reference_arc* (``geometricArc``) --
          the reference arc used for this pad
        * *start_line* (``geometricLine``) --
          line confining the side near the reference points start point
        * *end_line* (``geometricLine``) --
          line confining the side near the reference points end point
        * *minimum_overlap* (``float``)
          minimum overlap. default 0.1
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self.reference_arc = geometricArc(geometry=kwargs['reference_arc'])
        self.width = float(kwargs['width'])

        self.number = kwargs.get('number', "")
        self.layers = kwargs['layers']
        self.minimum_overlap = kwargs.get('minimum_overlap', 0.1)

        self.setRoundRadius(**kwargs)
        self.setLimitingLines(**kwargs)

    def setRoundRadius(self, **kwargs):
        if 'round_radius' in kwargs:
            self.round_radius = kwargs['round_radius']
            return

        round_radius_ratio = kwargs.get('round_radius_ratio', 0.25)
        max_round_radius = kwargs.get('max_round_radius', 0.25)
        r = self.width*round_radius_ratio
        if max_round_radius is not None and max_round_radius > 0:
            self.round_radius = min(r, max_round_radius)

    def setLimitingLines(self, **kwargs):
        if kwargs.get('start_line') is not None:
            self.start_line = geometricLine(geometry=kwargs.get('start_line'))
        else:
            self.start_line = None
        if kwargs.get('end_line') is not None:
            self.end_line = geometricLine(geometry=kwargs.get('end_line'))
        else:
            self.end_line = None

    def copy(self):
        return ArcPadPrimitive(
                    reference_arc=self.reference_arc,
                    width=self.width,
                    round_radius=self.round_radius,
                    number=self.number,
                    layers=self.layers,
                    start_line=self.start_line,
                    end_line=self.end_line,
                    minimum_overlap=self.minimum_overlap
                    )

    def rotate(self, angle, origin=(0, 0), use_degrees=True):
        r""" Rotate around given origin

        :params:
            * *angle* (``float``)
                rotation angle
            * *origin* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        self.reference_arc.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        if self.start_line is not None:
            self.start_line.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        if self.end_line is not None:
            self.end_line.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        return self

    def translate(self, distance_vector):
        r""" Translate

        :params:
            * *distance_vector* (``Vector2D``)
                2D vector defining by how much and in what direction to translate.
        """

        self.reference_arc.translate(distance_vector)
        if self.start_line is not None:
            self.start_line.translate(distance_vector)
        if self.end_line is not None:
            self.end_line.translate(distance_vector)
        return self

    def _getStep(self):
        line_width = self.round_radius*2
        if self.minimum_overlap >= line_width:
            raise ValueError('arc line width (round radius) too small for requested overlap')

        required_arcs = ceil((self.width-self.minimum_overlap) / (line_width-self.minimum_overlap))
        return (self.width-line_width)/(required_arcs-1)

    def _getArcPrimitives(self):
        line_width = self.round_radius*2
        step = self._getStep()

        r_inner = self.reference_arc.getRadius()-self.width/2+line_width/2
        r_outer = self.reference_arc.getRadius()+self.width/2-line_width/2

        ref_arc = Arc(geometry=self.reference_arc, width=line_width).setRadius(r_outer)

        nodes = []
        r = r_inner
        while r < r_outer:
            nodes.append(ref_arc.copy().setRadius(r))
            r += step
        nodes.append(ref_arc)

        if self.start_line is not None:
            nodes = self.__cutArcs(nodes, self.start_line, 1)
        if self.end_line is not None:
            nodes = self.__cutArcs(nodes, self.end_line, 0)
        nodes.append(Line(start=nodes[0].getEndPoint(), end=nodes[-1].getEndPoint(), width=line_width))
        nodes.append(Line(start=nodes[0].getStartPoint(), end=nodes[-2].getStartPoint(), width=line_width))

        return nodes

    def __cutArcs(self, arcs, line, index_to_keep):
        if line is None:
            return arcs
        result = []
        for current_arc in arcs:
            try:
                result.append(current_arc.cut(line)[index_to_keep])
            except IndexError as e:
                raise ValueError("Cutting the arc primitive with one of its endlines " +
                                 "did not result in the expected number of arcs.")
        return result

    def getVirtualChilds(self):
        at = self.reference_arc.getMidPoint()
        primitives = self._getArcPrimitives()
        for p in primitives:
            p.translate(-at)
        return [Pad(
                    number=self.number,
                    type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
                    at=at, size=self.width/2, layers=self.layers,
                    primitives=primitives
                    )]


class RingPad(Node):
    r"""Add a RingPad to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad (default: \"\")
        * *at* (``Vector2D``) --
          center position of the pad
        * *rotation* (``float``) --
          rotation of the pad
        * *inner_diameter* (``float``) --
          diameter of the copper free inner zone
        * *size* (``float``) --
          outside diameter of the pad
        * *num_anchors* (``int``) --
          number of anchor pads around the circle
        * *num_paste_zones* (``int``) --
          number of paste zones
        * *paste_to_paste_clearance* (``float``) --
          clearance between two paste zones,
          needed only if number of paste zones > 1
          default: 2*abs(solder_paste_margin)
        * *paste_round_radius_radio* (``float``) --
          round over radius ratio. default 0.25
          resulting radius must be larger than minimum overlap
        * *paste_max_round_radius* (``float``) --
          maximum round radius.
          Only used if number of paste zones > 1
          default: 0.25
          set to None to ignore
        * *solder_paste_margin* (``float``) --
          solder paste margin of the pad (default: 0)
        * *paste_outer_diameter* (``float``) --
          together with paste inner diameter an alternative for defining the paste area
        * *paste_inner_diameter* (``float``) --
          together with paste outer diameter an alternative for defining the paste area
        * *solder_mask_margin* (``float``) --
          solder mask margin of the pad (default: 0)
        * *minimum_overlap* (``float``) --
          minimum arc overlap. default 0.1
    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self.solder_mask_margin = kwargs.get('solder_mask_margin', 0)
        self.minimum_overlap = kwargs.get('minimum_overlap', 0.1)
        self._initPosition(**kwargs)
        self._initSize(**kwargs)
        self._initNumber(**kwargs)
        self._initPasteSettings(**kwargs)
        self._initNumAnchor(**kwargs)
        self._generatePads()

    def _initSize(self, **kwargs):
        _id = kwargs.get('inner_diameter')
        _od = kwargs.get('size')
        if _od is None or _id is None:
            raise KeyError('pad size or inside diameter not declared (like "size=1, inner_diameter=0.5")')
        if type(_id) not in [int, float] or type(_od) not in [int, float]:
            raise ValueError('ring pad size and inner_diameter only support int or float')
        if _id >= _od:
            raise ValueError('inner diameter must be larger than size')

        self.radius = (_id+_od)/4
        self.width = (_od-_id)/2
        self.size = _od
        self.is_circle = _id == 0

    def _initNumber(self, **kwargs):
        self.number = kwargs.get('number', "")  # default to an un-numbered pad

    def _initNumAnchor(self, **kwargs):
        self.num_anchor = int(kwargs.get('num_anchor', 1))
        if self.num_anchor < 1:
            raise ValueError('num_anchor must be a positive integer')

    def _initPosition(self, **kwargs):
        if 'at' not in kwargs:
            raise KeyError('center position not declared (like "at=[0,0]")')
        self.at = Vector2D(kwargs.get('at'))

    def _initPasteSettings(self, **kwargs):
        self.solder_paste_margin = kwargs.get('solder_paste_margin', 0)
        if 'paste_outer_diameter' in kwargs and 'paste_inner_diameter' in kwargs:
            self.paste_width = (kwargs['paste_outer_diameter'] - kwargs['paste_inner_diameter'])/2
            self.paste_center = (kwargs['paste_outer_diameter'] + kwargs['paste_inner_diameter'])/4
        else:
            self.paste_width = self.width + 2*self.solder_paste_margin
            self.paste_center = self.radius

        self.num_paste_zones = int(kwargs.get('num_paste_zones', 1))
        if self.num_paste_zones < 1:
            raise ValueError('num_paste_zones must be a positive integer')

        if self.num_paste_zones > 1:
            self.paste_max_round_radius = float(kwargs.get('paste_max_round_radius', 0.25))
            self.paste_round_radius_radio = float(
                kwargs.get('paste_round_radius_radio', 0.25))

            self.paste_to_paste_clearance = kwargs.get('paste_to_paste_clearance')
            if self.paste_to_paste_clearance is None:
                self.paste_to_paste_clearance = -self.solder_paste_margin

            if self.paste_round_radius_radio <= 0:
                raise ValueError('paste_round_radius_radio must be > 0')
            if self.paste_max_round_radius is not None and self.paste_max_round_radius <= 0:
                raise ValueError('paste_max_round_radius must be > 0')

            if self.paste_to_paste_clearance <= 0:
                raise ValueError('paste_to_paste_clearance must be > 0')

    def _generatePads(self):
        self.pads = []
        if self.num_paste_zones > 1:
            layers = ['F.Cu', 'F.Mask']
            self._generatePastePads()
        else:
            layers = ['F.Cu', 'F.Mask', 'F.Paste']

        if not self.is_circle:
            self._generateCopperPads()
        else:
            self.pads.append(
                Pad(number=self.number,
                    type=Pad.TYPE_SMT, shape=Pad.SHAPE_CIRCLE,
                    at=(self.at), size=self.size,
                    layers=layers
                    ))

    def _generatePastePads(self):
        ref_angle = 360/self.num_paste_zones

        ref_arc = geometricArc(
                    center=self.at,
                    start=self.at+(self.paste_center, 0),
                    angle=ref_angle)

        pad = ArcPadPrimitive(
                            number="", width=self.paste_width,
                            round_radius_ratio=self.paste_round_radius_radio,
                            max_round_radius=self.paste_max_round_radius,
                            layers=['F.Paste'], reference_arc=ref_arc,
                            minimum_overlap=self.minimum_overlap
                            )

        w = pad.round_radius*2
        y = (self.paste_to_paste_clearance + w)/2

        start_line = geometricLine(start=self.at+(0, y), end=self.at+(1, y))
        end_line = geometricLine(start=self.at+(0, -y), end=self.at+(1, -y)).rotate(ref_angle, origin=self.at)

        if self.num_paste_zones == 2:
            end_line = None

        pad.setLimitingLines(start_line=start_line, end_line=end_line)

        self.pads.append(pad)
        for i in range(1, self.num_paste_zones):
            self.pads.append(pad.copy().rotate(i*ref_angle, origin=self.at))

    def _generateMaskPads(self):
        w = self.width+2*self.solder_mask_margin
        self.pads.append(
            RingPadPrimitive(
                number="",
                at=self.at,
                width=self.width+2*self.solder_mask_margin,
                layers=['F.Mask'],
                radius=self.radius
                ))

    def _generateCopperPads(self):
        # kicad_mod.append(c)
        layers = ['F.Cu']
        if self.num_paste_zones == 1:
            if self.solder_paste_margin == 0:
                layers.append('F.Paste')
            else:
                self.pads.append(
                    RingPadPrimitive(
                        number="",
                        at=self.at,
                        width=self.width+2*self.solder_paste_margin,
                        layers=['F.Paste'],
                        radius=self.radius
                        ))

        if self.solder_mask_margin == 0:
            # bug in kicad so any clearance other than 0 needs a workaround
            layers.append('F.Mask')
        else:
            self._generateMaskPads()
        self.pads.append(
            RingPadPrimitive(
                number=self.number,
                at=self.at,
                width=self.width,
                layers=layers,
                radius=self.radius
                ))

        a = 360/self.num_anchor
        pos = Vector2D(self.radius, 0)
        for i in range(1, self.num_anchor):
            pos.rotate(a)
            self.pads.append(Pad(number=self.number,
                                 type=Pad.TYPE_SMT, shape=Pad.SHAPE_CIRCLE,
                                 at=(self.at+pos), size=self.width-0.0001,
                                 layers=['F.Cu'],
                                 ))

    def getVirtualChilds(self):
        return self.pads
