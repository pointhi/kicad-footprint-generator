#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path

from KicadModTree import *  # NOQA
from drawing_tools import *  # NOQA
from math import sqrt

crt_offset = 0.5 # different for connectors



def makeDSubStraight(pins, isMale, highDensity, rmx, rmy, pindrill, pad, mountingdrill, mountingpad, mountingdistance, outline_size, outline_cornerradius, connwidth, connwidthsmall, connheight, conn_cornerradius,
                        tags_additional=[], lib_name="${{KISYS3DMOD}}/Connectors_DSub", classname="DSub", classname_description="D-Sub connector", webpage=""):
    h_crt = max(outline_size[1], mountingpad[0]/2, mountingdrill/2)
    w_crt = max(outline_size[0], mountingpad[0]+mountingdistance, mountingpad[0]+mountingdistance)
    l_crt = -h_crt/2
    t_ctr = -w_crt/2

    h_fab = outline_size[1]
    w_fab = outline_size[0]
    l_fab = -h_fab/2
    t_fab = -w_fab/2
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = max(w_fab + 2 * slk_offset, coldist * (cols - 1) - pad[0] - 4 * slk_offset)
    l_slk = (coldist * (cols - 1) - w_slk) / 2
    t_slk = -overlen_top - slk_offset
    
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
	
	
	description = "{0}-pin {1}, straight, THT-mount".format(pins, classname_description)
	tags = "{0}-pin {1} straight THT".format(pins, classname_description)
	footprint_name="{0}{1}".format(classname.pins)
	if isMale:
		description = description+", male"
		tags = tags+" male"
		footprint_name=footprint_name+"_male"
	else:
		description = description+", female"
		tags = tags+" female"
		footprint_name=footprint_name+"_female"
	footprint_name=footprint_name+"_straight"
	if len(webpage)>0:
		description = description+", see {0}".format(webpage)
	
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
	if isMale:
		offset=[-((pins+1)/2-1)/2*rmx,-rmy/2]
	else:
		
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
	pinstop=(pins + 1)/2
	pinsbot=(pins - 1)/2
	
	x1=-(pinstop-1)/2*rmx
	y1=-rmy/2
	if not isMale:
		x1=-x1
	for p in range(1, pinstop+1): 
		 
		if p == 1: 
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers)) 
			keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
		else:
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers))
			keepouts=keepouts+addKeepoutRound(x1, y1, pad[0]+6*slk_offset, pad[1]+6*slk_offset)
		
		if isMale:
			x1=x1+rmx
		else:
			x1=x1-rmx

	x1=-(pinsbot-1)/2*rmx
	if not isMale:
		x1=-x1
	y1=rmy/2
	for p in range(pinstop+1, pins+1): 
		 
		if p == 1: 
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers)) 
			keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
		else:
			kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers))
			keepouts=keepouts+addKeepoutRound(x1, y1, pad[0]+6*slk_offset, pad[1]+6*slk_offset)
		
		if isMale:
			x1=x1+rmx
		else:
			x1=x1-rmx
	
	
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