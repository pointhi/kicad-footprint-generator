#!/usr/bin/env python3

import sys
import os
import re

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", ".."))

# load scripts
sys.path.append(os.path.join(sys.path[0], ".."))

from KicadModTree import *
from general.StandardBox import *

def qfn(args):

    extraffablines = []

    footprint_name = args["name"]
    description = args["description"]
    datasheet = args["datasheet"]
    fptag = args["tags"]
    SmdTht = args["smd_tht"]
    at = args["at"]
    size = args["size"]
    pins = args["pins"]
    extratexts = args["extratexts"]

    dir3D = 'Inductor_SMD.3dshapes'
    f = Footprint(footprint_name)

    file3Dname = "${KISYS3DMOD}/" + dir3D + "/" + footprint_name + ".wrl"
    words = footprint_name.split("_")
    if words[-1].lower().startswith('handsolder'):
        words[-1] = ''
        ff = '_'.join(words)
        file3Dname = "${KISYS3DMOD}/" + dir3D + "/" + ff + ".wrl"
    f.append(StandardBox(footprint=f, description=description, datasheet=datasheet, at=at, size=size, tags=fptag, SmdTht=SmdTht, extratexts=extratexts, pins=pins, file3Dname=file3Dname ))
    #
    #
    #
    file_handler = KicadFileHandler(f)
    file_handler.writeFile(footprint_name + ".kicad_mod")
    


if __name__ == '__main__':
	parser = ModArgparser(qfn)
	# the root node of .yml files is parsed as name
	parser.add_parameter("name", type=str, required=True)
	parser.add_parameter("description", type=str, required=True)
	parser.add_parameter("datasheet", type=str, required=True)
	parser.add_parameter("tags", type=str, required=True)
	parser.add_parameter("smd_tht", type=str, required=False, default='tht')
	parser.add_parameter("at", type=list, required=True)
	parser.add_parameter("size", type=list, required=False)
	parser.add_parameter("pins", type=list, required=True)
	parser.add_parameter("extratexts", type=list, required=False)


	# now run our script which handles the whole part of parsing the files
	parser.run()
