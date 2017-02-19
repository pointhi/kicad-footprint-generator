def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

def v_add(p1,p2):
    return [p1[0]+p2[0],p1[1]+p2[1]]

def round_crty_point(point):
    return [round_to(point[0],0.05),round_to(point[1],0.05)]

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
