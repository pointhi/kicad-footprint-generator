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
from footprint_scripts_dsub import *  # NOQA




if __name__ == '__main__':

    HighDensity=False
    rmx=2.77
    rmy=2.84
    rmy_unboxed2=2.54
    pindrill=1.0
    pad=1.6
    mountingdrill=3.2
    mountingpad=4
    side_angle_degree=10
    conn_cornerradius=1.6
    outline_cornerradius=1
    can_height_male=6
    can_height_female=6.17
    shieldthickness=0.4
    backcan_height=4.5
    smaller_backcan_height=2.8
    soldercup_length=2.9
    soldercup_diameter=1.2
    soldercup_padsize=[2*rmx/3,soldercup_length*1.2]
    soldercup_pad_edge_offset=0.25
    smaller_backcan_offset=1
    nut_diameter=5
    nut_length=5
    tags_additional=[]
    lib_name="${KISYS3DMOD}/Connectors_DSub"
    classname="DSUB"
    classname_description="D-Sub connector"
    webpage="https://disti-assets.s3.amazonaws.com/tonar/files/datasheets/16730.pdf"
    #                  0,             1,             2,             3,         4,                5,                  6
    #               pins, mounting_dist, outline_sizex, outlinesize_y, connwidth,  connheight_male,  connheight_female
    sizes_table=[
                [      9,            25,         30.85,         12.50,      16.3,              8.3,              7.9 ],
                [     15,         33.30,         39.20,         12.50,      24.6,              8.3,              7.9 ],
                [     25,         47.10,         53.10,         12.50,      38.3,              8.3,              7.9 ],
                [     37,         63.50,         69.40,         12.50,      54.8,              8.3,              7.9 ],
                ]
    for data in sizes_table:
        makeDSubStraight(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, mountingdrill=mountingdrill, mountingpad=mountingpad, mountingdistance=data[1], outline_size=[data[2],data[3]], outline_cornerradius=outline_cornerradius, connwidth=data[4], side_angle_degree=side_angle_degree, connheight=data[5], conn_cornerradius=conn_cornerradius, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
        makeDSubStraight(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, mountingdrill=mountingdrill, mountingpad=mountingpad, mountingdistance=data[1], outline_size=[data[2],data[3]], outline_cornerradius=outline_cornerradius, connwidth=data[4], side_angle_degree=side_angle_degree, connheight=data[6], conn_cornerradius=conn_cornerradius, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
        makeDSubStraight(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], outline_size=[data[2],data[3]], outline_cornerradius=outline_cornerradius, connwidth=data[4], side_angle_degree=side_angle_degree, connheight=data[5], conn_cornerradius=conn_cornerradius, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
        makeDSubStraight(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], outline_size=[data[2],data[3]], outline_cornerradius=outline_cornerradius, connwidth=data[4], side_angle_degree=side_angle_degree, connheight=data[6], conn_cornerradius=conn_cornerradius, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
        
        makeDSubEdge(pins=data[0], isMale=True, rmx=rmx, pad=soldercup_padsize, mountingdrill=mountingdrill, mountingdistance=data[1], shield_width=data[2], shieldthickness=shieldthickness, connwidth=data[4], can_height=can_height_male, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height, smaller_backcan_offset=smaller_backcan_offset, smaller_backcan_height=smaller_backcan_height, soldercup_length=soldercup_length, soldercup_diameter=soldercup_diameter, soldercup_pad_edge_offset=soldercup_pad_edge_offset, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
        makeDSubEdge(pins=data[0], isMale=False, rmx=rmx, pad=soldercup_padsize, mountingdrill=mountingdrill, mountingdistance=data[1], shield_width=data[2], shieldthickness=shieldthickness, connwidth=data[4], can_height=can_height_female, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height, smaller_backcan_offset=smaller_backcan_offset, smaller_backcan_height=smaller_backcan_height, soldercup_length=soldercup_length, soldercup_diameter=soldercup_diameter, soldercup_pad_edge_offset=soldercup_pad_edge_offset, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
        


    # boxed angled
    #                   mounting_pcb_distance,   pin_pcb_distance
    angled_distances=[
                        [                7.88,               5.34 ],
                        [                9.52,               8.10 ],
                        [               11.72,              10.30 ],
                        [               16.38,              14.96 ],
                        [                8.60,              14.96 ],
                    ]
    for data in sizes_table:
        for angled_distance in angled_distances:
            mounting_pcb_distance=angled_distance[0]-shieldthickness
            pin_pcb_distance=angled_distance[1]-shieldthickness
            backbox_height=max(pin_pcb_distance+rmy+pad/2, mounting_pcb_distance+mountingpad/2)+1
            makeDSubAngled(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=mountingdrill, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=mounting_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, can_width=data[4], can_height=can_height_male, backbox_width=data[2], backbox_height=backbox_height, nut_diameter=nut_diameter, nut_length=nut_length, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
            makeDSubAngled(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=mountingdrill, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=mounting_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, can_width=data[4], can_height=can_height_female, backbox_width=data[2], backbox_height=backbox_height, nut_diameter=nut_diameter, nut_length=nut_length, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
            #makeDSubAngled(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=mounting_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, can_width=data[4], can_height=can_height_male, backbox_width=data[2], backbox_height=backbox_height, nut_diameter=nut_diameter, nut_length=nut_length, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
            #makeDSubAngled(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=mounting_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, can_width=data[4], can_height=can_height_female, backbox_width=data[2], backbox_height=backbox_height, nut_diameter=nut_diameter, nut_length=nut_length, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage)
    
    # unboxed angled
    webpageunboxed='http://docs-europe.electrocomponents.com/webdocs/1585/0900766b81585df2.pdf'
    backcan_height_unboxed=4.1
    pin_pcb_distance=9.4
    mounting_pcb_distance=0
    for data in sizes_table:
        makeDSubAngled(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=pin_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, backbox_width=0, backbox_height=0, can_width=data[4], can_height=can_height_male, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height_unboxed, nut_diameter=0, nut_length=0, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpageunboxed)
        makeDSubAngled(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=rmx, rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=pin_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, backbox_width=0, backbox_height=0, can_width=data[4], can_height=can_height_female, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height_unboxed, nut_diameter=0, nut_length=0, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpageunboxed)
        # alternatice y-pin-pitch
        makeDSubAngled(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=rmx, rmy=rmy_unboxed2, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=pin_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, backbox_width=0, backbox_height=0, can_width=data[4], can_height=can_height_male, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height_unboxed, nut_diameter=0, nut_length=0, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpageunboxed)
        makeDSubAngled(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=rmx, rmy=rmy_unboxed2, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=pin_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, backbox_width=0, backbox_height=0, can_width=data[4], can_height=can_height_female, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height_unboxed, nut_diameter=0, nut_length=0, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpageunboxed)



    HighDensity=True
    rmy=1.98
        #           pins, mounting_dist, outline_sizex, outlinesize_y, connwidth,  connheight_male,  connheight_female, rmx,  HighDensityOffsetMidLeft
    sizes_table=[
                [     15,            25,         30.85,         12.50,      16.3,              8.3,              7.9,    2.29, 7.04 ],
                [     26,         33.30,         39.20,         12.50,      24.6,              8.3,              7.9,    2.29, 6.88 ],
                [     44,         47.10,         53.10,         12.50,      38.3,              8.3,              7.9,    2.29, 6.88 ],
                [     62,         63.50,         69.40,         12.50,      54.8,              8.3,              7.9,    2.41, 7.00 ],
                ]
    for data in sizes_table:
        makeDSubStraight(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=data[7], rmy=rmy, pindrill=pindrill, pad=pad, mountingdrill=mountingdrill, mountingpad=mountingpad, mountingdistance=data[1], outline_size=[data[2],data[3]], outline_cornerradius=outline_cornerradius, connwidth=data[4], side_angle_degree=side_angle_degree, connheight=data[5], conn_cornerradius=conn_cornerradius, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage, HighDensityOffsetMidLeft=data[8])
        makeDSubStraight(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=data[7], rmy=rmy, pindrill=pindrill, pad=pad, mountingdrill=mountingdrill, mountingpad=mountingpad, mountingdistance=data[1], outline_size=[data[2],data[3]], outline_cornerradius=outline_cornerradius, connwidth=data[4], side_angle_degree=side_angle_degree, connheight=data[6], conn_cornerradius=conn_cornerradius, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage, HighDensityOffsetMidLeft=data[8])
        #makeDSubStraight(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=data[7], rmy=rmy, pindrill=pindrill, pad=pad, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], outline_size=[data[2],data[3]], outline_cornerradius=outline_cornerradius, connwidth=data[4], side_angle_degree=side_angle_degree, connheight=data[5], conn_cornerradius=conn_cornerradius, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage, HighDensityOffsetMidLeft=data[8])
        #makeDSubStraight(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=data[7], rmy=rmy, pindrill=pindrill, pad=pad, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], outline_size=[data[2],data[3]], outline_cornerradius=outline_cornerradius, connwidth=data[4], side_angle_degree=side_angle_degree, connheight=data[6], conn_cornerradius=conn_cornerradius, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage, HighDensityOffsetMidLeft=data[8])
        
        
    #                   mounting_pcb_distance,   pin_pcb_distance,  backbox_height
    angled_distances=[
                        [                5.34,               3.43,             8.6 ],
                        [               11.29,               8.75,             0.0 ],
                    ]
    for data in sizes_table:
        for angled_distance in angled_distances:
            mounting_pcb_distance=angled_distance[0]-shieldthickness
            pin_pcb_distance=angled_distance[1]-shieldthickness
            if angled_distance[2]>0:
                backbox_height=angled_distance[2]
            else:
                backbox_height=max(pin_pcb_distance+rmy+pad/2, mounting_pcb_distance+mountingpad/2)+1
            makeDSubAngled(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=data[7], rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=mountingdrill, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=mounting_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, can_width=data[4], can_height=can_height_male, backbox_width=data[2], backbox_height=backbox_height, nut_diameter=nut_diameter, nut_length=nut_length, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage, HighDensityOffsetMidLeft=data[8])
            makeDSubAngled(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=data[7], rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=mountingdrill, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=mounting_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, can_width=data[4], can_height=can_height_male, backbox_width=data[2], backbox_height=backbox_height, nut_diameter=nut_diameter, nut_length=nut_length, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpage, HighDensityOffsetMidLeft=data[8])

    
    # unboxed angled
    webpageunboxed='http://docs-europe.electrocomponents.com/webdocs/1585/0900766b81585df2.pdf'
    backcan_height_unboxed=4.1
    pin_pcb_distance=9.4
    mounting_pcb_distance=0
    for data in sizes_table:
        makeDSubAngled(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=data[7], rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=pin_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, backbox_width=0, backbox_height=0, can_width=data[4], can_height=can_height_male, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height_unboxed, nut_diameter=0, nut_length=0, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpageunboxed, HighDensityOffsetMidLeft=data[8])
        makeDSubAngled(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=data[7], rmy=rmy, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=pin_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, backbox_width=0, backbox_height=0, can_width=data[4], can_height=can_height_female, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height_unboxed, nut_diameter=0, nut_length=0, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpageunboxed, HighDensityOffsetMidLeft=data[8])
        makeDSubAngled(pins=data[0], isMale=True, HighDensity=HighDensity, rmx=data[7], rmy=rmy_unboxed2, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=pin_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, backbox_width=0, backbox_height=0, can_width=data[4], can_height=can_height_male, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height_unboxed, nut_diameter=0, nut_length=0, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpageunboxed, HighDensityOffsetMidLeft=data[8])
        makeDSubAngled(pins=data[0], isMale=False, HighDensity=HighDensity, rmx=data[7], rmy=rmy_unboxed2, pindrill=pindrill, pad=pad, pin_pcb_distance=pin_pcb_distance, mountingdrill=0, mountingpad=mountingpad, mountingdistance=data[1], mounting_pcb_distance=pin_pcb_distance, shield_width=data[2], shield_thickness=shieldthickness, backbox_width=0, backbox_height=0, can_width=data[4], can_height=can_height_female, backcan_width=data[4]+2*shieldthickness, backcan_height=backcan_height_unboxed, nut_diameter=0, nut_length=0, tags_additional=tags_additional, lib_name=lib_name, classname=classname, classname_description=classname_description, webpage=webpageunboxed, HighDensityOffsetMidLeft=data[8])
            