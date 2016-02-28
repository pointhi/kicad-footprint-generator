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


class FileHandler(object):
    '''
    implement basic methodes to read and write footprints
    '''

    def __init__(self, kicad_mod):
        self.kicad_mod = kicad_mod


    def writeFile(self, filename):
        '''
        Write the output of serialize to a file
        '''
        f = open(filename,"w")

        output = self.serialize()
        f.write(output)

        f.close()


    def serialize(self):
        '''
        serialize a KicadModTree object
        '''
        raise NotImplementedError("serialize has to be implemented by child class")

        return None


    def readFile(filename):
        '''
        Read a footprint file and parse it
        '''
        f = open(filename,"r")

        input = f.read()

        return self.unserialize(input)


    def unserialize(self, input):
        '''
        parse a footprint and export it to a KicadModTree object
        '''
        raise NotImplementedError("serialize has to be implemented by child class")

        return KicadModTree()
