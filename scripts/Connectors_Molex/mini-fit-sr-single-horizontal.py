#!/usr/bin/env python

################################################################################
# kicad-footprint-generator is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kicad-footprint-generator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
################################################################################

"""
Molex Mini-Fit Sr. 42820 series
http://www.molex.com/pdm_docs/sd/428202214_sd.pdf
"""

pitch = 10.00
pincount = [2, 3, 4, 5, 6] # pins per row
part = "42820-{n}2XX" # Molex part number
part_name = "Molex_Mini-Fit_Sr_{part}_1x{n:02}_Pitch{p:.2f}mm_Horizontal" # KiCad footprint name
drill = 2.8
size = 5

def generate_footprint(pins):
    pn = part.format(n=pins)
    
    # Name, description, tags
    fp_name = part_name.format(n=pins, p=pitch, part=pn)
    footprint = Footprint(fp_name)
    description = "Molex Mini-Fit Sr. header, " + pn + ", 10.00mm pitch, single row, horizontal entry, with PCB retention clips."
    description += " http://www.molex.com/pdm_docs/sd/428202214_sd.pdf"
    footprint.setDescription(description)
    tags = "connector molex mini-fit-sr 42820"
    footprint.setTags(tags)
    
    # Dimensions
    P = (pins - 1) * pitch
    B = pins * pitch + 0.90 # connector length
    row = 5.00
    W = 21.00 # connector width

    # Reference and value fields
    footprint.append(Text(type='reference', text='REF**', at=[0, -24], layer='F.SilkS'))
    footprint.append(Text(type='user', text='%R', at=[P/2, -9], layer='F.Fab'))
    footprint.append(Text(type='value', text=fp_name, at=[P/2, 10], layer='F.Fab'))

    # Pads
    footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT))
    footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT, start=[0, row]))
    
    # PCB retention clips
    ret_dx = 5.73
    ret_dy = 9.00
    ret_drill = 3.00
    ret_size = 4.00
    footprint.append(Pad(at=[0-ret_dx, -ret_dy], type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=ret_size, drill=ret_drill, layers=Pad.LAYERS_THT))
    footprint.append(Pad(at=[P+ret_dx, -ret_dy], type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=ret_size, drill=ret_drill, layers=Pad.LAYERS_THT))
    
    # Outline
    xl1 = 0 - (B - P) / 2 # left
    xl2 = xl1 - 1.46
    xr1 = P + (B - P) / 2 # right
    xr2 = xr1 + 1.46
    yt1 = 0 - ret_dy - 13.56 # top
    yb1 = yt1 + 21.00 # bottom
    yb2 = yb1 + 7.60
    footprint.append(RectLine(start=[xl1, yt1], end=[xr1, yb1], layer='F.Fab', width=0.1))
    footprint.append(RectLine(start=[xl2, yt1], end=[xr2, yb1], layer='F.Fab', width=0.1))
    for i in range(pins):
        footprint.append(RectLine(start=[i*pitch-3.8/2, yb1], end=[i*pitch+3.8/2, yb2], layer='F.Fab', width=0.1))

    # Silkscreen
    off = 0.1
    off2 = 0.3
    silk1 = [
        {'x': P/2, 'y': yt1-off},
        {'x': xl2-off, 'y': yt1-off},
        {'x': xl2-off, 'y': -ret_dy-ret_size/2},
    ]
    footprint.append(PolygoneLine(polygone=silk1, layer='F.SilkS', width=0.12))
    footprint.append(PolygoneLine(polygone=silk1, layer='F.SilkS', width=0.12, x_mirror=P/2))
    silk2 = [
        {'x': xl2-off, 'y': -ret_dy+ret_size/2},
        {'x': xl2-off, 'y': yb1+off},
        {'x': -size/2-off2, 'y': yb1+off},
    ]
    footprint.append(PolygoneLine(polygone=silk2, layer='F.SilkS', width=0.12))
    footprint.append(PolygoneLine(polygone=silk2, layer='F.SilkS', width=0.12, x_mirror=P/2))
    for i in range(pins - 1):
        footprint.append(Line(start=[i*pitch+size/2+off2, yb1+off], end=[(i+1)*pitch-size/2-off2, yb1+off], layer='F.SilkS', width=0.12))
    
    # Pin 1 designator
    pin1 = [
        {'x': 0, 'y': yb1+1.2},
        {'x': 1.2, 'y': yb1},
        {'x': -1.2, 'y': yb1},
        {'x': 0, 'y': yb1+1.2},
    ]
    footprint.append(PolygoneLine(polygone=pin1, layer='F.Fab', width=0.1))
    footprint.append(PolygoneLine(polygone=pin1, layer='F.Fab', width=0.1, y_mirror=(yb1+yb2)/2))
    pin1 = [
        {'x': 0, 'y': 8},
        {'x': 0.5, 'y': 9},
        {'x': -0.5, 'y': 9},
        {'x': 0, 'y': 8},
    ]
    footprint.append(PolygoneLine(polygone=pin1, layer='F.SilkS', width=0.12))
    
    # Courtyard
    footprint.append(RectLine(start=[-ret_dx-ret_size/2, yt1], end=[P+ret_dx+ret_size/2, row+size/2], offset=0.5, grid=0.01, layer='F.CrtYd', width=0.05))
    
    # Location of 3D model
    footprint.append(Model(filename="${KISYS3DMOD}/Connectors_Molex.3dshapes/" + fp_name + ".wrl"))

    return footprint

if __name__ == '__main__':
    import sys
    import os

    # If specified as an argument, extract the target directory for output footprints
    if len(sys.argv) > 1:
        output_dir = os.path.abspath(sys.argv[1])
    else:
        output_dir = os.getcwd()
            
    # Import KicadModTree files
    sys.path.append(os.path.join(sys.path[0], os.pardir, os.pardir))
    from KicadModTree import *

    # Create footprints
    for pins in pincount:
        footprint = generate_footprint(pins)
        filename = os.path.join(output_dir, footprint.name + ".kicad_mod")
        print(filename)
        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)

