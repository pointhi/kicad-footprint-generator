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


from KicadModTree.Vector import *
from KicadModTree.nodes.Node import Node


'''
This is my new approach, using a render tree for footprint generation.

ADVANTAGES:

* simple point transformations
* automatic calculation of courtjard,...
* simple duplication of rendering structures

'''

# define in which order the general "lisp" operators are arranged
render_order = ['descr', 'tags', 'attr', 'solder_mask_margin',
                'solder_paste_margin', 'solder_paste_ratio', 'fp_text',
                'fp_circle', 'fp_line', 'pad', 'model']
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
        self.maskMargin = None
        self.pasteMargin = None
        self.pasteMarginRatio = None

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setTags(self, tags):
        self.tags = tags

    def setAttribute(self, value):
        self.attribute = value

    def setMaskMargin(self, value):
        self.maskMargin = value

    def setPasteMargin(self, value):
        self.pasteMargin = value

    def setPasteMarginRatio(self, value):
        # paste_margin_ratio is unitless between 0 and 1 while GUI uses percentage
        assert abs(value) <= 1, "Solder paste margin must be between -1 and 1. {} is too large.".format(value)

        self.pasteMarginRatio = value
