#!/usr/bin/env python

import sys
import os
import math
import time

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path

from KicadModTree import *  # NOQA
from tools import *


class pack:
    #      metal_/plastic_                                        ^
    #  <--------width------>                                      |
    #  +-------------------+                 ^                    y
    #  |                   |                 |                    x---->
    #  |        OO         | mounting drill  |
    #  |                   |                 |
    #  |   METAL           |                 |
    #  +-------------------+ ^               metal_height
    #  |                   | |               |
    #  |                   | |               |
    #  |   PLASTIC         | plastic_height  |
    #  |                   | |               |
    #  |                   | |               |
    #  |                   | |               |
    #  0-------------------+ v  0= ref pos   v
    #     |      |      |  ^
    #     |      |      |  |
    #     |      |      |  pin_minlength
    #     |      |      |  |
    #     |      |      |  v
    #    PPP    PPP    PPP      PADs
    #     <--rm-->
    #   <->
    #    pin_offset_x
    #
    #  0-------------------+  0= ref pos    ^             ^                z
    #  |   METAL           |                metal_depth   |                |
    #  +-------------------+ ^              v             pin_offset_z     |
    #  |   PLASTIC         | plastic_depth                |                v
    #  | PPP    PPP    PPP | |                            v
    #  +-------------------+ v
    #
    def __init__(self):
        self.plastic = [0, 0, 0]  # width,heigth,depth of plastic package, starting at bottom-left
        self.metal = [0, 0, 0]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
        self. metal_offset_x =0 # offset of metal from left
        self.pins = 0  # number of pins
        self.rm = 0  # pin distance
        self.pad = [0, 0]  # width/height of pads
        self.drill = 0  # diameter of pad drills
        self.name = ""  # name of package
        self.mounting_hole_pos = [0, 0]  # position of mounting hole from bottom-left
        self.mounting_hole_diameter = 0  # diameter of mounting hole in package
        self.mounting_hole_drill = 0  # diameter of mounting hole drill
        self.pin_minlength = 0  # min. elongation of pins before 90° bend
        self.pinw = [0, 0];  # width,height of pins
        self.tags = []  # description/keywords
        self.pin_offset_x = 0
        self.pin_offset_z = 0
        self. largepads =False
        self. fpnametags =[]
        self. additional_pin_pad =[] # Position des Zusatz-SMD-Pads
        self.additional_pin_pad_size = [] # Größe des Zusatz-SMD-Pads
        self.plastic_angled=[]
    
    def __init__(self ,name ,pins=3 ,rm=0 ,largepads=False):
        self. additional_pin_pad =[] # Position des Zusatz-SMD-Pads
        self.additional_pin_pad_size = [] # Größe des Zusatz-SMD-Pads
        self.largepads =largepads
        self.fpnametags = []
        self.metal_offset_x = 0  # offset of metal from left
        self.plastic_angled = []
        if (name == "SOT93"):
            self.plastic = [15.2, 12.7, 4.6]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [15.2, 21,
                          2]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.5  # pin distance
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [15.2 / 2, 21 - 4.4]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 4.25  # diameter of mounting hole in package
            self.mounting_hole_drill = 4  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1.15, 0.4];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 4.6 - 1.6 + 0.2
            if largepads:
                self.pad = [3.5, 5.5]
                self.largepads = True
        elif (name == "TO-264"):
            self.plastic = [20, 26, 5]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 0,
                          2]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.45  # pin distance
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 6]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.3  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.3  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1, 0.6];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = self.plastic[2] - (2.8 + 0.3)
            if largepads:
                self.pad = [3.5, 5.5]
                self.largepads = True
                
        elif (name == "TO-247"):
            self.plastic = [15.9, 20.95, 5.03]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [0, 0,
                          0]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.45  # pin distance
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 6.17]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.61  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.6  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1.2, 0.6];  # width,height of pins
            self.tags = ["TO-3P"]  # description/keywords
            self.fpnametags.append("TO-3P")
            self.pin_offset_z = self.plastic[2] - (2.4 + 0.3)
            if largepads:
                self.pad = [3.5, 5.5]
                self.largepads = True

        elif (name == "TO-280"):
            self.plastic = [16.6, 18.75, 5]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [8.5, 19.25,
                          0.5]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.45  # pin distance
            self.pad = [2.7, 4.5]  # width/height of pads
            self.drill = 1.7  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      14.8]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.61  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.6  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1.2, 0.5];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 2.5+0.25
            self.plastic_angled = [18.75-13.81,18.75-13.81]
            self.metal_offset_x = (self.plastic[0] - self.metal[0]) / 2  # offset of metal from left
            if largepads:
                self.pad = [3.7, 5.5]
                self.largepads = True
        elif (name == "TO-218"):
            self.plastic = [15.92, 12.7, 5.08]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 20.72,
                          1.27]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.47  # pin distance
            self.pad = [2.5, 3.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [15.2 / 2, 16.2]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 4.23  # diameter of mounting hole in package
            self.mounting_hole_drill = 4  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1.15, 0.4];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 3
            if largepads:
                self.pad = [3.5, 4.5]
                self.largepads = True
        elif (name == "TO-220"):
            self.plastic = [10, 9.25, 4.4]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 15.65,
                          1.27]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.54  # pin distance
            self.pad = [1.8, 1.8]  # width/height of pads
            self.drill = 1  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.metal[1] - 2.8]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.7  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.5  # diameter of mounting hole drill
            self.pin_minlength = 3.81  # min. elongation of pins before 90° bend
            self.pinw = [0.75, 0.5];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 2.5
            if pins == 5:
                self.tags.append("Pentawatt")
                self.fpnametags.append("Pentawatt")
                self.fpnametags.append("Multiwatt-5")
            if pins >5:
                self.tags.append("Multiwatt")
                self.fpnametags.append("Multiwatt-"+pins.str())
            if largepads:
                self.tags.append("large pads")
                self.pad = [2, 3.5]
                self.largepads = True
        elif (name == "TO-126"):
            self.plastic = [8, 11, 3.25]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [0, 0, 0]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.54  # pin distance
            self.pad = [1.8, 1.8]  # width/height of pads
            self.drill = 1  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 3.9]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.2  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.2  # diameter of mounting hole drill
            self.pin_minlength = 4  # min. elongation of pins before 90° bend
            self.pinw = [0.75, 0.5];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 2
            if largepads:
                self.tags.append("large pads")
                self.pad = [2.0, 2.3]
                self.largepads = True

        elif (name == "TO-251"):
            self.plastic = [6.5, 5.5, 2.3]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [5, 7, 0.5]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.3  # pin distance
            self.pad = [1.4, 1.4]  # width/height of pads
            self.drill = 0.8  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 3.9]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 0  # diameter of mounting hole in package
            self.mounting_hole_drill = 0  # diameter of mounting hole drill
            self.pin_minlength = 2  # min. elongation of pins before 90° bend
            self.pinw = [0.5, 0.5];  # width,height of pins
            self.tags = ["IIAK"]  # description/keywords
            self.fpnametags.append("IPAK")
            self.pin_offset_z = 1
            self.additional_pin_pad_size = [5.7, 6.2]  # Größe des Zusatz-SMD-Pads
            self.metal_offset_x = (self.plastic[0] - self.metal[0]) / 2  # offset of metal from left
            if largepads:
                self.tags.append("large pads")
                self.pad = [1.8, 1.8]
                self.additional_pin_pad_size = [6.3, 6.5]  # Größe des Zusatz-SMD-Pads
                self.largepads = True
            self.additional_pin_pad = [self.plastic[0] / 2, self.metal[1] - self.additional_pin_pad_size[
                1] / 3]  # Position des Zusatz-SMD-Pads

        elif (name == "SIPAC"):
            self.plastic = [6.6, 6.1, 2.3]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [5.33, 7.12, 0.53]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.286  # pin distance
            self.pad = [1.6, 1.6]  # width/height of pads
            self.drill = 1  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 3.9]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 0  # diameter of mounting hole in package
            self.mounting_hole_drill = 0  # diameter of mounting hole drill
            self.pin_minlength = 1.5  # min. elongation of pins before 90° bend
            self.pinw = [0.78, 0.5];  # width,height of pins
            self.tags = ["IIAK"]  # description/keywords
            self.fpnametags.append("IPAK")
            self.pin_offset_z = 1.07+0.23
            self.additional_pin_pad_size = [6, 6]  # Größe des Zusatz-SMD-Pads
            self.metal_offset_x = (self.plastic[0] - self.metal[0]) / 2  # offset of metal from left
            if largepads:
                self.tags.append("large pads")
                self.pad = [1.8, 1.8]
                self.additional_pin_pad_size = [6.3, 6.6]  # Größe des Zusatz-SMD-Pads
                self.largepads = True
            self.additional_pin_pad = [self.plastic[0] / 2, self.metal[1] - self.additional_pin_pad_size[
                1] / 3]  # Position des Zusatz-SMD-Pads

        elif (name == "TO-262"):
            self.plastic = [10, 9.25, 4.4]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [9.8, 9.75, 1.27]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.54  # pin distance
            self.pad = [1.8, 1.8]  # width/height of pads
            self.drill = 1.2  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 3.9]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 0  # diameter of mounting hole in package
            self.mounting_hole_drill = 0  # diameter of mounting hole drill
            self.pin_minlength = 13.5-4.55  # min. elongation of pins before 90° bend
            self.pinw = [1.05, 0.5];  # width,height of pins
            self.tags = ["IIPAK", "I2PAK", "I²PAK"]  # description/keywords
            self.fpnametags.append("I2PAK")
            self.pin_offset_z = 2.4+0.25
            self.additional_pin_pad_size = [10, 8]  # Größe des Zusatz-SMD-Pads
            self.metal_offset_x = (self.plastic[0] - self.metal[0]) / 2  # offset of metal from left
            if largepads:
                self.tags.append("large pads")
                self.pad = [1.8, 1.8]
                self.additional_pin_pad_size = [6.3, 6.5]  # Größe des Zusatz-SMD-Pads
                self.largepads = True
            self.additional_pin_pad = [self.plastic[0] / 2, self.metal[1] - self.additional_pin_pad_size[
                1] / 3]  # Position des Zusatz-SMD-Pads
        else:
            __init__()
        
        if rm > 0:
            self.rm = rm
        if pins != 3:
            self.name = "{0}-{1}pin".format(self.name, pins)
            self.pins = pins
            if rm <= 0:
                self.rm = 2 * self.rm / (pins - 1)
            else:
                self.rm = rm;
        self.pin_offset_x = (self.plastic[0] - (self.pins - 1) * self.rm) / 2
        self.pad[0] = min(self.pad[0], 0.75 * self.rm)
        if self.largepads:
            self.tags.append("large pads")


crt_offset = 0.25
slk_offset = 0.2
slk_dist = 0.25
lw_fab = 0.1
lw_crt = 0.05
lw_slk = 0.15
txt_offset = 1