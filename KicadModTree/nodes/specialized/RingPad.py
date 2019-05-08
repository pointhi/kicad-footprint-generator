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
from KicadModTree.Vector import *
from KicadModTree.nodes.base.Pad import Pad
from KicadModTree.nodes.base.Circle import Circle
from math import sqrt, sin, cos, pi


# Hacky solution as the sericalizer stuff does not work with inharitance
#class RingPadPrimitive(Pad):
class RingPadPrimitive(Node):
    def __init__(self, radius, width, at, layers, number):
        Node.__init__(self)
        #Pad.__init__(
        self.pad = Pad(
            #self,
            number=number,
            type=Pad.TYPE_SMT, shape=Pad.SHAPE_CUSTOM,
            at=(at+Vector2D(radius, 0)), size=width, layers=layers,
            primitives=[Circle(
                center=(-radius, 0),
                radius=radius,
                width=width
                )]
            )
    def getVirtualChilds(self):
        return [self.pad]

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
        * *inside_diameter* (``float``)
          diameter of the copper free inner zone
        * *size* (``float``)
          outside diameter of the pad
        * *num_anchors* (``int``)
          number of anchor pads around the circle
        * *num_paste_zones* (``int``)
          number of paste zones
        * *paste_to_paste_clearance* (``float``)
          clearance between two paste zones, needed only if number of paste zones > 1
        * *paste_round_radius* (``float``)
          round over radius for paste zones, must be larger than 0, Only used if number of paste zones > 1
        * *solder_paste_margin* (``float``) --
          solder paste margin of the pad (default: 0)
        * *solder_mask_margin* (``float``) --
          solder mask margin of the pad (default: 0)

    """

    def __init__(self, **kwargs):
        Node.__init__(self)
        self._initPosition(**kwargs)
        self._initSize(**kwargs)
        self._initNumber(**kwargs)
        self._initPasteSettings(**kwargs)
        self._initNumAnchor(**kwargs)
        self.solder_paste_margin = kwargs.get('solder_paste_margin', 0)
        self.solder_mask_margin = kwargs.get('solder_mask_margin', 0)
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
        self.num_paste_zones = int(kwargs.get('num_paste_zones', 1))
        if self.num_paste_zones < 1:
            raise ValueError('num_paste_zones must be a positive integer')

    def _generatePads(self):
        self._generateCopperPads()

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
        self.pads = []
        #kicad_mod.append(c)
        layers = ['F.Cu']
        if self.num_paste_zones == 1:
            layers.append('F.Paste')


        if self.solder_mask_margin == 0:
            layers.append('F.Mask') # bug in kicad so any clearance other than 0 needs a workaround
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

        a = 2*pi/self.num_anchor
        for i in range(1,self.num_anchor):
            pos = Vector2D(cos(a*i), sin(a*i))*self.radius
            self.pads.append(Pad(number=self.number,
                                 type=Pad.TYPE_SMT, shape=Pad.SHAPE_CIRCLE,
                                 at=(self.at+pos), size=self.width-0.0001,
                                 layers=['F.Cu'],
                                 ))

    def getVirtualChilds(self):
        return self.pads
