#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")	 # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path

from KicadModTree import *	# NOQA
from drawing_tools import *	 # NOQA
from math import sqrt

crt_offset = 0.5 # different for connectors

#
#  +----------------------------------------+					   ^				  
#  |	   H		   H		   H		| ^					   |				  
#  |										| |					   |				  
#  |	  OOO		  OOO		  OOO		| |secondHoleOffset	   | package_height	 
#  |	 OOOOO		 OOOOO		 OOOOO		| v					   |				  ^
#  |	  OOO		  OOO		  OOO		|					   |				  |
#  +----------------------------------------+ ^					   |				  | leftbottom_offset
#  |										| | bevel_height	   |				  |
#  +----------------------------------------+ v					   v				  v
#		   <--- rm ---->
#  <------>leftbottom_offset
#
#
#
def makeTerminalBlockStd(footprint_name, pins, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw=True, screw_pin_offset=[0,0], secondHoleDiameter=0, secondHoleOffset=[0,0], thirdHoleDiameter=0, thirdHoleOffset=[0,0], fourthHoleDiameter=0, fourthHoleOffset=[0,0],nibbleSize=[],nibblePos=[], fabref_offset=[0,0],
						tags_additional=[], lib_name="${{KISYS3DMOD}}/Connectors_Terminal_Blocks", classname="Connectors_Terminal_Blocks", classname_description="terminal block"):
						
	package_size=[2*leftbottom_offset[0]+(pins-1)*rm, package_height];
	
	h_fab = package_size[1]
	w_fab = package_size[0]
	l_fab = -leftbottom_offset[0]
	t_fab = -(h_fab-leftbottom_offset[1])
	
	h_slk = h_fab + 2 * slk_offset
	w_slk = w_fab + 2 * slk_offset
	l_slk = l_fab - slk_offset
	t_slk = t_fab - slk_offset
	
	h_crt = h_fab + 2 * crt_offset
	w_crt = w_fab + 2 * crt_offset
	l_crt = l_fab - crt_offset
	t_crt = t_fab - crt_offset
	
	
	text_size = w_fab*0.6
	fab_text_size_max = 1.0
	if text_size < fab_text_size_min:
		text_size = fab_text_size_min
	elif text_size > fab_text_size_max:
		text_size = fab_text_size_max
	text_size = round(text_size, 2)
	text_size = [text_size,text_size]
	text_t = text_size[0] * 0.15
	
	
	description = "{2}, {0} pins, pitch {1:02}mm".format(pins, rm,classname_description)
	tags = "THT {2} pitch {1:02}mm".format(pins, rm,classname_description)
	
	if (len(tags_additional) > 0):
		for t in tags_additional:
			footprint_name = footprint_name + "_" + t
			description = description + ", " + t
			tags = tags + " " + t
	
	print(footprint_name)
	
	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	kicad_mod.setDescription(description)
	kicad_mod.setTags(tags)
	
	# anchor for SMD-symbols is in the center, for THT-sybols at pin1
	offset=[0,0]
	kicad_modg = Translation(offset[0], offset[1])
	kicad_mod.append(kicad_modg)
	
	# set general values
	kicad_modg.append(Text(type='reference', text='REF**', at=[l_fab+w_fab/2, t_slk - txt_offset], layer='F.SilkS'))
	if (type(fabref_offset) in (tuple, list)):
		kicad_modg.append(Text(type='user', text='%R', at=[l_fab+w_fab/2+fabref_offset[0], t_fab+h_fab/2+fabref_offset[1]], layer='F.Fab', size=text_size ,thickness=text_t))
	else:
		kicad_modg.append(Text(type='user', text='%R', at=[l_fab+w_fab/2,  t_slk - txt_offset], layer='F.Fab', size=text_size ,thickness=text_t))
	kicad_modg.append(Text(type='value', text=footprint_name, at=[l_fab+w_fab/2, t_slk + h_slk + txt_offset], layer='F.Fab'))
	
	
	# create pads
	p1 = int(1)
	x1 = 0
	y1 = 0 
	 
	pad_type = Pad.TYPE_THT 
	pad_shape1 = Pad.SHAPE_RECT 
	pad_shapeother = Pad.SHAPE_OVAL 
	pad_layers = Pad.LAYERS_THT
	keepouts=[];
	for p in range(1, pins + 1): 
		 
		if p == 1: 
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers)) 
			keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
		else:
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers))
			keepouts=keepouts+addKeepoutRound(x1, y1, pad[0]+6*slk_offset, pad[1]+6*slk_offset)
		
		x1=x1+rm
	
	# create Body
	chamfer = min(h_fab/4, 1, bevel_height[0])
	bevelRectBL(kicad_modg,	 [l_fab,t_fab], [w_fab,h_fab], 'F.Fab', lw_fab, bevel_size=chamfer)
	for bh in bevel_height:
		kicad_modg.append(Line(start=[l_fab, t_fab + h_fab-bh], end=[l_fab+w_fab, t_fab + h_fab-bh], layer='F.Fab', width=lw_fab))
		kicad_modg.append(Line(start=[l_slk, t_fab + h_fab-bh], end=[l_slk+w_slk, t_fab + h_fab-bh], layer='F.SilkS', width=lw_slk))
	kicad_modg.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk + h_slk], layer='F.SilkS', width=lw_slk))
	# screws + other repeated features
	if screw_diameter>0:
		for p in range(1,pins+1):
			if screw_diameter>0:
				if slit_screw:
					addSlitScrew(kicad_modg, (p-1)*rm+screw_pin_offset[0], 0+screw_pin_offset[1], screw_diameter/2, 'F.Fab', lw_fab, roun=0.001)
					addSlitScrewWithKeepouts(kicad_modg, (p-1)*rm+screw_pin_offset[0], 0+screw_pin_offset[1], screw_diameter/2+3*slk_offset, 'F.SilkS', lw_slk, keepouts, roun=0.001)
				else:
					addCrossScrew(kicad_modg, (p-1)*rm+screw_pin_offset[0], 0+screw_pin_offset[1], screw_diameter/2, 'F.Fab', lw_fab, roun=0.001)
					addCrossScrewWithKeepouts(kicad_modg, (p-1)*rm+screw_pin_offset[0], 0+screw_pin_offset[1], screw_diameter/2+3*slk_offset, 'F.SilkS', lw_slk, keepouts, roun=0.001)
				
			if not (type(secondHoleDiameter) in (tuple, list)) and secondHoleDiameter>0 and (p-1)*rm+secondHoleOffset[0]<l_fab+w_fab:
				kicad_modg.append(Circle(center=[(p-1)*rm+secondHoleOffset[0], 0+secondHoleOffset[1]], radius=secondHoleDiameter/2, layer='F.Fab', width=lw_fab))
				addCircleWithKeepout(kicad_modg, (p-1)*rm+secondHoleOffset[0], 0+secondHoleOffset[1], secondHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
			if not (type(thirdHoleDiameter) in (tuple, list)) and thirdHoleDiameter>0 and (p-1)*rm+thirdHoleOffset[0]<l_fab+w_fab:
				kicad_modg.append(Circle(center=[(p-1)*rm+thirdHoleOffset[0], 0+thirdHoleOffset[1]], radius=thirdHoleDiameter/2, layer='F.Fab', width=lw_fab))
				addCircleWithKeepout(kicad_modg, (p-1)*rm+thirdHoleOffset[0], 0+thirdHoleOffset[1], thirdHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
			if not (type(fourthHoleDiameter) in (tuple, list)) and fourthHoleDiameter>0 and (p-1)*rm+fourthHoleOffset[0]<l_fab+w_fab:
				kicad_modg.append(Circle(center=[(p-1)*rm+fourthHoleOffset[0], 0+fourthHoleOffset[1]], radius=fourthHoleDiameter/2, layer='F.Fab', width=lw_fab))
				addCircleWithKeepout(kicad_modg, (p-1)*rm+fourthHoleOffset[0], 0+fourthHoleOffset[1], fourthHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
			if (type(secondHoleDiameter) in (tuple, list)) and (p-1)*rm+secondHoleOffset[0]<l_fab+w_fab:
				kicad_modg.append(RectLine(start=[(p-1)*rm+secondHoleOffset[0]-secondHoleDiameter[0]/2, 0+secondHoleOffset[1]-secondHoleDiameter[1]/2], end=[(p-1)*rm+secondHoleOffset[0]+secondHoleDiameter[0]/2, 0+secondHoleOffset[1]+secondHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
				addRectWithKeepout(kicad_modg, (p-1)*rm+secondHoleOffset[0]-secondHoleDiameter[0]/2, 0+secondHoleOffset[1]-secondHoleDiameter[1]/2, secondHoleDiameter[0],secondHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
			if (type(thirdHoleDiameter) in (tuple, list)) and (p-1)*rm+thirdHoleOffset[0]<l_fab+w_fab:
				kicad_modg.append(RectLine(start=[(p-1)*rm+thirdHoleOffset[0]-thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]-thirdHoleDiameter[1]/2], end=[(p-1)*rm+thirdHoleOffset[0]+thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]+thirdHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
				addRectWithKeepout(kicad_modg, (p-1)*rm+thirdHoleOffset[0]-thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]-thirdHoleDiameter[1]/2, thirdHoleDiameter[0],thirdHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
			if (type(fourthHoleDiameter) in (tuple, list)) and (p-1)*rm+fourthHoleOffset[0]<l_fab+w_fab:
				kicad_modg.append(RectLine(start=[(p-1)*rm+fourthHoleOffset[0]-fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]-fourthHoleDiameter[1]/2], end=[(p-1)*rm+fourthHoleOffset[0]+fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]+fourthHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
				addRectWithKeepout(kicad_modg, (p-1)*rm+fourthHoleOffset[0]-fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]-fourthHoleDiameter[1]/2, fourthHoleDiameter[0],fourthHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
	
	#nibble
	if len(nibbleSize)==2 and len(nibblePos)==2:
		kicad_modg.append(RectLine(start=[l_fab+nibblePos[0], t_fab+nibblePos[1]], end=[l_fab+nibblePos[0]+nibbleSize[0], t_fab+nibblePos[1]+nibbleSize[1]], layer='F.Fab', width=lw_fab))
		addRectWithKeepout(kicad_modg, l_fab+nibblePos[0]-slk_offset, t_fab+nibblePos[1]-slk_offset, nibbleSize[0],nibbleSize[1]+2*slk_offset, 'F.SilkS', lw_slk, keepouts)
		
				
				
	# create SILKSCREEN-pin1-marker
	kicad_modg.append(Line(start=[l_slk-2*lw_slk, t_slk + h_slk-chamfer], end=[l_slk-2*lw_slk, t_slk + h_slk+2*lw_slk], layer='F.SilkS', width=lw_slk))
	kicad_modg.append(Line(start=[l_slk-2*lw_slk, t_slk + h_slk+2*lw_slk], end=[l_slk-2*lw_slk+chamfer, t_slk + h_slk+2*lw_slk], layer='F.SilkS', width=lw_slk))
	
	# create courtyard
	kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
							  end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
							  layer='F.CrtYd', width=lw_crt))
	
	
	# add model
	kicad_modg.append(
		Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))
	
   
	# write file
	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile(footprint_name + '.kicad_mod')

