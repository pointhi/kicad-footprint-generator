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

import unittest

from KicadModTree.nodes.Node import *


class NodeTests(unittest.TestCase):

    def testInit(self):
        node = Node()
        self.assertTrue(node.getParent() is None)
        self.assertTrue(node.getRootNode() is node)
        self.assertTrue(len(node.getNormalChilds()) == 0)
        self.assertTrue(len(node.getVirtualChilds()) == 0)
        self.assertTrue(len(node.getAllChilds()) == 0)


    def testAppend(self):
        node = Node()
        self.assertTrue(len(node.getNormalChilds()) == 0)

        childNode1 = Node()
        node.append(childNode1)
        self.assertTrue(childNode1 in node.getNormalChilds())
        self.assertTrue(len(node.getNormalChilds()) == 1)

        childNode2 = Node()
        node.append(childNode2)
        self.assertTrue(childNode1 in node.getNormalChilds())
        self.assertTrue(childNode2 in node.getNormalChilds())
        self.assertTrue(len(node.getNormalChilds()) == 2)

        # TODO: add invalid type test
        # TODO: add duplicated node test


    def testExtend(self):
        node = Node()
        self.assertTrue(len(node.getNormalChilds()) == 0)

        childNode1 = Node()
        childNode2 = Node()
        node.extend([childNode1, childNode2])
        self.assertTrue(childNode1 in node.getNormalChilds())
        self.assertTrue(childNode2 in node.getNormalChilds())
        self.assertTrue(len(node.getNormalChilds()) == 2)

        childNode3 = Node()
        node.extend([childNode3])
        self.assertTrue(childNode1 in node.getNormalChilds())
        self.assertTrue(childNode2 in node.getNormalChilds())
        self.assertTrue(childNode3 in node.getNormalChilds())
        self.assertTrue(len(node.getNormalChilds()) == 3)

        node.extend([])
        self.assertTrue(childNode1 in node.getNormalChilds())
        self.assertTrue(childNode2 in node.getNormalChilds())
        self.assertTrue(childNode3 in node.getNormalChilds())
        self.assertTrue(len(node.getNormalChilds()) == 3)

        # TODO: add invalid type test
        # TODO: add duplicated node test


    def testRemove(self):
        node = Node()
        self.assertTrue(len(node.getNormalChilds()) == 0)

        childNode1 = Node()
        childNode2 = Node()
        node.extend([childNode1, childNode2])
        self.assertTrue(childNode1 in node.getNormalChilds())
        self.assertTrue(childNode2 in node.getNormalChilds())
        self.assertTrue(len(node.getNormalChilds()) == 2)

        node.remove(childNode1)
        self.assertTrue(childNode1 not in node.getNormalChilds())
        self.assertTrue(childNode2 in node.getNormalChilds())
        self.assertTrue(len(node.getNormalChilds()) == 1)

        # TODO: add invalid type test
