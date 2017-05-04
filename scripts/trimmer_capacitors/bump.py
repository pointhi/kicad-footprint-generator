from KicadModTree import *  # NOQA

def Bump(anchor, bump_length, bump_width, direction, layer, width, offset=(0, 0)):
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

