
from KicadModTree import *

def roundToBase(value, base):
    return round(value/base) * base

def parseAdditionalDrawing(footprint, drawing_definition, configuration, series_definition, body_edges, pincount):
    ref = drawing_definition.get('reference_point', ['center','center']).copy()

    if ref[0] == 'left':
        ref[0] = body_edges['left']
    elif ref[0] == 'center':
        ref[0] = (body_edges['left'] + body_edges['right'])/2
    elif ref[0] == 'right':
        ref[0] = body_edges['right']

    if ref[1] == 'top':
        ref[1] = body_edges['top']
    elif ref[1] == 'center':
        ref[1] = (body_edges['top'] + body_edges['bottom'])/2
    elif ref[1] == 'bottom':
        ref[1] = body_edges['bottom']

    if 'rectangle' in drawing_definition:
        if 'size' in drawing_definition['rectangle']:
            size = drawing_definition['rectangle']['size']
            start = [ref[0] - size[0]/2, ref[1] - size[1]/2]
            end = [ref[0] + size[0]/2, ref[1] + size[1]/2]
        elif 'start' in drawing_definition['rectangle'] and 'end' in drawing_definition['rectangle']:
            start = drawing_definition['rectangle']['start']
            start = [ref[0] + start[0], ref[1] + start[1]]
            end = drawing_definition['rectangle']['end']
            end = [ref[0] + end[0], ref[1] + end[1]]
        else:
            print('rectangle without size size defintion found. Ignored')
            return
    elif 'polygone' in drawing_definition:
        # ToDo: implement
        polygone = []
        for point in drawing_definition['polygone']:
            polygone.append({'x':ref[0]+point[0], 'y':ref[1]+point[1]})
    else:
        # not implemented.
        return
    #print(polygone)

    layer=drawing_definition.get('layer', 'F.Fab')
    if 'thickness' in drawing_definition:
        thickness = drawing_definition['thickness']
    elif 'Fab' in layer:
        thickness = configuration['fab_line_width']
    elif 'SilkS' in layer:
        thickness = configuration['silk_line_width']
    else:
        print('drawing not on silk or fab but no line thickness given.')
        return

    if 'repeat' in drawing_definition:
        repeat_def = drawing_definition['repeat']
        spacing = repeat_def['spacing']
        if spacing[0] == 'pitch':
            spacing[0] = series_definition['pitch']
        if spacing[1] == 'pitch':
            spacing[1] = series_definition['pitch']

        count = repeat_def['count']
        if count == 'pincount':
            count = pincount

        first = ref.copy()
        if repeat_def['reference_is'] == 'last':
            first[0] = (count-1)*spacing[0]
            first[1] = (count-1)*spacing[1]
            spacing[0] *= -1
            spacing[1] *= -1

        elif repeat_def['reference_is'] == 'center':
            first[0] = -(count-1)*spacing[0]/2
            first[1] = -(count-1)*spacing[1]/2


        for i in range(count):
            translation = Translation(first[0]+i*spacing[0], first[1]+i*spacing[1])
            if 'rectangle' in drawing_definition:
                translation.append(RectLine(start=start, end=end, layer=layer, width=thickness))
            elif 'polygone' in drawing_definition:
                translation.append(PolygoneLine(polygone=polygone, layer=layer, width=thickness))
            footprint.append(translation)

    else:
        if 'rectangle' in drawing_definition:
            footprint.append(RectLine(start=start, end=end, layer=layer, width=thickness))
        elif 'polygone' in drawing_definition:
            #print(polygone)
            footprint.append(PolygoneLine(polygone=polygone, layer=layer, width=thickness))
