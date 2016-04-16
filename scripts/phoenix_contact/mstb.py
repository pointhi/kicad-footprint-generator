#!/usr/bin/env python

import sys
import os
from collections import namedtuple
sys.path.append(os.path.join(sys.path[0],"..","..")) # load KicadModTree path
from KicadModTree import *
# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf


def v_add(p1,p2):
    return [p1[0]+p2[0],p1[1]+p2[1]]

lib_name="Connectors_Phoenix"
out_dir=lib_name+".pretty"+os.sep
packages_3d=lib_name+".3dshapes"+os.sep

Params = namedtuple("Params",[
    'series_name',
    'file_name',
    'angled',
    'flanged',
    'num_pins',
    'pin_pitch',
    'mount_hole',
    'order_info'
])

def generate_params(num_pins, series_name, pin_pitch, angled, flanged, order_info, mount_hole=False):
    return Params(
        series_name=series_name,
        file_name="PhonixContact_" + series_name + "_01x" + ('%02d' % num_pins) + "_"\
        + ('%.2f' % pin_pitch) + "mm_" + ('Angled' if angled else 'Vertical')\
        + ('_ThreadedFlange' + ('_MountHole' if mount_hole else '') if flanged else ''),
        angled=angled,
        flanged=flanged,
        num_pins=num_pins,
        pin_pitch=pin_pitch,
        mount_hole=mount_hole,
        order_info=order_info
    )


all_params = {
    'MSTBA_01x02_5.00mm' : generate_params( 2, "MSTBA", 5.0, True, False, {'1757475':'12A', '1923759':'16A (HC)'}),
    'MSTBA_01x03_5.00mm' : generate_params( 3, "MSTBA", 5.0, True, False, {'1757488':'12A', '1923762':'16A (HC)'}),
    'MSTBA_01x04_5.00mm' : generate_params( 4, "MSTBA", 5.0, True, False, {'1757491':'12A', '1923775':'16A (HC)'}),
    'MSTBA_01x05_5.00mm' : generate_params( 5, "MSTBA", 5.0, True, False, {'1757501':'12A', '1923788':'16A (HC)'}),
    'MSTBA_01x06_5.00mm' : generate_params( 6, "MSTBA", 5.0, True, False, {'1757514':'12A', '1923791':'16A (HC)'}),
    'MSTBA_01x07_5.00mm' : generate_params( 7, "MSTBA", 5.0, True, False, {'1757493':'12A', '1923801':'16A (HC)'}),
    'MSTBA_01x08_5.00mm' : generate_params( 8, "MSTBA", 5.0, True, False, {'1757527':'12A', '1923814':'16A (HC)'}),
    'MSTBA_01x09_5.00mm' : generate_params( 9, "MSTBA", 5.0, True, False, {'1757530':'12A', '1923827':'16A (HC)'}),
    'MSTBA_01x10_5.00mm' : generate_params(10, "MSTBA", 5.0, True, False, {'1757543':'12A', '1923830':'16A (HC)'}),
    'MSTBA_01x11_5.00mm' : generate_params(11, "MSTBA", 5.0, True, False, {'1757556':'12A', '1923843':'16A (HC)'}),
    'MSTBA_01x12_5.00mm' : generate_params(12, "MSTBA", 5.0, True, False, {'1757569':'12A', '1923856':'16A (HC)'}),
    'MSTBA_01x13_5.00mm' : generate_params(13, "MSTBA", 5.0, True, False, {'1757572':'12A'}),
    'MSTBA_01x14_5.00mm' : generate_params(14, "MSTBA", 5.0, True, False, {'1757585':'12A'}),
    'MSTBA_01x15_5.00mm' : generate_params(15, "MSTBA", 5.0, True, False, {'1757598':'12A'}),
    'MSTBA_01x16_5.00mm' : generate_params(16, "MSTBA", 5.0, True, False, {'1757608':'12A'}),
    'MSTB_01x02_5.00mm' : generate_params( 2, "MSTB", 5.0, True, True, {'1776692':'12A', '1923979':'16A (HC)'}),
    'MSTB_01x03_5.00mm' : generate_params( 3, "MSTB", 5.0, True, True, {'1776702':'12A', '1923982':'16A (HC)'}),
    'MSTB_01x04_5.00mm' : generate_params( 4, "MSTB", 5.0, True, True, {'1776715':'12A', '1923995':'16A (HC)'}),
    'MSTB_01x05_5.00mm' : generate_params( 5, "MSTB", 5.0, True, True, {'1776728':'12A', '1924004':'16A (HC)'}),
    'MSTB_01x06_5.00mm' : generate_params( 6, "MSTB", 5.0, True, True, {'1776731':'12A', '1924017':'16A (HC)'}),
    'MSTB_01x07_5.00mm' : generate_params( 7, "MSTB", 5.0, True, True, {'1776744':'12A', '1924020':'16A (HC)'}),
    'MSTB_01x08_5.00mm' : generate_params( 8, "MSTB", 5.0, True, True, {'1776757':'12A', '1924033':'16A (HC)'}),
    'MSTB_01x09_5.00mm' : generate_params( 9, "MSTB", 5.0, True, True, {'1776760':'12A', '1924046':'16A (HC)'}),
    'MSTB_01x10_5.00mm' : generate_params(10, "MSTB", 5.0, True, True, {'1776773':'12A', '1924059':'16A (HC)'}),
    'MSTB_01x11_5.00mm' : generate_params(11, "MSTB", 5.0, True, True, {'1776786':'12A', '1924062':'16A (HC)'}),
    'MSTB_01x12_5.00mm' : generate_params(12, "MSTB", 5.0, True, True, {'1776799':'12A', '1924075':'16A (HC)'}),
    'MSTB_01x13_5.00mm' : generate_params(13, "MSTB", 5.0, True, True, {'1776809':'12A'}),
    'MSTB_01x14_5.00mm' : generate_params(14, "MSTB", 5.0, True, True, {'1776812':'12A'}),
    'MSTB_01x15_5.00mm' : generate_params(15, "MSTB", 5.0, True, True, {'1776825':'12A'}),
    'MSTB_01x16_5.00mm' : generate_params(16, "MSTB", 5.0, True, True, {'1776838':'12A'}),
    'MSTB_01x02_5.00mm_MH' : generate_params( 2, "MSTB", 5.0, True, True, {'1776692':'12A', '1923979':'16A (HC)'}, mount_hole=True),
    'MSTB_01x03_5.00mm_MH' : generate_params( 3, "MSTB", 5.0, True, True, {'1776702':'12A', '1923982':'16A (HC)'}, mount_hole=True),
    'MSTB_01x04_5.00mm_MH' : generate_params( 4, "MSTB", 5.0, True, True, {'1776715':'12A', '1923995':'16A (HC)'}, mount_hole=True),
    'MSTB_01x05_5.00mm_MH' : generate_params( 5, "MSTB", 5.0, True, True, {'1776728':'12A', '1924004':'16A (HC)'}, mount_hole=True),
    'MSTB_01x06_5.00mm_MH' : generate_params( 6, "MSTB", 5.0, True, True, {'1776731':'12A', '1924017':'16A (HC)'}, mount_hole=True),
    'MSTB_01x07_5.00mm_MH' : generate_params( 7, "MSTB", 5.0, True, True, {'1776744':'12A', '1924020':'16A (HC)'}, mount_hole=True),
    'MSTB_01x08_5.00mm_MH' : generate_params( 8, "MSTB", 5.0, True, True, {'1776757':'12A', '1924033':'16A (HC)'}, mount_hole=True),
    'MSTB_01x09_5.00mm_MH' : generate_params( 9, "MSTB", 5.0, True, True, {'1776760':'12A', '1924046':'16A (HC)'}, mount_hole=True),
    'MSTB_01x10_5.00mm_MH' : generate_params(10, "MSTB", 5.0, True, True, {'1776773':'12A', '1924059':'16A (HC)'}, mount_hole=True),
    'MSTB_01x11_5.00mm_MH' : generate_params(11, "MSTB", 5.0, True, True, {'1776786':'12A', '1924062':'16A (HC)'}, mount_hole=True),
    'MSTB_01x12_5.00mm_MH' : generate_params(12, "MSTB", 5.0, True, True, {'1776799':'12A', '1924075':'16A (HC)'}, mount_hole=True),
    'MSTB_01x13_5.00mm_MH' : generate_params(13, "MSTB", 5.0, True, True, {'1776809':'12A'}, mount_hole=True),
    'MSTB_01x14_5.00mm_MH' : generate_params(14, "MSTB", 5.0, True, True, {'1776812':'12A'}, mount_hole=True),
    'MSTB_01x15_5.00mm_MH' : generate_params(15, "MSTB", 5.0, True, True, {'1776825':'12A'}, mount_hole=True),
    'MSTB_01x16_5.00mm_MH' : generate_params(16, "MSTB", 5.0, True, True, {'1776838':'12A'}, mount_hole=True),
    'MSTBVA_01x02_5.00mm' : generate_params( 2, "MSTBVA", 5.0, False, False, {'1755516':'12A', '1924198':'16A (HC)'}),
    'MSTBVA_01x03_5.00mm' : generate_params( 3, "MSTBVA", 5.0, False, False, {'1755529':'12A', '1924208':'16A (HC)'}),
    'MSTBVA_01x04_5.00mm' : generate_params( 4, "MSTBVA", 5.0, False, False, {'1755532':'12A', '1924211':'16A (HC)'}),
    'MSTBVA_01x05_5.00mm' : generate_params( 5, "MSTBVA", 5.0, False, False, {'1755545':'12A', '1924224':'16A (HC)'}),
    'MSTBVA_01x06_5.00mm' : generate_params( 6, "MSTBVA", 5.0, False, False, {'1755558':'12A', '1924237':'16A (HC)'}),
    'MSTBVA_01x07_5.00mm' : generate_params( 7, "MSTBVA", 5.0, False, False, {'1755561':'12A', '1924240':'16A (HC)'}),
    'MSTBVA_01x08_5.00mm' : generate_params( 8, "MSTBVA", 5.0, False, False, {'1755574':'12A', '1924253':'16A (HC)'}),
    'MSTBVA_01x09_5.00mm' : generate_params( 9, "MSTBVA", 5.0, False, False, {'1755587':'12A', '1924266':'16A (HC)'}),
    'MSTBVA_01x10_5.00mm' : generate_params(10, "MSTBVA", 5.0, False, False, {'1755503':'12A', '1924279':'16A (HC)'}),
    'MSTBVA_01x11_5.00mm' : generate_params(11, "MSTBVA", 5.0, False, False, {'1755590':'12A', '1924282':'16A (HC)'}),
    'MSTBVA_01x12_5.00mm' : generate_params(12, "MSTBVA", 5.0, False, False, {'1755600':'12A', '1924295':'16A (HC)'}),
    'MSTBVA_01x13_5.00mm' : generate_params(13, "MSTBVA", 5.0, False, False, {'1755613':'12A'}),
    'MSTBVA_01x14_5.00mm' : generate_params(14, "MSTBVA", 5.0, False, False, {'1755626':'12A'}),
    'MSTBVA_01x15_5.00mm' : generate_params(15, "MSTBVA", 5.0, False, False, {'1755639':'12A'}),
    'MSTBVA_01x16_5.00mm' : generate_params(16, "MSTBVA", 5.0, False, False, {'1755642':'12A'}),
    'MSTBV_01x02_5.00mm' : generate_params( 2, "MSTBV", 5.0, False, True, {'1776883':'12A', '1924415':'16A (HC)'}),
    'MSTBV_01x03_5.00mm' : generate_params( 3, "MSTBV", 5.0, False, True, {'1776896':'12A', '1924428':'16A (HC)'}),
    'MSTBV_01x04_5.00mm' : generate_params( 4, "MSTBV", 5.0, False, True, {'1776906':'12A', '1924431':'16A (HC)'}),
    'MSTBV_01x05_5.00mm' : generate_params( 5, "MSTBV", 5.0, False, True, {'1776919':'12A', '1924444':'16A (HC)'}),
    'MSTBV_01x06_5.00mm' : generate_params( 6, "MSTBV", 5.0, False, True, {'1776922':'12A', '1924457':'16A (HC)'}),
    'MSTBV_01x07_5.00mm' : generate_params( 7, "MSTBV", 5.0, False, True, {'1776935':'12A', '1924460':'16A (HC)'}),
    'MSTBV_01x08_5.00mm' : generate_params( 8, "MSTBV", 5.0, False, True, {'1776948':'12A', '1924473':'16A (HC)'}),
    'MSTBV_01x09_5.00mm' : generate_params( 9, "MSTBV", 5.0, False, True, {'1776951':'12A', '1924486':'16A (HC)'}),
    'MSTBV_01x10_5.00mm' : generate_params(10, "MSTBV", 5.0, False, True, {'1776964':'12A', '1924499':'16A (HC)'}),
    'MSTBV_01x11_5.00mm' : generate_params(11, "MSTBV", 5.0, False, True, {'1776977':'12A', '1924509':'16A (HC)'}),
    'MSTBV_01x12_5.00mm' : generate_params(12, "MSTBV", 5.0, False, True, {'1776980':'12A', '1924512':'16A (HC)'}),
    'MSTBV_01x13_5.00mm' : generate_params(13, "MSTBV", 5.0, False, True, {'1776993':'12A'}),
    'MSTBV_01x14_5.00mm' : generate_params(14, "MSTBV", 5.0, False, True, {'1776002':'12A'}),
    'MSTBV_01x15_5.00mm' : generate_params(15, "MSTBV", 5.0, False, True, {'1776015':'12A'}),
    'MSTBV_01x16_5.00mm' : generate_params(16, "MSTBV", 5.0, False, True, {'1776028':'12A'}),
    'MSTBV_01x02_5.00mm_MH' : generate_params( 2, "MSTBV", 5.0, False, True, {'1776883':'12A', '1924415':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x03_5.00mm_MH' : generate_params( 3, "MSTBV", 5.0, False, True, {'1776896':'12A', '1924428':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x04_5.00mm_MH' : generate_params( 4, "MSTBV", 5.0, False, True, {'1776906':'12A', '1924431':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x05_5.00mm_MH' : generate_params( 5, "MSTBV", 5.0, False, True, {'1776919':'12A', '1924444':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x06_5.00mm_MH' : generate_params( 6, "MSTBV", 5.0, False, True, {'1776922':'12A', '1924457':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x07_5.00mm_MH' : generate_params( 7, "MSTBV", 5.0, False, True, {'1776935':'12A', '1924460':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x08_5.00mm_MH' : generate_params( 8, "MSTBV", 5.0, False, True, {'1776948':'12A', '1924473':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x09_5.00mm_MH' : generate_params( 9, "MSTBV", 5.0, False, True, {'1776951':'12A', '1924486':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x10_5.00mm_MH' : generate_params(10, "MSTBV", 5.0, False, True, {'1776964':'12A', '1924499':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x11_5.00mm_MH' : generate_params(11, "MSTBV", 5.0, False, True, {'1776977':'12A', '1924509':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x12_5.00mm_MH' : generate_params(12, "MSTBV", 5.0, False, True, {'1776980':'12A', '1924512':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x13_5.00mm_MH' : generate_params(13, "MSTBV", 5.0, False, True, {'1776993':'12A'}, mount_hole=True),
    'MSTBV_01x14_5.00mm_MH' : generate_params(14, "MSTBV", 5.0, False, True, {'1776002':'12A'}, mount_hole=True),
    'MSTBV_01x15_5.00mm_MH' : generate_params(15, "MSTBV", 5.0, False, True, {'1776015':'12A'}, mount_hole=True),
    'MSTBV_01x16_5.00mm_MH' : generate_params(16, "MSTBV", 5.0, False, True, {'1776028':'12A'}, mount_hole=True),
    'MSTBA_01x02_5.08mm' : generate_params( 2, "MSTBA", 5.08, True, False, {'1757242':'12A', '1923869':'16A (HC)'}),
    'MSTBA_01x03_5.08mm' : generate_params( 3, "MSTBA", 5.08, True, False, {'1757255':'12A', '1923872':'16A (HC)'}),
    'MSTBA_01x04_5.08mm' : generate_params( 4, "MSTBA", 5.08, True, False, {'1757268':'12A', '1923885':'16A (HC)'}),
    'MSTBA_01x05_5.08mm' : generate_params( 5, "MSTBA", 5.08, True, False, {'1757271':'12A', '1923898':'16A (HC)'}),
    'MSTBA_01x06_5.08mm' : generate_params( 6, "MSTBA", 5.08, True, False, {'1757284':'12A', '1923908':'16A (HC)'}),
    'MSTBA_01x07_5.08mm' : generate_params( 7, "MSTBA", 5.08, True, False, {'1757297':'12A', '1923911':'16A (HC)'}),
    'MSTBA_01x08_5.08mm' : generate_params( 8, "MSTBA", 5.08, True, False, {'1757307':'12A', '1923924':'16A (HC)'}),
    'MSTBA_01x09_5.08mm' : generate_params( 9, "MSTBA", 5.08, True, False, {'1757310':'12A', '1923937':'16A (HC)'}),
    'MSTBA_01x10_5.08mm' : generate_params(10, "MSTBA", 5.08, True, False, {'1757323':'12A', '1923940':'16A (HC)'}),
    'MSTBA_01x11_5.08mm' : generate_params(11, "MSTBA", 5.08, True, False, {'1757336':'12A', '1923953':'16A (HC)'}),
    'MSTBA_01x12_5.08mm' : generate_params(12, "MSTBA", 5.08, True, False, {'1757349':'12A', '1923966':'16A (HC)'}),
    'MSTBA_01x13_5.08mm' : generate_params(13, "MSTBA", 5.08, True, False, {'1757352':'12A'}),
    'MSTBA_01x14_5.08mm' : generate_params(14, "MSTBA", 5.08, True, False, {'1757365':'12A'}),
    'MSTBA_01x15_5.08mm' : generate_params(15, "MSTBA", 5.08, True, False, {'1757378':'12A'}),
    'MSTBA_01x16_5.08mm' : generate_params(16, "MSTBA", 5.08, True, False, {'1757381':'12A'}),
    'MSTB_01x02_5.08mm' : generate_params( 2, "MSTB", 5.08, True, True, {'1776508':'12A', '1924088':'16A (HC)'}),
    'MSTB_01x03_5.08mm' : generate_params( 3, "MSTB", 5.08, True, True, {'1776511':'12A', '1924091':'16A (HC)'}),
    'MSTB_01x04_5.08mm' : generate_params( 4, "MSTB", 5.08, True, True, {'1776524':'12A', '1924101':'16A (HC)'}),
    'MSTB_01x05_5.08mm' : generate_params( 5, "MSTB", 5.08, True, True, {'1776537':'12A', '1924114':'16A (HC)'}),
    'MSTB_01x06_5.08mm' : generate_params( 6, "MSTB", 5.08, True, True, {'1776540':'12A', '1924127':'16A (HC)'}),
    'MSTB_01x07_5.08mm' : generate_params( 7, "MSTB", 5.08, True, True, {'1776553':'12A', '1924130':'16A (HC)'}),
    'MSTB_01x08_5.08mm' : generate_params( 8, "MSTB", 5.08, True, True, {'1776566':'12A', '1924143':'16A (HC)'}),
    'MSTB_01x09_5.08mm' : generate_params( 9, "MSTB", 5.08, True, True, {'1776579':'12A', '1924156':'16A (HC)'}),
    'MSTB_01x10_5.08mm' : generate_params(10, "MSTB", 5.08, True, True, {'1776582':'12A', '1924169':'16A (HC)'}),
    'MSTB_01x11_5.08mm' : generate_params(11, "MSTB", 5.08, True, True, {'1776595':'12A', '1924172':'16A (HC)'}),
    'MSTB_01x12_5.08mm' : generate_params(12, "MSTB", 5.08, True, True, {'1776605':'12A', '1924185':'16A (HC)'}),
    'MSTB_01x13_5.08mm' : generate_params(13, "MSTB", 5.08, True, True, {'1776618':'12A'}),
    'MSTB_01x14_5.08mm' : generate_params(14, "MSTB", 5.08, True, True, {'1776621':'12A'}),
    'MSTB_01x15_5.08mm' : generate_params(15, "MSTB", 5.08, True, True, {'1776634':'12A'}),
    'MSTB_01x16_5.08mm' : generate_params(16, "MSTB", 5.08, True, True, {'1776647':'12A'}),
    'MSTB_01x02_5.08mm_MH' : generate_params( 2, "MSTB", 5.08, True, True, {'1776508':'12A', '1924088':'16A (HC)'}, mount_hole=True),
    'MSTB_01x03_5.08mm_MH' : generate_params( 3, "MSTB", 5.08, True, True, {'1776511':'12A', '1924091':'16A (HC)'}, mount_hole=True),
    'MSTB_01x04_5.08mm_MH' : generate_params( 4, "MSTB", 5.08, True, True, {'1776524':'12A', '1924101':'16A (HC)'}, mount_hole=True),
    'MSTB_01x05_5.08mm_MH' : generate_params( 5, "MSTB", 5.08, True, True, {'1776537':'12A', '1924114':'16A (HC)'}, mount_hole=True),
    'MSTB_01x06_5.08mm_MH' : generate_params( 6, "MSTB", 5.08, True, True, {'1776540':'12A', '1924127':'16A (HC)'}, mount_hole=True),
    'MSTB_01x07_5.08mm_MH' : generate_params( 7, "MSTB", 5.08, True, True, {'1776553':'12A', '1924130':'16A (HC)'}, mount_hole=True),
    'MSTB_01x08_5.08mm_MH' : generate_params( 8, "MSTB", 5.08, True, True, {'1776566':'12A', '1924143':'16A (HC)'}, mount_hole=True),
    'MSTB_01x09_5.08mm_MH' : generate_params( 9, "MSTB", 5.08, True, True, {'1776579':'12A', '1924156':'16A (HC)'}, mount_hole=True),
    'MSTB_01x10_5.08mm_MH' : generate_params(10, "MSTB", 5.08, True, True, {'1776582':'12A', '1924169':'16A (HC)'}, mount_hole=True),
    'MSTB_01x11_5.08mm_MH' : generate_params(11, "MSTB", 5.08, True, True, {'1776595':'12A', '1924172':'16A (HC)'}, mount_hole=True),
    'MSTB_01x12_5.08mm_MH' : generate_params(12, "MSTB", 5.08, True, True, {'1776605':'12A', '1924185':'16A (HC)'}, mount_hole=True),
    'MSTB_01x13_5.08mm_MH' : generate_params(13, "MSTB", 5.08, True, True, {'1776618':'12A'}, mount_hole=True),
    'MSTB_01x14_5.08mm_MH' : generate_params(14, "MSTB", 5.08, True, True, {'1776621':'12A'}, mount_hole=True),
    'MSTB_01x15_5.08mm_MH' : generate_params(15, "MSTB", 5.08, True, True, {'1776634':'12A'}, mount_hole=True),
    'MSTB_01x16_5.08mm_MH' : generate_params(16, "MSTB", 5.08, True, True, {'1776647':'12A'}, mount_hole=True),
    'MSTBVA_01x02_5.08mm' : generate_params( 2, "MSTBVA", 5.08, False, False, {'1755736':'12A', '1924305':'16A (HC)'}),
    'MSTBVA_01x03_5.08mm' : generate_params( 3, "MSTBVA", 5.08, False, False, {'1755749':'12A', '1924318':'16A (HC)'}),
    'MSTBVA_01x04_5.08mm' : generate_params( 4, "MSTBVA", 5.08, False, False, {'1755752':'12A', '1924321':'16A (HC)'}),
    'MSTBVA_01x05_5.08mm' : generate_params( 5, "MSTBVA", 5.08, False, False, {'1755765':'12A', '1924334':'16A (HC)'}),
    'MSTBVA_01x06_5.08mm' : generate_params( 6, "MSTBVA", 5.08, False, False, {'1755778':'12A', '1924347':'16A (HC)'}),
    'MSTBVA_01x07_5.08mm' : generate_params( 7, "MSTBVA", 5.08, False, False, {'1755781':'12A', '1924350':'16A (HC)'}),
    'MSTBVA_01x08_5.08mm' : generate_params( 8, "MSTBVA", 5.08, False, False, {'1755794':'12A', '1924363':'16A (HC)'}),
    'MSTBVA_01x09_5.08mm' : generate_params( 9, "MSTBVA", 5.08, False, False, {'1755804':'12A', '1924376':'16A (HC)'}),
    'MSTBVA_01x10_5.08mm' : generate_params(10, "MSTBVA", 5.08, False, False, {'1755817':'12A', '1924389':'16A (HC)'}),
    'MSTBVA_01x11_5.08mm' : generate_params(11, "MSTBVA", 5.08, False, False, {'1755820':'12A', '1924392':'16A (HC)'}),
    'MSTBVA_01x12_5.08mm' : generate_params(12, "MSTBVA", 5.08, False, False, {'1755833':'12A', '1924402':'16A (HC)'}),
    'MSTBVA_01x13_5.08mm' : generate_params(13, "MSTBVA", 5.08, False, False, {'1755846':'12A'}),
    'MSTBVA_01x14_5.08mm' : generate_params(14, "MSTBVA", 5.08, False, False, {'1755859':'12A'}),
    'MSTBVA_01x15_5.08mm' : generate_params(15, "MSTBVA", 5.08, False, False, {'1755862':'12A'}),
    'MSTBVA_01x16_5.08mm' : generate_params(16, "MSTBVA", 5.08, False, False, {'1755875':'12A'}),
    'MSTBV_01x02_5.08mm' : generate_params( 2, "MSTBV", 5.08, False, True, {'1777073':'12A', '1924525':'16A (HC)'}),
    'MSTBV_01x03_5.08mm' : generate_params( 3, "MSTBV", 5.08, False, True, {'1777086':'12A', '1924538':'16A (HC)'}),
    'MSTBV_01x04_5.08mm' : generate_params( 4, "MSTBV", 5.08, False, True, {'1777099':'12A', '1924541':'16A (HC)'}),
    'MSTBV_01x05_5.08mm' : generate_params( 5, "MSTBV", 5.08, False, True, {'1777109':'12A', '1924554':'16A (HC)'}),
    'MSTBV_01x06_5.08mm' : generate_params( 6, "MSTBV", 5.08, False, True, {'1777112':'12A', '1924567':'16A (HC)'}),
    'MSTBV_01x07_5.08mm' : generate_params( 7, "MSTBV", 5.08, False, True, {'1777125':'12A', '1924570':'16A (HC)'}),
    'MSTBV_01x08_5.08mm' : generate_params( 8, "MSTBV", 5.08, False, True, {'1777138':'12A', '1924583':'16A (HC)'}),
    'MSTBV_01x09_5.08mm' : generate_params( 9, "MSTBV", 5.08, False, True, {'1777141':'12A', '1924596':'16A (HC)'}),
    'MSTBV_01x10_5.08mm' : generate_params(10, "MSTBV", 5.08, False, True, {'1777154':'12A', '1924606':'16A (HC)'}),
    'MSTBV_01x11_5.08mm' : generate_params(11, "MSTBV", 5.08, False, True, {'1777167':'12A', '1924619':'16A (HC)'}),
    'MSTBV_01x12_5.08mm' : generate_params(12, "MSTBV", 5.08, False, True, {'1777170':'12A', '1924622':'16A (HC)'}),
    'MSTBV_01x13_5.08mm' : generate_params(13, "MSTBV", 5.08, False, True, {'1777183':'12A'}),
    'MSTBV_01x14_5.08mm' : generate_params(14, "MSTBV", 5.08, False, True, {'1777196':'12A'}),
    'MSTBV_01x15_5.08mm' : generate_params(15, "MSTBV", 5.08, False, True, {'1777206':'12A'}),
    'MSTBV_01x16_5.08mm' : generate_params(16, "MSTBV", 5.08, False, True, {'1777219':'12A'}),
    'MSTBV_01x02_5.08mm_MH' : generate_params( 2, "MSTBV", 5.08, False, True, {'1777073':'12A', '1924525':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x03_5.08mm_MH' : generate_params( 3, "MSTBV", 5.08, False, True, {'1777086':'12A', '1924538':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x04_5.08mm_MH' : generate_params( 4, "MSTBV", 5.08, False, True, {'1777099':'12A', '1924541':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x05_5.08mm_MH' : generate_params( 5, "MSTBV", 5.08, False, True, {'1777109':'12A', '1924554':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x06_5.08mm_MH' : generate_params( 6, "MSTBV", 5.08, False, True, {'1777112':'12A', '1924567':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x07_5.08mm_MH' : generate_params( 7, "MSTBV", 5.08, False, True, {'1777125':'12A', '1924570':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x08_5.08mm_MH' : generate_params( 8, "MSTBV", 5.08, False, True, {'1777138':'12A', '1924583':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x09_5.08mm_MH' : generate_params( 9, "MSTBV", 5.08, False, True, {'1777141':'12A', '1924596':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x10_5.08mm_MH' : generate_params(10, "MSTBV", 5.08, False, True, {'1777154':'12A', '1924606':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x11_5.08mm_MH' : generate_params(11, "MSTBV", 5.08, False, True, {'1777167':'12A', '1924619':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x12_5.08mm_MH' : generate_params(12, "MSTBV", 5.08, False, True, {'1777170':'12A', '1924622':'16A (HC)'}, mount_hole=True),
    'MSTBV_01x13_5.08mm_MH' : generate_params(13, "MSTBV", 5.08, False, True, {'1777183':'12A'}, mount_hole=True),
    'MSTBV_01x14_5.08mm_MH' : generate_params(14, "MSTBV", 5.08, False, True, {'1777196':'12A'}, mount_hole=True),
    'MSTBV_01x15_5.08mm_MH' : generate_params(15, "MSTBV", 5.08, False, True, {'1777206':'12A'}, mount_hole=True),
    'MSTBV_01x16_5.08mm_MH' : generate_params(16, "MSTBV", 5.08, False, True, {'1777219':'12A'}, mount_hole=True)
}

drill = 1.4
mount_drill = 2.4
pin_Sx = 2.1
pin_Sy = 4.2

#lock_cutout=

def dimensions(num_pins, pitch, angled, flanged):
    lenght = (num_pins-1)*pitch + (3*pitch if flanged else pitch+2)
    width = 12 if angled else 8.6
    upper_to_pin = -2 if angled else -8.6+3.8
    left_to_pin = -(3*pitch if flanged else pitch+2)/2.0
    mount_hole_y = 2.5 if angled else 0.0
    mount_hole_left = [-pitch,mount_hole_y]
    mount_hole_right = [num_pins*pitch,mount_hole_y]
    return lenght, width, upper_to_pin, left_to_pin,\
        mount_hole_left, mount_hole_right

def generate_description(params):
    d = "Generic Phoenix Contact connector footprint for series: " + params.series_name + "; number of pins: " + ("%02d" %params.num_pins) + "; pin pitch: " + (('%.2f' % params.pin_pitch))\
        +"mm" + ('; Angled' if params.angled else '; Vertical')\
        + ('; threaded flange' + (' (footprint includes mount hole)' if params.mount_hole else '') if params.flanged else '')
    for order_num, info in params.order_info.iteritems():
        d += " || order number: " + order_num + " " + info
    return d

m = 'MSTBV_01x02_5.00mm_MH'
m2='MSTBV_01x03_5.00mm_MH'
m3='MSTBV_01x03_5.08mm_MH'
#to_generate = {m:all_params[m],m2:all_params[m2],m3:all_params[m3]}
to_generate=all_params
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for model, params in to_generate.iteritems():

    # Through-hole type shrouded header, Top entry type
    footprint_name = params.file_name

    length, width, upper_to_pin, left_to_pin, mount_hole_left, mount_hole_right\
        = dimensions(params.num_pins, params.pin_pitch, params.angled, params.flanged)

    p1=[left_to_pin,upper_to_pin]
    p2=v_add(p1,[length,width])
    center_x = (params.num_pins-1)/2.0*params.pin_pitch
    kicad_mod = Footprint(footprint_name)


    kicad_mod.setDescription(generate_description(params))
    kicad_mod.setTags("phonix contact " + model)

    # set general values
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[center_x, p1[1]-1], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[center_x,p2[1]+1.5], layer='F.Fab'))

    #add the pads
    for p in range(params.num_pins):
        Y = 0
        X = p * params.pin_pitch

        num = p+1
        kicad_mod.append(Pad(number=num, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL,
                            at=[X, Y], size=[pin_Sx, pin_Sy], drill=drill, layers=['*.Cu', '*.Mask', '*.Paste']))
    if params.mount_hole:
        kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_left, size=[drill, drill], drill=drill, layers=['*.Mask']))
        kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=mount_hole_right, size=[drill, drill], drill=drill, layers=['*.Mask']))
    #add an outline around the pins

    # create silscreen

    kicad_mod.append(RectLine(start=p1, end=p2, layer='F.SilkS'))

    if params.angled:
        lock_poly=[
            {'x':-1, 'y':0},
            {'x':1, 'y':0},
            {'x':1.5/2, 'y':-1.5},
            {'x':-1.5/2, 'y':-1.5},
            {'x':-1, 'y':0}
        ]
        kicad_mod.append(RectLine(start=[p1[0],p2[1]-1.5], end=[p2[0], p2[1]-1.5-1.8], layer='F.SilkS'))
        for i in range(-1 if params.flanged else 0, params.num_pins + (1 if params.flanged else 0)):
            lock_translation = Translation(i*params.pin_pitch, p2[1])
            lock_translation.append(PolygoneLine(polygone=lock_poly))
            kicad_mod.append(lock_translation)
    else:
        inner_len = params.num_pins*params.pin_pitch + 2 - 2*0.8 # sidethickness (0.8mm) measured
        inner_width = 5.03 #measured
        top_thickness = 1.7 #measured
        pi1 = [p1[0]+(length-inner_len)/2.0, p1[1]+top_thickness]
        pi2 = [p2[0]-(length-inner_len)/2.0, pi1[1]+inner_width]
        #kicad_mod.append(RectLine(start=pi1, end=pi2, layer='F.SilkS'))

        first_center = params.pin_pitch/2.0
        line_len = params.pin_pitch-2
        outher_line_len = (-left_to_pin-1 - params.pin_pitch) if params.flanged else (-left_to_pin-1)
        kicad_mod.append(Line(start=[p1[0], pi1[1]-1], end=[p1[0]+outher_line_len, pi1[1]-1]))
        kicad_mod.append(Line(start=[p2[0], pi1[1]-1], end=[p2[0]-outher_line_len, pi1[1]-1]))
        for i in range(-1 if params.flanged else 0, params.num_pins + (0 if params.flanged else -1)):
            chamfer_edge = Translation(i*params.pin_pitch, pi1[1]-1)
            chamfer_edge.append(Line(start=[first_center-line_len/2.0, 0], end=[first_center+line_len/2.0, 0]))
            kicad_mod.append(chamfer_edge)


        for i in range(-1 if params.flanged else 0, params.num_pins + (1 if params.flanged else 0)):
            lock_translation = Translation(i*params.pin_pitch, pi1[1])
            lock_translation.append(RectLine(start=[-1,0], end=[1,-top_thickness], layer='F.SilkS'))
            kicad_mod.append(lock_translation)

        if params.flanged:
            kicad_mod.append(Circle(center=mount_hole_left, radius=1.9, layer='F.SilkS'))
            kicad_mod.append(Circle(center=mount_hole_right, radius=1.9, layer='F.SilkS'))
            kicad_mod.append(Circle(center=mount_hole_left, radius=1, layer='F.SilkS'))
            kicad_mod.append(Circle(center=mount_hole_right, radius=1, layer='F.SilkS'))

        angle = -110.8
        arc_width = 4.0
        for i in range(params.num_pins):
            plug_arc = Translation(i*params.pin_pitch,0)
            plug_arc.append(Arc(start=[-arc_width/2.0,pi2[1]], center=[0,0.55], angle=angle))
            kicad_mod.append(plug_arc)



        for i in range(params.num_pins-1):
            lower_line = Translation(i*params.pin_pitch,pi2[1])
            lower_line.append(Line(start=[arc_width/2.0, 0], end=[params.pin_pitch-arc_width/2.0, 0], layer='F.SilkS'))
            kicad_mod.append(lower_line)

        arc_to_side = pi1[0]+arc_width/2.0
        poly=[
            {'x':pi1[0]-arc_to_side, 'y':pi2[1]},
            {'x':pi1[0], 'y':pi2[1]},
            {'x':pi1[0], 'y':pi1[1]},
            {'x':pi2[0], 'y':pi1[1]},
            {'x':pi2[0], 'y':pi2[1]},
            {'x':pi2[0]+arc_to_side, 'y':pi2[1]}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly))
    # create courtyard
    if params.angled:
        p1=[p1[0],-pin_Sy/2]
    p1=v_add(p1,[-0.25,-0.25])
    p2=v_add(p2,[0.25,0.25])
    kicad_mod.append(RectLine(start=p1, end=p2, layer='F.CrtYd'))

    #kicad_mod.addRectLine()

    # y1 = -1
    # x1 = -1
    # x2 = (rows - 1) * pitch + 1
    # y2 = (pincount - 1) * pitch + 1
    #
    # if rows == 1:
    #     kicad_mod.addPolygoneLine([{'y':x1,'x':y1 + pitch},{'y':x2,'x':y1+pitch}])
    #
    # elif rows == 2:
    #     kicad_mod.addPolygoneLine([{'y':x1,'x':y1 + pitch},
    #                                {'y':x1 + pitch,'x':y1+pitch},
    #                                {'y':x1 + pitch,'x':y1},
    #                                {'y':x2,'x':y1},
    #                                {'y':x2,'x':y1+pitch}])
    #
    # kicad_mod.addPolygoneLine([
    #                            {'y':x2,'x':y1 + pitch},
    #                            {'y':x2,'x':y2 + 0.2},
    #                            {'y':x1,'x':y2 + 0.2},
    #                            {'y':x1,'x':y1 + pitch}])
    #
    # d = 0.6
    #
    # #add a keepout
    # kicad_mod.addPolygoneLine([{'y':x1-d,'x':y1-d},
    #                            {'y':x2+d,'x':y1-d},
    #                            {'y':x2+d,'x':y2+d},
    #                            {'y':x1-d,'x':y2+d},
    #                            {'y':x1-d,'x':y1-d}],"F.CrtYd",0.05)
    #
    #
    # d = 0.5
    #
    # #add a pin-1 designator
    # kicad_mod.addPolygoneLine([{'y':x1-d,'x':0},
    #                            {'y':x1-d,'x':y1-d},
    #                            {'y':0,'x':y1-d}])
    #
    # #add the model
    p3dname = packages_3d + footprint_name + ".wrl"
    kicad_mod.append(Model(filename=p3dname,
                           at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
    # kicad_mod.model_rot['z'] = 0
    # if rows == 2:
    #     kicad_mod.model_pos['y'] = -pitch * 0.5 / 25.4
    #
    # if pincount % 2 == 0: #even
    #     kicad_mod.model_pos['x'] = (pincount / 2 - 0.5) * pitch / 25.4
    # else:
    #     kicad_mod.model_pos['x'] = (pincount / 2) * pitch / 25.4
    #
    # # output kicad model
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(out_dir+footprint_name + ".kicad_mod")
