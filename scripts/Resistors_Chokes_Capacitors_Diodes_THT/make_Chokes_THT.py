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
from resistor_tools import *
from footprint_scripts import *









if __name__ == '__main__':
    # standard resistors: http://cdn-reichelt.de/documents/datenblatt/B400/1_4W%23YAG.pdf
    type = "cyl"
    d2=0

    # axial Chokes
    seriesname = "Axial"; w = 9.5; d = 4; ddrill = 1; R_POW = 0; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/DS_SMCC_NEU.pdf, http://cdn-reichelt.de/documents/datenblatt/B400/LEADEDINDUCTORS.pdf"; name_additions=["Fastron","SMCC"]
    for rm in [12.7,15.24]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [2.54,5.08]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 7; d = 3.3; ddrill = 0.8; R_POW = 0; add_description="http://www.fastrongroup.com/image-show/70/MICC.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron","MICC"]
    for rm in [10.16,12.7]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [2.54,5.08]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 24; d = 7.5; ddrill = 1.2; R_POW = 0; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/DS_MESC.pdf"; name_additions=["Fastron","MESC"]
    for rm in [27.94]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 16; d = 7.5; ddrill = 1.1; R_POW = 0; add_description="http://www.fastrongroup.com/image-show/26/XHBCC.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron","XHBCC"]
    for rm in [20.32,25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 16; d = 6.3; ddrill = 1.1; R_POW = 0; add_description="http://www.fastrongroup.com/image-show/25/VHBCC.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron","VHBCC"]
    for rm in [20.32,25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions+["Fastron","MISC"], classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 14.5; d = 5.8; ddrill = 1.1; R_POW = 0; add_description="http://www.fastrongroup.com/image-show/18/HBCC.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron","HBCC"]
    for rm in [20.32,25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 12.8; d = 5.8; ddrill = 1.1; R_POW = 0; add_description="http://www.fastrongroup.com/image-show/18/HBCC.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron","HBCC"]
    for rm in [20.32,25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 12; d = 5; ddrill = 1.2; R_POW = 0; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/DS_MISC.pdf"; name_additions=["Fastron","MISC"]
    for rm in [15.24]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 11; d = 4.5; ddrill = 1.0; R_POW = 0; add_description="http://www.fastrongroup.com/image-show/21/MECC.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron","MECC"]
    for rm in [15.24]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 13; d = 4.5; ddrill = 1.2; R_POW = 0; add_description="http://www.fastrongroup.com/image-show/19/HCCC.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron","HCCC"]
    for rm in [15.24]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 14; d = 4.5; ddrill = 1.0; R_POW = 0; add_description="http://www.fastrongroup.com/image-show/20/LACC.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron","LACC"]
    for rm in [15.24]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 20; d = 8; ddrill = 1.2; R_POW = 0; add_description=""; name_additions=[]
    for rm in [25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 30; d = 8; ddrill = 1.4; R_POW = 0; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/DS_77A.pdf"; name_additions=[]
    for rm in [35.56]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions+["Fastron","77A"], classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions+["Fastron","77A"], classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 26; d = 9; ddrill = 1.2; R_POW = 0; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/DS_77A.pdf"; name_additions=["Fastron","77A"]
    for rm in [30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 26; d = 10; ddrill = 1.2; R_POW = 0; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/DS_77A.pdf"; name_additions=["Fastron","77A"]
    for rm in [30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    seriesname = "Axial"; w = 26; d = 11; ddrill = 1.2; R_POW = 0; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/DS_77A.pdf"; name_additions=["Fastron","77A"]
    for rm in [30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=name_additions, classname="Choke", lib_name="Choke_Axial_ThroughHole")

    # radial Chokes
    rm2=0; w2=0
    type = "round"; seriesname = "Radial";
    w = 12.5; w2=w; h = w; ddrill = 1.2; rm=9.0; rm2=0; R_POW=0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B400/DS_09HCP.pdf"; name_additions=["Fastron", "09HCP"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 12.5; w2=w; h = w; ddrill = 1.2; rm=7.0; rm2=0; R_POW=0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B400/DS_09HCP.pdf"; name_additions=["Fastron", "09HCP"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 13.5; w2=w; h = w; ddrill = 1.2; rm=7.0; rm2=0; R_POW=0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B400/DS_09HCP.pdf"; name_additions=["Fastron", "09HCP"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 12.0; w2=w; h = w; ddrill = 1; rm=5.0; rm2=0; R_POW=0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B400/DS_11P.pdf"; name_additions=["Fastron", "11P"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 10.5; w2=w; h = w; ddrill = 1; rm=5.0; rm2=0; R_POW=0; add_description = "http://www.abracon.com/Magnetics/radial/AISR-01.pdf"; name_additions=["Abacron", "AISR-01"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 10; w2=w; h = w; ddrill = 1; rm=5.0; rm2=0; R_POW=0; add_description = "http://www.fastrongroup.com/image-show/37/07M.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron", "07M"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 8.7; w2=w; h = w; ddrill = 1; rm=5.0; rm2=0; R_POW=0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B400/DS_07HCP.pdf"; name_additions=["Fastron", "07HCP"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 7.8; w2=w; h = w; ddrill = 1; rm=5.0; rm2=0; R_POW=0; add_description = "http://www.abracon.com/Magnetics/radial/AISR875.pdf"; name_additions=["Fastron", "07HCP"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 7.5; w2=w; h = w; ddrill = 1; rm=5.0; rm2=0; R_POW=0; add_description = "http://www.fastrongroup.com/image-show/39/07P.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron", "07P"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 7.5; w2=w; h = w; ddrill = 1; rm=3.5; rm2=0; R_POW=0; add_description = "http://www.fastrongroup.com/image-show/39/07P.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron", "07P"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 9.5; w2=w; h = w; ddrill = 1; rm=5.0; rm2=0; R_POW=0; add_description = "http://www.fastrongroup.com/image-show/107/07HVP%2007HVP_T.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron", "07HVP"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 10; w2=w; h = w; ddrill = 1; rm=5.0; rm2=0; R_POW=0; add_description = "http://www.fastrongroup.com/image-show/37/07M.pdf?type=Complete-DataSheet&productType=series"; name_additions=["Fastron", "07P"]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 7; w2=w; h = w; ddrill = 1; rm=3.0; rm2=0; R_POW=0; add_description = "http://www.abracon.com/Magnetics/radial/AIUR-16.pdf"; name_additions=[]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 6.0; w2=w; h = w; ddrill = 1; rm=4.0; rm2=0; R_POW=0; add_description = "http://www.abracon.com/Magnetics/radial/AIUR-07.pdf"; name_additions=[]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 18; w2=w; h = w; ddrill = 1; rm=10.0; rm2=0; R_POW=0; add_description = "http://www.abracon.com/Magnetics/radial/AIUR-15.pdf"; name_additions=[]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 21; w2=w; h = w; ddrill = 1; rm=19.0; rm2=0; R_POW=0; add_description = "http://www.abracon.com/Magnetics/radial/AIRD02.pdf"; name_additions=[]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 24; w2=w; h = w; ddrill = 1.5; rm=24.0; rm2=0; R_POW=0; add_description = ""; name_additions=[]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")
    w = 28; w2=w; h = w; ddrill = 1.5; rm=29.2; rm2=0; R_POW=0; add_description = ""; name_additions=[]
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=name_additions, add_description=add_description, classname="Choke", lib_name="Choke_Radial_ThroughHole")


