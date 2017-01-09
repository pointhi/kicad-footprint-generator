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
from crystal_tools import *
from crystal_footprints import *




if __name__ == '__main__':
    standardtags="SMD SMT crystal oscillator"
    # common settings
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_IQD_IQXO70", addSizeFootprintName=True, pins=4,
                  pad_sep_x=5.08, pad_sep_y=4.2, pad=[1.8,2.0], pack_width=7.5, pack_height=5, pack_bevel=0.4,
                   hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                   description="IQD Crystal Clock Oscillator IQXO-70, http://www.iqdfrequencyproducts.com/products/details/iqxo-70-11-30.pdf", tags=standardtags+"",
                   lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_Fordahl_DFAS15", addSizeFootprintName=True, pins=4,
                          pad_sep_x=2.6+1.5, pad_sep_y=1.6+1.2, pad=[1.5, 1.2], pack_width=5, pack_height=3.2, pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.5,
                          description="Ultraminiature Crystal Clock Oscillator TXCO Fordahl DFA S15-OV/UOV, http://www.iqdfrequencyproducts.com/products/details/iqxo-70-11-30.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_Fordahl_DFAS11", addSizeFootprintName=True, pins=4,
                          pad_sep_x=5.08, pad_sep_y=4.4, pad=[1.4,2], pack_width=7, pack_height=5,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="Miniature Crystal Clock Oscillator TXCO Fordahl DFA S11-OV/UOV, http://www.iqdfrequencyproducts.com/products/details/iqxo-70-11-30.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_Fordahl_DFAS2", addSizeFootprintName=True, pins=4,
                          pad_sep_x=5.08, pad_sep_y=4.4, pad=[1.4, 2], pack_width=7.3, pack_height=5.08,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="Mminiature Crystal Clock Oscillator TXCO Fordahl DFA S2-KS/LS/US, http://www.iqdfrequencyproducts.com/products/details/iqxo-70-11-30.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_Fordahl_DFAS3", addSizeFootprintName=True, pins=4,
                          pad_sep_x=5.08, pad_sep_y=6.4, pad=[1.5, 2.2], pack_width=9.1, pack_height=7.2,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="Miniature Crystal Clock Oscillator TXCO Fordahl DFA S3-KS/LS/US, http://www.iqdfrequencyproducts.com/products/details/iqxo-70-11-30.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_Fordahl_DFAS7", addSizeFootprintName=True, pins=4,
                          pad_sep_x=19.0, pad_sep_y=7.6, pad=[2.6,1.3], pack_width=19.9, pack_height=12.9,
                          pack_bevel=2,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="Miniature Crystal Clock Oscillator TXCO Fordahl DFA S7-K/L, http://www.iqdfrequencyproducts.com/products/details/iqxo-70-11-30.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_Fordahl_DFAS7", addSizeFootprintName=True, pins=4,
                          pad_sep_x=19.0, pad_sep_y=7.6, pad=[2.6, 1.3], pack_width=19.9, pack_height=12.9,
                          pack_bevel=2,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="Miniature Crystal Clock Oscillator TXCO Fordahl DFA S7-K/L, http://www.iqdfrequencyproducts.com/products/details/iqxo-70-11-30.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystal(footprint_name="Oscillator_SMD_Fordahl_DFAS1", addSizeFootprintName=True, pins=6,
                          pad_sep_x=2.54, pad_sep_y=8.9, pad=[1.27, 2.54], pack_width=14.8, pack_height=9.1,
                          pack_bevel=1,style="rect1bevel",
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.5,
                          description="Miniature Crystal Clock Oscillator TXCO Fordahl DFA S1-KHZ/LHZ, http://www.iqdfrequencyproducts.com/products/details/iqxo-70-11-30.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_Abracon_ASV", addSizeFootprintName=True, pins=4,
                          pad_sep_x=5.08, pad_sep_y=4.0, pad=[1.8, 2], pack_width=7, pack_height=5.08,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="Miniature Crystal Clock Oscillator Abracon ASV series, http://www.abracon.com/Oscillators/ASV.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_Abracon_ASE", addSizeFootprintName=True, pins=4,
                          pad_sep_x=2.1, pad_sep_y=1.65, pad=[1.3, 1.1], pack_width=3.2, pack_height=2.5,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.5,
                          description="Miniature Crystal Clock Oscillator Abracon ASE series, http://www.abracon.com/Oscillators/ASEseries.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_TXC_7C", addSizeFootprintName=True, pins=4,
                          pad_sep_x=2.54, pad_sep_y=2.2, pad=[1.4, 1.2], pack_width=5, pack_height=3.2,
                          pack_bevel=0.2,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=1,
                          description="Miniature Crystal Clock Oscillator TXC 7C series, http://www.txccorp.com/download/products/osc/7C_o.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_EuroQuartz_XO32", addSizeFootprintName=True, pins=4,
                          pad_sep_x=2.15, pad_sep_y=1.55, pad=[1,0.9], pack_width=3.2, pack_height=2.5,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.5,
                          description="Miniature Crystal Clock Oscillator EuroQuartz XO32 series, http://cdn-reichelt.de/documents/datenblatt/B400/XO32.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_EuroQuartz_XO53", addSizeFootprintName=True, pins=4,
                          pad_sep_x=2.54, pad_sep_y=2.2, pad=[1.4,1.2], pack_width=5, pack_height=3.2,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=1,
                          description="Miniature Crystal Clock Oscillator EuroQuartz XO53 series, http://cdn-reichelt.de/documents/datenblatt/B400/XO53.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_EuroQuartz_XO91", addSizeFootprintName=True, pins=4,
                          pad_sep_x=5, pad_sep_y=4.2, pad=[2, 2], pack_width=7, pack_height=5,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="Miniature Crystal Clock Oscillator EuroQuartz XO91 series, http://cdn-reichelt.de/documents/datenblatt/B400/XO91.pdf",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_SeikoEpson_SG8002JA", addSizeFootprintName=True, pins=4,
                          style="dip",
                          pad_sep_x=5.08, pad_sep_y=8.8,
                          pad=[1.3, 3], pack_width=14, pack_height=8.65, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Oscillator Seiko Epson SG-8002JA https://support.epson.biz/td/api/doc_check.php?mode=dl&lang=en&Parts=SG-8002DC",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_SeikoEpson_SG8002JC", addSizeFootprintName=True, pins=4,
                          style="dip",
                          pad_sep_x=5.08, pad_sep_y=4.6,
                          pad=[1.3, 2.1], pack_width=10.5, pack_height=5, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Oscillator Seiko Epson SG-8002JC https://support.epson.biz/td/api/doc_check.php?mode=dl&lang=en&Parts=SG-8002DC",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_SeikoEpson_SG8002CE", addSizeFootprintName=True, pins=4,
                          pad_sep_x=2.4, pad_sep_y=1.9, pad=[1.4,1.2], pack_width=3.2, pack_height=2.5,
                          pack_bevel=0.1,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.5,
                          description="SMD Crystal Oscillator Seiko Epson SG-8002CE https://support.epson.biz/td/api/doc_check.php?mode=dl&lang=en&Parts=SG-8002DC",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_SeikoEpson_SG8002LB", addSizeFootprintName=True, pins=4,
                          pad_sep_x=2.54, pad_sep_y=2.2, pad=[1.6, 1.5], pack_width=5, pack_height=3.2,
                          pack_bevel=0.0,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.5,
                          description="SMD Crystal Oscillator Seiko Epson SG-8002LB https://support.epson.biz/td/api/doc_check.php?mode=dl&lang=en&Parts=SG-8002DC",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_SeikoEpson_SG8002CA", addSizeFootprintName=True, pins=4,
                          pad_sep_x=5.08, pad_sep_y=4.2, pad=[1.8, 2], pack_width=7, pack_height=5,
                          pack_bevel=0.0,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="SMD Crystal Oscillator Seiko Epson SG-8002CA https://support.epson.biz/td/api/doc_check.php?mode=dl&lang=en&Parts=SG-8002DC",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Oscillator_SMD_SeikoEpson_SG210", addSizeFootprintName=True, pins=4,
                          pad_sep_x=1.7, pad_sep_y=1.3, pad=[1.1,0.9], pack_width=2.5, pack_height=2,
                          pack_bevel=0.0,
                          hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=2,
                          description="SMD Crystal Oscillator Seiko Epson SG-210 https://support.epson.biz/td/api/doc_check.php?mode=dl&lang=en&Parts=SG-210SED",
                          tags=standardtags + "",
                          lib_name="Oscillators", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])

