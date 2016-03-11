'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.

(C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
'''

from KicadModTree.Point import *
from KicadModTree.nodes.Node import Node
from KicadModTree.util.kicad_util import lispString


class Pad(Node):
    TYPE_THT = 'thru_hole'
    TYPE_SMT = 'smd'
    TYPE_CONNECT = 'connect'
    TYPE_NPTH = 'np_thru_hole'
    _TYPES = [TYPE_THT, TYPE_SMT, TYPE_CONNECT, TYPE_NPTH]

    SHAPE_CIRCLE = 'circle'
    SHAPE_OVAL = 'oval'
    SHAPE_RECT = 'rect'
    SHAPE_TRAPEZE = 'trapezoid'
    _SHAPES = [SHAPE_CIRCLE, SHAPE_OVAL, SHAPE_RECT, SHAPE_TRAPEZE]


    def __init__(self, **kwargs):
        Node.__init__(self)

        self._initNumber(**kwargs)
        self._initType(**kwargs)
        self._initShape(**kwargs)
        self._initPosition(**kwargs)
        self._initSize(**kwargs)
        self._initOffset(**kwargs)
        self._initDrill(**kwargs) # requires pad type and offset
        self._initSolderPasteMargin(**kwargs)
        self._initLayers(**kwargs)


    def _initNumber(self, **kwargs):
        self.number = kwargs.get('number')


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
        self.at = Point(kwargs.get('at'))

        self.rotation = kwargs.get('rotation', 0)


    def _initSize(self, **kwargs):
        if not kwargs.get('size'):
            raise KeyError('pad size not declared (like "size=[1,1]")')
        if type(kwargs.get('size')) in [int, float]:
            # when the attribute is a simple number, use it for x and y
            self.size = Point([kwargs.get('size'), kwargs.get('size')])
        else:
            self.size = Point(kwargs.get('size'))


    def _initOffset(self, **kwargs):
        self.offset = Point(kwargs.get('offset', [0,0]))


    def _initDrill(self, **kwargs):
        if self.type in [Pad.TYPE_THT, Pad.TYPE_NPTH]:
            if not kwargs.get('drill'):
                raise KeyError('drill size required (like "drill=1")')
            if type(kwargs.get('drill')) in [int, float]:
                # when the attribute is a simple number, use it for x and y
                self.drill = Point([kwargs.get('drill'), kwargs.get('drill')])
            else:
                self.drill = Point(kwargs.get('drill'))
            if self.drill.x < 0 or self.drill.y < 0:
                raise ValueError("negative drill size not allowed")
        else:
            self.drill = None
            if kwargs.get('drill'):
                pass  # TODO: throw warning because drill is not supported


    def _initSolderPasteMargin(self, **kwargs):
        self.solder_paste_margin_ratio = kwargs.get('solder_paste_margin_ratio', 0)


    def _initLayers(self, **kwargs):
        if not kwargs.get('layers'):
            raise KeyError('layers not declared (like "layers=[\'*.Cu\', \'*.Mask\', \'F.SilkS\']")')
        self.layers=kwargs.get('layers')


    def calculateOutline(self):
        return Node.calculateOutline(self)


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
