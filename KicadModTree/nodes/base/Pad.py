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

from KicadModTree.util.paramUtil import *
from KicadModTree.Vector import *
from KicadModTree.nodes.Node import Node
from KicadModTree.util.kicad_util import lispString
from KicadModTree.nodes.base.Arc import Arc
from KicadModTree.nodes.base.Circle import Circle
from KicadModTree.nodes.base.Line import Line
from KicadModTree.nodes.base.Polygon import Polygon


class RoundRadiusHandler(object):
    r"""Handles round radius setting of a pad

    :param \**kwargs:
        See below

    :Keyword Arguments:
    * *radius_ratio* (``float [0 <= r <= 0.5]``) --
      The radius ratio of the rounded rectangle. (default set by default_radius_ratio)
    * *maximum_radius* (``float``) --
      The maximum radius for the rounded rectangle.
      If the radius produced by the radius_ratio parameter for the pad would
      exceed the maximum radius, the ratio is reduced to limit the radius.
      (This is useful for IPC-7351C compliance as it suggests 25% ratio with limit 0.25mm)
    * *round_radius_exact* (``float``) --
      Set an exact round radius for a pad.
    * *default_radius_ratio* (``float [0 <= r <= 0.5]``) --
      This parameter allows to set the default radius ratio
      (backwards compatibility option for chamfered pads)
    """
    def __init__(self, **kwargs):
        default_radius_ratio = getOptionalNumberTypeParam(
                            kwargs, 'default_radius_ratio', default_value=0.25,
                            low_limit=0, high_limit=0.5)
        self.radius_ratio = getOptionalNumberTypeParam(
                            kwargs, 'radius_ratio', default_value=default_radius_ratio,
                            low_limit=0, high_limit=0.5)

        self.maximum_radius = getOptionalNumberTypeParam(kwargs, 'maximum_radius')
        self.round_radius_exact = getOptionalNumberTypeParam(kwargs, 'round_radius_exact')

        self.kicad4_compatible = kwargs.get('kicad4_compatible', False)

    def getRadiusRatio(self, shortest_sidelength):
        r"""get the resulting round radius ratio

        :param shortest_sidelength: shortest sidelength of a pad
        :return: the resulting round radius ratio to be used for the pad
        """
        if self.kicad4_compatible:
            return 0

        if self.round_radius_exact is not None:
            if self.round_radius_exact > shortest_sidelength/2:
                raise ValueError(
                    "requested round radius of {} is too large for pad size of {}"
                    .format(self.round_radius_exact, pad_size)
                    )
            if self.maximum_radius is not None:
                return min(self.round_radius_exact, self.maximum_radius)/shortest_sidelength
            else:
                return self.round_radius_exact/shortest_sidelength
        if self.maximum_radius is not None:
            if self.radius_ratio*shortest_sidelength > self.maximum_radius:
                return self.maximum_radius/shortest_sidelength

        return self.radius_ratio

    def getRoundRadius(self, shortest_sidelength):
        r"""get the resulting round radius

        :param shortest_sidelength: shortest sidelength of a pad
        :return: the resulting round radius to be used for the pad
        """
        return self.getRadiusRatio(shortest_sidelength)*shortest_sidelength

    def roundingRequested(self):
        r"""Check if the pad has a rounded corner

        :return: True if rounded corners are required
        """
        if self.kicad4_compatible:
            return False

        if self.maximum_radius == 0:
            return False

        if self.round_radius_exact == 0:
            return False

        if self.radius_ratio == 0:
            return False

        return True

    def limitMaxRadius(self, limit):
        r"""Set a new maximum limit

        :param limit: the new limit.
        """

        if not self.roundingRequested():
            return
        if self.maximum_radius is not None:
            self.maximum_radius = min(self.maximum_radius, limit)
        else:
            self.maximum_radius = limit

    def __str__(self):
        return "ratio {}, max {}, exact {}, v4 compatible {}".format(
                    self.radius_ratio, self.maximum_radius,
                    self.round_radius_exact, self.kicad4_compatible
                    )


class Pad(Node):
    r"""Add a Pad to the render tree

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *number* (``int``, ``str``) --
          number/name of the pad (default: \"\")
        * *type* (``Pad.TYPE_THT``, ``Pad.TYPE_SMT``, ``Pad.TYPE_CONNECT``, ``Pad.TYPE_NPTH``) --
          type of the pad
        * *shape* (``Pad.SHAPE_CIRCLE``, ``Pad.SHAPE_OVAL``, ``Pad.SHAPE_RECT``, ``SHAPE_ROUNDRECT``,
        ``Pad.SHAPE_TRAPEZE``, ``SHAPE_CUSTOM``) --
          shape of the pad
        * *layers* (``Pad.LAYERS_SMT``, ``Pad.LAYERS_THT``, ``Pad.LAYERS_NPTH``) --
          layers on which are used for the pad

        * *at* (``Vector2D``) --
          center position of the pad
        * *rotation* (``float``) --
          rotation of the pad
        * *size* (``float``, ``Vector2D``) --
          size of the pad
        * *offset* (``Vector2D``) --
          offset of the pad
        * *drill* (``float``, ``Vector2D``) --
          drill-size of the pad

        * *radius_ratio* (``float``) --
          The radius ratio of the rounded rectangle.
          Ignored for every shape except round rect.
        * *maximum_radius* (``float``) --
          The maximum radius for the rounded rectangle.
          If the radius produced by the radius_ratio parameter for the pad would
          exceed the maximum radius, the ratio is reduced to limit the radius.
          (This is useful for IPC-7351C compliance as it suggests 25% ratio with limit 0.25mm)
          Ignored for every shape except round rect.
        * *round_radius_exact* (``float``) --
          Set an exact round radius for a pad.
          Ignored for every shape except round rect
        * *round_radius_handler* (``RoundRadiusHandler``) --
          An instance of the RoundRadiusHandler class
          If this is given then all other round radius specifiers are ignored
          Ignored for every shape except round rect

        * *solder_paste_margin_ratio* (``float``) --
          solder paste margin ratio of the pad (default: 0)
        * *solder_paste_margin* (``float``) --
          solder paste margin of the pad (default: 0)
        * *solder_mask_margin* (``float``) --
          solder mask margin of the pad (default: 0)

        * *x_mirror* (``[int, float](mirror offset)``) --
          mirror x direction around offset "point"
        * *y_mirror* (``[int, float](mirror offset)``) --
          mirror y direction around offset "point"

    :Example:

    >>> from KicadModTree import *
    >>> Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
    ...     at=[0, 0], size=[2, 2], drill=1.2, layers=Pad.LAYERS_THT)
    """

    TYPE_THT = 'thru_hole'
    TYPE_SMT = 'smd'
    TYPE_CONNECT = 'connect'
    TYPE_NPTH = 'np_thru_hole'
    _TYPES = [TYPE_THT, TYPE_SMT, TYPE_CONNECT, TYPE_NPTH]

    SHAPE_CIRCLE = 'circle'
    SHAPE_OVAL = 'oval'
    SHAPE_RECT = 'rect'
    SHAPE_ROUNDRECT = 'roundrect'
    SHAPE_TRAPEZE = 'trapezoid'
    SHAPE_CUSTOM = 'custom'
    _SHAPES = [SHAPE_CIRCLE, SHAPE_OVAL, SHAPE_RECT, SHAPE_ROUNDRECT, SHAPE_TRAPEZE, SHAPE_CUSTOM]

    LAYERS_SMT = ['F.Cu', 'F.Mask', 'F.Paste']
    LAYERS_THT = ['*.Cu', '*.Mask']
    LAYERS_NPTH = ['*.Cu', '*.Mask']

    ANCHOR_CIRCLE = 'circle'
    ANCHOR_RECT = 'rect'
    _ANCHOR_SHAPE = [ANCHOR_CIRCLE, ANCHOR_RECT]

    SHAPE_IN_ZONE_CONVEX = 'convexhull'
    SHAPE_IN_ZONE_OUTLINE = 'outline'
    _SHAPE_IN_ZONE = [SHAPE_IN_ZONE_CONVEX, SHAPE_IN_ZONE_OUTLINE]

    def __init__(self, **kwargs):
        Node.__init__(self)
        self.radius_ratio = 0

        self._initNumber(**kwargs)
        self._initType(**kwargs)
        self._initShape(**kwargs)
        self._initPosition(**kwargs)
        self._initSize(**kwargs)
        self._initOffset(**kwargs)
        self._initDrill(**kwargs)  # requires pad type and offset
        self._initSolderPasteMargin(**kwargs)
        self._initSolderPasteMarginRatio(**kwargs)
        self._initSolderMaskMargin(**kwargs)
        self._initLayers(**kwargs)
        self._initMirror(**kwargs)

        if self.shape == self.SHAPE_OVAL and self.size[0] == self.size[1]:
            self.shape = self.SHAPE_CIRCLE

        if self.shape == Pad.SHAPE_OVAL or self.shape == Pad.SHAPE_CIRCLE:
            self.radius_ratio = 0.5
        if self.shape == Pad.SHAPE_ROUNDRECT:
            self._initRadiusRatio(**kwargs)

        if self.shape == Pad.SHAPE_CUSTOM:
            self._initAnchorShape(**kwargs)
            self._initShapeInZone(**kwargs)

            self.primitives = []
            if 'primitives' not in kwargs:
                raise KeyError('primitives must be declared for custom pads')

            for p in kwargs['primitives']:
                self.addPrimitive(p)

    def _initMirror(self, **kwargs):
        self.mirror = [None, None]
        if 'x_mirror' in kwargs and type(kwargs['x_mirror']) in [float, int]:
            self.mirror[0] = kwargs['x_mirror']
        if 'y_mirror' in kwargs and type(kwargs['y_mirror']) in [float, int]:
            self.mirror[1] = kwargs['y_mirror']

        if self.mirror[0] is not None:
            self.at.x = 2 * self.mirror[0] - self.at.x
            self.offset.x *= -1
        if self.mirror[1] is not None:
            self.at.y = 2 * self.mirror[1] - self.at.y
            self.offset.y *= -1

    def _initNumber(self, **kwargs):
        self.number = kwargs.get('number', "")  # default to an un-numbered pad

    def _initType(self, **kwargs):
        if not kwargs.get('type'):
            raise KeyError('type not declared (like "type=Pad.TYPE_THT")')
        self.type = kwargs.get('type')
        if self.type not in Pad._TYPES:
            raise ValueError('{type} is an invalid type for pads'.format(type=self.type))

    def _initShape(self, **kwargs):
        if not kwargs.get('shape'):
            raise KeyError('shape not declared (like "shape=Pad.SHAPE_CIRCLE")')
        self.shape = kwargs.get('shape')
        if self.shape not in Pad._SHAPES:
            raise ValueError('{shape} is an invalid shape for pads'.format(shape=self.shape))

    def _initPosition(self, **kwargs):
        if not kwargs.get('at'):
            raise KeyError('center position not declared (like "at=[0,0]")')
        self.at = Vector2D(kwargs.get('at'))

        self.rotation = kwargs.get('rotation', 0)

    def _initSize(self, **kwargs):
        if not kwargs.get('size'):
            raise KeyError('pad size not declared (like "size=[1,1]")')
        self.size = toVectorUseCopyIfNumber(kwargs.get('size'), low_limit=0)

    def _initOffset(self, **kwargs):
        self.offset = Vector2D(kwargs.get('offset', [0, 0]))

    def _initDrill(self, **kwargs):
        if self.type in [Pad.TYPE_THT, Pad.TYPE_NPTH]:
            if not kwargs.get('drill'):
                raise KeyError('drill size required (like "drill=1")')
            self.drill = toVectorUseCopyIfNumber(kwargs.get('drill'), low_limit=0)
        else:
            self.drill = None
            if kwargs.get('drill'):
                pass  # TODO: throw warning because drill is not supported

    def _initSolderPasteMarginRatio(self, **kwargs):
        self.solder_paste_margin_ratio = kwargs.get('solder_paste_margin_ratio', 0)

    def _initSolderPasteMargin(self, **kwargs):
        self.solder_paste_margin = kwargs.get('solder_paste_margin', 0)

    def _initSolderMaskMargin(self, **kwargs):
        self.solder_mask_margin = kwargs.get('solder_mask_margin', 0)

    def _initLayers(self, **kwargs):
        if not kwargs.get('layers'):
            raise KeyError('layers not declared (like "layers=[\'*.Cu\', \'*.Mask\', \'F.SilkS\']")')
        self.layers = kwargs.get('layers')

    def _initRadiusRatio(self, **kwargs):
        if('round_radius_handler' in kwargs):
            self.round_radius_handler = kwargs['round_radius_handler']
        else:
            self.round_radius_handler = RoundRadiusHandler(**kwargs)

        self.radius_ratio = self.round_radius_handler.getRadiusRatio(min(self.size))

        if self.radius_ratio == 0:
            self.shape = Pad.SHAPE_RECT

    def _initAnchorShape(self, **kwargs):
        self.anchor_shape = kwargs.get('anchor_shape', Pad.ANCHOR_CIRCLE)
        if self.anchor_shape not in Pad._ANCHOR_SHAPE:
            raise ValueError('{shape} is an illegal anchor shape'.format(shape=self.anchor_shape))

    def _initShapeInZone(self, **kwargs):
        self.shape_in_zone = kwargs.get('shape_in_zone', Pad.SHAPE_IN_ZONE_OUTLINE)
        if self.shape_in_zone not in Pad._SHAPE_IN_ZONE:
            raise ValueError('{shape} is an illegal specifier for the shape in zone option'
                             .format(shape=self.shape_in_zone))

    def rotate(self, angle, origin=(0, 0), use_degrees=True):
        r""" Rotate pad around given origin

        :params:
            * *angle* (``float``)
                rotation angle
            * *origin* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        self.at.rotate(angle=angle, origin=origin, use_degrees=use_degrees)
        a = angle if use_degrees else math.degrees(angle)

        # subtraction because kicad text field rotation is the wrong way round
        self.rotation -= a
        return self

    def translate(self, distance_vector):
        r""" Translate pad

        :params:
            * *distance_vector* (``Vector2D``)
                2D vector defining by how much and in what direction to translate.
        """

        self.at += distance_vector
        return self

    # calculate the outline of a pad
    def calculateBoundingBox(self):
        return Node.calculateBoundingBox(self)

    def _getRenderTreeText(self):
        render_strings = ['pad']
        render_strings.append(lispString(self.number))
        render_strings.append(lispString(self.type))
        render_strings.append(lispString(self.shape))
        render_strings.append(self.at.render('(at {x} {y})'))
        render_strings.append(self.size.render('(size {x} {y})'))
        render_strings.append('(drill {})'.format(self.drill))
        render_strings.append('(layers {})'.format(' '.join(self.layers)))

        render_text = Node._getRenderTreeText(self)
        render_text += '({})'.format(' '.join(render_strings))

        return render_text

    def addPrimitive(self, p):
        r""" add a primitve to a custom pad

        :param p: the primitive to add
        """
        self.primitives.append(p)

    def getRoundRadius(self):
        if self.shape == Pad.SHAPE_CUSTOM:
            r_max = 0
            for p in self.primitives:
                r = p.width/2
                if r > r_max:
                    r_max = r
            return r_max
        return self.round_radius_handler.getRoundRadius(min(self.size))
