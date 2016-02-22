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

import time

from .util import *
from .Point import *
from .Node import Node


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


class KicadModTree(Node):
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
        render_string = "(module {name} (layer F.Cu) (tedit {timestamp:X})\n".format(name=self.name, timestamp=int(time.time()))

        if self.description:
            render_string += '  (descr "{description}")\n'.format(description=self.description)

        if self.tags:
            render_string += '  (tags "{tags}")\n'.format(tags=self.tags)

        if self.attribute:
            render_string += '  (attr {attr})\n'.format(attr=self.attribute)

        # read render list, sort it by key and reformate multiline entities
        render_list = sorted(self.renderList(), key=lambda string: render_order.index(string.split()[0][1:]))
        render_list = [s.replace('\n', '\n  ') for s in render_list]

        render_string += "  "
        render_string += "\n  ".join(render_list)
        render_string += "\n"

        render_string += ")"

        return render_string


    def __str__(self):
        return self.render()


    def write(self, path=None):
        if not path:
            path = self.name + '.kicad_mod'

        f = open(path,"w")

        f.write(self.__str__())
        f.close()
