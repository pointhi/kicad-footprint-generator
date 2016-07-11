def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

def v_add(p1,p2):
    return [p1[0]+p2[0],p1[1]+p2[1]]

def round_crty_point(point):
    return [round_to(point[0],0.05),round_to(point[1],0.05)]

def v_offset(point, offset):
    return [
        point[0] + (offset if point[0] >=0 else -offset),
        point[1] + (offset if point[1] >=0 else -offset)
    ]
