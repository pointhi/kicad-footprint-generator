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

import sys
import io


class FileHandler(object):
    r"""some basic methods to write footprints, and which is the base class of footprint writer implementations

    :param kicad_mod:
        Main object representing the footprint
    :type kicad_mod: ``KicadModTree.Footprint``

    :Example:

    >>> from KicadModTree import *
    >>> kicad_mod = Footprint("example_footprint")
    >>> file_handler = KicadFileHandler(kicad_mod)  # KicadFileHandler is a implementation of FileHandler
    >>> file_handler.writeFile('example_footprint.kicad_mod')
    """

    def __init__(self, kicad_mod):
        self.kicad_mod = kicad_mod

    def writeFile(self, filename):
        r"""Write the output of FileHandler.serialize to a file

        :param filename:
            path of the output file
        :type filename: ``str``

        :Example:

        >>> from KicadModTree import *
        >>> kicad_mod = Footprint("example_footprint")
        >>> file_handler = KicadFileHandler(kicad_mod)  # KicadFileHandler is a implementation of FileHandler
        >>> file_handler.writeFile('example_footprint.kicad_mod')
        """

        with io.open(filename, "w", newline='\n') as f:
            output = self.serialize()

            # convert to unicode if running python2
            if sys.version_info[0] == 2 and type(output) != unicode:
                output = unicode(output, "utf-8")

            f.write(output)

            f.close()

    def serialize(self):
        r"""Get a valid string representation of the footprint in the specified format

        :Example:

        >>> from KicadModTree import *
        >>> kicad_mod = Footprint("example_footprint")
        >>> file_handler = KicadFileHandler(kicad_mod)  # KicadFileHandler is a implementation of FileHandler
        >>> print(file_handler.serialize())
        """

        raise NotImplementedError("serialize has to be implemented by child class")
