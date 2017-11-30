#!/usr/bin/env python3

import sys

def get_name(pin_count):
    return 'Molex-502250-{0}91_2Rows_{0}_P0.3mm_Horizontal'.format(pin_count)

def make_module(f, pin_count):
    y_offset = 0.0375
    pitch = 0.3
    odd_pad_size = (0.26, 0.80)
    even_pad_size = (0.3, 0.65)
    anchor_pad_size = (0.4, 0.85)
    row_spacing = 2.875
    pins_width = pitch * (pin_count - 1)
    anchor_pad_spacing = pins_width + 1.4
    width = pins_width + 2.1
    bar_width = pins_width + 0.48
    bar_height = 0.91
    bar_bottom = 1.5325 + y_offset
    name = get_name(pin_count)

    f.write("(module {name} (layer F.Cu) (tedit 5980D929)\n".format(name=name))
    url='http://www.molex.com/pdm_docs/sd/502250{0}91_sd.pdf'.format(pin_count)
    f.write('  (descr "Molex 0.30mm Pitch Easy-On BackFlip Type FFC/FPC '
                'Connector, 0.9mm Height, Right Angle, Surface Mount, '
                '{pin_count} Circuits ({url})")\n'.format(
                    pin_count=pin_count, url=url))
    f.write('  (tags "molex FFC/FPC connector Pitch 0.3mm right angle")\n')
    f.write('  (attr smd)\n')

    f.write('  (fp_text reference REF** (at 0 -3.00) (layer F.SilkS)\n'
            '    (effects (font (size 1 1) (thickness 0.15)))\n'
            '  )\n')
    f.write('  (fp_text value {name} (at 0 3.75) (layer F.Fab)\n'
            '    (effects (font (size 1 1) (thickness 0.15)))\n'
            '  )\n'.format(name=name))
    f.write('  (fp_text user %R (at 0 0) (layer F.Fab)\n'
            '    (effects (font (size 1 1) (thickness 0.1)))\n'
            '  )\n')

    def fp_line(**kw):
        f.write('  (fp_line (start {start[0]:1.5g} {start[1]:1.5g}) '
            '(end {end[0]:1.5g} {end[1]:1.5g}) (layer {layer}) '
            '(width {width}))\n'.format(**kw))
    def fp_polyline(points, **kw):
        for i in range(len(points) - 1):
            fp_line(start=points[i], end=points[i+1], **kw)

    outline_side = [(0, 0), (0, 0.45), (0.28, 0.45), (0.28, 0.815), (0, 0.815),
        (0, 3.53), (0.30, 3.53), (0.30, 3.28)]
    origin = (-width/2, 1.7475 - y_offset)
    outline = ([(p[0] + origin[0], p[1] - origin[1]) for p in outline_side] +
      [(-p[0] - origin[0], p[1] - origin[1]) for p in outline_side[::-1]] +
      [(outline_side[0][0] + origin[0], outline_side[0][1] - origin[1])])
    fp_polyline(outline, layer='F.Fab', width=0.1)

    silk_side = [(-0.05, 1.25), (-0.05, 3.58), (0.30, 3.58)]
    fp_polyline([(p[0] + origin[0], p[1] - origin[1]) for p in silk_side],
        layer='F.SilkS', width=0.1)
    fp_polyline([(-p[0] - origin[0], p[1] - origin[1]) for p in silk_side],
        layer='F.SilkS', width=0.1)
    fp_line(start=(origin[0]-0.05, -origin[1]-0.05),
        end=(origin[0]+0.75, -origin[1]-0.05), layer='F.SilkS', width=0.1)
    fp_line(start=(origin[0]+width+0.05, -origin[1]-0.05),
        end=(origin[0]+width-0.75, -origin[1]-0.05), layer='F.SilkS', width=0.1)

    def fp_rect(l, t, r, b, **kw):
        fp_line(start=(l, t), end=(r, t), **kw)
        fp_line(start=(r, t), end=(r, b), **kw)
        fp_line(start=(r, b), end=(l, b), **kw)
        fp_line(start=(l, b), end=(l, t), **kw)

    ctyd_width = anchor_pad_spacing + anchor_pad_size[0] + 1.0
    fp_rect(
        round(ctyd_width/2, 2),
        round(bar_bottom + bar_height + 0.5, 2),
        round(-ctyd_width/2, 2),
        round(-row_spacing/2 - odd_pad_size[1]/2 - 0.5, 2),
        width=0.05, layer='F.CrtYd')

    for pin in range(1, pin_count+1):
        pad_size = odd_pad_size if (pin % 2) == 1 else even_pad_size
        x = (pin - 1) * pitch - pins_width / 2
        y = (-1 if (pin % 2) == 1 else 1) * row_spacing / 2 + y_offset
        f.write("  (pad {pin} smd rect (at {x:1.5g} {y:1.5g}) "
            "(size {pad_size[0]} {pad_size[1]}) "
            "(layers F.Cu F.Paste F.Mask))\n".format(**locals()))

    def anchor_pad(direction):
        f.write("  (pad \"\" smd rect (at {x:1.5g} {y:1.5g}) "
            "(size {pad_size[0]} {pad_size[1]}) "
            "(layers F.Cu F.Paste F.Mask))\n".format(
                    x=anchor_pad_spacing / 2 * direction,
                    y=0.325 - row_spacing/2 + y_offset,
                    pad_size=anchor_pad_size))
    anchor_pad(-1)
    anchor_pad(1)

    f.write('  (model ${{KISYS3DMOD}}/Conn_Molex.3dshapes/{0}.wrl\n'
            '    (at (xyz 0 0 0))\n'
            '    (scale (xyz 1 1 1))\n'
            '    (rotate (xyz 0 0 0))\n'
            '  )\n'.format(name))

    f.write(")\n")

for pin_count in [17, 21, 23, 27, 33, 35, 39, 41, 51]:
    with open(get_name(pin_count) + '.kicad_mod', 'w') as f:
        make_module(f, pin_count)
