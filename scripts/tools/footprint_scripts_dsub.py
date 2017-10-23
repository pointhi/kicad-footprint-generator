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



def makeDSubStraight(pins, isMale, HighDensity, rmx, rmy, pindrill, pad, mountingdrill, mountingpad, mountingdistance, outline_size, outline_cornerradius, connwidth, connheight, side_angle_degree, conn_cornerradius,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/Connectors_DSub", classname="DSub", classname_description="D-Sub connector", webpage="", HighDensityOffsetMidLeft=0):
						
	hasMountingHoles=mountingdrill>0 and mountingdistance>0
	
	# rectangular outside of connector outer part on F.Fab
	w_fab = outline_size[0]
	h_fab = outline_size[1]
	l_fab = -w_fab/2
	t_fab = -h_fab/2

	# rectangular outside of connector inner part on F.Fab
	wi_fab = connwidth
	hi_fab = connheight
	li_fab = -wi_fab/2
	ti_fab = -hi_fab/2


	# rectangular outside of connector outer part on silkscreen
	h_slk = h_fab + 2 * slk_offset
	w_slk = w_fab + 2 * slk_offset
	l_slk = l_fab - slk_offset
	t_slk = t_fab - slk_offset
	
	# rectangular outside of connector inner part on silkscreen
	hi_slk = hi_fab + 2 * slk_offset
	wi_slk = wi_fab + 2 * slk_offset
	li_slk = li_fab - slk_offset
	ti_slk = ti_fab - slk_offset
	
	package_size=[0,0];
	
	w_crt = max([w_fab, mountingpad+mountingdistance, mountingpad+mountingdistance])+2*crt_offset
	h_crt = max([h_fab, mountingpad, mountingdrill])+2*crt_offset
	l_crt = -w_crt/2
	t_crt = -h_crt/2
	
	
	text_size = w_fab*0.6
	fab_text_size_max = 1.0
	if text_size < fab_text_size_min:
		text_size = fab_text_size_min
	elif text_size > fab_text_size_max:
		text_size = fab_text_size_max
	text_size = round(text_size, 2)
	text_size = [text_size,text_size]
	text_t = text_size[0] * 0.15
	
	
	description = "{0}-pin {1}, straight/vertical, THT-mount".format(pins, classname_description)
	tags = "{0}-pin {1} straight vertical THT".format(pins, classname_description)
	footprint_name="{0}-{1}".format(classname,pins)
	if HighDensity:
		footprint_name=footprint_name+"-HD"
	if isMale:
		description = description+", male"
		tags = tags+" male"
		footprint_name=footprint_name+"_Male"
	else:
		description = description+", female"
		tags = tags+" female"
		footprint_name=footprint_name+"_Female"
	
	description = description+", pitch {0}x{1}mm".format(rmx,rmy)
	tags = tags+" pitch {0}x{1}mm".format(rmx,rmy)
	footprint_name=footprint_name+"_P{0:3.2f}x{1:3.2f}mm".format(rmx,rmy)
	footprint_name=footprint_name+"_Vertical"

	description = description+", distance of mounting holes {0}mm".format(mountingdistance)
	tags = tags+" mounting holes distance {0}mm".format(mountingdistance)
	#footprint_name=footprint_name+"_MHDist{0:3.2f}mm".format(mountingdistance)
	
	if not hasMountingHoles:
		footprint_name=footprint_name+"_NoMountingHoles"

	if len(webpage)>0:
		description = description+", see {0}".format(webpage)
	
	if (len(tags_additional) > 0):
		for t in tags_additional:
			footprint_name = footprint_name + "_" + t
			description = description + ", " + t
			tags = tags + " " + t
	
	print(footprint_name)
	
	pinstop=int((pins + 1)/2)
	pinsmid=0
	pinsbot=int((pins - 1)/2)
	drmy=rmy/2
	if HighDensity:
		pinstop=int((pins+1)/3)
		pinsmid=pinstop
		pinsbot=pins-pinstop-pinsbot
		drmy=rmy

	y1=-drmy
	x10=-(pinstop-1)/2*rmx
	topoffset=0
	botoffset=rmx/2
	if HighDensity:
		x10=-mountingdistance/2+HighDensityOffsetMidLeft
		topoffset=rmx/2
		botoffset=rmx/2
		
	
	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	kicad_mod.setDescription(description)
	kicad_mod.setTags(tags)
	
	# anchor for SMD-symbols is in the center, for THT-sybols at pin1
	if not isMale:
		offset=[x10+topoffset,drmy]
	else:
		offset=[-(topoffset+x10),drmy]
	kicad_modg = Translation(offset[0], offset[1])
	kicad_mod.append(kicad_modg)
	
	# set general values
	kicad_modg.append(Text(type='reference', text='REF**', at=[l_fab+w_fab/2, t_slk - txt_offset], layer='F.SilkS'))
	kicad_modg.append(Text(type='user', text='%R', at=[0,0], layer='F.Fab', size=text_size ,thickness=text_t))
	kicad_modg.append(Text(type='value', text=footprint_name, at=[l_fab+w_fab/2, t_slk + h_slk + txt_offset], layer='F.Fab'))
	
	
	# create pads
	p1 = int(1)
	x1 = 0
	y1 = 0 
	 
	pad_type = Pad.TYPE_THT 
	hole_type = Pad.TYPE_NPTH 
	pad_shape1 = Pad.SHAPE_RECT 
	pad_shapeother = Pad.SHAPE_CIRCLE
	pad_layers = Pad.LAYERS_THT
	keepouts=[];

	
	
	y1=-drmy
	x1pos=0
	if isMale:
		x1=x10+topoffset
	else:
		x1=-x10-topoffset
			
	for p in range(1, pinstop+1): 
		 
		if p == 1: 
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers)) 
			keepouts=keepouts+addKeepoutRect(x1, y1, pad+8*slk_offset, pad+8*slk_offset)
			x1pos=x1
		else:
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers))
			keepouts=keepouts+addKeepoutRound(x1, y1, pad+(slk_pad_offset+2*lw_slk), pad+(slk_pad_offset+2*lw_slk))
		
		if isMale:
			x1=x1+rmx
		else:
			x1=x1-rmx
	if HighDensity:
		if isMale:
			x1=x10;
		else:
			x1=-x10;
		y1=0
		for p in range(pinstop+1, pinstop+pinsmid+1): 
			 
			if p == 1: 
				kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers)) 
				keepouts=keepouts+addKeepoutRect(x1, y1, pad+8*slk_offset, pad+8*slk_offset)
			else:
				kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers))
				keepouts=keepouts+addKeepoutRound(x1, y1, pad+(slk_pad_offset+2*lw_slk), pad+(slk_pad_offset+2*lw_slk))
			
			if isMale:
				x1=x1+rmx
			else:
				x1=x1-rmx

	if isMale:
		x1=x10+botoffset
	else:
		x1=-x10-botoffset
	y1=drmy
	for p in range(pinstop+pinsmid+1, pins+1): 
		 
		if p == 1: 
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers)) 
			keepouts=keepouts+addKeepoutRect(x1, y1, pad+8*slk_offset, pad+8*slk_offset)
		else:
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers))
			keepouts=keepouts+addKeepoutRound(x1, y1, pad+(slk_pad_offset+2*lw_slk), pad+(slk_pad_offset+2*lw_slk))
		
		if isMale:
			x1=x1+rmx
		else:
			x1=x1-rmx
	
	
	if hasMountingHoles and mountingpad>0:
		kicad_modg.append(Pad(number=0, type=pad_type, shape=pad_shapeother, at=[-mountingdistance/2, 0], size=[mountingpad,mountingpad], drill=mountingdrill, layers=pad_layers))
		keepouts=keepouts+addKeepoutRound(-mountingdistance/2, 0, mountingpad+(slk_pad_offset+2*lw_slk), mountingpad+(slk_pad_offset+2*lw_slk))
		kicad_modg.append(Pad(number=0, type=pad_type, shape=pad_shapeother, at=[mountingdistance/2, 0], size=[mountingpad,mountingpad], drill=mountingdrill, layers=pad_layers))
		keepouts=keepouts+addKeepoutRound(mountingdistance/2, 0, mountingpad+(slk_pad_offset+2*lw_slk), mountingpad+(slk_pad_offset+2*lw_slk))
	if hasMountingHoles and mountingpad<=0:
		kicad_modg.append(Pad(number=0, type=hole_type, shape=pad_shapeother, at=[-mountingdistance/2, 0], size=[0,0], drill=mountingdrill, layers=pad_layers))
		keepouts=keepouts+addKeepoutRound(-mountingdistance/2, 0, mountingpad+(slk_pad_offset+2*lw_slk), mountingpad+(slk_pad_offset+2*lw_slk))
		kicad_modg.append(Pad(number=0, type=hole_type, shape=pad_shapeother, at=[mountingdistance/2, 0], size=[0,0], drill=mountingdrill, layers=pad_layers))
		keepouts=keepouts+addKeepoutRound(mountingdistance/2, 0, mountingpad+(slk_pad_offset+2*lw_slk), mountingpad+(slk_pad_offset+2*lw_slk))
	
	# outline
	addRoundedRect(kicad_modg, [l_fab, t_fab], [w_fab, h_fab], outline_cornerradius, layer='F.Fab', width=lw_fab)
	addRoundedRect(kicad_modg, [l_slk, t_slk], [w_slk, h_slk], outline_cornerradius+slk_offset, layer='F.SilkS', width=lw_slk)

	#pin1 mark
	allEqualSidedDownTriangle(kicad_modg, xcenter=[x1pos, -h_slk/2-text_size[0]*0.75], side_length=text_size[0]/2, layer='F.SilkS', width=lw_slk)
	
	# connector_inside
	allRoundedBevelRect(kicad_modg, [li_fab, ti_fab], [wi_fab, hi_fab], side_angle_degree, conn_cornerradius, layer='F.Fab', width=lw_fab)
	allRoundedBevelRect(kicad_modg, [li_slk, ti_slk], [wi_slk, hi_slk], side_angle_degree, conn_cornerradius+slk_offset, layer='F.SilkS', width=lw_slk)

	# create courtyard
	kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
							  end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
							  layer='F.CrtYd', width=lw_crt))
	
	
	# add model
	kicad_mod.append(
		Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))
	
   
	# write file
	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile(footprint_name + '.kicad_mod')
	
	
	



def makeDSubEdge(pins, isMale, rmx, pad, mountingdrill, mountingdistance, shield_width, connwidth, can_height, shieldthickness, backcan_width, backcan_height, smaller_backcan_offset, smaller_backcan_height, soldercup_length, soldercup_diameter,soldercup_pad_edge_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/Connectors_DSub", classname="DSub", classname_description="D-Sub connector", webpage=""):
						
	w_slk=int((pins-1)/2)*rmx+pad[0]+(slk_pad_offset+2*lw_slk)
	h_slk=pad[1]
	l_slk=-w_slk/2
	t_slk=-h_slk/2
						
	text_size = w_slk*0.6
	fab_text_size_max = 1.0
	if text_size < fab_text_size_min:
		text_size = fab_text_size_min
	elif text_size > fab_text_size_max:
		text_size = fab_text_size_max
	text_size = round(text_size, 2)
	text_size = [text_size,text_size]
	text_t = text_size[0] * 0.15
	
	
	description = "{0}-pin {1}, solder-cups edge-mounted".format(pins, classname_description)
	tags = "{0}-pin {1} edge mount solder cup".format(pins, classname_description)
	footprint_name="{0}-{1}".format(classname,pins)
	if isMale:
		description = description+", male"
		tags = tags+" male"
		footprint_name=footprint_name+"_Male"
	else:
		description = description+", female"
		tags = tags+" female"
		footprint_name=footprint_name+"_Female"
	
	description = description+", x-pin-pitch {0}mm".format(rmx)
	tags = tags+" x-pin-pitch {0}mm".format(rmx)
	footprint_name=footprint_name+"_P{0:3.2f}mm".format(rmx)
	footprint_name=footprint_name+"_EdgeMount"

	description = description+", distance of mounting holes {0}mm".format(mountingdistance)
	tags = tags+" mounting holes distance {0}mm".format(mountingdistance)
	#footprint_name=footprint_name+"_MHDist{0:3.2f}mm".format(mountingdistance)
	
	if len(webpage)>0:
		description = description+", see {0}".format(webpage)
	
	if (len(tags_additional) > 0):
		for t in tags_additional:
			footprint_name = footprint_name + "_" + t
			description = description + ", " + t
			tags = tags + " " + t
	
	print(footprint_name)
	
	pinstop=int((pins + 1)/2)
	pinsbot=int((pins - 1)/2)

	y1=-pad[1]/2
	x10=-(pinstop-1)/2*rmx
	topoffset=0
	botoffset=rmx/2
		
	
	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	kicad_mod.setDescription(description)
	kicad_mod.setTags(tags)
	kicad_mod.setAttribute('smd')
	
	# anchor for SMD-symbols is in the center, for THT-sybols at pin1
	
	ypcb_edge=pad[1]/2+soldercup_pad_edge_offset;
	
	# set general values
	kicad_mod.append(Text(type='reference', text='REF**', at=[x10-topoffset-pad[0]/2-text_size[0]*3, 0], layer='F.SilkS'))
	kicad_mod.append(Text(type='user', text='%R', at=[0,ypcb_edge+smaller_backcan_height/2], layer='F.Fab', size=text_size ,thickness=text_t))
	kicad_mod.append(Text(type='value', text=footprint_name, at=[0, ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness+can_height+text_size[0]], layer='F.Fab'))
	
	
	# create pads
	p1 = int(1)
	x1 = 0
	y1 = 0 
	 
	pad_type = Pad.TYPE_SMT
	pad_shape1 = Pad.SHAPE_RECT 
	pad_layers_top = ['F.Cu', 'F.Mask', 'F.Paste']
	pad_layers_bot = ['B.Cu', 'B.Mask', 'B.Paste']
	slk_layers_top = 'F.SilkS'
	slk_layers_bot = 'B.SilkS'
	keepouts=[];

	
	
	y1=0
	if isMale:
		x1=x10+topoffset
	else:
		x1=-x10-topoffset
	x_pin1=0;
	leftmost=0
	rightmost=0
	for p in range(1, pinstop+1): 
		kicad_mod.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=0, layers=pad_layers_top)) 
		keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
		kicad_mod.append(RectLine(start=[x1-soldercup_diameter/2, ypcb_edge-soldercup_length], end=[x1+soldercup_diameter/2, ypcb_edge], layer='F.Fab', width=lw_fab))
		if p==1:
			x_pin1=x1;
		leftmost=min(leftmost, x1-pad[0]/2)
		rightmost=max(rightmost, x1+pad[0]/2)
		if isMale:
			x1=x1+rmx
		else:
			x1=x1-rmx
	

	if isMale:
		x1=x10+botoffset
	else:
		x1=-x10-botoffset
	y1=0
	for p in range(pinstop+1, pins+1): 
		 
		kicad_mod.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=0, layers=pad_layers_bot)) 
		keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
		kicad_mod.append(RectLine(start=[x1-soldercup_diameter/2, ypcb_edge-soldercup_length], end=[x1+soldercup_diameter/2, ypcb_edge], layer='B.Fab', width=lw_fab))
		leftmost=min(leftmost, x1-pad[0]/2)
		rightmost=max(rightmost, x1+pad[0]/2)
		if isMale:
			x1=x1+rmx
		else:
			x1=x1-rmx


	
	smaller_backcup_width=backcan_width-2*smaller_backcan_offset
	#fabrication_layer
	kicad_mod.append(RectLine(start=[-smaller_backcup_width/2, ypcb_edge], end=[smaller_backcup_width/2, ypcb_edge+smaller_backcan_height], layer='F.Fab', width=lw_fab))
	kicad_mod.append(RectLine(start=[-backcan_width/2, ypcb_edge+smaller_backcan_height], end=[backcan_width/2, ypcb_edge+smaller_backcan_height+backcan_height], layer='F.Fab', width=lw_fab))
	kicad_mod.append(RectLine(start=[-shield_width/2, ypcb_edge+smaller_backcan_height+backcan_height], end=[shield_width/2, ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness], layer='F.Fab', width=lw_fab))
	kicad_mod.append(RectLine(start=[-connwidth/2, ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness], end=[connwidth/2, ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness+can_height], layer='F.Fab', width=lw_fab))
	
	# create courtyard
	kicad_mod.append(PolygoneLine(polygone=[[roundCrt(leftmost-crt_offset), roundCrt(-pad[1]/2-crt_offset)],
							                [roundCrt(rightmost + crt_offset), roundCrt(-pad[1]/2-crt_offset)],
							                [roundCrt(rightmost + crt_offset), roundCrt(ypcb_edge-crt_offset)],
											[roundCrt(smaller_backcup_width/2 + crt_offset), roundCrt(ypcb_edge-crt_offset)],
											[roundCrt(smaller_backcup_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height-crt_offset)],
											[roundCrt(backcan_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height-crt_offset)],
											[roundCrt(backcan_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height-crt_offset)],
											[roundCrt(shield_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height-crt_offset)],
											[roundCrt(shield_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness+crt_offset)],
											[roundCrt(connwidth/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness+crt_offset)],
											[roundCrt(connwidth/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness+can_height+crt_offset)],
											[-roundCrt(connwidth/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness+can_height+crt_offset)],
											[-roundCrt(connwidth/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness+crt_offset)],
											[-roundCrt(shield_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height+shieldthickness+crt_offset)],
											[-roundCrt(shield_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height-crt_offset)],
											[-roundCrt(backcan_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height+backcan_height-crt_offset)],
											[-roundCrt(backcan_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height-crt_offset)],
											[-roundCrt(smaller_backcup_width/2 + crt_offset), roundCrt(ypcb_edge+smaller_backcan_height-crt_offset)],
											[-roundCrt(smaller_backcup_width/2 + crt_offset), roundCrt(ypcb_edge-crt_offset)],
							                [-roundCrt(rightmost + crt_offset), roundCrt(ypcb_edge-crt_offset)],
							                [-roundCrt(rightmost + crt_offset), roundCrt(-pad[1]/2-crt_offset)]
											],
							  layer='F.CrtYd', width=lw_crt))
	
	#silkscreen + PDB-edge
	kicad_mod.append(PolygoneLine(polygone=[[-x10+topoffset+pad[0]/2+slk_pad_offset, y1+pad[1]/2], 
	                                        [-x10+topoffset+pad[0]/2+slk_pad_offset, y1-pad[1]/2-slk_pad_offset],
											[x10-topoffset-pad[0]/2-slk_pad_offset, y1-pad[1]/2-slk_pad_offset],
											[x10-topoffset-pad[0]/2-slk_pad_offset, y1+pad[1]/2]], layer=slk_layers_top, width=lw_slk))
	if isMale:
		kicad_mod.append(PolygoneLine(polygone=[[x_pin1-topoffset-pad[0]/2-(slk_pad_offset+2*lw_slk), y1], 
	                                        [x_pin1-topoffset-pad[0]/2-(slk_pad_offset+2*lw_slk), y1-pad[1]/2-(slk_pad_offset+2*lw_slk)], 
											[x_pin1-topoffset+rmx, y1-pad[1]/2-(slk_pad_offset+2*lw_slk)]], layer=slk_layers_top, width=lw_slk))
	else:
		kicad_mod.append(PolygoneLine(polygone=[[x_pin1+topoffset+pad[0]/2+(slk_pad_offset+2*lw_slk), y1], 
	                                        [x_pin1+topoffset+pad[0]/2+(slk_pad_offset+2*lw_slk), y1-pad[1]/2-(slk_pad_offset+2*lw_slk)], 
											[x_pin1+topoffset-rmx, y1-pad[1]/2-(slk_pad_offset+2*lw_slk)]], layer=slk_layers_top, width=lw_slk))
	
	kicad_mod.append(Line(start=[-shield_width/2, ypcb_edge], end=[shield_width/2, pad[1]/2+soldercup_pad_edge_offset], layer='Dwgs.User', width=lw_crt))
	kicad_mod.append(Text(type='user', text='PCB edge', at=[-shield_width/2+5*text_size[0], ypcb_edge-text_size[1]*2/3], layer='Dwgs.User', size=[text_size[0]/2,text_size[1]/2] ,thickness=text_t/2))
	
	
	# add model
	kicad_mod.append(
		Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))
	
   
	# write file
	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile(footprint_name + '.kicad_mod')
	
	



def makeDSubAngled(pins, isMale, HighDensity, rmx, rmy, pindrill, pad, pin_pcb_distance, mountingdrill, mountingpad, mountingdistance, mounting_pcb_distance, shield_width, shield_thickness, can_width, can_height, backbox_width, backbox_height, nut_diameter, nut_length, backcan_width=0, backcan_height=0,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/Connectors_DSub", classname="DSub", classname_description="D-Sub connector", webpage="", HighDensityOffsetMidLeft=0):
						
	hasMountingHoles=mountingdrill>0 and mountingdistance>0
	hasNoBackBox=backcan_width*backcan_height>0 and backbox_width*backbox_height==0

	text_size = 1
	text_size = round(text_size, 2)
	text_size = [text_size,text_size]
	text_t = text_size[0] * 0.15
	
	
	description = "{0}-pin {1}, horizontal/angled (90 deg), THT-mount".format(pins, classname_description)
	tags = "{0}-pin {1} horizontal angled 90deg THT".format(pins, classname_description)
	footprint_name="{0}-{1}".format(classname,pins)
	if HighDensity:
		footprint_name=footprint_name+"-HD"
	if isMale:
		description = description+", male"
		tags = tags+" male"
		footprint_name=footprint_name+"_Male"
	else:
		description = description+", female"
		tags = tags+" female"
		footprint_name=footprint_name+"_Female"

	rmy_default=2.84
	footprint_name=footprint_name+"_P{0:3.2f}x{1:3.2f}mm".format(rmx,rmy)
	description = description+", pitch {0}x{1}mm, pin-PCB-offset {2}mm".format(rmx,rmy,pin_pcb_distance)
	tags = tags+" pitch {0}x{1}mm pin-PCB-offset {2}mm".format(rmx,rmy,pin_pcb_distance)

	footprint_name=footprint_name+"_Horizontal"
	footprint_name=footprint_name+"_EdgePinOffset{0:3.2f}mm".format(pin_pcb_distance)
	
	if hasMountingHoles:
		description = description+", distance of mounting holes {0}mm, distance of mounting holes to PCB edge {1}mm".format(mountingdistance, mounting_pcb_distance)
		tags = tags+" mounting-holes-distance {0}mm mounting-hole-offset {0}mm".format(mountingdistance, mounting_pcb_distance)
		footprint_name=footprint_name+"_MountingHolesOffset{0:3.2f}mm".format(mounting_pcb_distance)
	else:
		if hasNoBackBox:
			footprint_name=footprint_name+"_NoBox"
		else:
			footprint_name=footprint_name+"_NoMountingHoles"


	if len(webpage)>0:
		description = description+", see {0}".format(webpage)
	
	if (len(tags_additional) > 0):
		for t in tags_additional:
			footprint_name = footprint_name + "_" + t
			description = description + ", " + t
			tags = tags + " " + t
	
	print(footprint_name)
	
	rows=2
	pinstop=int((pins + 1)/2)
	pinsmid=0
	pinsbot=int((pins - 1)/2)
	drmy=rmy/2
	if HighDensity:
		rows=3
		pinstop=int((pins+1)/3)
		pinsmid=pinstop
		pinsbot=pins-pinstop-pinsbot
		drmy=rmy

	y1=-drmy
	x10=-(pinstop-1)/2*rmx
	topoffset=0
	botoffset=rmx/2
	if HighDensity:
		x10=-mountingdistance/2+HighDensityOffsetMidLeft
		topoffset=rmx/2
		botoffset=rmx/2
	
	ypcb_edge=drmy+pin_pcb_distance
	
	back_height=backbox_height
	if hasNoBackBox:
		back_height=pin_pcb_distance+rmy*(rows-1)+pad/2

	w_crt = max([backbox_width, shield_width])+2*crt_offset
	h_crt = max([backbox_height, mounting_pcb_distance+mountingpad/2])+max([nut_length, can_height])+shield_thickness+2*crt_offset
	if hasNoBackBox:
		h_crt = back_height+max([nut_length, can_height])+shield_thickness+2*crt_offset
	l_crt = -w_crt/2
	t_crt = -max([backbox_height-pin_pcb_distance-drmy, drmy+pad/2])-crt_offset
	
	
	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	kicad_mod.setDescription(description)
	kicad_mod.setTags(tags)
	
	# anchor for SMD-symbols is in the center, for THT-sybols at pin1
	if not isMale:
		offset=[x10+topoffset,drmy]
	else:
		offset=[-(topoffset+x10),drmy]
	kicad_modg = Translation(offset[0], offset[1])
	kicad_mod.append(kicad_modg)
	
	# set general values
	kicad_modg.append(Text(type='reference', text='REF**', at=[0, ypcb_edge-back_height-text_size[0]], layer='F.SilkS'))
	kicad_modg.append(Text(type='user', text='%R', at=[0,ypcb_edge+shield_thickness+can_height/2], layer='F.Fab', size=text_size ,thickness=text_t))
	kicad_modg.append(Text(type='value', text=footprint_name, at=[0, ypcb_edge+shield_thickness+can_height+text_size[0]*1.5], layer='F.Fab'))
	
	
	# create pads
	p1 = int(1)
	x1 = 0
	y1 = 0 
	 
	pad_type = Pad.TYPE_THT 
	hole_type = Pad.TYPE_NPTH 
	pad_shape1 = Pad.SHAPE_RECT 
	pad_shapeother = Pad.SHAPE_CIRCLE
	pad_layers = Pad.LAYERS_THT
	keepouts=[];

	
	
	y1=-drmy
	if isMale:
		x1=x10+topoffset
	else:
		x1=-x10-topoffset
	x1pos=0
	leftmost=0
	rightmost=0
	for p in range(1, pinstop+1): 
		 
		if p == 1: 
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers)) 
			keepouts=keepouts+addKeepoutRect(x1, y1, pad+8*slk_offset, pad+8*slk_offset)
			x1pos=x1
		else:
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers))
			keepouts=keepouts+addKeepoutRound(x1, y1, pad+(slk_pad_offset+2*lw_slk), pad+(slk_pad_offset+2*lw_slk))
		if hasNoBackBox:
			kicad_modg.append(Line(start=[x1-lw_fab, y1], end=[x1-lw_fab, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
			kicad_modg.append(Line(start=[x1, y1], end=[x1, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
			kicad_modg.append(Line(start=[x1+lw_fab, y1], end=[x1+lw_fab, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
		leftmost=min(leftmost,x1)
		rightmost=max(rightmost,x1)
		if isMale:
			x1=x1+rmx
		else:
			x1=x1-rmx
	if HighDensity:
		if isMale:
			x1=x10;
		else:
			x1=-x10;
		y1=0
		for p in range(pinstop+1, pinstop+pinsmid+1): 
			 
			if p == 1: 
				kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers)) 
				keepouts=keepouts+addKeepoutRect(x1, y1, pad+8*slk_offset, pad+8*slk_offset)
			else:
				kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers))
				keepouts=keepouts+addKeepoutRound(x1, y1, pad+(slk_pad_offset+2*lw_slk), pad+(slk_pad_offset+2*lw_slk))
			if hasNoBackBox:
				kicad_modg.append(Line(start=[x1-lw_fab, y1], end=[x1-lw_fab, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
				kicad_modg.append(Line(start=[x1, y1], end=[x1, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
				kicad_modg.append(Line(start=[x1+lw_fab, y1], end=[x1+lw_fab, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
			
			leftmost=min(leftmost,x1)
			rightmost=max(rightmost,x1)
			if isMale:
				x1=x1+rmx
			else:
				x1=x1-rmx

	if isMale:
		x1=x10+botoffset
	else:
		x1=-x10-botoffset
	y1=drmy
	for p in range(pinstop+pinsmid+1, pins+1): 
		 
		if p == 1: 
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers)) 
			keepouts=keepouts+addKeepoutRect(x1, y1, pad+8*slk_offset, pad+8*slk_offset)
		else:
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=pindrill, layers=pad_layers))
			keepouts=keepouts+addKeepoutRound(x1, y1, pad+(slk_pad_offset+2*lw_slk), pad+(slk_pad_offset+2*lw_slk))
		if hasNoBackBox:
			kicad_modg.append(Line(start=[x1-lw_fab, y1], end=[x1-lw_fab, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
			kicad_modg.append(Line(start=[x1, y1], end=[x1, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
			kicad_modg.append(Line(start=[x1+lw_fab, y1], end=[x1+lw_fab, ypcb_edge-backcan_height], layer='F.Fab', width=lw_fab))
		
		leftmost=min(leftmost,x1)
		rightmost=max(rightmost,x1)
		if isMale:
			x1=x1+rmx
		else:
			x1=x1-rmx
	
	
	# mounting holes
	if hasMountingHoles and mountingpad>0:
		kicad_modg.append(Pad(number=0, type=pad_type, shape=pad_shapeother, at=[-mountingdistance/2, ypcb_edge-mounting_pcb_distance], size=[mountingpad,mountingpad], drill=mountingdrill, layers=pad_layers))
		keepouts=keepouts+addKeepoutRound(-mountingdistance/2, ypcb_edge-mounting_pcb_distance, mountingpad+(slk_pad_offset+2*lw_slk), mountingpad+(slk_pad_offset+2*lw_slk))
		kicad_modg.append(Pad(number=0, type=pad_type, shape=pad_shapeother, at=[mountingdistance/2, ypcb_edge-mounting_pcb_distance], size=[mountingpad,mountingpad], drill=mountingdrill, layers=pad_layers))
		keepouts=keepouts+addKeepoutRound(mountingdistance/2, ypcb_edge-mounting_pcb_distance, mountingpad+(slk_pad_offset+2*lw_slk), mountingpad+(slk_pad_offset+2*lw_slk))
	if hasMountingHoles and mountingpad<=0 and backbox_width*backbox_height==0:
		kicad_modg.append(Pad(number=0, type=hole_type, shape=pad_shapeother, at=[-mountingdistance/2, ypcb_edge-mounting_pcb_distance], size=[0,0], drill=mountingdrill, layers=pad_layers))
		keepouts=keepouts+addKeepoutRound(-mountingdistance/2, ypcb_edge-mounting_pcb_distance, mountingpad+(slk_pad_offset+2*lw_slk), mountingpad+(slk_pad_offset+2*lw_slk))
		kicad_modg.append(Pad(number=0, type=hole_type, shape=pad_shapeother, at=[mountingdistance/2, ypcb_edge-mounting_pcb_distance], size=[0,0], drill=mountingdrill, layers=pad_layers))
		keepouts=keepouts+addKeepoutRound(mountingdistance/2, ypcb_edge-mounting_pcb_distance, mountingpad+(slk_pad_offset+2*lw_slk), mountingpad+(slk_pad_offset+2*lw_slk))

	# PCB edge marker
	#kicad_modg.append(Line(start=[-shield_width/2, ypcb_edge], end=[shield_width/2, ypcb_edge], layer='Dwgs.User', width=lw_crt))
	#kicad_modg.append(Text(type='user', text='PCB edge', at=[-shield_width/2+5*text_size[0], ypcb_edge-text_size[1]*2/3], layer='Dwgs.User', size=[text_size[0]/2,text_size[1]/2] ,thickness=text_t/2))
		
	# outline
	if not hasNoBackBox:
		kicad_modg.append(RectLine(start=[-backbox_width/2, ypcb_edge-backbox_height], end=[backbox_width/2, ypcb_edge], layer='F.Fab', width=lw_fab))
	else:
		kicad_modg.append(RectLine(start=[-backcan_width/2, ypcb_edge-backcan_height], end=[backcan_width/2, ypcb_edge], layer='F.Fab', width=lw_fab))
	kicad_modg.append(RectLine(start=[-shield_width/2, ypcb_edge], end=[shield_width/2, ypcb_edge+shield_thickness], layer='F.Fab', width=lw_fab))
	kicad_modg.append(RectLine(start=[-can_width/2, ypcb_edge+shield_thickness], end=[can_width/2, ypcb_edge+shield_thickness+can_height], layer='F.Fab', width=lw_fab))
	if nut_length>0 and nut_diameter>0:
		kicad_modg.append(RectLine(start=[-mountingdistance/2-nut_diameter/2, ypcb_edge+shield_thickness], end=[-mountingdistance/2+nut_diameter/2, ypcb_edge+shield_thickness+nut_length], layer='F.Fab', width=lw_fab))
		kicad_modg.append(RectLine(start=[mountingdistance/2-nut_diameter/2, ypcb_edge+shield_thickness], end=[mountingdistance/2+nut_diameter/2, ypcb_edge+shield_thickness+nut_length], layer='F.Fab', width=lw_fab))
	if hasMountingHoles:
		kicad_modg.append(Line(start=[-mountingdistance/2-mountingdrill/2, ypcb_edge], end=[-mountingdistance/2-mountingdrill/2, ypcb_edge-mounting_pcb_distance], layer='F.Fab', width=lw_fab))
		kicad_modg.append(Line(start=[-mountingdistance/2+mountingdrill/2, ypcb_edge], end=[-mountingdistance/2+mountingdrill/2, ypcb_edge-mounting_pcb_distance], layer='F.Fab', width=lw_fab))
		kicad_modg.append(Arc(start=[-mountingdistance/2-mountingdrill/2, ypcb_edge-mounting_pcb_distance], center=[-mountingdistance/2, ypcb_edge-mounting_pcb_distance], angle=180, layer='F.Fab', width=lw_fab))
		kicad_modg.append(Line(start=[mountingdistance/2-mountingdrill/2, ypcb_edge], end=[mountingdistance/2-mountingdrill/2, ypcb_edge-mounting_pcb_distance], layer='F.Fab', width=lw_fab))
		kicad_modg.append(Line(start=[mountingdistance/2+mountingdrill/2, ypcb_edge], end=[mountingdistance/2+mountingdrill/2, ypcb_edge-mounting_pcb_distance], layer='F.Fab', width=lw_fab))
		kicad_modg.append(Arc(start=[mountingdistance/2-mountingdrill/2, ypcb_edge-mounting_pcb_distance], center=[mountingdistance/2, ypcb_edge-mounting_pcb_distance], angle=180, layer='F.Fab', width=lw_fab))

	# silkscreen
	if not hasNoBackBox:
		kicad_modg.append(PolygoneLine(polygone=[
												 [-backbox_width/2-slk_offset, ypcb_edge-lw_slk/2], 
												 [-backbox_width/2-slk_offset, ypcb_edge-backbox_height-slk_offset], 
												 [backbox_width/2+slk_offset, ypcb_edge-backbox_height-slk_offset], 
												 [backbox_width/2+slk_offset, ypcb_edge-lw_slk/2], 
												], layer='F.SilkS', width=lw_slk))
		allEqualSidedDownTriangle(kicad_modg, xcenter=[x1pos, ypcb_edge-backbox_height-slk_offset-text_size[0]*0.75], side_length=text_size[0]/2, layer='F.SilkS', width=lw_slk)
	else:	
		kicad_modg.append(PolygoneLine(polygone=[
												 [-backcan_width/2-slk_offset, ypcb_edge-lw_slk/2], 
												 [-backcan_width/2-slk_offset, ypcb_edge-backcan_height-slk_offset], 
												 [leftmost-pad/2-slk_pad_offset, ypcb_edge-backcan_height-slk_offset], 
												 [leftmost-pad/2-slk_pad_offset, ypcb_edge-back_height-slk_pad_offset], 
												 [rightmost+pad/2+slk_pad_offset, ypcb_edge-back_height-slk_pad_offset], 
												 [rightmost+pad/2+slk_pad_offset, ypcb_edge-backcan_height-slk_offset], 
												 [backcan_width/2+slk_offset, ypcb_edge-backcan_height-slk_offset], 
												 [backcan_width/2+slk_offset, ypcb_edge-lw_slk/2], 
												], layer='F.SilkS', width=lw_slk))
		allEqualSidedDownTriangle(kicad_modg, xcenter=[x1pos, ypcb_edge-back_height-slk_offset-text_size[0]*0.75], side_length=text_size[0]/2, layer='F.SilkS', width=lw_slk)
	
	# create courtyard
	if not hasNoBackBox:
		kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
								  end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
								  layer='F.CrtYd', width=lw_crt))
	else:
		kicad_mod.append(PolygoneLine(polygone=[
												 [roundCrt(offset[0]-can_width/2-crt_offset), roundCrt(offset[1]+ypcb_edge+shield_thickness+can_height+crt_offset)], 
												 [roundCrt(offset[0]-can_width/2-crt_offset), roundCrt(offset[1]+ypcb_edge+shield_thickness+crt_offset)], 
												 [roundCrt(offset[0]-shield_width/2-crt_offset), roundCrt(offset[1]+ypcb_edge+shield_thickness+crt_offset)], 
												 [roundCrt(offset[0]-shield_width/2-crt_offset), roundCrt(offset[1]+ypcb_edge-crt_offset)], 
												 [roundCrt(offset[0]-backcan_width/2-crt_offset), roundCrt(offset[1]+ypcb_edge-crt_offset)], 
												 [roundCrt(offset[0]-backcan_width/2-crt_offset), roundCrt(offset[1]+ypcb_edge-backcan_height-crt_offset)], 
												 [roundCrt(offset[0]+leftmost-pad/2-crt_offset), roundCrt(offset[1]+ypcb_edge-backcan_height-crt_offset)], 
												 [roundCrt(offset[0]+leftmost-pad/2-crt_offset), roundCrt(offset[1]+ypcb_edge-back_height-crt_offset)], 
												 [roundCrt(offset[0]+rightmost+pad/2+crt_offset), roundCrt(offset[1]+ypcb_edge-back_height-crt_offset)], 
												 [roundCrt(offset[0]+rightmost+pad/2+crt_offset), roundCrt(offset[1]+ypcb_edge-backcan_height-crt_offset)], 
												 [roundCrt(offset[0]+backcan_width/2+crt_offset), roundCrt(offset[1]+ypcb_edge-backcan_height-crt_offset)], 
												 [roundCrt(offset[0]+backcan_width/2+crt_offset), roundCrt(offset[1]+ypcb_edge-crt_offset)], 
												 [roundCrt(offset[0]+shield_width/2+crt_offset), roundCrt(offset[1]+ypcb_edge-crt_offset)], 
												 [roundCrt(offset[0]+shield_width/2+crt_offset), roundCrt(offset[1]+ypcb_edge+shield_thickness+crt_offset)], 
												 [roundCrt(offset[0]+can_width/2+crt_offset), roundCrt(offset[1]+ypcb_edge+shield_thickness+crt_offset)], 
												 [roundCrt(offset[0]+can_width/2+crt_offset), roundCrt(offset[1]+ypcb_edge+shield_thickness+can_height+crt_offset)], 
												 [roundCrt(offset[0]-can_width/2-crt_offset), roundCrt(offset[1]+ypcb_edge+shield_thickness+can_height+crt_offset)], 
												], layer='F.CrtYd', width=lw_crt))
	
	
	# add model
	kicad_mod.append(
		Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))
	
   
	# write file
	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile(footprint_name + '.kicad_mod')
	
	
	