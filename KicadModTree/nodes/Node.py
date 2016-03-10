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

from copy import deepcopy

from KicadModTree.Point import *


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
        moving all childs into the node, and using the node as new parent of those childs
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


    def serialize(self):
        nodes = [self]
        for child in self.getAllChilds():
            nodes += child.serialize()
        return nodes


    def getNormalChilds(self):
        '''
        Get all normal childs of this node
        '''
        return self._childs


    def getVirtualChilds(self):
        '''
        Get virtual childs of this node
        '''
        return []


    def getAllChilds(self):
        '''
        Get virtual and normal childs of this node
        '''
        return self.getNormalChilds() + self.getVirtualChilds()


    def getParent(self):
        '''
        get Parent Node of this Node
        '''
        return self._parent


    def getRootNode(self):
        '''
        get Root Node of this Node
        '''

        # TODO: recursion detection

        if not self.getParent():
            return self

        return self.getParent().getRootNode()


    def getRealPosition(self, coordinate, rotation=None):
        '''
        return position of point after applying all transformation and rotation operations
        '''
        if not self._parent:
            if rotation is None:
                return Point(coordinate)
            else:
                return Point(coordinate), rotation

        return self._parent.getRealPosition(coordinate, rotation)


    def calculateOutline(self, outline=None):
        min_x, min_y = 0, 0
        max_x, max_y = 0, 0

        if outline:
            min_x = outline['min']['x']
            min_y = outline['min']['y']
            max_x = outline['max']['x']
            max_y = outline['max']['y']

        for child in self.getAllChilds():
            child_outline = child.calculateOutline()

            min_x = min([min_x, child_outline['min']['x']])
            min_y = min([min_y, child_outline['min']['y']])
            max_x = max([max_x, child_outline['max']['x']])
            max_y = max([max_y, child_outline['max']['y']])

        return {'min':Point(min_x, min_y), 'max':Point(max_x, max_y)}


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
        for child in self.getNormalChilds():
            tree_str += '\n  '
            tree_str += '  '.join(child.getRenderTree(rendered_nodes).splitlines(True))

        return tree_str


    def getCompleteRenderTree(self, rendered_nodes=None):
        '''
        print virtual render tree
        '''
        if rendered_nodes is None:
            rendered_nodes = set()

        if self in rendered_nodes:
            raise Exception('recursive definition of render tree!')

        rendered_nodes.add(self)

        tree_str = "{0} {1}".format(self._getRenderTreeSymbol(), self._getRenderTreeText())
        for child in self.getAllChilds():
            tree_str += '\n  '
            tree_str += '  '.join(child.getCompleteRenderTree(rendered_nodes).splitlines(True))

        return tree_str
