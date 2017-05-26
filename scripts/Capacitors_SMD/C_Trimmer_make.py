#!/usr/bin/env python

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
import os
import argparse
import yaml
import pprint

sys.path.append(os.path.join(sys.path[0], "../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA


if __name__ == '__main__':

    print('Making DPAK footprints')

    from C_Trimmer_factory import *

    CONFIG = 'C_Trimmer_config.yaml' 
                
    f = Factory(CONFIG)

    for series in f.build_list:
        series.build_series(verbose=f.verbose)

