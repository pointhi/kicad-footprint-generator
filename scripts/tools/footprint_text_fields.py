import sys, os
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
from KicadModTree import *  # NOQA

def _roundToBase(value, base):
    return round(value/base) * base

def _getTextFieldDetails(field_definition, body_edges, courtyard, text_y_inside_position = 'center', allow_rotation = False):
    body_size = [body_edges['right'] - body_edges['left'], body_edges['bottom'] - body_edges['top']]
    body_center = [(body_edges['right'] + body_edges['left'])/2, (body_edges['bottom'] + body_edges['top'])/2]

    position_y = field_definition['position_y']
    at = body_center.copy()


    if body_size[0] < body_size[1] and allow_rotation and position_y == 'inside':
        rotation = 1
    else:
        rotation = 0

    if 'size' in field_definition:
        size = field_definition['size']
        fontwidth = field_definition['fontwidth']
    elif 'size_min' in field_definition and 'size_max' in field_definition:
        # We want at least 3 char reference designators space. If we can't fit these we move the reverence to the outside.
        size_max = field_definition['size_max']
        size_min = field_definition['size_min']
        if body_size[rotation] >= 4*size_max[1]:
            if body_size[0] >= 4*size_max[1]:
                rotation = 0
            size = size_max
        elif body_size[rotation] < 4*size_min[1]:
            size = size_min
            if body_size[rotation] < 3*size_min[1]:
                if position_y == 'inside':
                    rotation = 0
                    position_y = 'outside_top'
        else:
            fs = _roundToBase(body_size[rotation]/4, 0.01)
            size = [fs, fs]

        if size[1] > body_size[(rotation+1)%2]-0.2:
            fs = max(body_size[(rotation+1)%2]-0.2, size_min[1])
            size = [fs, fs]

        fontwidth = _roundToBase(field_definition['thickness_factor']*size[0], 0.01)
    else:
        rotation = 0
        position_y = 'outside_top'
        size = [1,1]
        fontwidth = 0.15

    if position_y == 'inside':
        if text_y_inside_position == 'top':
            position_y = 'inside_top'
        elif text_y_inside_position == 'bottom':
            position_y = 'inside_bottom'
        elif text_y_inside_position == 'left':
            position_y = 'inside_left'
        elif text_y_inside_position == 'right':
            position_y = 'inside_right'
        elif isinstance(text_y_inside_position,int) or isinstance(text_y_inside_position,float):
            at[1] = text_y_inside_position

    text_edge_offset = size[0]/2+0.2
    if position_y == 'outside_top':
        at = [body_center[0], courtyard['top']-text_edge_offset]
    elif position_y == 'inside_top':
        at = [body_center[0], body_edges['top']+text_edge_offset]
    elif position_y == 'inside_left':
        at = [body_edges['left'] + text_edge_offset, body_center[1]]
        rotation = 1
    elif position_y == 'inside_right':
        at = [body_edges['right'] - text_edge_offset, body_center[1]]
        rotation = 1
    elif position_y == 'outside_bottom':
        at = [body_center[0], courtyard['bottom']+text_edge_offset]
    elif position_y == 'inside_bottom':
        at = [body_center[0], body_edges['bottom']-text_edge_offset]


    at = [_roundToBase(at[0],0.01), _roundToBase(at[1],0.01)]
    return {'at': at, 'size': size, 'layer': field_definition['layer'], 'thickness': fontwidth, 'rotation': rotation*90}

def addTextFields(kicad_mod, configuration, body_edges, courtyard, fp_name, text_y_inside_position = 'center', allow_rotation = False):
    reference_fields = configuration['references']
    kicad_mod.append(Text(type='reference', text='REF**',
        **_getTextFieldDetails(reference_fields[0], body_edges, courtyard, text_y_inside_position, allow_rotation)))

    for additional_ref in reference_fields[1:]:
        kicad_mod.append(Text(type='user', text='%R',
        **_getTextFieldDetails(additional_ref, body_edges, courtyard, text_y_inside_position, allow_rotation)))

    value_fields = configuration['values']
    kicad_mod.append(Text(type='value', text=fp_name,
        **_getTextFieldDetails(value_fields[0], body_edges, courtyard, text_y_inside_position, allow_rotation)))

    for additional_value in value_fields[1:]:
        kicad_mod.append(Text(type='user', text='%V',
            **_getTextFieldDetails(additional_value, body_edges, courtyard, text_y_inside_position, allow_rotation)))
