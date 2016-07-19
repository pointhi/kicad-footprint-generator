from collections import namedtuple
from global_params import generate_footprint_name

Params = namedtuple("Params",[
    'series_name',
    'file_name',
    'angled',
    'flanged',
    'num_pins',
    'pin_pitch',
    'mount_hole',
    'order_info',
    'mount_hole_to_pin',
    'side_to_pin',
    'back_to_pin'
])

def generate_params(num_pins, series_name, pin_pitch, angled, flanged, order_info, mount_hole=False, mount_hole_to_pin=None, side_to_pin=None, back_to_pin=None):

    return Params(
        series_name=series_name,
        file_name=generate_footprint_name(series_name, num_pins, pin_pitch, angled, mount_hole, flanged),
        angled=angled,
        flanged=flanged,
        num_pins=num_pins,
        pin_pitch=pin_pitch,
        mount_hole=mount_hole,
        order_info=order_info,
        mount_hole_to_pin=pin_pitch if mount_hole_to_pin is None else mount_hole_to_pin,
        side_to_pin=(3*pin_pitch if flanged else pin_pitch+2)/2.0 if side_to_pin is None else side_to_pin,
        back_to_pin= (8-9.2 if angled else 3-7.25) if back_to_pin is None else back_to_pin
    )


all_params = {
    ##################################################################################################################
    # Pin Pitch 3.50mm
    ##################################################################################################################
    'MC_01x02_G_3.5mm' : generate_params( 2, "MC-G", 3.5, True, False, {'1844210':'8A 160V'}, side_to_pin=2.45),
    'MC_01x03_G_3.5mm' : generate_params( 3, "MC-G", 3.5, True, False, {'1844223':'8A 160V'}, side_to_pin=2.45),
    'MC_01x04_G_3.5mm' : generate_params( 4, "MC-G", 3.5, True, False, {'1844236':'8A 160V'}, side_to_pin=2.45),
    'MC_01x05_G_3.5mm' : generate_params( 5, "MC-G", 3.5, True, False, {'1844249':'8A 160V'}, side_to_pin=2.45),
    'MC_01x06_G_3.5mm' : generate_params( 6, "MC-G", 3.5, True, False, {'1844252':'8A 160V'}, side_to_pin=2.45),
    'MC_01x07_G_3.5mm' : generate_params( 7, "MC-G", 3.5, True, False, {'1844265':'8A 160V'}, side_to_pin=2.45),
    'MC_01x08_G_3.5mm' : generate_params( 8, "MC-G", 3.5, True, False, {'1844278':'8A 160V'}, side_to_pin=2.45),
    'MC_01x09_G_3.5mm' : generate_params( 9, "MC-G", 3.5, True, False, {'1844281':'8A 160V'}, side_to_pin=2.45),
    'MC_01x10_G_3.5mm' : generate_params(10, "MC-G", 3.5, True, False, {'1844294':'8A 160V'}, side_to_pin=2.45),
    'MC_01x11_G_3.5mm' : generate_params(11, "MC-G", 3.5, True, False, {'1844304':'8A 160V'}, side_to_pin=2.45),
    'MC_01x12_G_3.5mm' : generate_params(12, "MC-G", 3.5, True, False, {'1844317':'8A 160V'}, side_to_pin=2.45),
    'MC_01x13_G_3.5mm' : generate_params(13, "MC-G", 3.5, True, False, {'1844320':'8A 160V'}, side_to_pin=2.45),
    'MC_01x14_G_3.5mm' : generate_params(14, "MC-G", 3.5, True, False, {'1844333':'8A 160V'}, side_to_pin=2.45),
    'MC_01x15_G_3.5mm' : generate_params(15, "MC-G", 3.5, True, False, {'1844346':'8A 160V'}, side_to_pin=2.45),
    'MC_01x16_G_3.5mm' : generate_params(16, "MC-G", 3.5, True, False, {'1844359':'8A 160V'}, side_to_pin=2.45),
    ###################################################################################################################
    'MC_01x02_GF_3.5mm' : generate_params( 2, "MC-GF", 3.5, True, True, {'1843790':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x03_GF_3.5mm' : generate_params( 3, "MC-GF", 3.5, True, True, {'1843800':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x04_GF_3.5mm' : generate_params( 4, "MC-GF", 3.5, True, True, {'1843813':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x05_GF_3.5mm' : generate_params( 5, "MC-GF", 3.5, True, True, {'1843826':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x06_GF_3.5mm' : generate_params( 6, "MC-GF", 3.5, True, True, {'1843839':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x07_GF_3.5mm' : generate_params( 7, "MC-GF", 3.5, True, True, {'1843842':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x08_GF_3.5mm' : generate_params( 8, "MC-GF", 3.5, True, True, {'1843855':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x09_GF_3.5mm' : generate_params( 9, "MC-GF", 3.5, True, True, {'1843868':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x10_GF_3.5mm' : generate_params(10, "MC-GF", 3.5, True, True, {'1843871':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x11_GF_3.5mm' : generate_params(11, "MC-GF", 3.5, True, True, {'1843884':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x12_GF_3.5mm' : generate_params(12, "MC-GF", 3.5, True, True, {'1843897':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x13_GF_3.5mm' : generate_params(13, "MC-GF", 3.5, True, True, {'1843907':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x14_GF_3.5mm' : generate_params(14, "MC-GF", 3.5, True, True, {'1843910':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x15_GF_3.5mm' : generate_params(15, "MC-GF", 3.5, True, True, {'1843923':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MC_01x16_GF_3.5mm' : generate_params(16, "MC-GF", 3.5, True, True, {'1843936':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    ###################################################################################################################
    'MC_01x02_GF_3.5mm_MH' : generate_params( 2, "MC-GF", 3.5, True, True, {'1843790':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x03_GF_3.5mm_MH' : generate_params( 3, "MC-GF", 3.5, True, True, {'1843800':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x04_GF_3.5mm_MH' : generate_params( 4, "MC-GF", 3.5, True, True, {'1843813':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x05_GF_3.5mm_MH' : generate_params( 5, "MC-GF", 3.5, True, True, {'1843826':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x06_GF_3.5mm_MH' : generate_params( 6, "MC-GF", 3.5, True, True, {'1843839':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x07_GF_3.5mm_MH' : generate_params( 7, "MC-GF", 3.5, True, True, {'1843842':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x08_GF_3.5mm_MH' : generate_params( 8, "MC-GF", 3.5, True, True, {'1843855':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x09_GF_3.5mm_MH' : generate_params( 9, "MC-GF", 3.5, True, True, {'1843868':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x10_GF_3.5mm_MH' : generate_params(10, "MC-GF", 3.5, True, True, {'1843871':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x11_GF_3.5mm_MH' : generate_params(11, "MC-GF", 3.5, True, True, {'1843884':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x12_GF_3.5mm_MH' : generate_params(12, "MC-GF", 3.5, True, True, {'1843897':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x13_GF_3.5mm_MH' : generate_params(13, "MC-GF", 3.5, True, True, {'1843907':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x14_GF_3.5mm_MH' : generate_params(14, "MC-GF", 3.5, True, True, {'1843910':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x15_GF_3.5mm_MH' : generate_params(15, "MC-GF", 3.5, True, True, {'1843923':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MC_01x16_GF_3.5mm_MH' : generate_params(16, "MC-GF", 3.5, True, True, {'1843936':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    ###################################################################################################################
    'MCV_01x02_G_3.5mm' : generate_params( 2, "MCV-G", 3.5, False, False, {'1843606':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x03_G_3.5mm' : generate_params( 3, "MCV-G", 3.5, False, False, {'1843619':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x04_G_3.5mm' : generate_params( 4, "MCV-G", 3.5, False, False, {'1843622':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x05_G_3.5mm' : generate_params( 5, "MCV-G", 3.5, False, False, {'1843635':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x06_G_3.5mm' : generate_params( 6, "MCV-G", 3.5, False, False, {'1843648':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x07_G_3.5mm' : generate_params( 7, "MCV-G", 3.5, False, False, {'1843651':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x08_G_3.5mm' : generate_params( 8, "MCV-G", 3.5, False, False, {'1843664':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x09_G_3.5mm' : generate_params( 9, "MCV-G", 3.5, False, False, {'1843677':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x10_G_3.5mm' : generate_params(10, "MCV-G", 3.5, False, False, {'1843680':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x11_G_3.5mm' : generate_params(11, "MCV-G", 3.5, False, False, {'1843693':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x12_G_3.5mm' : generate_params(12, "MCV-G", 3.5, False, False, {'1843703':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x13_G_3.5mm' : generate_params(13, "MCV-G", 3.5, False, False, {'1843716':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x14_G_3.5mm' : generate_params(14, "MCV-G", 3.5, False, False, {'1843729':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x15_G_3.5mm' : generate_params(15, "MCV-G", 3.5, False, False, {'1843732':'8A 160V'}, side_to_pin=2.45),
    'MCV_01x16_G_3.5mm' : generate_params(16, "MCV-G", 3.5, False, False, {'1843745':'8A 160V'}, side_to_pin=2.45),
    ###################################################################################################################
    'MCV_01x02_GF_3.5mm' : generate_params( 2, "MCV-GF", 3.5, False, True, {'1843224':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x03_GF_3.5mm' : generate_params( 3, "MCV-GF", 3.5, False, True, {'1843237':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x04_GF_3.5mm' : generate_params( 4, "MCV-GF", 3.5, False, True, {'1843240':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x05_GF_3.5mm' : generate_params( 5, "MCV-GF", 3.5, False, True, {'1843253':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x06_GF_3.5mm' : generate_params( 6, "MCV-GF", 3.5, False, True, {'1843266':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x07_GF_3.5mm' : generate_params( 7, "MCV-GF", 3.5, False, True, {'1843279':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x08_GF_3.5mm' : generate_params( 8, "MCV-GF", 3.5, False, True, {'1843282':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x09_GF_3.5mm' : generate_params( 9, "MCV-GF", 3.5, False, True, {'1843295':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x10_GF_3.5mm' : generate_params(10, "MCV-GF", 3.5, False, True, {'1843305':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x11_GF_3.5mm' : generate_params(11, "MCV-GF", 3.5, False, True, {'1843318':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x12_GF_3.5mm' : generate_params(12, "MCV-GF", 3.5, False, True, {'1843321':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x13_GF_3.5mm' : generate_params(13, "MCV-GF", 3.5, False, True, {'1843334':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x14_GF_3.5mm' : generate_params(14, "MCV-GF", 3.5, False, True, {'1843347':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x15_GF_3.5mm' : generate_params(15, "MCV-GF", 3.5, False, True, {'1843350':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    'MCV_01x16_GF_3.5mm' : generate_params(16, "MCV-GF", 3.5, False, True, {'1843363':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3),
    ###################################################################################################################
    'MCV_01x02_GF_3.5mm_MH' : generate_params( 2, "MCV-GF", 3.5, False, True, {'1843224':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x03_GF_3.5mm_MH' : generate_params( 3, "MCV-GF", 3.5, False, True, {'1843237':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x04_GF_3.5mm_MH' : generate_params( 4, "MCV-GF", 3.5, False, True, {'1843240':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x05_GF_3.5mm_MH' : generate_params( 5, "MCV-GF", 3.5, False, True, {'1843253':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x06_GF_3.5mm_MH' : generate_params( 6, "MCV-GF", 3.5, False, True, {'1843266':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x07_GF_3.5mm_MH' : generate_params( 7, "MCV-GF", 3.5, False, True, {'1843279':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x08_GF_3.5mm_MH' : generate_params( 8, "MCV-GF", 3.5, False, True, {'1843282':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x09_GF_3.5mm_MH' : generate_params( 9, "MCV-GF", 3.5, False, True, {'1843295':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x10_GF_3.5mm_MH' : generate_params(10, "MCV-GF", 3.5, False, True, {'1843305':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x11_GF_3.5mm_MH' : generate_params(11, "MCV-GF", 3.5, False, True, {'1843318':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x12_GF_3.5mm_MH' : generate_params(12, "MCV-GF", 3.5, False, True, {'1843321':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x13_GF_3.5mm_MH' : generate_params(13, "MCV-GF", 3.5, False, True, {'1843334':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x14_GF_3.5mm_MH' : generate_params(14, "MCV-GF", 3.5, False, True, {'1843347':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x15_GF_3.5mm_MH' : generate_params(15, "MCV-GF", 3.5, False, True, {'1843350':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    'MCV_01x16_GF_3.5mm_MH' : generate_params(16, "MCV-GF", 3.5, False, True, {'1843363':'8A 160V'}, side_to_pin=6.9, mount_hole_to_pin=4.3, mount_hole=True),
    ##################################################################################################################
    # Pin Pitch 3.81mm
    ##################################################################################################################
    'MC_01x02_G_3.81mm' : generate_params( 2, "MC-G", 3.81, True, False, {'1803277':'8A 160V'}, side_to_pin=2.6),
    'MC_01x03_G_3.81mm' : generate_params( 3, "MC-G", 3.81, True, False, {'1803280':'8A 160V'}, side_to_pin=2.6),
    'MC_01x04_G_3.81mm' : generate_params( 4, "MC-G", 3.81, True, False, {'1803293':'8A 160V'}, side_to_pin=2.6),
    'MC_01x05_G_3.81mm' : generate_params( 5, "MC-G", 3.81, True, False, {'1803303':'8A 160V'}, side_to_pin=2.6),
    'MC_01x06_G_3.81mm' : generate_params( 6, "MC-G", 3.81, True, False, {'1803316':'8A 160V'}, side_to_pin=2.6),
    'MC_01x07_G_3.81mm' : generate_params( 7, "MC-G", 3.81, True, False, {'1803329':'8A 160V'}, side_to_pin=2.6),
    'MC_01x08_G_3.81mm' : generate_params( 8, "MC-G", 3.81, True, False, {'1803332':'8A 160V'}, side_to_pin=2.6),
    'MC_01x09_G_3.81mm' : generate_params( 9, "MC-G", 3.81, True, False, {'1803345':'8A 160V'}, side_to_pin=2.6),
    'MC_01x10_G_3.81mm' : generate_params(10, "MC-G", 3.81, True, False, {'1803358':'8A 160V'}, side_to_pin=2.6),
    'MC_01x11_G_3.81mm' : generate_params(11, "MC-G", 3.81, True, False, {'1803361':'8A 160V'}, side_to_pin=2.6),
    'MC_01x12_G_3.81mm' : generate_params(12, "MC-G", 3.81, True, False, {'1803374':'8A 160V'}, side_to_pin=2.6),
    'MC_01x13_G_3.81mm' : generate_params(13, "MC-G", 3.81, True, False, {'1803387':'8A 160V'}, side_to_pin=2.6),
    'MC_01x14_G_3.81mm' : generate_params(14, "MC-G", 3.81, True, False, {'1803390':'8A 160V'}, side_to_pin=2.6),
    'MC_01x15_G_3.81mm' : generate_params(15, "MC-G", 3.81, True, False, {'1803400':'8A 160V'}, side_to_pin=2.6),
    'MC_01x16_G_3.81mm' : generate_params(16, "MC-G", 3.81, True, False, {'1803413':'8A 160V'}, side_to_pin=2.6),
    ###################################################################################################################
    'MC_01x02_GF_3.81mm' : generate_params( 2, "MC-GF", 3.81, True, True, {'1827868':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x03_GF_3.81mm' : generate_params( 3, "MC-GF", 3.81, True, True, {'1827871':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x04_GF_3.81mm' : generate_params( 4, "MC-GF", 3.81, True, True, {'1827884':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x05_GF_3.81mm' : generate_params( 5, "MC-GF", 3.81, True, True, {'1827897':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x06_GF_3.81mm' : generate_params( 6, "MC-GF", 3.81, True, True, {'1827907':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x07_GF_3.81mm' : generate_params( 7, "MC-GF", 3.81, True, True, {'1827910':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x08_GF_3.81mm' : generate_params( 8, "MC-GF", 3.81, True, True, {'1827923':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x09_GF_3.81mm' : generate_params( 9, "MC-GF", 3.81, True, True, {'1827936':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x10_GF_3.81mm' : generate_params(10, "MC-GF", 3.81, True, True, {'1827949':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x11_GF_3.81mm' : generate_params(11, "MC-GF", 3.81, True, True, {'1827952':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x12_GF_3.81mm' : generate_params(12, "MC-GF", 3.81, True, True, {'1827965':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x13_GF_3.81mm' : generate_params(13, "MC-GF", 3.81, True, True, {'1827978':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x14_GF_3.81mm' : generate_params(14, "MC-GF", 3.81, True, True, {'1827981':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x15_GF_3.81mm' : generate_params(15, "MC-GF", 3.81, True, True, {'1827994':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x16_GF_3.81mm' : generate_params(16, "MC-GF", 3.81, True, True, {'1828003':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    ###################################################################################################################
    'MC_01x02_GF_3.81mm_MH' : generate_params( 2, "MC-GF", 3.81, True, True, {'1827868':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x03_GF_3.81mm_MH' : generate_params( 3, "MC-GF", 3.81, True, True, {'1827871':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x04_GF_3.81mm_MH' : generate_params( 4, "MC-GF", 3.81, True, True, {'1827884':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x05_GF_3.81mm_MH' : generate_params( 5, "MC-GF", 3.81, True, True, {'1827897':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x06_GF_3.81mm_MH' : generate_params( 6, "MC-GF", 3.81, True, True, {'1827907':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x07_GF_3.81mm_MH' : generate_params( 7, "MC-GF", 3.81, True, True, {'1827910':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x08_GF_3.81mm_MH' : generate_params( 8, "MC-GF", 3.81, True, True, {'1827923':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x09_GF_3.81mm_MH' : generate_params( 9, "MC-GF", 3.81, True, True, {'1827936':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x10_GF_3.81mm_MH' : generate_params(10, "MC-GF", 3.81, True, True, {'1827949':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x11_GF_3.81mm_MH' : generate_params(11, "MC-GF", 3.81, True, True, {'1827952':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x12_GF_3.81mm_MH' : generate_params(12, "MC-GF", 3.81, True, True, {'1827965':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x13_GF_3.81mm_MH' : generate_params(13, "MC-GF", 3.81, True, True, {'1827978':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x14_GF_3.81mm_MH' : generate_params(14, "MC-GF", 3.81, True, True, {'1827981':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x15_GF_3.81mm_MH' : generate_params(15, "MC-GF", 3.81, True, True, {'1827994':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x16_GF_3.81mm_MH' : generate_params(16, "MC-GF", 3.81, True, True, {'1828003':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    ###################################################################################################################
    'MCV_01x02_G_3.81mm' : generate_params( 2, "MCV-G", 3.81, False, False, {'1803426':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x03_G_3.81mm' : generate_params( 3, "MCV-G", 3.81, False, False, {'1803439':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x04_G_3.81mm' : generate_params( 4, "MCV-G", 3.81, False, False, {'1803442':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x05_G_3.81mm' : generate_params( 5, "MCV-G", 3.81, False, False, {'1803455':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x06_G_3.81mm' : generate_params( 6, "MCV-G", 3.81, False, False, {'1803468':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x07_G_3.81mm' : generate_params( 7, "MCV-G", 3.81, False, False, {'1803471':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x08_G_3.81mm' : generate_params( 8, "MCV-G", 3.81, False, False, {'1803484':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x09_G_3.81mm' : generate_params( 9, "MCV-G", 3.81, False, False, {'1803497':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x10_G_3.81mm' : generate_params(10, "MCV-G", 3.81, False, False, {'1803507':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x11_G_3.81mm' : generate_params(11, "MCV-G", 3.81, False, False, {'1803510':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x12_G_3.81mm' : generate_params(12, "MCV-G", 3.81, False, False, {'1803523':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x13_G_3.81mm' : generate_params(13, "MCV-G", 3.81, False, False, {'1803536':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x14_G_3.81mm' : generate_params(14, "MCV-G", 3.81, False, False, {'1803549':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x15_G_3.81mm' : generate_params(15, "MCV-G", 3.81, False, False, {'1803552':'8A 160V'}, side_to_pin=2.6),
    'MCV_01x16_G_3.81mm' : generate_params(16, "MCV-G", 3.81, False, False, {'1803565':'8A 160V'}, side_to_pin=2.6),
    ###################################################################################################################
    'MCV_01x02_GF_3.81mm' : generate_params( 2, "MCV-GF", 3.81, False, True, {'1830596':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x03_GF_3.81mm' : generate_params( 3, "MCV-GF", 3.81, False, True, {'1830606':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x04_GF_3.81mm' : generate_params( 4, "MCV-GF", 3.81, False, True, {'1830619':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x05_GF_3.81mm' : generate_params( 5, "MCV-GF", 3.81, False, True, {'1830622':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x06_GF_3.81mm' : generate_params( 6, "MCV-GF", 3.81, False, True, {'1830635':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x07_GF_3.81mm' : generate_params( 7, "MCV-GF", 3.81, False, True, {'1830648':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x08_GF_3.81mm' : generate_params( 8, "MCV-GF", 3.81, False, True, {'1830651':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x09_GF_3.81mm' : generate_params( 9, "MCV-GF", 3.81, False, True, {'1830664':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x10_GF_3.81mm' : generate_params(10, "MCV-GF", 3.81, False, True, {'1830677':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x11_GF_3.81mm' : generate_params(11, "MCV-GF", 3.81, False, True, {'1830680':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x12_GF_3.81mm' : generate_params(12, "MCV-GF", 3.81, False, True, {'1830693':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x13_GF_3.81mm' : generate_params(13, "MCV-GF", 3.81, False, True, {'1830703':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x14_GF_3.81mm' : generate_params(14, "MCV-GF", 3.81, False, True, {'1830716':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x15_GF_3.81mm' : generate_params(15, "MCV-GF", 3.81, False, True, {'1830729':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MCV_01x16_GF_3.81mm' : generate_params(16, "MCV-GF", 3.81, False, True, {'1830732':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    ###################################################################################################################
    'MCV_01x02_GF_3.81mm_MH' : generate_params( 2, "MCV-GF", 3.81, False, True, {'1830596':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x03_GF_3.81mm_MH' : generate_params( 3, "MCV-GF", 3.81, False, True, {'1830606':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x04_GF_3.81mm_MH' : generate_params( 4, "MCV-GF", 3.81, False, True, {'1830619':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x05_GF_3.81mm_MH' : generate_params( 5, "MCV-GF", 3.81, False, True, {'1830622':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x06_GF_3.81mm_MH' : generate_params( 6, "MCV-GF", 3.81, False, True, {'1830635':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x07_GF_3.81mm_MH' : generate_params( 7, "MCV-GF", 3.81, False, True, {'1830648':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x08_GF_3.81mm_MH' : generate_params( 8, "MCV-GF", 3.81, False, True, {'1830651':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x09_GF_3.81mm_MH' : generate_params( 9, "MCV-GF", 3.81, False, True, {'1830664':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x10_GF_3.81mm_MH' : generate_params(10, "MCV-GF", 3.81, False, True, {'1830677':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x11_GF_3.81mm_MH' : generate_params(11, "MCV-GF", 3.81, False, True, {'1830680':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x12_GF_3.81mm_MH' : generate_params(12, "MCV-GF", 3.81, False, True, {'1830693':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x13_GF_3.81mm_MH' : generate_params(13, "MCV-GF", 3.81, False, True, {'1830703':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x14_GF_3.81mm_MH' : generate_params(14, "MCV-GF", 3.81, False, True, {'1830716':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x15_GF_3.81mm_MH' : generate_params(15, "MCV-GF", 3.81, False, True, {'1830729':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MCV_01x16_GF_3.81mm_MH' : generate_params(16, "MCV-GF", 3.81, False, True, {'1830732':'8A 160V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    ##################################################################################################################
    # Pin Pitch 5.08mm
    ##################################################################################################################
    'MC_01x02_G_5.08mm' : generate_params( 2, "MC-G", 5.08, True, False, {'1836189':'8A 320V'}, side_to_pin=2.54),
    'MC_01x03_G_5.08mm' : generate_params( 3, "MC-G", 5.08, True, False, {'1836192':'8A 320V'}, side_to_pin=2.54),
    'MC_01x04_G_5.08mm' : generate_params( 4, "MC-G", 5.08, True, False, {'1836202':'8A 320V'}, side_to_pin=2.54),
    'MC_01x05_G_5.08mm' : generate_params( 5, "MC-G", 5.08, True, False, {'1836215':'8A 320V'}, side_to_pin=2.54),
    'MC_01x06_G_5.08mm' : generate_params( 6, "MC-G", 5.08, True, False, {'1836228':'8A 320V'}, side_to_pin=2.54),
    'MC_01x07_G_5.08mm' : generate_params( 7, "MC-G", 5.08, True, False, {'1836231':'8A 320V'}, side_to_pin=2.54),
    'MC_01x08_G_5.08mm' : generate_params( 8, "MC-G", 5.08, True, False, {'1836244':'8A 320V'}, side_to_pin=2.54),
    'MC_01x09_G_5.08mm' : generate_params( 9, "MC-G", 5.08, True, False, {'1836257':'8A 320V'}, side_to_pin=2.54),
    'MC_01x10_G_5.08mm' : generate_params(10, "MC-G", 5.08, True, False, {'1836260':'8A 320V'}, side_to_pin=2.54),
    'MC_01x11_G_5.08mm' : generate_params(11, "MC-G", 5.08, True, False, {'1836273':'8A 320V'}, side_to_pin=2.54),
    'MC_01x12_G_5.08mm' : generate_params(12, "MC-G", 5.08, True, False, {'1836286':'8A 320V'}, side_to_pin=2.54),
    ###################################################################################################################
    'MC_01x02_GF_5.08mm' : generate_params( 2, "MC-GF", 5.08, True, True, {'1847466':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x03_GF_5.08mm' : generate_params( 3, "MC-GF", 5.08, True, True, {'1847479':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x04_GF_5.08mm' : generate_params( 4, "MC-GF", 5.08, True, True, {'1847482':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x05_GF_5.08mm' : generate_params( 5, "MC-GF", 5.08, True, True, {'1847495':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x06_GF_5.08mm' : generate_params( 6, "MC-GF", 5.08, True, True, {'1847505':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x07_GF_5.08mm' : generate_params( 7, "MC-GF", 5.08, True, True, {'1847518':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x08_GF_5.08mm' : generate_params( 8, "MC-GF", 5.08, True, True, {'1847521':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x09_GF_5.08mm' : generate_params( 9, "MC-GF", 5.08, True, True, {'1847534':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x10_GF_5.08mm' : generate_params(10, "MC-GF", 5.08, True, True, {'1847547':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x11_GF_5.08mm' : generate_params(11, "MC-GF", 5.08, True, True, {'1847550':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    'MC_01x12_GF_5.08mm' : generate_params(12, "MC-GF", 5.08, True, True, {'1847563':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5),
    ###################################################################################################################
    'MC_01x02_GF_5.08mm_MH' : generate_params( 2, "MC-GF", 5.08, True, True, {'1847466':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x03_GF_5.08mm_MH' : generate_params( 3, "MC-GF", 5.08, True, True, {'1847479':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x04_GF_5.08mm_MH' : generate_params( 4, "MC-GF", 5.08, True, True, {'1847482':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x05_GF_5.08mm_MH' : generate_params( 5, "MC-GF", 5.08, True, True, {'1847495':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x06_GF_5.08mm_MH' : generate_params( 6, "MC-GF", 5.08, True, True, {'1847505':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x07_GF_5.08mm_MH' : generate_params( 7, "MC-GF", 5.08, True, True, {'1847518':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x08_GF_5.08mm_MH' : generate_params( 8, "MC-GF", 5.08, True, True, {'1847521':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x09_GF_5.08mm_MH' : generate_params( 9, "MC-GF", 5.08, True, True, {'1847534':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x10_GF_5.08mm_MH' : generate_params(10, "MC-GF", 5.08, True, True, {'1847547':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x11_GF_5.08mm_MH' : generate_params(11, "MC-GF", 5.08, True, True, {'1847550':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    'MC_01x12_GF_5.08mm_MH' : generate_params(12, "MC-GF", 5.08, True, True, {'1847563':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True),
    ###################################################################################################################
    'MCV_01x02_G_5.08mm' : generate_params( 2, "MCV-G", 5.08, False, False, {'1836299':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x03_G_5.08mm' : generate_params( 3, "MCV-G", 5.08, False, False, {'1836309':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x04_G_5.08mm' : generate_params( 4, "MCV-G", 5.08, False, False, {'1836312':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x05_G_5.08mm' : generate_params( 5, "MCV-G", 5.08, False, False, {'1836325':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x06_G_5.08mm' : generate_params( 6, "MCV-G", 5.08, False, False, {'1836338':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x07_G_5.08mm' : generate_params( 7, "MCV-G", 5.08, False, False, {'1836341':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x08_G_5.08mm' : generate_params( 8, "MCV-G", 5.08, False, False, {'1836354':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x09_G_5.08mm' : generate_params( 9, "MCV-G", 5.08, False, False, {'1836367':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x10_G_5.08mm' : generate_params(10, "MCV-G", 5.08, False, False, {'1836370':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x11_G_5.08mm' : generate_params(11, "MCV-G", 5.08, False, False, {'1836383':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    'MCV_01x12_G_5.08mm' : generate_params(12, "MCV-G", 5.08, False, False, {'1836396':'8A 320V'}, side_to_pin=2.54, back_to_pin=2.9-7.25),
    ###################################################################################################################
    'MCV_01x02_GF_5.08mm' : generate_params( 2, "MCV-GF", 5.08, False, True, {'1847615':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x03_GF_5.08mm' : generate_params( 3, "MCV-GF", 5.08, False, True, {'1847628':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x04_GF_5.08mm' : generate_params( 4, "MCV-GF", 5.08, False, True, {'1847631':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x05_GF_5.08mm' : generate_params( 5, "MCV-GF", 5.08, False, True, {'1847644':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x06_GF_5.08mm' : generate_params( 6, "MCV-GF", 5.08, False, True, {'1847657':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x07_GF_5.08mm' : generate_params( 7, "MCV-GF", 5.08, False, True, {'1847660':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x08_GF_5.08mm' : generate_params( 8, "MCV-GF", 5.08, False, True, {'1847673':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x09_GF_5.08mm' : generate_params( 9, "MCV-GF", 5.08, False, True, {'1847686':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x10_GF_5.08mm' : generate_params(10, "MCV-GF", 5.08, False, True, {'1847699':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x11_GF_5.08mm' : generate_params(11, "MCV-GF", 5.08, False, True, {'1847709':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    'MCV_01x12_GF_5.08mm' : generate_params(12, "MCV-GF", 5.08, False, True, {'1847712':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, back_to_pin=2.9-7.25),
    ###################################################################################################################
    'MCV_01x02_GF_5.08mm_MH' : generate_params( 2, "MCV-GF", 5.08, False, True, {'1847615':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x03_GF_5.08mm_MH' : generate_params( 3, "MCV-GF", 5.08, False, True, {'1847628':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x04_GF_5.08mm_MH' : generate_params( 4, "MCV-GF", 5.08, False, True, {'1847631':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x05_GF_5.08mm_MH' : generate_params( 5, "MCV-GF", 5.08, False, True, {'1847644':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x06_GF_5.08mm_MH' : generate_params( 6, "MCV-GF", 5.08, False, True, {'1847657':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x07_GF_5.08mm_MH' : generate_params( 7, "MCV-GF", 5.08, False, True, {'1847660':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x08_GF_5.08mm_MH' : generate_params( 8, "MCV-GF", 5.08, False, True, {'1847673':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x09_GF_5.08mm_MH' : generate_params( 9, "MCV-GF", 5.08, False, True, {'1847686':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x10_GF_5.08mm_MH' : generate_params(10, "MCV-GF", 5.08, False, True, {'1847699':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x11_GF_5.08mm_MH' : generate_params(11, "MCV-GF", 5.08, False, True, {'1847709':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25),
    'MCV_01x12_GF_5.08mm_MH' : generate_params(12, "MCV-GF", 5.08, False, True, {'1847712':'8A 320V'}, side_to_pin=7.1, mount_hole_to_pin=4.5, mount_hole=True, back_to_pin=2.9-7.25)
}

class seriesParams():
    drill = 1.2
    mount_drill = 2.4
    mount_screw_head_r = 2.0
    pin_Sx = 1.8
    pin_Sy = 3.6
    flange_lenght = 4.8
    scoreline_from_back = 6.0

    plug_cut_len = 3.0
    plug_cut_width = 4.3
    plug_arc_len = 1.5
    plug_trapezoid_short = 2.5
    plug_trapezoid_long = 3.0
    plug_trapezoid_width = 1
    plug_seperator_distance = 1.5

    silkGab = pin_Sx/2.0+0.15



#lock_cutout=
CalcDim=namedtuple("CalcDim",[
    "length", "width", "left_to_pin",
    "mount_hole_left", "mount_hole_right", "flange_width",
    "plug_front", "plug_back"
])
def dimensions(params):
    mount_hole_y = 0.9 if params.angled else 0.0
    width = 9.2 if params.angled else 7.25
    return CalcDim(
        length = (params.num_pins-1)*params.pin_pitch + 2*params.side_to_pin
        ,width = width
        ,left_to_pin = -params.side_to_pin
        ,mount_hole_left = [-params.mount_hole_to_pin,mount_hole_y]
        ,mount_hole_right = [(params.num_pins-1)*params.pin_pitch+params.mount_hole_to_pin,mount_hole_y]
        ,flange_width = 9.2 if params.angled else 6.0
        ,plug_front = width + params.back_to_pin -0.75
        ,plug_back = params.back_to_pin+0.6+0.25
    )

def generate_description(params):
    d = "Generic Phoenix Contact connector footprint for series: " + params.series_name + "; number of pins: " + ("%02d" %params.num_pins) + "; pin pitch: " + (('%.2f' % params.pin_pitch))\
        +"mm" + ('; Angled' if params.angled else '; Vertical')\
        + ('; threaded flange' + (' (footprint includes mount hole)' if params.mount_hole else '') if params.flanged else '')
    for order_num, info in params.order_info.iteritems():
        d += " || order number: " + order_num + " " + info
    return d
