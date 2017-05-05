from KicadModTree import *  # NOQA

def add_corners(m, start_pos, end_pos, size_x, size_y, layer, width, offset=(0, 0)):

    # If specifed, an 'offset' can be applied to the corners.
    # For example, creating corners around a given Rect of a specified size
    # offset for the rect line

    # For the offset to work properly, start-pos must be top-left, and end-pos must be bottom-right
    x1 = min(start_pos[0], end_pos[0])
    x2 = max(start_pos[0], end_pos[0])
    y1 = min(start_pos[1], end_pos[1])
    y2 = max(start_pos[1], end_pos[1])

    # Put the offset (if any) back in
    start_pos[0] = x1 - offset[0]
    start_pos[1] = y1 - offset[1]
    end_pos[1] = x2 + offset[0]
    end_pos[1] = y2 + offset[1]

    m.append(Line(start=[start_pos[0], start_pos[1]], end=[start_pos[0]+size_x, start_pos[1]], layer=layer, width=width))
    m.append(Line(start=[start_pos[0], start_pos[1]], end=[start_pos[0], start_pos[1]+size_y], layer=layer, width=width))

    m.append(Line(start=[start_pos[0], end_pos[1]], end=[start_pos[0]+size_x, end_pos[1]], layer=layer, width=width))
    m.append(Line(start=[start_pos[0], end_pos[1]], end=[start_pos[0], end_pos[1]-size_y], layer=layer, width=width))

    m.append(Line(start=[start_pos[0], start_pos[1]], end=[start_pos[0]+size_x, start_pos[1]], layer=layer, width=width))
    m.append(Line(start=[start_pos[0], start_pos[1]], end=[start_pos[0], start_pos[1]+size_y], layer=layer, width=width))

    m.append(Line(start=[start_pos[0], end_pos[1]], end=[start_pos[0]+size_x, end_pos[1]], layer=layer, width=width))
    m.append(Line(start=[start_pos[0], end_pos[1]], end=[start_pos[0], end_pos[1]-size_y], layer=layer, width=width))

    return m
#  Line(start=[-1, 0], end=[-1, 0], layer='F.SilkS')


"""

    if direction == 'up':
        delta_x = bump_length
        delta_y = -bump_width
        start_x = anchor[0]
        start_y = anchor[1] - offset[1]
    elif direction == 'down':
        delta_x = bump_length
        delta_y = bump_width
        start_x = anchor[0]
        start_y = anchor[1] + offset[1]
    elif direction == 'left':
        delta_x = -bump_width
        delta_y = bump_length
        start_x = anchor[0] - offset[0]
        start_y = anchor[1]
    elif direction == 'right':
        delta_x = bump_width
        delta_y = bump_length
        start_x = anchor[0] + offset[0]
        start_y = anchor[1]
    else:
        print('ADD_BUMP: invalid direction {:s}'.format(direction))
        return []
    if direction in ['up', 'down']:
        polygon_line = [
                         {'x': start_x - delta_x / 2.0, 'y': start_y },
                         {'x': start_x - delta_x / 2.0, 'y': start_y + delta_y},
                         {'x': start_x + delta_x / 2.0, 'y': start_y + delta_y},
                         {'x': start_x + delta_x / 2.0, 'y': start_y} ]
    else:
        polygon_line = [
                         {'x': start_x, 'y': start_y - delta_y / 2.0 },
                         {'x': start_x + delta_x, 'y': start_y - delta_y / 2.0},
                         {'x': start_x + delta_x, 'y': start_y + delta_y / 2.0},
                         {'x': start_x, 'y': start_y + delta_y / 2.0} ]
    return PolygoneLine(polygone=polygon_line, layer=layer, width=width)
"""

