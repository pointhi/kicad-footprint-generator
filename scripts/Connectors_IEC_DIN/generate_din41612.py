#!/usr/bin/env python3

import sys
import os
import math

sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))
sys.path.append(os.path.join(sys.path[0],"..","..")) # for KicadModTree
sys.path.append(os.path.join(sys.path[0],"..","tools")) # for drawing_tools

from KicadModTree import *
from drawing_tools import *


footprint_name = "Conn_DIN41612_B-64-female"
# "Conn"(ector): Called like this by ERNI and ept
#     Not "Socket", because it does not host (small) components
# "B-64": called like this by ERNI. Pin count only is shorter than descriptive
#     row configuration.

# init kicad footprint
kicad_mod = Footprint(footprint_name)
kicad_mod.setDescription("DIN 41612 connector, family B, straight backplane part, 32 pins wide, full configuration")
kicad_mod.setTags("DIN 41512 IEC 60603 B straight backplane")

# some drawings

def B64Female(kicad_mod):
	cols = 32
	# When a manufacturer is mentioned in the comment, it means that
	# the value is explicitly stated in a datasheet by this company.
	npth_b_offset_y = -0.3 # ERNI and ept
	npth_step = 90 # ERNI and ept
	npth_drill = 2.8 # ERNI and ept
	col_step = -2.54 # ERNI and ept
	row_step = 2.54 # ERNI and ept
	pin_drill = 1 # ERNI and ept
	pin_pad = 1.7 # same as module pinheader
	outer_length = 95 # maximum value from ERNI and ept
	outer_width = 8.1 # ERNI and ept
	jack_width = 5.95 # ERNI: 6(-0.1), ept: 5.95(±0.05)
	jack_length = 85 # ERNI
	notch_depth = 1 # ERNI and ept
	notch_bottom_offset = -3 # ERNI and ept

	mid_x = 0.5 * col_step * (cols - 1)
	mid_y = 0.5 * row_step
	
	# ------ Pins and holes ------
	for col in range(1, cols + 1):
		a_shape = Pad.SHAPE_CIRCLE
		if col == 1:
			a_shape = Pad.SHAPE_RECT
		kicad_mod.append(Pad(number='A' + str(col), type=Pad.TYPE_THT, shape=a_shape,
				     at=[col_step*(col-1), 0], size=pin_pad, drill=pin_drill, layers=Pad.LAYERS_THT))
		kicad_mod.append(Pad(number='B' + str(col), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
				     at=[col_step*(col-1), row_step], size=pin_pad, drill=pin_drill, layers=Pad.LAYERS_THT))

	# non-plated drill holes, assumed to be equally distant to pins
	npth_x_left  = mid_x - npth_step * 0.5
	npth_x_right = mid_x + npth_step * 0.5
	npth_y = row_step + npth_b_offset_y
	kicad_mod.append(Pad(number="", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
		             at=[npth_x_left, npth_y], size=npth_drill, drill=npth_drill, layers=Pad.LAYERS_NPTH))
	kicad_mod.append(Pad(number="", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
		             at=[npth_x_right, npth_y], size=npth_drill, drill=npth_drill, layers=Pad.LAYERS_NPTH))

	# ------ Courtyard ------
	# KLC: connectors should have 0.5mm clearance
	kicad_mod.append(RectLine(
		start=[mid_x - outer_length/2 - 0.5, mid_y - outer_width/2 - 0.5],
		end=[mid_x + outer_length/2 + 0.5, mid_y + outer_width/2 + 0.5],
		layer='F.CrtYd'))

	# ------ Fabrication layer ------
	j_l_x = mid_x - jack_length * 0.5 # jack left
	j_r_x = mid_x + jack_length * 0.5 # jack right
	j_t_y = mid_y - jack_width * 0.5 # jack top
	j_b_y = mid_y + jack_width * 0.5 # jack bottom
	n_y  = j_b_y + notch_bottom_offset # notch
	n_l_x = j_l_x + notch_depth # notch left
	n_r_x = j_r_x - notch_depth # notch right

	jack_notch_left  = [[n_l_x, j_t_y], [j_l_x, j_t_y], [j_l_x, n_y], [n_l_x, n_y], [n_l_x, j_b_y]]
	jack_notch_right = [[n_r_x, j_b_y], [n_r_x, n_y], [j_r_x, n_y], [j_r_x, j_t_y], [n_r_x, j_t_y]]
	pin_a1_arrow = [ # form taken from module Connectors_Molex
		[ 0.0, mid_y - outer_width/2 - 0.2],
		[-0.3, mid_y - outer_width/2 - 0.8],
		[ 0.3, mid_y - outer_width/2 - 0.8],
		[ 0.0, mid_y - outer_width/2 - 0.2],
	]

	kicad_mod.append(PolygoneLine(
		polygone=jack_notch_left + jack_notch_right + [jack_notch_left[0]],
		layer='F.Fab'))
	kicad_mod.append(PolygoneLine(
		polygone=pin_a1_arrow,
		width=0.12,
		layer='F.Fab'))
	kicad_mod.append(Text(
		type='value', text=footprint_name,
		at=[mid_x, mid_y + outer_width/2 + 1.3],
		layer='F.Fab'))
	# Very small Reference Designator to fit between the pins.
	kicad_mod.append(Text(
		type='user', text='%R',
		at=[mid_x, mid_y + 0],
		size=[0.6, 0.6], thickness=0.07,
		layer='F.Fab'))

	# ------ Silk screen ------
	# assume plastic part to be centered around the pins
	# silk screen must be visible, so add 0.1 mm
	kicad_mod.append(RectLine(
		start=[mid_x - outer_length/2 - 0.1, mid_y - outer_width/2 - 0.1],
		end=[mid_x + outer_length/2 + 0.1, mid_y + outer_width/2 + 0.1],
		width=0.15,
		layer='F.SilkS'))
	kicad_mod.append(PolygoneLine(
		polygone=jack_notch_left,
		width=0.15,
		layer='F.SilkS'))
	kicad_mod.append(PolygoneLine(
		polygone=jack_notch_right,
		width=0.15,
		layer='F.SilkS'))
	kicad_mod.append(PolygoneLine(
		polygone=pin_a1_arrow,
		width=0.12,
		layer='F.SilkS'))
	kicad_mod.append(Text(
		type='reference', text='REF**',
		at=[mid_x, mid_y - outer_width/2 - 1.0],
		layer='F.SilkS'))



B64Female(kicad_mod)

# output kicad model
file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile(footprint_name + '.kicad_mod')
