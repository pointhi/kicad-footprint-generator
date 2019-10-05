import sys
import os
sys.path.append(os.path.join(sys.path[0],"..",".."))

import argparse
from KicadModTree import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commandline tool for generating ring pads.')
    parser.add_argument('-n', '--name', metavar='fp_name', type=str,
                        help='Name of the generated footprint. default: output', default='output')
    parser.add_argument('--at', type=float, nargs=2, help='position of the pad, default: at origin', default=[0,0], metavar=('x', 'y'))
    parser.add_argument('-v', '--verbose', action='count', help='set debug level')
    parser.add_argument('-i', '--inner_diameter', type=float, help='inside diameter', required=True)
    parser.add_argument('-o', '--outer_diameter', type=float, help='outside diameter', required=True)
    parser.add_argument('-p', '--number', type=str, help='the pin number, default: 1', default='1')
    parser.add_argument('--anchor_count', type=int, help='number of anchor (trace connection points), default: 4', default=4)
    parser.add_argument('--paste_count', type=int, help='number of paste areas, default: 4', default=4)
    parser.add_argument('--paste_round_radius_radio', type=float, help='round radius ratio for the paste pads', default=0.25)
    parser.add_argument('--paste_clearance', type=float, help='clearance between paste areas', nargs='?')
    parser.add_argument('--mask_margin', type=float, help='soldermask margin, default:0', default=0)
    parser.add_argument('--paste_margin', type=float, help='solderpaste margin, default:0 (means controlled by footprint or board setup)', default=0)
    args = parser.parse_args()

kicad_mod = Footprint(args.name)

kicad_mod.append(
    RingPad(
        number=args.number, at=args.at,
        size=args.outer_diameter, inner_diameter=args.inner_diameter,
        num_anchor=args.anchor_count, num_paste_zones=args.paste_count,
        solder_paste_margin=args.paste_margin, solder_mask_margin=args.mask_margin,
        paste_round_radius_radio=args.paste_round_radius_radio,
        paste_to_paste_clearance=args.paste_clearance))


file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile(args.name + '.kicad_mod')
