def getTextFieldDetails(field_definition, crtyd_top, crtyd_bottom, center_x, params):
    position_y = field_definition['position']
    top_pos =[center_x + (0 if params.num_pins > 2 else 1),
        crtyd_top - field_definition['size'][1]/2.0]
    inner_ref = [center_x + (0 if params.num_pins > 2 else 1),
        (3 if params.angled else -3)]

    inner_value = [center_x, crtyd_bottom - 1.0 - field_definition['size'][1]/2.0]

    bottom_pos = [center_x, crtyd_bottom + field_definition['size'][1]/2.0]
    if position_y == 'top':
        at = top_pos
    elif position_y == 'inside_top':
        at = inner_ref
    elif position_y == 'inside_bottom':
        at = inner_value
    elif position_y == 'bottom':
        at = bottom_pos
    else:
        at = [0,0]

    return {'at': at, 'size': field_definition['size'], 'layer': field_definition['layer'], 'thickness': field_definition['fontwidth']}

def round_to(value, base):
    return round(value/base) * base

def v_add(p1,p2):
    return [p1[0]+p2[0],p1[1]+p2[1]]

def round_crty_point(point, grid_size):
    return [round_to(point[0], grid_size),round_to(point[1], grid_size)]

def offset_dir(coordinate, offset, center=0):
    if coordinate > center:
        return coordinate + offset
    elif coordinate< center:
        return coordinate - offset
    else:
        return coordinate

def v_offset(point, offset, center = (0,0)):
    if type(center) is dict:
        center_x = float(center.get('x', 0.))
        center_y = float(center.get('y', 0.))
    else:
        center_x=center[0]
        center_y=center[1]

    if type(point) is dict:
        result={}
        result['x']=offset_dir(float(point.get('x', 0.)), offset, center_x)
        result['y']=offset_dir(float(point.get('y', 0.)), offset, center_y)
        return result

    return [
        point[0] + (offset if point[0] >=center_x else -offset),
        point[1] + (offset if point[1] >=center_y else -offset)
    ]

def offset_polyline(polyline_points, offset, center=(0,0)):
    resulting_points = []
    for point in polyline_points:
        resulting_points.append(v_offset(point,offset,center))

    return resulting_points

def create_pin1_marker_triangle(bottom_y, center_x = 0, dimensions = [0.6,0.6], with_top_line = True):
    marker_width = dimensions[0]
    marker_height = dimensions[1]

    marker_top=bottom_y-marker_height
    marker_poly=[
        {'x':center_x+marker_width/2, 'y':marker_top},
        {'x':center_x, 'y':bottom_y},
        {'x':center_x-marker_width/2, 'y':marker_top}
    ]
    if with_top_line:
        marker_poly.append({'x':center_x+marker_width/2, 'y':marker_top})
    return marker_poly

def create_pin1_marker_corner(top_y, left_x, sidelength = [1,1]):
    marker_poly=[
        {'x':left_x, 'y':top_y + sidelength[1]},
        {'x':left_x, 'y':top_y},
        {'x':left_x + sidelength[0], 'y':top_y}
    ]

    return marker_poly
