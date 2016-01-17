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
'''

import math
import time
from copy import deepcopy
from util import parse_coordinate, parse_coordinate_xy, parse_coordinate_xyz, render_position_xy, render_position_xyz


'''
This is my new approach, using a render tree for footprint generation.

ADVANTAGES:

* simple point transformations
* automatic calculation of courtjard,...
* simple duplication of rendering structures

'''


# define in which order the general "lisp" operators are arranged
render_order = ['descr', 'tags', 'attr', 'fp_text', 'fp_circle', 'fp_line', 'pad', 'model']
# TODO: sort Text by type


class Node(object):
    def __init__(self):
        self._parent = None
        self._childs = []


    def append(self, node):
        '''
        add node to child
        '''
        if not isinstance(node, Node):
            raise Exception('invalid object, has to be based on Node')

        self._childs.append(node)

        if node._parent:
            raise Exception('muliple parents are not allowed!')
        node._parent = self


    def extend(self, nodes):
        '''
        add list of nodes to child
        '''
        for node in nodes:
            self.append(node)


    def remove(self, node):
        '''
        remove child from node
        '''
        while self._childs.count(node):
            self._childs.remove(node)

        node._parent = None


    def insert(self, node):
        '''
        moving all childs into the node, and using the node as new child
        '''
        if not isinstance(node, Node):
            raise Exception('invalid object, has to be based on Node')

        for child in self._childs.copy():
            self.remove(child)
            node.append(child)

        self.append(node)


    def copy(self):
        copy = deepcopy(self)
        copy._parent = None
        return copy


    def getRootNode(self):
        if not self._parent:
            return self

        return self._parent.getRootNode()


    def renderList(self):
        render_list = []
        
        # TODO: recursion detection
        
        for child in self._childs:
            child_render_list = child.renderList()
            if type(child_render_list) is list and len(child_render_list):
                render_list.extend(child_render_list)
        return render_list


    def getRealPosition(self, coordinate):
        if not self._parent:
            return parse_coordinate(coordinate)
        
        return self._parent.getRealPosition(coordinate)


    def calculateOutline(self, outline=None):
        min_x, min_y = 0, 0
        max_x, max_y = 0, 0

        if outline:
            min_x = outline['min']['x']
            min_y = outline['min']['y']
            max_x = outline['max']['x']
            max_y = outline['max']['y']

        for child in self._childs:
            child_outline = child.calculateOutline()

            min_x = min([min_x, child_outline['min']['x']])
            min_y = min([min_y, child_outline['min']['y']])
            max_x = max([max_x, child_outline['max']['x']])
            max_y = max([max_y, child_outline['max']['y']])

        return {'min':parse_coordinate_xy((min_x, min_y)), 'max':parse_coordinate_xy((max_x, max_y))}


    def _getRenderTreeText(self):
        '''
        Text which is displayed when generating a render tree
        '''
        return type(self).__name__


    def _getRenderTreeSymbol(self):
        '''
        Symbol which is displayed when generating a render tree
        '''
        if self._parent is None:
            return "+"

        return "*"


    def getRenderTree(self, rendered_nodes=None):
        '''
        print render tree
        '''
        if rendered_nodes is None:
            rendered_nodes = set()

        if self in rendered_nodes:
            raise Exception('recursive definition of render tree!')

        rendered_nodes.add(self)

        tree_str = "{0} {1}".format(self._getRenderTreeSymbol(), self._getRenderTreeText())
        for child in self._childs:
            tree_str += '\r\n  '
            tree_str += '  '.join(child.getRenderTree(rendered_nodes).splitlines(True))

        return tree_str


class Translation(Node):
    '''
    Apply translation to the child tree
    '''
    def __init__(self, x, y):
        Node.__init__(self)

        # translation information
        self.offset_x = x
        self.offset_y = y


    def getRealPosition(self, coordinate):
        parsed_coordinate = parse_coordinate(coordinate)

        # calculate translation
        translation_coordinate = {'x': parsed_coordinate['x'] + self.offset_x
                                 ,'y': parsed_coordinate['y'] + self.offset_y
                                 ,'r': parsed_coordinate['r']}

        if not self._parent:
            return translation_coordinate
        else:
            return self._parent.getRealPosition(translation_coordinate)


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [x: {x}, y: {y}]".format(x=self.offset_x
                                                 ,y=self.offset_y)

        return render_text


class Rotation(Node):
    '''
    Apply rotation to the child tree
    '''
    def __init__(self, r):
        Node.__init__(self)
        self.rotation = r # as degree


    def getRealPosition(self, coordinate):
        parsed_coordinate = parse_coordinate(coordinate)
        
        phi = self.rotation*math.pi/180
        rotation_coordinate = {'x': parsed_coordinate['x']*math.cos(phi) + parsed_coordinate['y']*math.sin(phi)
                              ,'y': -parsed_coordinate['x']*math.sin(phi) + parsed_coordinate['y']*math.cos(phi)
                              ,'r': parsed_coordinate['r'] + self.rotation}

        if not self._parent:
            return rotation_coordinate
        else:
            return self._parent.getRealPosition(rotation_coordinate)


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [r: {r}]".format(r=self.rotation)

        return render_text


class Line(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.start_pos = parse_coordinate(kwargs['start'])
        self.end_pos = parse_coordinate(kwargs['end'])

        self.layer=kwargs['layer']
        self.width=kwargs['width']


    def renderList(self):
        render_list = ["(fp_line {start} {end} (layer {layer}) (width {width}))".format(start=render_position_xy('start', self.getRealPosition(self.start_pos))
                                                                                       ,end=render_position_xy('end', self.getRealPosition(self.end_pos))
                                                                                       ,layer=self.layer
                                                                                       ,width=self.width)]
        render_list.extend(Node.renderList(self))
        return render_list


    def calculateOutline(self):
        render_start_pos = self.getRealPosition(self.start_pos)
        render_end_pos = self.getRealPosition(self.end_pos)

        min_x = min([render_start_pos['x'], render_end_pos['x']])
        min_y = min([render_start_pos['y'], render_end_pos['y']])
        max_x = max([render_start_pos['x'], render_end_pos['x']])
        max_y = max([render_start_pos['y'], render_end_pos['y']])

        return Node.calculateOutline({'min':parse_coordinate_xy((min_x, min_y)), 'max':parse_coordinate_xy((max_x, max_y))})


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " (fp_line {start} {end} (layer {layer}) (width {width}))".format(start=render_position_xy('start', self.start_pos)
                                                                                        ,end=render_position_xy('end', self.end_pos)
                                                                                        ,layer=self.layer
                                                                                        ,width=self.width)
        
        return render_text


class PolygoneLine(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.polygone_line = kwargs['polygone']
        
        self.layer=kwargs['layer']
        self.width=kwargs['width']
        
        self.extend(self._createChildNodes(self.polygone_line))

    def _createChildNodes(self, polygone_line):
        nodes = []

        for line_start, line_end in zip(polygone_line, polygone_line[1:]):
            nodes.append(Line(start=line_start, end=line_end, layer=self.layer, width=self.width))

        return nodes


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " ["
        
        node_strings = []
        for node in self.polygone_line:
            node_position = parse_coordinate(node)
            node_strings.append("[x: {x}, y: {y}]".format(x=node_position['x']
                                                         ,y=node_position['y']))

        if len(node_strings) <= 6:
            render_text += " ,".join(node_strings)
        else:
            # display only a few nodes of the beginning and the end of the polygone line
            render_text += " ,".join(node_strings[:3])
            render_text += " ,... ,"
            render_text += " ,".join(node_strings[-3:])

        render_text += "]"

        return render_text


class RectLine(PolygoneLine):
    def __init__(self, **kwargs):
        self.start_pos = parse_coordinate(kwargs['start'])
        self.end_pos = parse_coordinate(kwargs['end'])

        polygone_line = [{'x':self.start_pos['x'], 'y':self.start_pos['y']}
                        ,{'x':self.start_pos['x'], 'y':self.end_pos['y']}
                        ,{'x':self.end_pos['x'], 'y':self.end_pos['y']}
                        ,{'x':self.end_pos['x'], 'y':self.start_pos['y']}
                        ,{'x':self.start_pos['x'], 'y':self.start_pos['y']}]

        PolygoneLine.__init__(self, polygone=polygone_line, layer=kwargs['layer'], width=kwargs['width'])


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [start: [x: {sx}, y: {sy}] end: [x: {ex}, y: {ey}]]".format(sx=self.start_pos['x']
                                                                                    ,sy=self.start_pos['y']
                                                                                    ,ex=self.end_pos['x']
                                                                                    ,ey=self.end_pos['y'])

        return render_text


class Circle(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.center_pos = parse_coordinate(kwargs['center'])
        self.radius = kwargs['radius']

        self.end_pos = {'x':self.center_pos['x']+self.radius, 'y':self.center_pos['y']}

        self.layer=kwargs['layer']
        self.width=kwargs['width']


    def renderList(self):
        render_list = ["(fp_circle {center} {end} (layer {layer}) (width {width}))".format(center=render_position_xy('center', self.getRealPosition(self.center_pos))
                                                                                          ,end=render_position_xy('end', self.getRealPosition(self.end_pos))
                                                                                          ,layer=self.layer
                                                                                          ,width=self.width)]
        render_list.extend(Node.renderList(self))
        return render_list


    def calculateOutline(self):
        min_x = self.center_pos['x']-self.radius
        min_y = self.center_pos['y']-self.radius
        max_x = self.center_pos['x']+self.radius
        max_y = self.center_pos['y']+self.radius

        return Node.calculateOutline({'min':parse_coordinate_xy((min_x, min_y)), 'max':parse_coordinate_xy((max_x, max_y))})


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " (fp_circle {center} {end} (layer {layer}) (width {width}))".format(center=render_position_xy('center', self.center_pos)
                                                                                           ,end=render_position_xy('end', self.end_pos)
                                                                                           ,layer=self.layer
                                                                                           ,width=self.width)

        return render_text


class Arc(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.start_pos = parse_coordinate(kwargs['start'])
        self.end_pos = parse_coordinate(kwargs['end'])
        self.angle = kwargs['angle']

        self.layer=kwargs['layer']
        self.width=kwargs['width']


    def renderList(self):
        render_list = ["(fp_arc {start} {end} (angle {angle}) (layer {layer}) (width {width}))".format(start=render_position_xy('start', self.getRealPosition(self.start_pos))
                                                                                                      ,end=render_position_xy('end', self.getRealPosition(self.end_pos))
                                                                                                      ,angle=self.angle
                                                                                                      ,layer=self.layer
                                                                                                      ,width=self.width)]
        render_list.extend(Node.renderList(self))
        return render_list


    def calculateOutline(self):
        min_x = min(self.start_pos['x'], self.end_pos['x'])
        min_y = min(self.start_pos['y'], self.end_pos['y'])
        max_x = max(self.start_pos['x'], self.end_pos['x'])
        max_y = max(self.start_pos['y'], self.end_pos['y'])

        return Node.calculateOutline({'min':parse_coordinate_xy((min_x, min_y)), 'max':parse_coordinate_xy((max_x, max_y))})


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " (fp_arc {start} {end} (angle {angle}) (layer {layer}) (width {width}))".format(start=render_position_xy('center', self.start_pos)
                                                                                                       ,end=render_position_xy('end', self.end_pos)
                                                                                                       ,angle=self.angle
                                                                                                       ,layer=self.layer
                                                                                                       ,width=self.width)

        return render_text

class Text(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.type = kwargs['type']
        self.text = kwargs['text']
        self.at = parse_coordinate_xy(kwargs['at'])

        self.layer=kwargs['layer']
        self.thickness = kwargs.get('thickness', 0.15)


    def renderList(self):
        render_string = "(fp_text {type} {text} {at} (layer {layer})\r\n".format(type=self.type
                                                                                ,text=self.text
                                                                                ,at=render_position_xy('at', self.getRealPosition(self.at))
                                                                                ,layer=self.layer)
        render_string += "  (effects (font (thickness {thickness})))\r\n".format(thickness=self.thickness)
        render_string += ")"

        render_list = [render_string]

        render_list.extend(Node.renderList(self))
        return render_list


    def calculateOutline(self):
        # TODO: implementation

        return Node.calculateOutline()


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [type: {type} text: {text}, at: {at}, layer: {layer}, thickness: {thickness}]".format(type=self.type
                                                                                                              ,text=self.text
                                                                                                              ,at=render_position_xy('at', self.getRealPosition(self.at))
                                                                                                              ,layer=self.layer
                                                                                                              ,thickness=self.thickness)

        return render_text


class Model(Node):
    def __init__(self, **kwargs):
        Node.__init__(self)
        self.filename = kwargs['filename']
        self.at = parse_coordinate_xyz(kwargs['at'])
        self.scale = parse_coordinate_xyz(kwargs['scale'])
        self.rotate = parse_coordinate_xyz(kwargs['rotate'])


    def renderList(self):
        render_string = "(model {filename}\r\n".format(filename=self.filename)
        render_string += "  (at {at})\r\n".format(at=render_position_xyz('xyz', self.at)) # TODO: apply position from parent nodes (missing z)
        render_string += "  (scale {at})\r\n".format(at=render_position_xyz('xyz', self.scale)) # TODO: apply scale from parent nodes
        render_string += "  (rotate {at})\r\n".format(at=render_position_xyz('xyz', self.rotate)) # TODO: apply rotation from parent nodes
        render_string += ")"

        render_list = [render_string]

        render_list.extend(Node.renderList(self))
        return render_list


    def _getRenderTreeText(self):
        render_text = Node._getRenderTreeText(self)
        render_text += " [filename: {filename}, at: {at}, scale: {scale}, rotate: {rotate}]".format(filename=self.filename
                                                                                                   ,at=render_position_xyz('xyz', self.at)
                                                                                                   ,scale=render_position_xyz('xyz', self.scale)
                                                                                                   ,rotate=render_position_xyz('xyz', self.rotate))

        return render_text


class KicadMod(Node):
    '''
    Root Node to generate KicadMod
    '''
    def __init__(self, name):
        Node.__init__(self)
        
        self.name = name
        self.description = None
        self.tags = None
        self.attribute = None
        
        # generate courtyard automatically from footprint (TODO)
        self.auto_courtyard = False
        self.courtyard_distance = 0.25


    def setName(self, name):
        self.name = name


    def setDescription(self, description):
        self.description = description


    def setTags(self, tags):
        self.tags = tags


    def setAttribute(self, value):
        self.attribute = value


    def render(self):
        render_string = "(module {name} (layer F.Cu) (tedit {timestamp:X})\r\n".format(name=self.name, timestamp=int(time.time()))

        if self.description:
            render_string += '  (descr "{description}")\r\n'.format(description=self.description)

        if self.tags:
            render_string += '  (tags "{tags}")\r\n'.format(tags=self.tags)

        if self.attribute:
            render_string += '  (attr {attr})\r\n'.format(attr=self.attribute)

        # read render list, sort it by key and reformate multiline entities
        render_list = sorted(self.renderList(), key=lambda string: render_order.index(string.split()[0][1:]))
        render_list = [s.replace('\r\n', '\r\n  ') for s in render_list]

        render_string += "  "
        render_string += "\r\n  ".join(render_list)
        render_string += "\r\n"

        render_string += ")"

        return render_string


    def __str__(self):
        return self.render()

