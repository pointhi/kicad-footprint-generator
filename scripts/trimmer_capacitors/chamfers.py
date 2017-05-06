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

from KicadModTree import *


def add_rect_chamfer(m, start_pos, end_pos, layer, width, offset=(0,0), chamfers=[]):

    # For the offset and chamfer to work properly, start-pos must be top-left, and end-pos must be bottom-right
    x1 = min(start_pos[0], end_pos[0])
    x2 = max(start_pos[0], end_pos[0])
    y1 = min(start_pos[1], end_pos[1])
    y2 = max(start_pos[1], end_pos[1])

    # Put the offset (if any) back in
    start_pos[0] = x1 - offset[0]
    start_pos[1] = y1 - offset[1]
    end_pos[0] = x2 + offset[0]
    end_pos[1] = y2 + offset[1]
        
    # Work out intermediate positions on each side to use later when drawing corners or chamfers
    JOG = 0.01  # avoid coincident intermediate points on non-chamfered sides
    top_left_mid_pos = Point([start_pos[0] + JOG, start_pos[1]])
    top_right_mid_pos = Point([end_pos[0] - JOG, start_pos[1]])
    bottom_left_mid_pos = Point([start_pos[0] + JOG, end_pos[1]])
    bottom_right_mid_pos = Point([end_pos[0] - JOG, end_pos[1]])
    left_top_mid_pos = Point([start_pos[0], start_pos[1] + JOG])
    left_bottom_mid_pos = Point([start_pos[0], end_pos[1] - JOG])
    right_top_mid_pos = Point([end_pos[0], start_pos[1] + JOG])
    right_bottom_mid_pos = Point([end_pos[0], end_pos[1] - JOG])

    # Set the positions of the corners
    top_left_pos = Point([start_pos[0], start_pos[1]])
    top_right_pos = Point([end_pos[0], start_pos[1]])
    bottom_left_pos = Point([start_pos[0], end_pos[1]])
    bottom_right_pos = Point([end_pos[0], end_pos[1]])

    for c in chamfers:
        # Need to shift chamfered edges so they maintain constant distance from non-offset line
        # tan(22.5) = 0.414 works correctly when chamfer is at 45 degrees (same  and Y offset), 
        # and still looks OK when X and Y offsets are different
        try:
            x_delta = c['size'] + 0.414 * offset[0]
            y_delta = c['size'] + 0.414 * offset[1]
            if c['corner'] == 'topleft':
                top_left_pos.x = start_pos[0] + (x_delta) / 2.0
                top_left_pos.y = start_pos[1] + (y_delta) / 2.0
                top_left_mid_pos.x = start_pos[0] + (x_delta)
                left_top_mid_pos.y = start_pos[1] + (y_delta)
            elif c['corner'] == 'topright':
                top_right_pos.x = end_pos[0] - (x_delta) / 2.0
                top_right_pos.y = start_pos[1] + (y_delta) / 2.0
                top_right_mid_pos.x = end_pos[0] - (x_delta)
                right_top_mid_pos.y = start_pos[1] + (y_delta)
            elif c['corner'] == 'bottomleft':
                bottom_left_pos.x = start_pos[0] + (x_delta) / 2.0
                bottom_left_pos.y = end_pos[1] - (y_delta) / 2.0
                bottom_left_mid_pos.x = start_pos[0] + (x_delta)
                left_bottom_mid_pos.y = end_pos[1] - (y_delta)
            elif c['corner'] == 'bottomright':
                bottom_right_pos.x = end_pos[0] - (x_delta) / 2.0
                bottom_right_pos.y = end_pos[1] - (y_delta) / 2.0
                bottom_right_mid_pos.x = end_pos[0] - (x_delta)
                right_bottom_mid_pos.y = end_pos[1] - (y_delta)
            elif c['corner'] == 'all':
                chamfers.append({'corner': 'topleft', 'size': c['size']})
                chamfers.append({'corner': 'topright', 'size': c['size']})
                chamfers.append({'corner': 'bottomleft', 'size': c['size']})
                chamfers.append({'corner': 'bottomright', 'size': c['size']})
            else:
                pass
        except Exception as e:
            # print(e)
            pass
    polygon_line = [
                     {'x': top_left_pos.x, 'y': top_left_pos.y},
                     {'x': top_left_mid_pos.x, 'y': top_left_mid_pos.y},
                     {'x': top_right_mid_pos.x, 'y': top_right_mid_pos.y},
                     {'x': top_right_pos.x, 'y': top_right_pos.y},
                     {'x': right_top_mid_pos.x, 'y': right_top_mid_pos.y},
                     {'x': right_bottom_mid_pos.x, 'y': right_bottom_mid_pos.y},
                     {'x': bottom_right_pos.x, 'y': bottom_right_pos.y},
                     {'x': bottom_right_mid_pos.x, 'y': bottom_right_mid_pos.y},
                     {'x': bottom_left_mid_pos.x, 'y': bottom_left_mid_pos.y},
                     {'x': bottom_left_pos.x, 'y': bottom_left_pos.y},
                     {'x': left_bottom_mid_pos.x, 'y': left_bottom_mid_pos.y},
                     {'x': left_top_mid_pos.x, 'y': left_top_mid_pos.y},
                     {'x': top_left_pos.x, 'y': top_left_pos.y} ]
    m.append(PolygoneLine(polygone=polygon_line, layer=layer, width=width))
    return m

