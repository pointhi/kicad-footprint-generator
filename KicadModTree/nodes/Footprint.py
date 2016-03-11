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


class Footprint(Node):
    '''
    Root Node to generate KicadMod
    '''
    def __init__(self, name):
        Node.__init__(self)

        self.name = name
        self.description = None
        self.tags = None
        self.attribute = None


    def setName(self, name):
        self.name = name


    def setDescription(self, description):
        self.description = description


    def setTags(self, tags):
        self.tags = tags


    def setAttribute(self, value):
        self.attribute = value
