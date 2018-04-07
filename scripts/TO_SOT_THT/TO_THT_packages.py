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


class pack_round:
    #
    #
    #
    #
    #  |\    ~~~~~~~
    #  \ \/          \
    #   \               \
    #  /                 \
    #  |  PP1        PP   |
    #  \                 /
    #   \               /
    #     \    PP    /
    #        ~~~~~~~
    def __init__(self):
        self.diameter_inner = 0  # diameter of top can
        self.diameter_outer = 0  # diameter of bottom can
        self.mark_width=0 # width of marking
        self.mark_len=0 # length of marking
        self.pins = 0  # number of pins
        self.pin_circle_diameter = 0  # pin circle diameterdistance
        self.pin1_angle=0 # starting angle of first pin
        self.pin_dangle=90 # angle between two pins (in degrees)
        self.mark_angle=-45 # angular position of marking
        self.pad = [0, 0]  # width/height of pads
        self.drill = 0  # diameter of pad drills
        self.name = ""  # name of package
        self.tags = []  # description/keywords
        self.largepads =False
        self.fpnametags =[]
        self.window_diameter=0 # diameter of an on-top glass window
        self.used_pins=[] # if filled: the device may have up to self.pins pins, but only the given pin positions (0-based count) are actualy used
        self.more_packnames=[] # additional package names, e.g. "I2PAK" for TO-262
        self.webpage="";

    def __init__(self, name, pins=3, modifier="", largepads=False):
        self.diameter_inner = 0  # diameter of top can
        self.diameter_outer = 0  # diameter of bottom can
        self.mark_width = 0  # width of marking
        self.mark_len = 0  # length of marking
        self.pins = pins  # number of pins
        self.pin_circle_diameter = 0  # pin circle diameterdistance
        self.pin1_angle = 180  # starting angle of first pin
        self.mark_angle = -45  # angular position of marking
        self.pad = [0, 0]  # width/height of pads
        self.drill = 0  # diameter of pad drills
        self.name = ""  # name of package
        self.tags = []  # description/keywords
        self.largepads = largepads
        self.fpnametags = []
        self.window_diameter=0 # diameter of an on-top glass window
        self.pin_dangle = -90  # angle between two pins (in degrees)
        self.used_pins = []  # if filled: the device may have up to self.pins pins, but only the given pin positions (0-based count) are actualy used
        self.more_packnames = []  # additional package names, e.g. "I2PAK" for TO-262
        if pins == 2:
            self.pin_dangle = -180
        elif pins == 4:
            self.pin_dangle = -90
        elif pins >4:
            self.pin_dangle = -360/pins
        self.mark_angle = self.pin1_angle + 45  # angular position of marking
        self.name = name
        self.webpage="";

        if (name == "TO-18") or (name=="TO-46") or (name=="TO-52") or (name=="TO-72"):
            self.diameter_inner = 4.8  # diameter of top can
            self.diameter_outer = 5.8  # diameter of bottom can
            self.mark_width = 1.16  # width of marking
            self.mark_len = 1.17  # length of marking
            self.pin_circle_diameter = 2.54  # pin circle diameterdistance
            self.pad = [1.2,1.2]  # width/height of pads
            self.drill = 0.7  # diameter of pad drills
            self.name = self.name + "-{0}".format(pins)  # name of package
            if len(modifier)>0:
                self.name = self.name +"_"+modifier
                self.tags.append(modifier)
            if largepads:
                self.pad = [1.5, 1.5]  # width/height of pads

            if (modifier=="Window") or (modifier=="Lens"):
                self.window_diameter = 4  # diameter of an on-top glass window


        if (name == "TO-5") or (name == "TO-5_PD5.08") or (name == "TO-11") or (name == "TO-12") or (name == "TO-33") or (name == "TO-39") or (name == "TO-99") or (name == "TO-78") or (name == "TO-100") or (name == "TO-75"):
            self.diameter_inner = 8.5  # diameter of top can
            self.diameter_outer = 9.4  # diameter of bottom can
            self.mark_width = 0.86  # width of marking
            self.mark_len = 1.14  # length of marking
            self.pin_circle_diameter = 5.08  # pin circle diameterdistance
            if (pins==6):
                self.pins=8
                self.pin_dangle = -360 / self.pins
                self.used_pins=[0,1,2,4,5,6]
            elif (pins>6) and (name != "TO-5_PD5.08"):
                self.pin_circle_diameter = 5.84  # pin circle diameterdistance
            elif pins>8:
                self.mark_angle = self.pin1_angle + 36  # angular position of marking
            if (name == "TO-100"):
                self.pin_circle_diameter = 5.84  # pin circle diameterdistance
            self.pad = [1.2, 1.2]  # width/height of pads
            self.drill = 0.7  # diameter of pad drills
            if (name == "TO-5_PD5.08"):
                self.name = "TO-5" + "-{0}_PD5.08".format(pins)  # name of package
            else:
                self.name = self.name + "-{0}".format(pins)  # name of package
            if len(modifier) > 0:
                self.name = self.name + "_" + modifier
                self.tags.append(modifier)
            if largepads:
                self.pad = [1.5, 1.5]  # width/height of pads
            if (modifier == "Window") or (modifier == "Lens"):
                self.window_diameter = 5.9  # diameter of an on-top glass window



        if (name == "TO-8"):
            self.diameter_inner = 13.2  # diameter of top can
            self.diameter_outer = 14.4  # diameter of bottom can
            self.mark_width = 0.0  # width of marking
            self.mark_len = 0  # length of marking
            self.pin_circle_diameter = 7.1  # pin circle diameterdistance
            self.pad = [1.6, 1.6]  # width/height of pads
            self.drill = 1.1  # diameter of pad drills
            self.name = self.name + "-{0}".format(pins)  # name of package
            if len(modifier) > 0:
                self.name = self.name + "_" + modifier
                self.tags.append(modifier)
            if largepads:
                self.pad = [2, 2]  # width/height of pads
            if (modifier == "Window") or (modifier == "Lens"):
                self.window_diameter = 0.43*25.4  # diameter of an on-top glass window


        if (name == "TO-17"):
            self.diameter_inner = 4.2  # diameter of top can
            self.diameter_outer = 5.2  # diameter of bottom can
            self.mark_width = 0.76  # width of marking
            self.mark_len = 0.75  # length of marking
            self.pin_circle_diameter = 1.8  # pin circle diameterdistance
            self.pad = [0.9,0.9]  # width/height of pads
            self.drill = 0.6  # diameter of pad drills
            self.name = self.name + "-{0}".format(pins)  # name of package
            if len(modifier) > 0:
                self.name = self.name + "_" + modifier
                self.tags.append(modifier)
            if largepads:
                self.pad = [1.3, 1.3]  # width/height of pads
            if (modifier == "Window") or (modifier == "Lens"):
                self.window_diameter = 3.5  # diameter of an on-top glass window
        
        
        if (name == "TO-38"):
            self.diameter_inner = 12.3  # diameter of top can
            self.diameter_outer = 17.3  # diameter of bottom can
            self.mark_width = 0.0  # width of marking
            self.mark_len = 0.0  # length of marking
            self.pin_circle_diameter = 5.08  # pin circle diameterdistance
            self.pad = [1.3, 1.3]  # width/height of pads
            self.drill = 0.8  # diameter of pad drills
            self.name = self.name + "-{0}".format(pins)  # name of package
            if len(modifier) > 0:
                self.name = self.name + "_" + modifier
                self.tags.append(modifier)
            if largepads:
                self.pad = [1.6, 1.6]  # width/height of pads
            if (modifier == "Window") or (modifier == "Lens"):
                self.window_diameter = 8  # diameter of an on-top glass window
        

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
        self.largepads =False
        self.fpnametags =[]
        self.additional_pin_pad =[] # Position des Zusatz-SMD-Pads
        self.additional_pin_pad_size = [] # Größe des Zusatz-SMD-Pads
        self.plastic_angled=[]
        self.metal_angled = []
        self.staggered_type=0 # 0=no staggering, 1=type1-staggering (pin1=fron), 2=type2-staggering (pin1=back)
        self.staggered_rm=[5.08,5.08] # y-distance between pins [vertical, horizontal]
        self.staggered_pin_offset_z = 0 # z-offset of back-pins in staggered mode [vertical, horizontal]
        self.staggered_pin_minlength = 0  # y-offset of back-pins in staggered mode
        self.staggered_pad=[] # pad size in staggered mode
        self.rm_list = []
        self.more_packnames = []  # additional package names, e.g. "I2PAK" for TO-262
        self.webpage="";

    def __init__(self ,name ,pins=3 ,rm=0, staggered_type=0,largepads=False,pitchy=0,ypinoffset=0):
        self. additional_pin_pad =[] # Position des Zusatz-SMD-Pads
        self.additional_pin_pad_size = [] # Größe des Zusatz-SMD-Pads
        self.largepads =largepads
        self.fpnametags = []
        self.metal_offset_x = 0  # offset of metal from left
        self.plastic_angled = []
        self.metal_angled = []
        self.staggered_type=staggered_type
        self.staggering_rm=[5.08,2.54] # y-distance between pins
        self.staggered_pin_offset_z=0
        self.staggered_pin_minlength = 0 # y-offset of back-pins in staggered mode
        self.staggered_pad = []  # pad size in staggered mode
        self.addpinstext=True
        self.rm_list = []
        self.more_packnames = []  # additional package names, e.g. "I2PAK" for TO-262
        self.webpage="";

        if (name == "TO-218"):
            self.webpage="https://www.vishay.com/docs/95214/fto218.pdf"
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
            self.tags = ["SOT-93"]  # description/keywords
            #self.more_packnames.append("SOT-93")
            self.pin_offset_z = 3
            if largepads:
                self.pad = [3.5, 4.5]
                self.largepads = True

               
        elif (name == "TO-3P"):
            self.webpage="https://toshiba.semicon-storage.com/ap-en/design-support/package/detail.TO-3P(N).html"
            self.plastic = [15.5, 19.3, 4.5]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 20, 1.5]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.45  # pin distance
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 3.5]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.2  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.4  # diameter of mounting hole drill
            self.pin_minlength = 3.0  # min. elongation of pins before 90° bend
            self.pinw = [1.0, 0.6];  # width,height of pins
            self.tags = []
            self.metal_angled=[1.15,2]
            self.plastic_angled = [2.19, 3.5]
            self.tags = [""]  # description/keywords
            self.pin_offset_z = 3.0
            self.addpinstext=True
            if largepads:
                self.pad = [3.5, 5.5]
                self.largepads = True                
                
        elif (name == "TO-3PB"):
            self.webpage="http://www.onsemi.com/pub/Collateral/340AC.PDF"
            self.plastic = [15.6, 18.5, 4.8]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 20, 2]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.45  # pin distance
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 3.5]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.2  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.4  # diameter of mounting hole drill
            self.pin_minlength = 1.6  # min. elongation of pins before 90° bend
            self.pinw = [1.0, 0.6];  # width,height of pins
            self.tags = []
            self.metal_angled=[1.3,2.3]
            self.plastic_angled = [2.7, 4.7]
            self.tags = [""]  # description/keywords
            self.pin_offset_z = 1.7
            self.addpinstext=True
            if largepads:
                self.pad = [3.5, 5.5]
                self.largepads = True  
                
        elif (name == "TO-264"):
            self.webpage="https://www.fairchildsemi.com/package-drawings/TO/TO264A03.pdf"
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
            self.webpage="https://toshiba.semicon-storage.com/us/product/mosfet/to-247-4l.html"
            if (pins==5):
                self.webpage="http://ww1.microchip.com/downloads/en/DeviceDoc/20005685A.pdf"
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
            self.tags = []
            if (pins==4):
                self.rm_list = [5.08,2.54,2.54]
            self.pin_offset_z = self.plastic[2] - (2.4 + 0.3)
            if largepads:
                self.pad = [3.5, 5.5]
                self.largepads = True



        elif (name == "TO-220"):
            self.webpage="https://www.vishay.com/docs/66542/to-220-1.pdf"
            if (pins==2):
                self.webpage="https://www.centralsemi.com/PDFS/CASE/TO-220-2PD.PDF"
            #if (pins==4):
            #    self.webpage="https://www.centralsemi.com/PDFS/CASE/TO-220-2PD.PDF"
            if (pins==5):
                self.webpage="http://www.analog.com/media/en/package-pcb-resources/package/pkg_pdf/ltc-legacy-to-220/to-220_5_05-08-1421.pdf?domain=www.linear.com, http://www.analog.com/media/en/package-pcb-resources/package/pkg_pdf/ltc-legacy-to-220/to-220_5_05-08-1491.pdf, https://www.diodes.com/assets/Package-Files/TO220-5.pdf"
            self.plastic = [10, 9.25, 4.4]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 15.65, 1.27]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.54  # pin distance
            self.pad = [2,2]  # width/height of pads
            self.drill = 1.1  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.metal[1] - 2.8]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.7  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.5  # diameter of mounting hole drill
            self.pin_minlength = 3.81  # min. elongation of pins before 90° bend
            self.pinw = [0.75, 0.5];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 3.15
            self.staggered_rm = [3.7,3.8]# y-distance between pins
            self.staggered_pin_offset_z = 4.5  # z-offset of back-pins in staggered mode
            self.staggered_pin_minlength = 2.05  # y-offset of back-pins in staggered mode
            self.staggered_pad = [1.8, 1.8]  # width/height of pads
            if pins == 5:
                self.tags.append("Pentawatt")
                self.tags.append("Multiwatt-5")
                #self.more_packnames.append("Pentawatt")
                #self.more_packnames.append("Multiwatt-5")
                self.staggered_pin_minlength = 2.05+1.28  # y-offset of back-pins in staggered mode
                self.rm = 1.7
                self.pad = [1.3, 1.8]
            if pins == 9:
                self.pinw = [0.5, 0.38];
                self.drill = 0.7
                self.pad = [1.3, 1.3]
                self.staggered_pad = [1.5, 1.5]  # width/height of pads
            if pins >5:
                self.tags.append("Multiwatt-{0}".format(pins))
                #self.more_packnames.append("Multiwatt-{0}".format(pins))
            if pins>9:
                if pins==11:
                    self.webpage="http://www.st.com/resource/en/datasheet/tda7391lv.pdf"
                if pins==15:
                    self.webpage="https://www.sparkfun.com/datasheets/Robotics/L298_H_Bridge.pdf"
                self.plastic = [20.2, 10.7, 5]  # width,heigth,depth of plastic package, starting at bottom-left
                self.metal = [self.plastic[0], 17.5,1.6]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
                self.metal_angled = [2.25,2.25]
                self.pins = 15  # number of pins
                self.rm = 1.3  # pin distance
                self.pad = [1.8, 1.8]  # width/height of pads
                self.drill = 1  # diameter of pad drills
                self.name = name+"-{0}".format(pins)  # name of package
                self.addpinstext=False
                self.mounting_hole_pos = [self.plastic[0] / 2, 17.5-2.8]  # position of mounting hole from bottom-left
                self.mounting_hole_diameter = 3.7  # diameter of mounting hole in package
                self.mounting_hole_drill = 3.5  # diameter of mounting hole drill
                self.pin_minlength = 3.81  # min. elongation of pins before 90° bend
                self.pinw = [0.7, 0.5];  # width,height of pins
                self.tags = []  # description/keywords
                self.pin_offset_z = 4.55 
                self.staggered_rm = [5.08,2.54]  # y-distance between pins
                self.staggered_pin_offset_z = 4.5  # z-offset of back-pins in staggered mode
                self.staggered_pin_minlength= 3.3  # y-offset of back-pins in staggered mode
                self.staggered_pad = [1.8, 1.8]  # width/height of pads            if largepads:
            if largepads:
                self.tags.append("large pads")
                self.pad = [2, 3.5]
                self.largepads = True

        elif (name == "TO-220F"):
            self.webpage="http://www.st.com/resource/en/datasheet/stp20nm60.pdf"
            if pins==4:
                self.webpage="https://www.njr.com/semicon/PDF/package/TO-220F-4_E.pdf"
            self.plastic = [10.26, 15.87-6.68, 4.7]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 15.87, 2.52]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.54  # pin distance
            self.pad = [2, 2]  # width/height of pads
            self.drill = 1.2  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.metal[1] - 3.3]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.7  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.5  # diameter of mounting hole drill
            self.pin_minlength = 3.23  # min. elongation of pins before 90° bend
            self.pinw = [0.6, 0.7];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 2.76+0.575/2
            self.staggered_rm = [3.7,3.8]# y-distance between pins
            self.staggered_pin_offset_z = 4.5  # z-offset of back-pins in staggered mode
            self.staggered_pin_minlength = 2.05  # y-offset of back-pins in staggered mode
            self.staggered_pad = [1.8, 1.8]  # width/height of pads
            if pins == 5:
                self.tags.append("PentawattF-")
                self.tags.append("MultiwattF-5")
                #self.more_packnames.append("Pentawatt")
                #self.more_packnames.append("Multiwatt-5")
                self.staggered_pin_minlength = 2.05+1.28  # y-offset of back-pins in staggered mode
                self.rm = 1.7
                self.pad = [1.3, 1.8]
            if pins == 9:
                self.pinw = [0.5, 0.38];
                self.drill = 0.7
                self.pad = [1.3, 1.3]
                self.staggered_pad = [1.5, 1.5]  # width/height of pads
            if pins >9:
                if pins==11:
                    self.webpage="http://www.ti.com/lit/ds/symlink/lm3886.pdf"
                self.plastic = [20.02, 10.64, 4.5]  # width,heigth,depth of plastic package, starting at bottom-left
                self.metal = [self.plastic[0], 19.58,3.3]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
                self.metal_angled = [2.84,2.84]
                self.pins = pins  # number of pins
                self.rm = 1.7  # pin distance
                self.pad = [1.8, 1.8]  # width/height of pads
                self.drill = 1  # diameter of pad drills
                self.name = name+"-{0}".format(pins)  # name of package
                self.addpinstext=False
                self.mounting_hole_pos = [self.plastic[0] / 2, 17.5-2.8]  # position of mounting hole from bottom-left
                self.mounting_hole_diameter = 3.7  # diameter of mounting hole in package
                self.mounting_hole_drill = 3.5  # diameter of mounting hole drill
                self.pin_minlength = 3.81  # min. elongation of pins before 90° bend
                self.pinw = [0.7, 0.5];  # width,height of pins
                self.tags = []  # description/keywords
                self.pin_offset_z = 4.29
                self.staggered_rm = [5.08,2.54]  # y-distance between pins
                self.staggered_pin_offset_z = 4.5  # z-offset of back-pins in staggered mode
                self.staggered_pin_minlength= 3.3  # y-offset of back-pins in staggered mode
                self.staggered_pad = [1.8, 1.8]  # width/height of pads
                self.tags.append("MultiwattF-{0}".format(pins))
                #self.more_packnames.append("Multiwatt-{0}".format(pins))
            if largepads:
                self.tags.append("large pads")
                self.pad = [2, 3.5]
                self.largepads = True
                
                
        elif (name == "Multiwatt"):
            self.plastic = [20.2, 10.7, 5]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 17.5,1.6]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.metal_angled = [2.25,2.25]
            self.pins = 15  # number of pins
            self.rm = 1.3  # pin distance
            self.pad = [1.8, 1.8]  # width/height of pads
            self.drill = 1  # diameter of pad drills
            self.name = name+"-{0}".format(pins)  # name of package
            self.addpinstext=False
            self.mounting_hole_pos = [self.plastic[0] / 2, 17.5-2.8]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.7  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.5  # diameter of mounting hole drill
            self.pin_minlength = 3.81  # min. elongation of pins before 90° bend
            self.pinw = [0.7, 0.5];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 4.55
            self.staggered_rm = [5.08,2.54]  # y-distance between pins
            self.staggered_pin_offset_z = 4.5  # z-offset of back-pins in staggered mode
            self.staggered_pin_minlength= 3.3  # y-offset of back-pins in staggered mode
            self.staggered_pad = [1.8, 1.8]  # width/height of pads
            if pins == 5:
                self.tags.append("Pentawatt")
                self.more_packnames.append("Pentawatt")
            if pins != 5:
                self.tags.append("Multiwatt-{0}".format(pins))
            if largepads:
                self.tags.append("large pads")
                self.pad = [2, 3.5]
                self.largepads = True
    
        elif (name == "TO-126"):
            self.webpage="https://www.diodes.com/assets/Package-Files/TO126.pdf"
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
            self.webpage="https://www.diodes.com/assets/Package-Files/TO251.pdf"
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
            self.tags = ["IPAK"]  # description/keywords
            #self.more_packnames.append("IPAK")
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

        elif (name == "SIPAK"):
            self.plastic = [6.6, 6.4, 2.3]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [5.33, 7.12, 0.4]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.286  # pin distance
            self.pad = [1.8, 1.8]  # width/height of pads
            self.drill = 1.1  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 3.9]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 0  # diameter of mounting hole in package
            self.mounting_hole_drill = 0  # diameter of mounting hole drill
            self.pin_minlength = 1.02  # min. elongation of pins before 90° bend
            self.pinw = [0.9, 0.5];  # width,height of pins
            self.tags = []   # description/keywords
            self.pin_offset_z = 1.17+0.25
            self.addpinstext=False
            self.additional_pin_pad_size = [5.5, 6.2]  # Größe des Zusatz-SMD-Pads
            self.metal_offset_x = (self.plastic[0] - self.metal[0]) / 2  # offset of metal from left
            if largepads:
                self.tags.append("large pads")
                self.pad = [1.8, 1.8]
                self.additional_pin_pad_size = [6.3, 6.5]  # Größe des Zusatz-SMD-Pads
                self.largepads = True
            self.additional_pin_pad = [self.plastic[0] / 2, self.metal[1] - self.additional_pin_pad_size[
                1] / 3]  # Position des Zusatz-SMD-Pads


        elif (name == "TO-262"):
            self.webpage="https://www.diodes.com/assets/Package-Files/TO262.pdf"
            self.plastic = [10, 9.25, 4.4]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [9.8, 9.75, 1.27]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.54  # pin distance
            self.pad = [2.2, 2.2]  # width/height of pads
            self.drill = 1.2  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2,
                                      self.plastic[1] - 3.9]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 0  # diameter of mounting hole in package
            self.mounting_hole_drill = 0  # diameter of mounting hole drill
            self.pin_minlength = 13.5-4.55  # min. elongation of pins before 90° bend
            self.pinw = [1.05, 0.5];  # width,height of pins
            self.tags = ["IIPAK", "I2PAK", "I²PAK"]  # description/keywords
            #self.more_packnames.append("I2PAK")
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
            print("DID NOT FIND '", name,"'")
            self.__init__()
        
        if rm > 0:
            self.rm = rm
        if self.addpinstext:
            self.name = "{0}-{1}".format(self.name, pins)
        if pins != 3:
            self.pins = pins
            if rm <= 0:
                self.rm = 2 * self.rm / (pins - 1)
            else:
                self.rm = rm;
        self.pin_offset_x = (self.plastic[0] - (self.pins - 1) * self.rm) / 2
        if len(self.rm_list)>0:
            pl=0
            for rm in self.rm_list:
                pl=pl+rm
            self.pin_offset_x = (self.plastic[0] - pl) / 2
        self.pad[0] = min(self.pad[0], 0.75 * self.rm)
        if self.largepads:
            self.tags.append("large pads")
        if self.staggered_type==1:
            self.tags.append("staggered type-1")
            self.fpnametags=["StaggeredType1"]+self.fpnametags
        if self.staggered_type==2:
            self.tags.append("staggered type-2")
            self.fpnametags=["StaggeredType2"] + self.fpnametags
            
        if pitchy>0:
            self.staggered_rm = [pitchy,pitchy]  # y-distance between pins

        if ypinoffset!=0:
            self.pin_offset_z = ypinoffset

crt_offset = 0.25
slk_offset = 0.12
slk_dist = 0.15
lw_fab = 0.1
lw_crt = 0.05
lw_slk = 0.12
txt_offset = 1