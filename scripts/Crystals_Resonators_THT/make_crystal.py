#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","tools")) # load kicad_mod path

from KicadModTree import *  # NOQA
from drawing_tools import *
from footprint_scripts_crystals import *


if __name__ == '__main__':
    standardtags="THT crystal"
    standardtagsres="THT ceramic resonator filter"
    
    script3dhc49="crystal_hc49_2pin.py"
    with open(script3dhc49, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3dhc493p="crystal_hc49_3pin.py"
    with open(script3dhc493p, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3dres3="resonator_3pin.py"
    with open(script3dres3, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3dres2="resonator_2pin.py"
    with open(script3dres2, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3dhc49h="crystal_hc49_2pin_hor.py"
    with open(script3dhc49h, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")

    
    # common settings
    makeCrystalAll(footprint_name="Crystal_AT310_d3.0mm_l10.0mm_Horizontal",
                rm=2.54, pad_size=1, ddrill=0.5, pack_width=10.5, pack_height=3, pack_rm=1.2, pack_offset=3,
                package_pad=True, package_pad_offset=3.5, package_pad_size=[10.5,3.2],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat", description="Crystal THT AT310 10.0mm-10.5mm length 3.0mm diameter", lib_name="Crystals", tags=["AT310"],
                offset3d=[1.27/25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_AT310_d3.0mm_l10.0mm_Vertical",
                rm=2.54, pad_size=1, ddrill=0.5, pack_diameter=3,
                description="Crystal THT AT310 10.0mm-10.5mm length 3.0mm diameter", lib_name="Crystals", tags=["AT310"],
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalAll(footprint_name="Crystal_C26-LF_d2.1mm_l6.5mm_Horizontal",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=6.5, pack_height=2.06, pack_rm=0.7, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[6.5,2.2],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat", description="Crystal THT C26-LF 6.5mm length 2.06mm diameter", tags=["C26-LF"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_C26-LF_d2.1mm_l6.5mm_Vertical",
                rm=1.9, pad_size=1, ddrill=0.5, pack_diameter=2.06,
                description="Crystal THT C26-LF 6.5mm length 2.06mm diameter", tags=["C26-LF"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalAll(footprint_name="Crystal_C38-LF_d3.0mm_l8.0mm_Horizontal",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=8, pack_height=3, pack_rm=1.09, pack_offset=2.5,
                package_pad=True, package_pad_offset=3, package_pad_size=[8,3],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat", description="Crystal THT C38-LF 8.0mm length 3.0mm diameter", tags=["C38-LF"],
                lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_C38-LF_d3.0mm_l8.0mm_Vertical",
                rm=1.9, pad_size=1, ddrill=0.5, pack_diameter=3,
                description="Crystal THT C38-LF 8.0mm length 3.0mm diameter", tags=["C38-LF"],
                lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_Round_d3.0mm_Vertical",
                rm=1.9, pad_size=1, ddrill=0.5, pack_diameter=3,
                description="Crystal THT C38-LF 8.0mm length 3.0mm diameter", tags=["C38-LF"],
                lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalAll(footprint_name="Crystal_DS26_d2.0mm_l6.0mm_Horizontal",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=6, pack_height=2, pack_rm=0.7, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[6,2.5],
                package_pad_add_holes=True, package_pad_drill_size=[1, 1], package_pad_ddrill=0.5,
                style="flat", description="Crystal THT DS26 6.0mm length 2.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS26"],lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_DS26_d2.0mm_l6.0mm_Vertical",
                rm=1.9, pad_size=1, ddrill=0.5, pack_diameter=2,
                description="Crystal THT DS26 6.0mm length 2.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS26"],lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_Round_d2.0mm_Vertical",
                rm=1.9, pad_size=1, ddrill=0.5, pack_diameter=2,
                description="Crystal THT DS26 6.0mm length 2.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS26"],lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalAll(footprint_name="Crystal_DS15_d1.5mm_l5.0mm_Horizontal",
                rm=1.7, pad_size=1, ddrill=0.5, pack_width=5, pack_height=1.5, pack_rm=0.5, pack_offset=1.5,
                package_pad=True, package_pad_offset=2, package_pad_size=[5,2],
                package_pad_add_holes=True, package_pad_drill_size=[1, 1], package_pad_ddrill=0.5,
                style="flat",
                description="Crystal THT DS15 5.0mm length 1.5mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS15"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_DS15_d1.5mm_l5.0mm_Vertical",
                rm=1.7, pad_size=1, ddrill=0.5, pack_diameter=1.5,
                description="Crystal THT DS15 5.0mm length 1.5mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS15"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_Round_d1.5mm_Vertical",
                rm=1.7, pad_size=1, ddrill=0.5, pack_diameter=1.5,
                description="Crystal THT DS15 5.0mm length 1.5mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS15"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalAll(footprint_name="Crystal_DS10_d1.0mm_l4.3mm_Horizontal",
                rm=1.5, pad_size=1, ddrill=0.5, pack_width=4.3, pack_height=1, pack_rm=0.3, pack_offset=1.5,
                package_pad=True, package_pad_offset=2, package_pad_size=[4.3, 1.5],
                package_pad_add_holes=True, package_pad_drill_size=[1, 1], package_pad_ddrill=0.5,
                style="flat",
                description="Crystal THT DS10 4.3mm length 1.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS10"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_DS10_d1.0mm_l4.3mm_Vertical",
                rm=1.5, pad_size=1, ddrill=0.5, pack_diameter=1,
                description="Crystal THT DS10 4.3mm length 1.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS10"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalRoundVert(footprint_name="Crystal_Round_d1.0mm_Vertical",
                rm=1.5, pad_size=1, ddrill=0.5, pack_diameter=1,
                description="Crystal THT DS10 1.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS10"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeCrystalAll(footprint_name="Crystal_HC49-U_Horizontal",
                rm=4.9, pad_size=1.5, ddrill=0.8, pack_width=13.0, pack_height=10.9, pack_rm=4.9, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[13.5, 11],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="hc49",
                description="Crystal THT HC-49/U http://5hertz.com/pdfs/04404_D.pdf",
                lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49h, height3d=4.65, iheight3d=4)
    makeCrystalHC49Vert(footprint_name = "Crystal_HC49-U_Vertical", pins=2,
                        rm=4.88, pad_size=1.5, ddrill=0.8, pack_width=10.9, pack_height=4.65,
                        innerpack_width=10, innerpack_height=4,
                        tags=standardtags+"HC-49/U", description="Crystal THT HC-49/U http://5hertz.com/pdfs/04404_D.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=13)
    makeCrystalHC49Vert(footprint_name="Crystal_HC49-U-3pin_Vertical", pins=3,
                        rm=4.88, pad_size=1.5, ddrill=0.8, pack_width=10.9, pack_height=4.65,
                        innerpack_width=10, innerpack_height=4,
                        tags=standardtags+"HC-49/U", description="Crystal THT HC-49/U, 3pin-version, http://www.raltron.com/products/pdfspecs/crystal_hc_49_45_51.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc493p, height3d=13)
    makeCrystalHC49Vert(footprint_name = "Crystal_HC49-4H_Vertical", pins=2,
                        rm=4.88, pad_size=1.5, ddrill=0.8, pack_width=11.05, pack_height=4.65,
                        innerpack_width=10, innerpack_height=4,
                        tags=standardtags+"HC-49-4H", description="Crystal THT HC-49-4H http://5hertz.com/pdfs/04404_D.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=4)
    makeCrystalAll(footprint_name="Crystal_HC18-U_Horizontal",
                rm=4.9, pad_size=1.5, ddrill=0.8, pack_width=13.0, pack_height=10.9, pack_rm=4.9, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[13.5, 11],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="hc49",
                description="Crystal THT HC-18/U http://5hertz.com/pdfs/04404_D.pdf",
                lib_name="Crystals",
                   offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                   script3d=script3dhc49h, height3d=4.65, iheight3d=4)
    makeCrystalHC49Vert(footprint_name="Crystal_HC18-U_Vertical", pins=2,
                        rm=4.9, pad_size=1.5, ddrill=0.8, pack_width=10.9, pack_height=4.65,
                        innerpack_width=10, innerpack_height=4,
                        tags=standardtags+"HC-18/U",
                        description="Crystal THT HC-18/U, http://5hertz.com/pdfs/04404_D.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=13)
    makeCrystalAll(footprint_name="Crystal_HC33-U_Horizontal",
                rm=12.34, pad_size=2.7, ddrill=1.7, pack_width=19.7, pack_height=19.23, pack_rm=12.34, pack_offset=2.5,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[20.5, 20],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="hc49",
                description="Crystal THT HC-33/U http://pdi.bentech-taiwan.com/PDI/GEN20SPEV20HC3320U.pdf",
                lib_name="Crystals",
                   offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                   script3d=script3dhc49h, height3d=8.94, iheight3d=8.05)
    makeCrystalHC49Vert(footprint_name="Crystal_HC33-U_Vertical", pins=2,
                        rm=12.34, pad_size=2.7, ddrill=1.7, pack_width=19.23, pack_height=8.94,
                        innerpack_width=18.42, innerpack_height=8.05,
                        tags=standardtags+"HC-33/U",
                        description="Crystal THT HC-33/U, http://pdi.bentech-taiwan.com/PDI/GEN20SPEV20HC3320U.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=19.7)
    makeCrystalAll(footprint_name="Crystal_HC50_Horizontal",
                   rm=4.9, pad_size=2.3, ddrill=1.5, pack_width=13.36, pack_height=11.05, pack_rm=4.9, pack_offset=2.5,
                   package_pad=True, package_pad_offset=2.5, package_pad_size=[14, 11.5],
                   package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                   style="hc49",
                   description="Crystal THT HC-50 http://www.crovencrystals.com/croven_pdf/HC-50_Crystal_Holder_Rev_00.pdf",
                   lib_name="Crystals",
                   offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                   script3d=script3dhc49h, height3d=4.65, iheight3d=3.8)
    makeCrystalHC49Vert(footprint_name="Crystal_HC50_Vertical", pins=2,
                        rm=4.9, pad_size=2.3, ddrill=1.5, pack_width=11.05, pack_height=4.65,
                        innerpack_width=10.2, innerpack_height=3.8,
                        tags=standardtags+"HC-50",
                        description="Crystal THT HC-50, http://www.crovencrystals.com/croven_pdf/HC-50_Crystal_Holder_Rev_00.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=13.36)
    makeCrystalAll(footprint_name="Crystal_HC51_Horizontal",
                   rm=12.35, pad_size=2.3, ddrill=1.2, pack_width=19.7, pack_height=19.3, pack_rm=12.35, pack_offset=2.5,
                   package_pad=True, package_pad_offset=2.5, package_pad_size=[20.5, 20],
                   package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                   style="hc49",
                   description="Crystal THT HC-51 http://www.crovencrystals.com/croven_pdf/HC-51_Crystal_Holder_Rev_00.pdf",
                   lib_name="Crystals",
                   offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                   script3d=script3dhc49h, height3d=8.9, iheight3d=7.6)
    makeCrystalHC49Vert(footprint_name="Crystal_HC51-U_Vertical", pins=2,
                        rm=12.35, pad_size=2.3, ddrill=1.2, pack_width=19.3, pack_height=8.9,
                        innerpack_width=18, innerpack_height=7.6,
                        tags=standardtags+"HC-51/U",
                        description="Crystal THT HC-51/U, http://www.crovencrystals.com/croven_pdf/HC-51_Crystal_Holder_Rev_00.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=19.7)
    makeCrystalAll(footprint_name="Crystal_HC52-U_Horizontal",
                   rm=3.8, pad_size=1.5, ddrill=0.8, pack_width=8.8, pack_height=8, pack_rm=3.8, pack_offset=1.5,
                   package_pad=True, package_pad_offset=1.5, package_pad_size=[9.5, 8.5],
                   package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                   style="hc49",
                   description="Crystal THT HC-51/U http://www.kvg-gmbh.de/assets/uploads/files/product_pdfs/XS71xx.pdf",
                   lib_name="Crystals",
                   offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                   script3d=script3dhc49h, height3d=3.3, iheight3d=2.3)
    makeCrystalHC49Vert(footprint_name="Crystal_HC52-U_Vertical", pins=2,
                        rm=3.8, pad_size=1.5, ddrill=0.8, pack_width=8, pack_height=3.3,
                        innerpack_width=7, innerpack_height=2.3,
                        tags=standardtags+"HC-52/U",
                        description="Crystal THT HC-52/U, http://www.kvg-gmbh.de/assets/uploads/files/product_pdfs/XS71xx.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=8.8)
    makeCrystalHC49Vert(footprint_name="Crystal_HC52-U-3pin_Vertical", pins=3,
                        rm=3.8, pad_size=1.5, ddrill=0.8, pack_width=8, pack_height=3.3,
                        innerpack_width=7, innerpack_height=2.3,
                        tags=standardtags+"HC-52/U",
                        description="Crystal THT HC-52/U, http://www.kvg-gmbh.de/assets/uploads/files/product_pdfs/XS71xx.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc493p, height3d=8.8)
    makeCrystalAll(footprint_name="Crystal_HC52-8mm_Horizontal",
                   rm=3.8, pad_size=1.5, ddrill=0.8, pack_width=8, pack_height=8, pack_rm=3.8, pack_offset=1.5,
                   package_pad=True, package_pad_offset=1.5, package_pad_size=[8.5, 8.5],
                   package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                   style="hc49",
                   description="Crystal THT HC-51/8mm http://www.kvg-gmbh.de/assets/uploads/files/product_pdfs/XS71xx.pdf",
                   lib_name="Crystals",
                   offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                   script3d=script3dhc49h, height3d=3.3, iheight3d=2.3)
    makeCrystalHC49Vert(footprint_name="Crystal_HC52-8mm_Vertical", pins=2,
                        rm=3.8, pad_size=1.5, ddrill=0.8, pack_width=8, pack_height=3.3,
                        innerpack_width=7, innerpack_height=2.3,
                        tags=standardtags+"HC-49/U",
                        description="Crystal THT HC-52/8mm, http://www.kvg-gmbh.de/assets/uploads/files/product_pdfs/XS71xx.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=8)
    makeCrystalAll(footprint_name="Crystal_HC52-6mm_Horizontal",
                   rm=3.8, pad_size=1.5, ddrill=0.8, pack_width=6, pack_height=8, pack_rm=3.8, pack_offset=1.5,
                   package_pad=True, package_pad_offset=1.5, package_pad_size=[6.5, 8.5],
                   package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                   style="hc49",
                   description="Crystal THT HC-51/6mm http://www.kvg-gmbh.de/assets/uploads/files/product_pdfs/XS71xx.pdf",
                   lib_name="Crystals",
                   offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                   script3d=script3dhc49h, height3d=3.3, iheight3d=2.3)
    makeCrystalHC49Vert(footprint_name="Crystal_HC52-6mm_Vertical", pins=2,
                        rm=3.8, pad_size=1.5, ddrill=0.8, pack_width=8, pack_height=3.3,
                        innerpack_width=7, innerpack_height=2.3,
                        tags=standardtags+"HC-49/U",
                        description="Crystal THT HC-52/6mm, http://www.kvg-gmbh.de/assets/uploads/files/product_pdfs/XS71xx.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dhc49, height3d=6)
    makeCrystalHC49Vert(footprint_name="Resonator_Murata_DSN6", pins=3, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=7, pack_height=2.54,
                        innerpack_width=7, innerpack_height=2.54,
                        tags=standardtagsres+" DSN6",
                        description="Ceramic Resomator/Filter Murata DSN6, http://cdn-reichelt.de/documents/datenblatt/B400/DSN6NC51H.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres3, height3d=8)
    makeCrystalHC49Vert(footprint_name="Resonator_Murata_DSS6", pins=3, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=7, pack_height=2.54,
                        innerpack_width=7, innerpack_height=2.54,
                        tags=standardtagsres + " DSS6",
                        description="Ceramic Resomator/Filter Murata DSS6, http://cdn-reichelt.de/documents/datenblatt/B400/DSN6NC51H.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres3, height3d=7)
    makeCrystalHC49Vert(footprint_name="Resonator_Murata_CSTLSxxxG", pins=3, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=8, pack_height=3,
                        innerpack_width=8, innerpack_height=3,
                        tags=standardtagsres + " CSTLSxxxG",
                        description="Ceramic Resomator/Filter Murata CSTLSxxxG, http://www.murata.com/~/media/webrenewal/support/library/catalog/products/timingdevice/ceralock/p17e.ashx",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres3, height3d=5.5)
    makeCrystalHC49Vert(footprint_name="Resonator_Murata_CSTLSxxxX", pins=3, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=5.5, pack_height=3,
                        innerpack_width=5.5, innerpack_height=3,
                        tags=standardtagsres + " CSTLSxxxX",
                        description="Ceramic Resomator/Filter Murata CSTLSxxxX, http://www.murata.com/~/media/webrenewal/support/library/catalog/products/timingdevice/ceralock/p17e.ashx",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres3, height3d=5.5)
    makeCrystalHC49Vert(footprint_name="Resonator", pins=2, addSizeFootprintName=True,
                        rm=5, pad_size=1.5, ddrill=0.8, pack_width=10, pack_height=5,
                        innerpack_width=10, innerpack_height=5,
                        tags=standardtagsres + "",
                        description="Ceramic Resomator/Filter 10.0x5.0 RedFrequency MG/MT/MX series, http://www.red-frequency.com/download/datenblatt/redfrequency-datenblatt-ir-zta.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres2, height3d=10)
    makeCrystalHC49Vert(footprint_name="Resonator", pins=3, addSizeFootprintName=True,
                        rm=5, pad_size=1.5, ddrill=0.8, pack_width=10, pack_height=5,
                        innerpack_width=10, innerpack_height=5,
                        tags=standardtagsres + "",
                        description="Ceramic Resomator/Filter 10.0x5.0mm^2 RedFrequency MG/MT/MX series, http://www.red-frequency.com/download/datenblatt/redfrequency-datenblatt-ir-zta.pdf",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres3, height3d=10)
    makeCrystalHC49Vert(footprint_name="Resonator", pins=3, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=7, pack_height=2.5,
                        innerpack_width=7, innerpack_height=2.5,
                        tags=standardtagsres + "",
                        description="Ceramic Resomator/Filter 7.0x2.5mm^2",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres3, height3d=5.5)
    makeCrystalHC49Vert(footprint_name="Resonator", pins=2, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=7, pack_height=2.5,
                        innerpack_width=7, innerpack_height=2.5,
                        tags=standardtagsres + "",
                        description="Ceramic Resomator/Filter 7.0x2.5mm^2",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres2, height3d=5.5)
    makeCrystalHC49Vert(footprint_name="Resonator", pins=3, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=8, pack_height=3.5,
                        innerpack_width=8, innerpack_height=3.5,
                        tags=standardtagsres + "",
                        description="Ceramic Resomator/Filter 8.0x3.5mm^2",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres3, height3d=6.5)
    makeCrystalHC49Vert(footprint_name="Resonator", pins=2, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=8, pack_height=3.5,
                        innerpack_width=8, innerpack_height=3.5,
                        tags=standardtagsres + "",
                        description="Ceramic Resomator/Filter 8.0x3.5mm^2",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres2, height3d=6.5)
    makeCrystalHC49Vert(footprint_name="Resonator", pins=3, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=6, pack_height=3.0,
                        innerpack_width=6, innerpack_height=3.0,
                        tags=standardtagsres + "",
                        description="Ceramic Resomator/Filter 6.0x3.0mm^2",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres3, height3d=6.5)
    makeCrystalHC49Vert(footprint_name="Resonator", pins=2, addSizeFootprintName=True,
                        rm=5, pad_size=1.7, ddrill=1, pack_width=6, pack_height=3.0,
                        innerpack_width=6, innerpack_height=3.0,
                        tags=standardtagsres + "",
                        description="Ceramic Resomator/Filter 6.0x3.0mm^2",
                        lib_name="Crystals",
                        offset3d=[0, 0, 0], scale3d=[1/2.54, 1/2.54, 1/2.54], rotate3d=[0, 0, 0],
                        script3d=script3dres2, height3d=6.5)
