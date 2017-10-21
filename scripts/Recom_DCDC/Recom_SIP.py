#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")	 # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","tools")) # load kicad_mod path

from KicadModTree import *	# NOQA
from drawing_tools import *
from footprint_scripts_sip import *


if __name__ == '__main__':
	pins=3
	rm=2.54
	ddrill=1.2
	pad=[1.7, 2.5]
	package_size=[11.5,8.5,17.5]
	left_offset=3.21
	top_offset=package_size[1]-2
	makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
			footprint_name='DCDC-Conv_RECOM_R-78B-2.0', 
			description="DCDC-Converter, RECOM, RECOM_R-78B-2.0, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78Bxx-2.0.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
			tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
			lib_name='Converters_DCDC_ACDC')
			
	package_size=[11.5,8.5,10.4]
	ddrill=1.0
	pad=[1.5, 2.3]
	makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
			footprint_name='DCDC-Conv_RECOM_R-78E-0.5', 
			description="DCDC-Converter, RECOM, RECOM_R-78E-0.5, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78Exx-0.5.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
			tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
			lib_name='Converters_DCDC_ACDC')
			

	package_size=[11.5,8.5,17.5]
	ddrill=1.0
	pad=[1.5, 2.3]
	top_offset=2
	pin_bottom_offset=1.5
	makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
			footprint_name='DCDC-Conv_RECOM_R-78HB-0.5', 
			description="DCDC-Converter, RECOM, RECOM_R-78HB-0.5, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78HBxx-0.5_L.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
			tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
			lib_name='Converters_DCDC_ACDC')
	makeSIPHorizontal(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, pin_bottom_offset=pin_bottom_offset, 
			footprint_name='DCDC-Conv_RECOM_R-78HB-0.5L', 
			description="DCDC-Converter, RECOM, RECOM_R-78HB-0.5L, SIP-{0}, Horizontally Mounted, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78HBxx-0.5_L.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
			tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
			lib_name='Converters_DCDC_ACDC')
			

	pins=4
	package_size=[11.5,8.5,17.5]
	ddrill=1.0
	pad=[1.5, 2.3]
	left_offset=2
	top_offset=package_size[1]-2
	makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
			footprint_name='DCDC-Conv_RECOM_R-78S-0.1', 
			description="DCDC-Converter, RECOM, RECOM_R-78S-0.1, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78Sxx-0.1.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
			tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
			lib_name='Converters_DCDC_ACDC')

	pins=12
	package_size=[32.2,9.1,15]
	ddrill=1.0
	pad=[1.5, 2.3]
	left_offset=2.13
	top_offset=0.7
	pin_bottom_offset=0.5
	makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
			footprint_name='DCDC-Conv_RECOM_R5xxxPA', 
			description="DCDC-Converter, RECOM, RECOM_R5xxxPA, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-5xxxPA_DA.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
			tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
			lib_name='Converters_DCDC_ACDC')
	makeSIPHorizontal(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, pin_bottom_offset=pin_bottom_offset, 
			footprint_name='DCDC-Conv_RECOM_R5xxxDA', 
			description="DCDC-Converter, RECOM, RECOM_R5xxxDA, SIP-{0}, Horizontally Mounted, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-5xxxPA_DA.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
			tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
			lib_name='Converters_DCDC_ACDC')
