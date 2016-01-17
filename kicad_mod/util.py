'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
'''


def formatFloat(val):
    return ('%f' % val).rstrip('0').rstrip('.')


def parse_coordinate(coord):
    '''
    parse coordinates of different styles, and return them as python dictionary
    '''
    x, y, r = 0, 0, 0

    if type(coord) is list or type(coord) is tuple:
        if len(coord) == 2:
            # only x and y
            x = coord[0]
            y = coord[1]
        elif len(coord) == 3:
            # x, y and rotation
            x = coord[0]
            y = coord[1]
            r = coord[2]
        else:
            raise TypeError('coordinate is writte as (x, y) or (x, y, r)')
    elif type(coord) is dict:
        x = coord.get('x', 0)
        y = coord.get('y', 0)
        r = coord.get('r', 0)
    else:
        raise TypeError('unknow datatype')

    # TODO: typecheck

    return {'x':x, 'y':y, 'r':r}


def parse_coordinate_xy(coord):
    parsed_coord = parse_coordinate(coord)
    return {'x':parsed_coord['x'], 'y':parsed_coord['y']}


def parse_coordinate_xyz(coord):
    '''
    parse coordinates of different styles, and return them as python dictionary
    '''
    x, y, z = 0, 0, 0

    if type(coord) is list or type(coord) is tuple:
        if len(coord) == 3:
            x = coord[0]
            y = coord[1]
            z = coord[2]
        else:
            raise TypeError('coordinate is writte as (x, y, z)')
    elif type(coord) is dict:
        x = coord.get('x', 0)
        y = coord.get('y', 0)
        z = coord.get('z', 0)
    else:
        raise TypeError('unknow datatype')

    # TODO: typecheck

    return {'x':x, 'y':y, 'z':z}


def render_position_xy(keyword, position):
    coord = parse_coordinate(position)
    return '({keyword} {x} {y})'.format(keyword=keyword
                                       ,x=formatFloat(coord['x'])
                                       ,y=formatFloat(coord['y']))


def render_position_xyz(keyword, position):
    coord = parse_coordinate_xyz(position)
    return '({keyword} {x} {y} {z})'.format(keyword=keyword
                                           ,x=formatFloat(coord['x'])
                                           ,y=formatFloat(coord['y'])
                                           ,z=formatFloat(coord['z']))


def render_position_xyr(keyword, position):
    coord = parse_coordinate(position)
    return '({keyword} {x} {y} {r})'.format(keyword=keyword
                                           ,x=formatFloat(coord['x'])
                                           ,y=formatFloat(coord['y'])
                                           ,r=formatFloat(coord['r']))

