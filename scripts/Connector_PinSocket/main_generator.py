# -*- coding: utf8 -*-
#!/usr/bin/env python

#
# Parts script module for socket strip footprints for KicCad
#
# This module is built on top of the kicad-footprint-generator framework
# by Thomas Pointhuber, https://github.com/pointhi/kicad-footprint-generator
#
# This module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.

#
# (C) 2017 Terje Io, <http://github.com/terjeio>
#

# 2017-11-25

#
# NOTE: many footprints are based on legacy dimensions which does not have any documented datasheet sources
#       see parameter.yaml for which
#

import sys

from parameters import params

import socket_strips

if __name__ == '__main__':

    series = [
        socket_strips.pinSocketVerticalTHT,
        socket_strips.pinSocketHorizontalTHT,
        socket_strips.pinSocketVerticalSMD
    ]

    params = params()
    if params.loaded is not True:
        print(params.loaded)
        sys.exit(1)

#    models = params.getSampleModels(series, 4)
    models = params.getAllModels(series)
    i = 0
    for variant in models.keys():
        params = models[variant].params
        model = models[variant].model(params)
        if model.make_me:
            model.make()
        i += 1

    print("\nFootprints made:", i)

### EOF ###
