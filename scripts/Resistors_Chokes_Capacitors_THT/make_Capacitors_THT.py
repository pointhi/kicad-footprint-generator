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
    R_POW = 0
    specialtags=["Capacitor"]
    
    ###########################################################
    # rectangular capacitors
    ###########################################################
    type = "simple"
    #       w    d    rm    ddrill               name_additions                 add_description
    caps=[
        [  13,   3,   10,      1,              ["FKS3","FKP3","MKS4"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf, http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  13,   4,   10,      1,              ["FKS3","FKP3","MKS4"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf, http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [13.5,   4,   10,      1,              ["FKS3","FKP3","MKS4"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf, http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  13,   5,   10,      1,              ["FKS3","FKP3","MKS4"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf, http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [13.5,   5,   10,      1,              ["FKS3","FKP3","MKS4"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf, http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  13,   6,   10,      1,              ["FKS3","FKP3","MKS4"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf, http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  13,   8,   10,      1,              ["FKS3","FKP3","MKS4"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf, http://www.wima.com/EN/WIMA_MKS_4.pdf"],

        [  10,   3,  7.5,      1,              ["FKS3","FKP3"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf"],
        [  10,   4,  7.5,      1,              ["FKS3","FKP3"],                      "http://www.wima.com/EN/WIMA_FKS_3.pdf"],
        
        [  18,   5,   15,    1.2,              ["FKS3","FKP3"],                          "http://www.wima.com/EN/WIMA_FKS_3.pdf"],
        [  18,   6,   15,    1.2,              ["FKS3","FKP3"],                          "http://www.wima.com/EN/WIMA_FKS_3.pdf"],
        [  18,   7,   15,    1.2,              ["FKS3","FKP3"],                          "http://www.wima.com/EN/WIMA_FKS_3.pdf"],
        [  18,   8,   15,    1.2,              ["FKS3","FKP3"],                          "http://www.wima.com/EN/WIMA_FKS_3.pdf"],
        [  18,   9,   15,    1.2,              ["FKS3","FKP3"],                          "http://www.wima.com/EN/WIMA_FKS_3.pdf"],
        [  18,  11,   15,    1.2,              ["FKS3","FKP3"],                          "http://www.wima.com/EN/WIMA_FKS_3.pdf"],

        [  19,   5,   15,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  19,   6,   15,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  19,   7,   15,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  19,   8,   15,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  19,   9,   15,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  19,  11,   15,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],

        [26.5,   5, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [26.5,   6, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [26.5,   7, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [26.5, 8.5, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [26.5,10.5, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [26.5,11.5, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  28,   8, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  28,  10, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  28,  12, 22.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],

        [31.5,   9, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [31.5,  11, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [31.5,  13, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [31.5,  15, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [31.5,  17, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [31.5,  20, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],

        [  33,  13, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  33,  15, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  33,  20, 27.5,    1.2,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        
        [41.5,   9, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  11, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  13, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  15, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  17, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  19, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  20, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  24, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  31, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  35, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [41.5,  40, 37.5,      1.4,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],


        
               
        #[  56,  19, 48.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        #[  56,  23, 48.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        #[  56,  27, 48.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        #[  56,  33, 48.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        #[  56,  37, 48.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        
        #[  57,  25, 52.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        #[  57,  45, 52.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        #[  57,  50, 52.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        #[  57,  55, 52.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        #[  57,  65, 52.5,      1.1,            ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],

        [  27,   9,   22,      1.1,              [""],                          ""],
        [  27,   9,   23,      1.1,              [""],                          ""],
        [  27,  11,   22,      1.1,              [""],                          ""],
        [  32,  15,   27,      1.1,              [""],                          ""],
        [   4, 2.5,  2.5,      0.8,              [""],                          ""],
        [ 7.5, 6.5,    5,      0.8,              [""],                          ""],
        [   7, 2.5,    5,      0.8,              [""],                          ""],
        [   7,   2,    5,      0.8,              [""],                          ""],
        [   7, 2.5,    5,      0.8,              [""],                          ""],
        [   7, 3.5,    5,      0.8,              [""],                          ""],
        [   7, 4.5,    5,      0.8,              [""],                          ""],
        [   7,   6,    5,      0.8,              [""],                          ""],
        [   7, 6.5,    5,      0.9,              [""],                          ""],

        [ 4.6, 5.5,  2.5,      0.7,              ["MKS02", "FKP02"],                     "http://www.wima.de/DE/WIMA_MKS_02.pdf"],
        [ 4.6, 4.6,  2.5,      0.7,              ["MKS02", "FKP02"],                     "http://www.wima.de/DE/WIMA_MKS_02.pdf"],
        [ 4.6, 3.8,  2.5,      0.7,              ["MKS02", "FKP02"],                     "http://www.wima.de/DE/WIMA_MKS_02.pdf"],
        [ 4.6, 3.0,  2.5,      0.7,              ["MKS02", "FKP02"],                     "http://www.wima.de/DE/WIMA_MKS_02.pdf"],
        [ 4.6,   2,  2.5,      0.7,              ["MKS02", "FKP02"],                     "http://www.wima.de/DE/WIMA_MKS_02.pdf"],
                                                                                                                              
        [ 7.2, 2.5,    5,      0.8,              ["FKS2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],
        [ 7.2, 3.0,    5,      0.8,              ["FKS2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],
        [ 7.2, 3.5,    5,      0.8,              ["FKS2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],
        [ 7.2, 4.5,    5,      0.8,              ["FKS2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],
        [ 7.2, 5.5,    5,      0.8,              ["FKS2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],
        [ 7.2, 7.2,    5,      0.8,              ["FKS2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],
        [ 7.2, 8.5,    5,      0.8,              ["FKP2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],
        [ 7.2,  11,    5,      0.8,              ["FKS2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],
        [ 7.2, 2.5,    5,      0.8,              ["FKS2","FKP2","MKS2","MKP2"],                      "http://www.wima.com/EN/WIMA_FKS_2.pdf"],

        [  10, 2.5,  7.5,        1,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  10, 3.0,  7.5,        1,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [  10, 4.0,  7.5,        1,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [10.3, 4.5,  7.5,        1,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [10.3,   5,  7.5,        1,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [10.3, 5.7,  7.5,        1,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],
        [10.3, 7.2,  7.5,        1,              ["MKS4"],                          "http://www.wima.com/EN/WIMA_MKS_4.pdf"],

    ]
    
    for w in [2.5, 2.6, 2.7, 3.2, 3.3, 3.4, 3.6, 3.8, 3.9, 4.0, 4.2, 4.9, 5.1, 5.7, 6.4, 6.7, 7.7, 8.5, 9.5, 9.8]:
        caps+=[   9, w,  7.5,      0.8,            ["MKT"],                           "https://en.tdk.eu/inf/20/20/db/fc_2009/MKT_B32560_564.pdf"],

    for w in [2.8,3.4,3.5,4.2,4.3,5.1,5.3,6.3,6.4,7.3,8.8]:
        caps+=[11.0, w,   10,      0.8,            ["MKT"],                           "https://en.tdk.eu/inf/20/20/db/fc_2009/MKT_B32560_564.pdf"],

    for w in [2,5,2.6,2.8,3.2,3.5,3.6,4.0,4.3,4.5,5.1,5.2,5.6,6.4,6.6,6.9,7.3,7.5,7.8,8.0,8.8,9.5,9.8]:
        caps+=[11.5, w,   10,      0.8,            ["MKT"],                           "https://en.tdk.eu/inf/20/20/db/fc_2009/MKT_B32560_564.pdf"],

    for w in [4.7,4.9,5,6,7,7.3,8.7,8.9,9,9.2,10.7,10.9,11.2,11.8,13.5,13.7,13.9]:
        caps+=[16.5, w,   15,      1.1,            ["MKT"],                           "https://en.tdk.eu/inf/20/20/db/fc_2009/MKT_B32560_564.pdf"],

    for w in [7,8.3,8.6,10.1,10.3,10.9,12.2,12.6,12.8]:
        caps+=[  24, w, 22.5,      1.2,            ["MKT"],                           "https://en.tdk.eu/inf/20/20/db/fc_2009/MKT_B32560_564.pdf"],

    for w in [7.6,7.8,7.9,9.1,9.6,11,11.9,12.2,13,13.8,14.2,16]:
        caps+=[  29, w, 27.5,      1.2,            ["MKT"],                           "https://en.tdk.eu/inf/20/20/db/fc_2009/MKT_B32560_564.pdf"],

    for c in caps:
        seriesname = "Rect";
        w = c[0];
        d = c[1];
        w2 = 0;
        rm = c[2];
        ddrill = c[3];
        add_description = c[5];
        name_additions = c[4]
        makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=d, ddrill=ddrill, R_POW=R_POW,
                                    type=type, w2=w2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                    specialfpname="", add_description=add_description, name_additions=name_additions,
                                    specialtags=specialtags, classname="C", lib_name="Capacitors_ThroughHole")


    ###########################################################
    # rectangular capacitors with 2 RMs
    ###########################################################
    caps=[]
    #           w        h       rm     rm2     ddrill
    caps+=[     7,     3.5,     2.5,      5,       0.8,            [""],                           ""],
    caps+=[    10,       5,       5,    7.5,       0.8,            [""],                           ""],
    caps+=[    13,     6.5,     7.5,     10,       0.8,            [""],                           ""],

    for c in caps:
        seriesname = "Rect";
        type="simple"
        w = c[0];
        d = c[1];
        w2 = 0;
        rm = c[2];
        rm2 = c[3];
        ddrill = c[4];
        add_description = c[6];
        name_additions = c[5]
        makeResistorRadial(seriesname=seriesname, rm=rm, rm2=rm2, w=w, h=d, ddrill=ddrill, R_POW=R_POW,
                                    type=type, w2=w2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                    specialfpname="", add_description=add_description, name_additions=name_additions,
                                    specialtags=specialtags, classname="C", lib_name="Capacitors_ThroughHole")



    ###########################################################
    # disc capacitors
    ###########################################################

    #       d    w    rm    ddrill               name_additions                 add_description
    caps = [
        [  12, 4.4, 7.75,      1.2,                          [],                              ""],
        [   3,   2,  2.5,      0.8,                          [],                              ""],
        [   6, 4.4,    5,      0.8,                          [],                              ""],
        [ 7.5, 4.4,    5,      0.8,                          [],                              ""],
        [   5, 2.5,  2.5,      0.8,                          [],                              "http://cdn-reichelt.de/documents/datenblatt/B300/DS_KERKO_TC.pdf"],
        [   5, 2.5,    5,      0.8,                          [],                              "http://cdn-reichelt.de/documents/datenblatt/B300/DS_KERKO_TC.pdf"],
        [   6, 2.5,    5,      0.8,                          [],                              "http://cdn-reichelt.de/documents/datenblatt/B300/DS_KERKO_TC.pdf"],
        [   7, 2.5,    5,      0.8,                          [],                              "http://cdn-reichelt.de/documents/datenblatt/B300/DS_KERKO_TC.pdf"],
        [   8, 2.5,    5,      0.8,                          [],                              "http://cdn-reichelt.de/documents/datenblatt/B300/DS_KERKO_TC.pdf"],
        [   9, 2.5,    5,      0.8,                          [],                              "http://cdn-reichelt.de/documents/datenblatt/B300/DS_KERKO_TC.pdf"],
        [  10, 2.5,    5,      0.8,                          [],                              "http://cdn-reichelt.de/documents/datenblatt/B300/DS_KERKO_TC.pdf"],
        [  3.0,1.6,  2.5,      0.8,                          [],                              "http://www.vishay.com/docs/45233/krseries.pdf"],
        [  3.4,2.1,  2.5,      0.8,                          [],                              "http://www.vishay.com/docs/45233/krseries.pdf"],
        [  3.8,2.6,  2.5,      0.8,                          [],                              "http://www.vishay.com/docs/45233/krseries.pdf"],
        [  4.3,1.9,    5,      0.8,                          [],                              "http://www.vishay.com/docs/45233/krseries.pdf"],
        [  4.7,2.5,    5,      0.8,                          [],                              "http://www.vishay.com/docs/45233/krseries.pdf"],
        [  5.1,3.2,    5,      0.8,                          [],                              "http://www.vishay.com/docs/45233/krseries.pdf"],

        [  7.5,5.0,    5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [  7.5,5.0,  7.5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [  7.5,5.0,   10,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [    8,5.0,    5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [    8,5.0,  7.5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [    8,5.0,   10,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [    9,5.0,    5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [    9,5.0,  7.5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [    9,5.0,   10,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [ 10.5,5.0,    5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [ 10.5,5.0,  7.5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [ 10.5,5.0,   10,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [   11,5.0,    5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [   11,5.0,  7.5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [   11,5.0,   10,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],

        [ 12.5,5.0,  7.5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [ 12.5,5.0,   10,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [ 14.5,5.0,  7.5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [ 14.5,5.0,   10,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [ 16.0,5.0,  7.5,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
        [ 16.0,5.0,   10,        1,                          [],                              "http://www.vishay.com/docs/28535/vy2series.pdf"],
    ]
    
    for c in caps:
        seriesname = "Disc";
        type = "disc"
        w = c[0];
        d = c[1];
        w2 = 0;
        rm = c[2];
        ddrill = c[3];
        add_description = c[5];
        name_additions = c[4]
        makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=d, ddrill=ddrill, R_POW=R_POW,
                           type=type, w2=w2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                           specialfpname="", add_description=add_description, name_additions=name_additions,
                           specialtags=specialtags, classname="C", lib_name="Capacitors_ThroughHole")



    
    
    
    
    
    
    
    
    ###########################################################
    # axial capacitors
    ###########################################################

    d2=0
    seriesname = "Axial"; w = 3.8; d = 2.6; ddrill = 0.8; R_POW = 0; add_description = "http://www.vishay.com/docs/45231/arseries.pdf"; name_additions = []
    for rm in [7.5, 10, 12.5, 15]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW,
                                    type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                    specialfpname="", add_description=add_description, name_additions=name_additions,
                                    specialtags=name_additions, classname="C", lib_name="Capacitors_ThroughHole")

    seriesname = "Axial"; w = 5.1; d = 3.1; ddrill = 0.8; R_POW = 0; add_description = "http://www.vishay.com/docs/45231/arseries.pdf"; name_additions = []
    for rm in [7.5, 10, 12.5, 15]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW,
                                    type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                    specialfpname="", add_description=add_description, name_additions=name_additions,
                                    specialtags=name_additions, classname="C", lib_name="Capacitors_ThroughHole")
    for w in [12,17,19,22]:
        if w == 12:
            rms = [15, 20]
            ds=[6.5,7.5,8.5,9.5,10.5]
        if w == 17:
            rms = [20, 25]
            ds=[6.5,7.0]
        if w == 19:
            rms = [25]
            ds=[7.5, 8.0, 9, 9.5]
        if w == 22:
            rms = [27.5]
            ds=[9.5,10.5]
        for d in ds:
            for rm in rms:
                seriesname = "Axial"; ddrill = 0.8; R_POW = 0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B300/STYROFLEX.pdf"; name_additions = []
                makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW,
                                            type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                            specialfpname="", add_description=add_description, name_additions=name_additions,
                                            specialtags=name_additions, classname="C", lib_name="Capacitors_ThroughHole")
    seriesname = "Axial"; w = 12; d = 6.5; ddrill = 0.8; R_POW = 0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B300/STYROFLEX.pdf"; name_additions = []
    for rm in [15,20]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW,
                                    type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                    specialfpname="", add_description=add_description, name_additions=name_additions,
                                    specialtags=name_additions, classname="C", lib_name="Capacitors_ThroughHole")
    seriesname = "Axial"; w = 12; d = 7.5; ddrill = 0.8; R_POW = 0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B300/STYROFLEX.pdf"; name_additions = []
    for rm in [15,20]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW,
                                    type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                    specialfpname="", add_description=add_description, name_additions=name_additions,
                                    specialtags=name_additions, classname="C", lib_name="Capacitors_ThroughHole")
    seriesname = "Axial"; w = 12; d = 8.5; ddrill = 0.8; R_POW = 0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B300/STYROFLEX.pdf"; name_additions = []
    for rm in [15,20]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW,
                                    type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                    specialfpname="", add_description=add_description, name_additions=name_additions,
                                    specialtags=name_additions, classname="C", lib_name="Capacitors_ThroughHole")
    seriesname = "Axial"; w = 12; d = 9.5; ddrill = 0.8; R_POW = 0; add_description = "http://cdn-reichelt.de/documents/datenblatt/B300/STYROFLEX.pdf"; name_additions = []
    for rm in [15,20]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW,
                                    type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                                    specialfpname="", add_description=add_description, name_additions=name_additions,
                                    specialtags=name_additions, classname="C", lib_name="Capacitors_ThroughHole")









    ###########################################################
    # tantal polarized capacitors
    ###########################################################
    specialtags=["Tantal Electrolytic Capacitor"]
    #            d           rm    ddrill               name_additions                 add_description
    caps = [
        [      4.5,         2.5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      4.5,           5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      5.0,         2.5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      5.0,           5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      5.5,         2.5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      5.5,           5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      6.0,         2.5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      6.0,           5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      7.0,         2.5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      7.0,           5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      8.0,         2.5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      8.0,           5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      9.0,         2.5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [      9.0,           5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [     10.5,         2.5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        [     10.5,           5,      0.8,                          [],                "http://cdn-reichelt.de/documents/datenblatt/B300/TANTAL-TB-Serie%23.pdf"],
        
    ]
    
    for c in caps:
        seriesname = "Radial_Tantal";
        type = "round"
        deco="tantal"
        d = c[0];
        w2 = 0;
        rm = c[1];
        ddrill = c[2];
        add_description = c[4];
        name_additions = c[3]
        makeResistorRadial(seriesname=seriesname, rm=rm, w=d, h=d, ddrill=ddrill, R_POW=R_POW,
                           type=type, w2=w2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                           specialfpname="", add_description=add_description, name_additions=name_additions,
                           specialtags=specialtags, classname="CP", lib_name="Capacitors_ThroughHole", deco=deco)
    
    ###########################################################
    # radial electrolytic capacitors
    ###########################################################
    specialtags=["Electrolytic Capacitor"]
    #            d           rm    rm2,   ddrill               name_additions                specialtags                  add_description
    caps = [
        [        4,         1.5,     0,      0.8,                          [],               [],               "" ],
        [        5,           2,     0,      0.8,                          [],               [],               "" ],
        [        5,         2.5,     0,      0.8,                          [],               [],               "" ],
        [      6.3,         2.5,     0,      0.8,                          [],               [],               "" ],
        [      7.5,         2.5,     0,      0.8,                          [],               [],               "" ],
        [        8,         2.5,     0,      0.8,                          [],               [],               "" ],
        [        8,         3.5,     0,      0.8,                          [],               [],               "" ],
        [        8,         3.8,     0,      0.8,                          [],               [],               "" ],
        [       10,           5,     0,        1,                          [],               [],               "" ],
        [       10,           5,   7.5,        1,                          [],               [],               "" ],
        [       10,         7.5,     0,        1,                          [],               [],               "" ],
        [       10,         2.5,     0,      0.8,                          [],               [],               "" ],
        [       10,         2.5,     5,      0.8,                          [],               [],               "" ],
        [     12.5,           5,     0,      1.2,                          [],               [],               "" ],
        [     12.5,         7.5,     0,      1.2,                          [],               [],               "" ],
        [     12.5,         2.5,     0,      1.2,                          [],               [],               "" ],
        [       13,           5,     0,      1.2,                          [],               [],               "" ],
        [       13,         7.5,     0,      1.2,                          [],               [],               "" ],
        [       13,         2.5,     0,      1.2,                          [],               [],               "" ],
        [       14,           5,     0,      1.2,                          [],               [],               "" ],
        [       14,         7.5,     0,      1.2,                          [],               [],               "" ],
        [       16,         7.5,     0,      1.2,                          [],               [],               "" ],
        [       17,         7.5,     0,      1.2,                          [],               [],               "" ],
        [       18,         7.5,     0,      1.2,                          [],               [],               "" ],
        [       22,          10,     0,      1.2,                          [],               [],               "" ],
        [       24,          10,     0,      1.2,                          [],               [],               "" ],
        [       26,          10,     0,      1.2,                          [],               [],               "" ],
        [       30,          10,     0,      1.2,                          [],               [],               "" ],
        [       35,          10,     0,      1.2,                          [],               [],               "" ],
        [       22,          10,     0,      0.8,                          [],               [],               "" ],
        [       22,          10,     0,      0.8,                          [],               [],               "" ],
        [       22,          10,     0,      0.8,                          [],               [],               "" ],
    
    ]
    
    for c in caps:
        seriesname = "Radial";
        type = "round"
        deco = "elco"
        d = c[0];
        w2 = 0;
        rm = c[1];
        rm2=c[2]
        ddrill = c[3];
        add_description = c[6];
        name_additions = c[4]
        special_tags=specialtags+c[5]
        makeResistorRadial(seriesname=seriesname, rm=rm, rm2=rm2, w=d, h=d, ddrill=ddrill, R_POW=R_POW,
                           type=type, w2=w2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                           specialfpname="", add_description=add_description, name_additions=name_additions,
                           specialtags=special_tags, classname="CP", lib_name="Capacitors_ThroughHole", deco=deco)

    ###########################################################
    # axial electrolytic capacitors
    ###########################################################
    specialtags = ["Electrolytic Capacitor"]
    #            d          l           rm          ddrill               name_additions                specialtags                  add_description
    caps = [
        [       16,        40,          48,            1.2,                          [],                        [],                              ""],
        [        5,        11,          18,            1.2,                          [],                        [],                              ""],
        [        6,        11,          18,            1.2,                          [],                        [],                              ""],
        [        8,        21,          28,            1.2,                          [],                        [],                              ""],
    ]
    
    for c in caps:
        seriesname = "Axial";
        type = "cyl"
        deco = "elco"
        d = c[0];
        l = c[1];
        rm = c[2]
        ddrill = c[3];
        add_description = c[6];
        name_additions = c[4]
        special_tags = specialtags + c[5]
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=l, d=d, ddrill=ddrill, R_POW=R_POW,
                           type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1,
                           specialfpname="", add_description=add_description, name_additions=name_additions,
                           specialtags=special_tags, classname="CP", lib_name="Capacitors_ThroughHole", deco=deco)
    
    
