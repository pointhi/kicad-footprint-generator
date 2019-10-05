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
# (C) 2016-2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

from KicadModTree.FileHandler import FileHandler
from KicadModTree.util.kicad_util import *
from KicadModTree.nodes.base.Pad import Pad  # TODO: why .KicadModTree is not enough?
from KicadModTree.nodes.base.Arc import Arc
from KicadModTree.nodes.base.Circle import Circle
from KicadModTree.nodes.base.Line import Line
from KicadModTree.nodes.base.Polygon import Polygon


DEFAULT_LAYER_WIDTH = {'F.SilkS': 0.12,
                       'B.SilkS': 0.12,
                       'F.Fab': 0.10,
                       'B.Fab': 0.10,
                       'F.CrtYd': 0.05,
                       'B.CrtYd': 0.05}

DEFAULT_WIDTH_POLYGON_PAD = 0

DEFAULT_WIDTH = 0.15


def _get_layer_width(layer, width=None):
    if width is not None:
        return width
    else:
        return DEFAULT_LAYER_WIDTH.get(layer, DEFAULT_WIDTH)


class KicadFileHandler(FileHandler):
    r"""Implementation of the FileHandler for .kicad_mod files

    :param kicad_mod:
        Main object representing the footprint
    :type kicad_mod: ``KicadModTree.Footprint``

    :Example:

    >>> from KicadModTree import *
    >>> kicad_mod = Footprint("example_footprint")
    >>> file_handler = KicadFileHandler(kicad_mod)
    >>> file_handler.writeFile('example_footprint.kicad_mod')
    """

    def __init__(self, kicad_mod):
        FileHandler.__init__(self, kicad_mod)

    def serialize(self, **kwargs):
        r"""Get a valid string representation of the footprint in the .kicad_mod format

        :Example:

        >>> from KicadModTree import *
        >>> kicad_mod = Footprint("example_footprint")
        >>> file_handler = KicadFileHandler(kicad_mod)
        >>> print(file_handler.serialize())
        """

        sexpr = ['module', self.kicad_mod.name,
                 ['layer', 'F.Cu'],
                 ['tedit', formatTimestamp(kwargs.get('timestamp'))],
                 SexprSerializer.NEW_LINE
                ]  # NOQA

        if self.kicad_mod.description:
            sexpr.append(['descr', self.kicad_mod.description])
            sexpr.append(SexprSerializer.NEW_LINE)

        if self.kicad_mod.tags:
            sexpr.append(['tags', self.kicad_mod.tags])
            sexpr.append(SexprSerializer.NEW_LINE)

        if self.kicad_mod.attribute:
            sexpr.append(['attr', self.kicad_mod.attribute])
            sexpr.append(SexprSerializer.NEW_LINE)

        if self.kicad_mod.maskMargin:
            sexpr.append(['solder_mask_margin', self.kicad_mod.maskMargin])
            sexpr.append(SexprSerializer.NEW_LINE)

        if self.kicad_mod.pasteMargin:
            sexpr.append(['solder_paste_margin', self.kicad_mod.pasteMargin])
            sexpr.append(SexprSerializer.NEW_LINE)

        if self.kicad_mod.pasteMarginRatio:
            sexpr.append(['solder_paste_ratio', self.kicad_mod.pasteMarginRatio])
            sexpr.append(SexprSerializer.NEW_LINE)

        sexpr.extend(self._serializeTree())

        return str(SexprSerializer(sexpr))

    def _serializeTree(self):
        nodes = self.kicad_mod.serialize()

        grouped_nodes = {}

        for single_node in nodes:
            node_type = single_node.__class__.__name__

            current_nodes = grouped_nodes.get(node_type, [])
            current_nodes.append(single_node)

            grouped_nodes[node_type] = current_nodes

        sexpr = []

        # serialize initial text nodes
        if 'Text' in grouped_nodes:
            reference_nodes = list(filter(lambda node: node.type == 'reference', grouped_nodes['Text']))
            for node in reference_nodes:
                sexpr.append(self._serialize_Text(node))
                sexpr.append(SexprSerializer.NEW_LINE)
                grouped_nodes['Text'].remove(node)

            value_nodes = list(filter(lambda node: node.type == 'value', grouped_nodes['Text']))
            for node in value_nodes:
                sexpr.append(self._serialize_Text(node))
                sexpr.append(SexprSerializer.NEW_LINE)
                grouped_nodes['Text'].remove(node)

        for key, value in sorted(grouped_nodes.items()):
            # check if key is a base node, except Model
            if key not in {'Arc', 'Circle', 'Line', 'Pad', 'Polygon', 'Text'}:
                continue

            # render base nodes
            for node in value:
                sexpr.append(self._callSerialize(node))
                sexpr.append(SexprSerializer.NEW_LINE)

        # serialize 3D Models at the end
        if grouped_nodes.get('Model'):
            for node in grouped_nodes.get('Model'):
                sexpr.append(self._serialize_Model(node))
                sexpr.append(SexprSerializer.NEW_LINE)

        return sexpr

    def _callSerialize(self, node):
        '''
        call the corresponding method to serialize the node
        '''
        method_type = node.__class__.__name__
        method_name = "_serialize_{0}".format(method_type)
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            exception_string = "{name} (node) not found, cannot serialized the node of type {type}"
            raise NotImplementedError(exception_string.format(name=method_name, type=method_type))

    def _serialize_ArcPoints(self, node):
        # in KiCAD, some file attributes of Arc are named not in the way of their real meaning
        center_pos = node.getRealPosition(node.center_pos)
        end_pos = node.getRealPosition(node.start_pos)

        return [
                ['start', center_pos.x, center_pos.y],
                ['end', end_pos.x, end_pos.y],
                ['angle', node.angle]
               ]

    def _serialize_Arc(self, node):
        sexpr = ['fp_arc']
        sexpr += self._serialize_ArcPoints(node)
        sexpr += [
                  ['layer', node.layer],
                  ['width', _get_layer_width(node.layer, node.width)]
                 ]  # NOQA

        return sexpr

    def _serialize_CirclePoints(self, node):
        center_pos = node.getRealPosition(node.center_pos)
        end_pos = node.getRealPosition(node.center_pos + (node.radius, 0))

        return [
                ['center', center_pos.x, center_pos.y],
                ['end', end_pos.x, end_pos.y]
               ]

    def _serialize_Circle(self, node):
        sexpr = ['fp_circle']
        sexpr += self._serialize_CirclePoints(node)
        sexpr += [
                  ['layer', node.layer],
                  ['width', _get_layer_width(node.layer, node.width)]
                 ]  # NOQA

        return sexpr

    def _serialize_LinePoints(self, node):
        start_pos = node.getRealPosition(node.start_pos)
        end_pos = node.getRealPosition(node.end_pos)
        return [
                ['start', start_pos.x, start_pos.y],
                ['end', end_pos.x, end_pos.y]
               ]

    def _serialize_Line(self, node):
        start_pos = node.getRealPosition(node.start_pos)
        end_pos = node.getRealPosition(node.end_pos)

        sexpr = ['fp_line']
        sexpr += self._serialize_LinePoints(node)
        sexpr += [
                ['layer', node.layer],
                 ['width', _get_layer_width(node.layer, node.width)]
                ]  # NOQA

        return sexpr

    def _serialize_Text(self, node):
        sexpr = ['fp_text', node.type, node.text]

        position, rotation = node.getRealPosition(node.at, node.rotation)
        if rotation:
            sexpr.append(['at', position.x, position.y, rotation])
        else:
            sexpr.append(['at', position.x, position.y])

        sexpr.append(['layer', node.layer])
        if node.hide:
            sexpr.append('hide')
        sexpr.append(SexprSerializer.NEW_LINE)

        effects = [
                'effects',
                ['font',
                    ['size', node.size.x, node.size.y],
                    ['thickness', node.thickness]]]

        if node.mirror:
            effects.append(['justify', 'mirror'])

        sexpr.append(effects)
        sexpr.append(SexprSerializer.NEW_LINE)

        return sexpr

    def _serialize_Model(self, node):
        sexpr = ['model', node.filename,
                 SexprSerializer.NEW_LINE,
                 ['at', ['xyz', node.at.x, node.at.y, node.at.z]],
                 SexprSerializer.NEW_LINE,
                 ['scale', ['xyz', node.scale.x, node.scale.y, node.scale.z]],
                 SexprSerializer.NEW_LINE,
                 ['rotate', ['xyz', node.rotate.x, node.rotate.y, node.rotate.z]],
                 SexprSerializer.NEW_LINE
                ]  # NOQA

        return sexpr

    def _serialize_CustomPadPrimitives(self, pad):
        all_primitives = []
        for p in pad.primitives:
            all_primitives.extend(p.serialize())

        grouped_nodes = {}

        for single_node in all_primitives:
            node_type = single_node.__class__.__name__

            current_nodes = grouped_nodes.get(node_type, [])
            current_nodes.append(single_node)

            grouped_nodes[node_type] = current_nodes

        sexpr_primitives = []

        for key, value in sorted(grouped_nodes.items()):
            # check if key is a base node, except Model
            if key not in {'Arc', 'Circle', 'Line', 'Pad', 'Polygon', 'Text'}:
                continue

            # render base nodes
            for p in value:
                if isinstance(p, Polygon):
                    sp = ['gr_poly',
                          self._serialize_PolygonPoints(p, newline_after_pts=True)
                         ]  # NOQA
                elif isinstance(p, Line):
                    sp = ['gr_line'] + self._serialize_LinePoints(p)
                elif isinstance(p, Circle):
                    sp = ['gr_circle'] + self._serialize_CirclePoints(p)
                elif isinstance(p, Arc):
                    sp = ['gr_arc'] + self._serialize_ArcPoints(p)
                else:
                    raise TypeError('Unsuported type of primitive for custom pad.')
                sp.append(['width', DEFAULT_WIDTH_POLYGON_PAD if p.width is None else p.width])
                sexpr_primitives.append(sp)
                sexpr_primitives.append(SexprSerializer.NEW_LINE)

        return sexpr_primitives

    def _serialize_Pad(self, node):
        sexpr = ['pad', node.number, node.type, node.shape]

        position, rotation = node.getRealPosition(node.at, node.rotation)
        if not rotation % 360 == 0:
            sexpr.append(['at', position.x, position.y, rotation])
        else:
            sexpr.append(['at', position.x, position.y])

        sexpr.append(['size', node.size.x, node.size.y])

        if node.type in [Pad.TYPE_THT, Pad.TYPE_NPTH]:
            if node.drill.x == node.drill.y:
                sexpr.append(['drill', node.drill.x])
            else:
                sexpr.append(['drill', 'oval', node.drill.x, node.drill.y])

        sexpr.append(['layers'] + node.layers)
        if node.shape == Pad.SHAPE_ROUNDRECT:
            sexpr.append(['roundrect_rratio', node.radius_ratio])

        if node.shape == Pad.SHAPE_CUSTOM:
            # gr_line, gr_arc, gr_circle or gr_poly
            sexpr.append(SexprSerializer.NEW_LINE)
            sexpr.append(['options',
                         ['clearance', node.shape_in_zone],
                         ['anchor', node.anchor_shape]
                        ])  # NOQA
            sexpr.append(SexprSerializer.NEW_LINE)
            sexpr_primitives = self._serialize_CustomPadPrimitives(node)
            sexpr.append(['primitives', SexprSerializer.NEW_LINE] + sexpr_primitives)

        if node.solder_paste_margin_ratio != 0 or node.solder_mask_margin != 0 or node.solder_paste_margin != 0:
            sexpr.append(SexprSerializer.NEW_LINE)
            if node.solder_mask_margin != 0:
                sexpr.append(['solder_mask_margin', node.solder_mask_margin])
            if node.solder_paste_margin_ratio != 0:
                sexpr.append(['solder_paste_margin_ratio', node.solder_paste_margin_ratio])
            if node.solder_paste_margin != 0:
                sexpr.append(['solder_paste_margin', node.solder_paste_margin])

        return sexpr

    def _serialize_PolygonPoints(self, node, newline_after_pts=False):
        node_points = ['pts']
        if newline_after_pts:
            node_points.append(SexprSerializer.NEW_LINE)
        points_appended = 0
        for n in node.nodes:
            if points_appended >= 4:
                points_appended = 0
                node_points.append(SexprSerializer.NEW_LINE)
            points_appended += 1

            n_pos = node.getRealPosition(n)
            node_points.append(['xy', n_pos.x, n_pos.y])

        return node_points

    def _serialize_Polygon(self, node):
        node_points = self._serialize_PolygonPoints(node)

        sexpr = ['fp_poly',
                 node_points,
                 ['layer', node.layer],
                 ['width', _get_layer_width(node.layer, node.width)]
                ]  # NOQA

        return sexpr
