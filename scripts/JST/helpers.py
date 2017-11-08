
from KicadModTree.nodes.base.Pad import Pad  # NOQA

def roundToBase(value, base):
    return round(value/base) * base

def getTextFieldDetails(field_definition, crtyd_top, crtyd_bottom, center):
    position_y = field_definition['position']

    if position_y == 'top':
        at = [center[0], crtyd_top - field_definition['size'][0] * 5/4.0]
    elif position_y == 'center':
        at = center
    elif position_y == 'bottom':
        at = [center[0], crtyd_bottom + field_definition['size'][0] * 5/4.0]
    else:
        at = center

    return {'at': at, 'size': field_definition['size'], 'layer': field_definition['layer'], 'thickness': field_definition['fontwidth']}

def createNumberedPadsSMD(kicad_mod, pincount, pitch, size, position_y):

    at = [-(pincount-1)/2.0*pitch, position_y]
    for i in range(pincount):
        kicad_mod.append(Pad(number= i+1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
            layers=Pad.LAYERS_SMT, at=at, size=size))
        at[0] += pitch
