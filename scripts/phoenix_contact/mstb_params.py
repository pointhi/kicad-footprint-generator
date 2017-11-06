from collections import namedtuple
from collections import OrderedDict

class seriesParams():
    drill = 1.4
    annular_ring = 0.35 # overwritten by minimum pad to pad clearance.
    mount_drill = 2.4
    mount_screw_head_r = 2.1
    mount_screw_info = "ISO 1481-ST 2.2x6.5 C or ISO 7049-ST 2.2x6.5 C (http://www.fasteners.eu/standards/ISO/7049/)"

    # Connector voltage ratings:
    # Rated voltage (III/3) 250 V
    # Rated voltage (III/2) 320 V
    # Rated voltage (II/2) 400 V
    # Rated surge voltage (III/3) 4 kV
    # Rated surge voltage (III/2) 4 kV
    # Rated surge voltage (II/2) 4 kV
    # VDE 0110-1/4.97 4kV -> 3mm clearance
    MSTB_min_pad_to_pad_clearance = 3.0

    #Rated surge voltage (III/3) 6 kV
    #Rated surge voltage (III/2) 6 kV
    #Rated surge voltage (II/2) 6 kV
    #Rated voltage (III/3) 400 V
    #Rated voltage (III/2) 630 V
    #Rated voltage (II/2) 630 V
    # VDE 0110-1/4.97 6kV -> 5.5mm
    GMSTB_min_pad_to_pad_clearance = 5.5

Params = namedtuple("Params",[
    'series_name',
    'angled',
    'flanged',
    'num_pins',
    'pin_pitch',
    'mount_hole',
    'order_info',
    'mount_hole_to_pin',
    'side_to_pin',
    'pin_Sx',
    'pin_Sy'
])

def generate_params(num_pins, series_name, pin_pitch, angled, flanged, order_info, mount_hole=False, mount_hole_to_pin=None,
        side_to_pin=None, min_pad_to_pad_clearance=seriesParams.MSTB_min_pad_to_pad_clearance):
    nominal_pin_Sx = seriesParams.drill + 2 * seriesParams.annular_ring
    nominal_pin_Sy = seriesParams.drill + 2 * 1.1
    return Params(
        series_name=series_name,
        angled=angled,
        flanged=flanged,
        num_pins=num_pins,
        pin_pitch=pin_pitch,
        mount_hole=mount_hole,
        order_info=order_info,
        mount_hole_to_pin=pin_pitch if mount_hole_to_pin is None else mount_hole_to_pin,
        side_to_pin=(3*pin_pitch if flanged else pin_pitch+2)/2.0 if side_to_pin is None else side_to_pin,
        pin_Sx= nominal_pin_Sx if (pin_pitch - nominal_pin_Sx) >= min_pad_to_pad_clearance else (pin_pitch - min_pad_to_pad_clearance),
        pin_Sy = nominal_pin_Sy
    )


all_params = {
    ##################################################################################################################
    # Pin Pitch 5.00mm
    ##################################################################################################################
    'MSTBA_01x02_G_5.00mm' : generate_params( 2, "MSTBA-G", 5.0, True, False, OrderedDict([('1757475', '12A'), ('1923759', '16A (HC)')])),
    'MSTBA_01x03_G_5.00mm' : generate_params( 3, "MSTBA-G", 5.0, True, False, OrderedDict([('1757488', '12A'), ('1923762', '16A (HC)')])),
    'MSTBA_01x04_G_5.00mm' : generate_params( 4, "MSTBA-G", 5.0, True, False, OrderedDict([('1757491', '12A'), ('1923775', '16A (HC)')])),
    'MSTBA_01x05_G_5.00mm' : generate_params( 5, "MSTBA-G", 5.0, True, False, OrderedDict([('1757501', '12A'), ('1923788', '16A (HC)')])),
    'MSTBA_01x06_G_5.00mm' : generate_params( 6, "MSTBA-G", 5.0, True, False, OrderedDict([('1757514', '12A'), ('1923791', '16A (HC)')])),
    'MSTBA_01x07_G_5.00mm' : generate_params( 7, "MSTBA-G", 5.0, True, False, OrderedDict([('1757493', '12A'), ('1923801', '16A (HC)')])),
    'MSTBA_01x08_G_5.00mm' : generate_params( 8, "MSTBA-G", 5.0, True, False, OrderedDict([('1757527', '12A'), ('1923814', '16A (HC)')])),
    'MSTBA_01x09_G_5.00mm' : generate_params( 9, "MSTBA-G", 5.0, True, False, OrderedDict([('1757530', '12A'), ('1923827', '16A (HC)')])),
    'MSTBA_01x10_G_5.00mm' : generate_params(10, "MSTBA-G", 5.0, True, False, OrderedDict([('1757543', '12A'), ('1923830', '16A (HC)')])),
    'MSTBA_01x11_G_5.00mm' : generate_params(11, "MSTBA-G", 5.0, True, False, OrderedDict([('1757556', '12A'), ('1923843', '16A (HC)')])),
    'MSTBA_01x12_G_5.00mm' : generate_params(12, "MSTBA-G", 5.0, True, False, OrderedDict([('1757569', '12A'), ('1923856', '16A (HC)')])),
    'MSTBA_01x13_G_5.00mm' : generate_params(13, "MSTBA-G", 5.0, True, False, OrderedDict([('1757572', '12A')])),
    'MSTBA_01x14_G_5.00mm' : generate_params(14, "MSTBA-G", 5.0, True, False, OrderedDict([('1757585', '12A')])),
    'MSTBA_01x15_G_5.00mm' : generate_params(15, "MSTBA-G", 5.0, True, False, OrderedDict([('1757598', '12A')])),
    'MSTBA_01x16_G_5.00mm' : generate_params(16, "MSTBA-G", 5.0, True, False, OrderedDict([('1757608', '12A')])),
    ###################################################################################################################
    'MSTB_01x02_GF_5.00mm' : generate_params( 2, "MSTB-GF", 5.0, True, True, OrderedDict([('1776692', '12A'), ('1923979', '16A (HC)')])),
    'MSTB_01x03_GF_5.00mm' : generate_params( 3, "MSTB-GF", 5.0, True, True, OrderedDict([('1776702', '12A'), ('1923982', '16A (HC)')])),
    'MSTB_01x04_GF_5.00mm' : generate_params( 4, "MSTB-GF", 5.0, True, True, OrderedDict([('1776715', '12A'), ('1923995', '16A (HC)')])),
    'MSTB_01x05_GF_5.00mm' : generate_params( 5, "MSTB-GF", 5.0, True, True, OrderedDict([('1776728', '12A'), ('1924004', '16A (HC)')])),
    'MSTB_01x06_GF_5.00mm' : generate_params( 6, "MSTB-GF", 5.0, True, True, OrderedDict([('1776731', '12A'), ('1924017', '16A (HC)')])),
    'MSTB_01x07_GF_5.00mm' : generate_params( 7, "MSTB-GF", 5.0, True, True, OrderedDict([('1776744', '12A'), ('1924020', '16A (HC)')])),
    'MSTB_01x08_GF_5.00mm' : generate_params( 8, "MSTB-GF", 5.0, True, True, OrderedDict([('1776757', '12A'), ('1924033', '16A (HC)')])),
    'MSTB_01x09_GF_5.00mm' : generate_params( 9, "MSTB-GF", 5.0, True, True, OrderedDict([('1776760', '12A'), ('1924046', '16A (HC)')])),
    'MSTB_01x10_GF_5.00mm' : generate_params(10, "MSTB-GF", 5.0, True, True, OrderedDict([('1776773', '12A'), ('1924059', '16A (HC)')])),
    'MSTB_01x11_GF_5.00mm' : generate_params(11, "MSTB-GF", 5.0, True, True, OrderedDict([('1776786', '12A'), ('1924062', '16A (HC)')])),
    'MSTB_01x12_GF_5.00mm' : generate_params(12, "MSTB-GF", 5.0, True, True, OrderedDict([('1776799', '12A'), ('1924075', '16A (HC)')])),
    'MSTB_01x13_GF_5.00mm' : generate_params(13, "MSTB-GF", 5.0, True, True, OrderedDict([('1776809', '12A')])),
    'MSTB_01x14_GF_5.00mm' : generate_params(14, "MSTB-GF", 5.0, True, True, OrderedDict([('1776812', '12A')])),
    'MSTB_01x15_GF_5.00mm' : generate_params(15, "MSTB-GF", 5.0, True, True, OrderedDict([('1776825', '12A')])),
    'MSTB_01x16_GF_5.00mm' : generate_params(16, "MSTB-GF", 5.0, True, True, OrderedDict([('1776838', '12A')])),
    ###################################################################################################################
    'MSTB_01x02_GF_5.00mm_MH' : generate_params( 2, "MSTB-GF", 5.0, True, True, OrderedDict([('1776692', '12A'), ('1923979', '16A (HC)')]), mount_hole=True),
    'MSTB_01x03_GF_5.00mm_MH' : generate_params( 3, "MSTB-GF", 5.0, True, True, OrderedDict([('1776702', '12A'), ('1923982', '16A (HC)')]), mount_hole=True),
    'MSTB_01x04_GF_5.00mm_MH' : generate_params( 4, "MSTB-GF", 5.0, True, True, OrderedDict([('1776715', '12A'), ('1923995', '16A (HC)')]), mount_hole=True),
    'MSTB_01x05_GF_5.00mm_MH' : generate_params( 5, "MSTB-GF", 5.0, True, True, OrderedDict([('1776728', '12A'), ('1924004', '16A (HC)')]), mount_hole=True),
    'MSTB_01x06_GF_5.00mm_MH' : generate_params( 6, "MSTB-GF", 5.0, True, True, OrderedDict([('1776731', '12A'), ('1924017', '16A (HC)')]), mount_hole=True),
    'MSTB_01x07_GF_5.00mm_MH' : generate_params( 7, "MSTB-GF", 5.0, True, True, OrderedDict([('1776744', '12A'), ('1924020', '16A (HC)')]), mount_hole=True),
    'MSTB_01x08_GF_5.00mm_MH' : generate_params( 8, "MSTB-GF", 5.0, True, True, OrderedDict([('1776757', '12A'), ('1924033', '16A (HC)')]), mount_hole=True),
    'MSTB_01x09_GF_5.00mm_MH' : generate_params( 9, "MSTB-GF", 5.0, True, True, OrderedDict([('1776760', '12A'), ('1924046', '16A (HC)')]), mount_hole=True),
    'MSTB_01x10_GF_5.00mm_MH' : generate_params(10, "MSTB-GF", 5.0, True, True, OrderedDict([('1776773', '12A'), ('1924059', '16A (HC)')]), mount_hole=True),
    'MSTB_01x11_GF_5.00mm_MH' : generate_params(11, "MSTB-GF", 5.0, True, True, OrderedDict([('1776786', '12A'), ('1924062', '16A (HC)')]), mount_hole=True),
    'MSTB_01x12_GF_5.00mm_MH' : generate_params(12, "MSTB-GF", 5.0, True, True, OrderedDict([('1776799', '12A'), ('1924075', '16A (HC)')]), mount_hole=True),
    'MSTB_01x13_GF_5.00mm_MH' : generate_params(13, "MSTB-GF", 5.0, True, True, OrderedDict([('1776809', '12A')]), mount_hole=True),
    'MSTB_01x14_GF_5.00mm_MH' : generate_params(14, "MSTB-GF", 5.0, True, True, OrderedDict([('1776812', '12A')]), mount_hole=True),
    'MSTB_01x15_GF_5.00mm_MH' : generate_params(15, "MSTB-GF", 5.0, True, True, OrderedDict([('1776825', '12A')]), mount_hole=True),
    'MSTB_01x16_GF_5.00mm_MH' : generate_params(16, "MSTB-GF", 5.0, True, True, OrderedDict([('1776838', '12A')]), mount_hole=True),
    ###################################################################################################################
    'MSTBVA_01x02_G_5.00mm' : generate_params( 2, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755516', '12A'), ('1924198', '16A (HC)')])),
    'MSTBVA_01x03_G_5.00mm' : generate_params( 3, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755529', '12A'), ('1924208', '16A (HC)')])),
    'MSTBVA_01x04_G_5.00mm' : generate_params( 4, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755532', '12A'), ('1924211', '16A (HC)')])),
    'MSTBVA_01x05_G_5.00mm' : generate_params( 5, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755545', '12A'), ('1924224', '16A (HC)')])),
    'MSTBVA_01x06_G_5.00mm' : generate_params( 6, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755558', '12A'), ('1924237', '16A (HC)')])),
    'MSTBVA_01x07_G_5.00mm' : generate_params( 7, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755561', '12A'), ('1924240', '16A (HC)')])),
    'MSTBVA_01x08_G_5.00mm' : generate_params( 8, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755574', '12A'), ('1924253', '16A (HC)')])),
    'MSTBVA_01x09_G_5.00mm' : generate_params( 9, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755587', '12A'), ('1924266', '16A (HC)')])),
    'MSTBVA_01x10_G_5.00mm' : generate_params(10, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755503', '12A'), ('1924279', '16A (HC)')])),
    'MSTBVA_01x11_G_5.00mm' : generate_params(11, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755590', '12A'), ('1924282', '16A (HC)')])),
    'MSTBVA_01x12_G_5.00mm' : generate_params(12, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755600', '12A'), ('1924295', '16A (HC)')])),
    'MSTBVA_01x13_G_5.00mm' : generate_params(13, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755613', '12A')])),
    'MSTBVA_01x14_G_5.00mm' : generate_params(14, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755626', '12A')])),
    'MSTBVA_01x15_G_5.00mm' : generate_params(15, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755639', '12A')])),
    'MSTBVA_01x16_G_5.00mm' : generate_params(16, "MSTBVA-G", 5.0, False, False, OrderedDict([('1755642', '12A')])),
    ###################################################################################################################
    'MSTBV_01x02_GF_5.00mm' : generate_params( 2, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776883', '12A'), ('1924415', '16A (HC)')])),
    'MSTBV_01x03_GF_5.00mm' : generate_params( 3, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776896', '12A'), ('1924428', '16A (HC)')])),
    'MSTBV_01x04_GF_5.00mm' : generate_params( 4, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776906', '12A'), ('1924431', '16A (HC)')])),
    'MSTBV_01x05_GF_5.00mm' : generate_params( 5, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776919', '12A'), ('1924444', '16A (HC)')])),
    'MSTBV_01x06_GF_5.00mm' : generate_params( 6, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776922', '12A'), ('1924457', '16A (HC)')])),
    'MSTBV_01x07_GF_5.00mm' : generate_params( 7, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776935', '12A'), ('1924460', '16A (HC)')])),
    'MSTBV_01x08_GF_5.00mm' : generate_params( 8, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776948', '12A'), ('1924473', '16A (HC)')])),
    'MSTBV_01x09_GF_5.00mm' : generate_params( 9, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776951', '12A'), ('1924486', '16A (HC)')])),
    'MSTBV_01x10_GF_5.00mm' : generate_params(10, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776964', '12A'), ('1924499', '16A (HC)')])),
    'MSTBV_01x11_GF_5.00mm' : generate_params(11, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776977', '12A'), ('1924509', '16A (HC)')])),
    'MSTBV_01x12_GF_5.00mm' : generate_params(12, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776980', '12A'), ('1924512', '16A (HC)')])),
    'MSTBV_01x13_GF_5.00mm' : generate_params(13, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776993', '12A')])),
    'MSTBV_01x14_GF_5.00mm' : generate_params(14, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776002', '12A')])),
    'MSTBV_01x15_GF_5.00mm' : generate_params(15, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776015', '12A')])),
    'MSTBV_01x16_GF_5.00mm' : generate_params(16, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776028', '12A')])),
    ###################################################################################################################
    'MSTBV_01x02_GF_5.00mm_MH' : generate_params( 2, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776883', '12A'), ('1924415', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x03_GF_5.00mm_MH' : generate_params( 3, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776896', '12A'), ('1924428', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x04_GF_5.00mm_MH' : generate_params( 4, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776906', '12A'), ('1924431', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x05_GF_5.00mm_MH' : generate_params( 5, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776919', '12A'), ('1924444', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x06_GF_5.00mm_MH' : generate_params( 6, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776922', '12A'), ('1924457', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x07_GF_5.00mm_MH' : generate_params( 7, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776935', '12A'), ('1924460', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x08_GF_5.00mm_MH' : generate_params( 8, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776948', '12A'), ('1924473', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x09_GF_5.00mm_MH' : generate_params( 9, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776951', '12A'), ('1924486', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x10_GF_5.00mm_MH' : generate_params(10, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776964', '12A'), ('1924499', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x11_GF_5.00mm_MH' : generate_params(11, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776977', '12A'), ('1924509', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x12_GF_5.00mm_MH' : generate_params(12, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776980', '12A'), ('1924512', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x13_GF_5.00mm_MH' : generate_params(13, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776993', '12A')]), mount_hole=True),
    'MSTBV_01x14_GF_5.00mm_MH' : generate_params(14, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776002', '12A')]), mount_hole=True),
    'MSTBV_01x15_GF_5.00mm_MH' : generate_params(15, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776015', '12A')]), mount_hole=True),
    'MSTBV_01x16_GF_5.00mm_MH' : generate_params(16, "MSTBV-GF", 5.0, False, True, OrderedDict([('1776028', '12A')]), mount_hole=True),
    ##################################################################################################################
    # Pin Pitch 5.08mm
    ##################################################################################################################
    'MSTBA_01x02_G_5.08mm' : generate_params( 2, "MSTBA-G", 5.08, True, False, OrderedDict([('1757242', '12A'), ('1923869', '16A (HC)')])),
    'MSTBA_01x03_G_5.08mm' : generate_params( 3, "MSTBA-G", 5.08, True, False, OrderedDict([('1757255', '12A'), ('1923872', '16A (HC)')])),
    'MSTBA_01x04_G_5.08mm' : generate_params( 4, "MSTBA-G", 5.08, True, False, OrderedDict([('1757268', '12A'), ('1923885', '16A (HC)')])),
    'MSTBA_01x05_G_5.08mm' : generate_params( 5, "MSTBA-G", 5.08, True, False, OrderedDict([('1757271', '12A'), ('1923898', '16A (HC)')])),
    'MSTBA_01x06_G_5.08mm' : generate_params( 6, "MSTBA-G", 5.08, True, False, OrderedDict([('1757284', '12A'), ('1923908', '16A (HC)')])),
    'MSTBA_01x07_G_5.08mm' : generate_params( 7, "MSTBA-G", 5.08, True, False, OrderedDict([('1757297', '12A'), ('1923911', '16A (HC)')])),
    'MSTBA_01x08_G_5.08mm' : generate_params( 8, "MSTBA-G", 5.08, True, False, OrderedDict([('1757307', '12A'), ('1923924', '16A (HC)')])),
    'MSTBA_01x09_G_5.08mm' : generate_params( 9, "MSTBA-G", 5.08, True, False, OrderedDict([('1757310', '12A'), ('1923937', '16A (HC)')])),
    'MSTBA_01x10_G_5.08mm' : generate_params(10, "MSTBA-G", 5.08, True, False, OrderedDict([('1757323', '12A'), ('1923940', '16A (HC)')])),
    'MSTBA_01x11_G_5.08mm' : generate_params(11, "MSTBA-G", 5.08, True, False, OrderedDict([('1757336', '12A'), ('1923953', '16A (HC)')])),
    'MSTBA_01x12_G_5.08mm' : generate_params(12, "MSTBA-G", 5.08, True, False, OrderedDict([('1757349', '12A'), ('1923966', '16A (HC)')])),
    'MSTBA_01x13_G_5.08mm' : generate_params(13, "MSTBA-G", 5.08, True, False, OrderedDict([('1757352', '12A')])),
    'MSTBA_01x14_G_5.08mm' : generate_params(14, "MSTBA-G", 5.08, True, False, OrderedDict([('1757365', '12A')])),
    'MSTBA_01x15_G_5.08mm' : generate_params(15, "MSTBA-G", 5.08, True, False, OrderedDict([('1757378', '12A')])),
    'MSTBA_01x16_G_5.08mm' : generate_params(16, "MSTBA-G", 5.08, True, False, OrderedDict([('1757381', '12A')])),
    ###################################################################################################################
    'MSTB_01x02_GF_5.08mm' : generate_params( 2, "MSTB-GF", 5.08, True, True, OrderedDict([('1776508', '12A'), ('1924088', '16A (HC)')])),
    'MSTB_01x03_GF_5.08mm' : generate_params( 3, "MSTB-GF", 5.08, True, True, OrderedDict([('1776511', '12A'), ('1924091', '16A (HC)')])),
    'MSTB_01x04_GF_5.08mm' : generate_params( 4, "MSTB-GF", 5.08, True, True, OrderedDict([('1776524', '12A'), ('1924101', '16A (HC)')])),
    'MSTB_01x05_GF_5.08mm' : generate_params( 5, "MSTB-GF", 5.08, True, True, OrderedDict([('1776537', '12A'), ('1924114', '16A (HC)')])),
    'MSTB_01x06_GF_5.08mm' : generate_params( 6, "MSTB-GF", 5.08, True, True, OrderedDict([('1776540', '12A'), ('1924127', '16A (HC)')])),
    'MSTB_01x07_GF_5.08mm' : generate_params( 7, "MSTB-GF", 5.08, True, True, OrderedDict([('1776553', '12A'), ('1924130', '16A (HC)')])),
    'MSTB_01x08_GF_5.08mm' : generate_params( 8, "MSTB-GF", 5.08, True, True, OrderedDict([('1776566', '12A'), ('1924143', '16A (HC)')])),
    'MSTB_01x09_GF_5.08mm' : generate_params( 9, "MSTB-GF", 5.08, True, True, OrderedDict([('1776579', '12A'), ('1924156', '16A (HC)')])),
    'MSTB_01x10_GF_5.08mm' : generate_params(10, "MSTB-GF", 5.08, True, True, OrderedDict([('1776582', '12A'), ('1924169', '16A (HC)')])),
    'MSTB_01x11_GF_5.08mm' : generate_params(11, "MSTB-GF", 5.08, True, True, OrderedDict([('1776595', '12A'), ('1924172', '16A (HC)')])),
    'MSTB_01x12_GF_5.08mm' : generate_params(12, "MSTB-GF", 5.08, True, True, OrderedDict([('1776605', '12A'), ('1924185', '16A (HC)')])),
    'MSTB_01x13_GF_5.08mm' : generate_params(13, "MSTB-GF", 5.08, True, True, OrderedDict([('1776618', '12A')])),
    'MSTB_01x14_GF_5.08mm' : generate_params(14, "MSTB-GF", 5.08, True, True, OrderedDict([('1776621', '12A')])),
    'MSTB_01x15_GF_5.08mm' : generate_params(15, "MSTB-GF", 5.08, True, True, OrderedDict([('1776634', '12A')])),
    'MSTB_01x16_GF_5.08mm' : generate_params(16, "MSTB-GF", 5.08, True, True, OrderedDict([('1776647', '12A')])),
    ###################################################################################################################
    'MSTB_01x02_GF_5.08mm_MH' : generate_params( 2, "MSTB-GF", 5.08, True, True, OrderedDict([('1776508', '12A'), ('1924088', '16A (HC)')]), mount_hole=True),
    'MSTB_01x03_GF_5.08mm_MH' : generate_params( 3, "MSTB-GF", 5.08, True, True, OrderedDict([('1776511', '12A'), ('1924091', '16A (HC)')]), mount_hole=True),
    'MSTB_01x04_GF_5.08mm_MH' : generate_params( 4, "MSTB-GF", 5.08, True, True, OrderedDict([('1776524', '12A'), ('1924101', '16A (HC)')]), mount_hole=True),
    'MSTB_01x05_GF_5.08mm_MH' : generate_params( 5, "MSTB-GF", 5.08, True, True, OrderedDict([('1776537', '12A'), ('1924114', '16A (HC)')]), mount_hole=True),
    'MSTB_01x06_GF_5.08mm_MH' : generate_params( 6, "MSTB-GF", 5.08, True, True, OrderedDict([('1776540', '12A'), ('1924127', '16A (HC)')]), mount_hole=True),
    'MSTB_01x07_GF_5.08mm_MH' : generate_params( 7, "MSTB-GF", 5.08, True, True, OrderedDict([('1776553', '12A'), ('1924130', '16A (HC)')]), mount_hole=True),
    'MSTB_01x08_GF_5.08mm_MH' : generate_params( 8, "MSTB-GF", 5.08, True, True, OrderedDict([('1776566', '12A'), ('1924143', '16A (HC)')]), mount_hole=True),
    'MSTB_01x09_GF_5.08mm_MH' : generate_params( 9, "MSTB-GF", 5.08, True, True, OrderedDict([('1776579', '12A'), ('1924156', '16A (HC)')]), mount_hole=True),
    'MSTB_01x10_GF_5.08mm_MH' : generate_params(10, "MSTB-GF", 5.08, True, True, OrderedDict([('1776582', '12A'), ('1924169', '16A (HC)')]), mount_hole=True),
    'MSTB_01x11_GF_5.08mm_MH' : generate_params(11, "MSTB-GF", 5.08, True, True, OrderedDict([('1776595', '12A'), ('1924172', '16A (HC)')]), mount_hole=True),
    'MSTB_01x12_GF_5.08mm_MH' : generate_params(12, "MSTB-GF", 5.08, True, True, OrderedDict([('1776605', '12A'), ('1924185', '16A (HC)')]), mount_hole=True),
    'MSTB_01x13_GF_5.08mm_MH' : generate_params(13, "MSTB-GF", 5.08, True, True, OrderedDict([('1776618', '12A')]), mount_hole=True),
    'MSTB_01x14_GF_5.08mm_MH' : generate_params(14, "MSTB-GF", 5.08, True, True, OrderedDict([('1776621', '12A')]), mount_hole=True),
    'MSTB_01x15_GF_5.08mm_MH' : generate_params(15, "MSTB-GF", 5.08, True, True, OrderedDict([('1776634', '12A')]), mount_hole=True),
    'MSTB_01x16_GF_5.08mm_MH' : generate_params(16, "MSTB-GF", 5.08, True, True, OrderedDict([('1776647', '12A')]), mount_hole=True),
    ###################################################################################################################
    'MSTBVA_01x02_G_5.08mm' : generate_params( 2, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755736', '12A'), ('1924305', '16A (HC)')])),
    'MSTBVA_01x03_G_5.08mm' : generate_params( 3, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755749', '12A'), ('1924318', '16A (HC)')])),
    'MSTBVA_01x04_G_5.08mm' : generate_params( 4, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755752', '12A'), ('1924321', '16A (HC)')])),
    'MSTBVA_01x05_G_5.08mm' : generate_params( 5, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755765', '12A'), ('1924334', '16A (HC)')])),
    'MSTBVA_01x06_G_5.08mm' : generate_params( 6, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755778', '12A'), ('1924347', '16A (HC)')])),
    'MSTBVA_01x07_G_5.08mm' : generate_params( 7, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755781', '12A'), ('1924350', '16A (HC)')])),
    'MSTBVA_01x08_G_5.08mm' : generate_params( 8, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755794', '12A'), ('1924363', '16A (HC)')])),
    'MSTBVA_01x09_G_5.08mm' : generate_params( 9, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755804', '12A'), ('1924376', '16A (HC)')])),
    'MSTBVA_01x10_G_5.08mm' : generate_params(10, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755817', '12A'), ('1924389', '16A (HC)')])),
    'MSTBVA_01x11_G_5.08mm' : generate_params(11, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755820', '12A'), ('1924392', '16A (HC)')])),
    'MSTBVA_01x12_G_5.08mm' : generate_params(12, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755833', '12A'), ('1924402', '16A (HC)')])),
    'MSTBVA_01x13_G_5.08mm' : generate_params(13, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755846', '12A')])),
    'MSTBVA_01x14_G_5.08mm' : generate_params(14, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755859', '12A')])),
    'MSTBVA_01x15_G_5.08mm' : generate_params(15, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755862', '12A')])),
    'MSTBVA_01x16_G_5.08mm' : generate_params(16, "MSTBVA-G", 5.08, False, False, OrderedDict([('1755875', '12A')])),
    ###################################################################################################################
    'MSTBV_01x02_GF_5.08mm' : generate_params( 2, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777073', '12A'), ('1924525', '16A (HC)')])),
    'MSTBV_01x03_GF_5.08mm' : generate_params( 3, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777086', '12A'), ('1924538', '16A (HC)')])),
    'MSTBV_01x04_GF_5.08mm' : generate_params( 4, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777099', '12A'), ('1924541', '16A (HC)')])),
    'MSTBV_01x05_GF_5.08mm' : generate_params( 5, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777109', '12A'), ('1924554', '16A (HC)')])),
    'MSTBV_01x06_GF_5.08mm' : generate_params( 6, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777112', '12A'), ('1924567', '16A (HC)')])),
    'MSTBV_01x07_GF_5.08mm' : generate_params( 7, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777125', '12A'), ('1924570', '16A (HC)')])),
    'MSTBV_01x08_GF_5.08mm' : generate_params( 8, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777138', '12A'), ('1924583', '16A (HC)')])),
    'MSTBV_01x09_GF_5.08mm' : generate_params( 9, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777141', '12A'), ('1924596', '16A (HC)')])),
    'MSTBV_01x10_GF_5.08mm' : generate_params(10, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777154', '12A'), ('1924606', '16A (HC)')])),
    'MSTBV_01x11_GF_5.08mm' : generate_params(11, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777167', '12A'), ('1924619', '16A (HC)')])),
    'MSTBV_01x12_GF_5.08mm' : generate_params(12, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777170', '12A'), ('1924622', '16A (HC)')])),
    'MSTBV_01x13_GF_5.08mm' : generate_params(13, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777183', '12A')])),
    'MSTBV_01x14_GF_5.08mm' : generate_params(14, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777196', '12A')])),
    'MSTBV_01x15_GF_5.08mm' : generate_params(15, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777206', '12A')])),
    'MSTBV_01x16_GF_5.08mm' : generate_params(16, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777219', '12A')])),
    ###################################################################################################################
    'MSTBV_01x02_GF_5.08mm_MH' : generate_params( 2, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777073', '12A'), ('1924525', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x03_GF_5.08mm_MH' : generate_params( 3, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777086', '12A'), ('1924538', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x04_GF_5.08mm_MH' : generate_params( 4, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777099', '12A'), ('1924541', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x05_GF_5.08mm_MH' : generate_params( 5, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777109', '12A'), ('1924554', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x06_GF_5.08mm_MH' : generate_params( 6, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777112', '12A'), ('1924567', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x07_GF_5.08mm_MH' : generate_params( 7, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777125', '12A'), ('1924570', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x08_GF_5.08mm_MH' : generate_params( 8, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777138', '12A'), ('1924583', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x09_GF_5.08mm_MH' : generate_params( 9, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777141', '12A'), ('1924596', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x10_GF_5.08mm_MH' : generate_params(10, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777154', '12A'), ('1924606', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x11_GF_5.08mm_MH' : generate_params(11, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777167', '12A'), ('1924619', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x12_GF_5.08mm_MH' : generate_params(12, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777170', '12A'), ('1924622', '16A (HC)')]), mount_hole=True),
    'MSTBV_01x13_GF_5.08mm_MH' : generate_params(13, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777183', '12A')]), mount_hole=True),
    'MSTBV_01x14_GF_5.08mm_MH' : generate_params(14, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777196', '12A')]), mount_hole=True),
    'MSTBV_01x15_GF_5.08mm_MH' : generate_params(15, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777206', '12A')]), mount_hole=True),
    'MSTBV_01x16_GF_5.08mm_MH' : generate_params(16, "MSTBV-GF", 5.08, False, True, OrderedDict([('1777219', '12A')]), mount_hole=True),
    ##################################################################################################################
    # High Voltage Versions (pin pitch 7.5mm)
    ##################################################################################################################
    'GMSTBA_01x02_G_7.50mm' : generate_params( 2, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766343', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x03_G_7.50mm' : generate_params( 3, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766356', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x04_G_7.50mm' : generate_params( 4, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766369', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x05_G_7.50mm' : generate_params( 5, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766372', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x06_G_7.50mm' : generate_params( 6, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766385', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x07_G_7.50mm' : generate_params( 7, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766398', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x08_G_7.50mm' : generate_params( 8, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766408', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x09_G_7.50mm' : generate_params( 9, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766411', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x10_G_7.50mm' : generate_params(10, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766424', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x11_G_7.50mm' : generate_params(11, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766437', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x12_G_7.50mm' : generate_params(12, "GMSTBA-G", 7.50, True, False, OrderedDict([('1766440', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    ##################################################################################################################
    'GMSTBVA_01x02_G_7.50mm' : generate_params( 2, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766660', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x03_G_7.50mm' : generate_params( 3, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766673', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x04_G_7.50mm' : generate_params( 4, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766686', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x05_G_7.50mm' : generate_params( 5, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766699', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x06_G_7.50mm' : generate_params( 6, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766709', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x07_G_7.50mm' : generate_params( 7, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766712', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x08_G_7.50mm' : generate_params( 8, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766725', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x09_G_7.50mm' : generate_params( 9, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766738', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x10_G_7.50mm' : generate_params(10, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766741', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x11_G_7.50mm' : generate_params(11, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766754', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x12_G_7.50mm' : generate_params(12, "GMSTBVA-G", 7.50, False, False, OrderedDict([('1766767', '12A 630V')]), side_to_pin=3.75, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    ##################################################################################################################
    # High Voltage Versions (pin pitch 7.62mm)
    ##################################################################################################################
    'GMSTBA_01x02_G_7.62mm' : generate_params( 2, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766233', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x03_G_7.62mm' : generate_params( 3, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766246', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x04_G_7.62mm' : generate_params( 4, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766259', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x05_G_7.62mm' : generate_params( 5, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766262', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x06_G_7.62mm' : generate_params( 6, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766275', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x07_G_7.62mm' : generate_params( 7, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766288', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x08_G_7.62mm' : generate_params( 8, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766291', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x09_G_7.62mm' : generate_params( 9, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766301', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x10_G_7.62mm' : generate_params(10, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766314', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x11_G_7.62mm' : generate_params(11, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766327', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBA_01x12_G_7.62mm' : generate_params(12, "GMSTBA-G", 7.62, True, False, OrderedDict([('1766330', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    ###################################################################################################################
    'GMSTB_01x02_GF_7.62mm' : generate_params( 2, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806229', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x03_GF_7.62mm' : generate_params( 3, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806232', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x04_GF_7.62mm' : generate_params( 4, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806245', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x05_GF_7.62mm' : generate_params( 5, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806258', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x06_GF_7.62mm' : generate_params( 6, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806261', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x07_GF_7.62mm' : generate_params( 7, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806274', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x08_GF_7.62mm' : generate_params( 8, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806287', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x09_GF_7.62mm' : generate_params( 9, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806290', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x10_GF_7.62mm' : generate_params(10, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806300', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x11_GF_7.62mm' : generate_params(11, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806313', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x12_GF_7.62mm' : generate_params(12, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806326', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    ###################################################################################################################
    'GMSTB_01x02_GF_7.62mm_MH' : generate_params( 2, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806229', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x03_GF_7.62mm_MH' : generate_params( 3, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806232', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x04_GF_7.62mm_MH' : generate_params( 4, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806245', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x05_GF_7.62mm_MH' : generate_params( 5, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806258', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x06_GF_7.62mm_MH' : generate_params( 6, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806261', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x07_GF_7.62mm_MH' : generate_params( 7, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806274', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x08_GF_7.62mm_MH' : generate_params( 8, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806287', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x09_GF_7.62mm_MH' : generate_params( 9, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806290', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x10_GF_7.62mm_MH' : generate_params(10, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806300', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x11_GF_7.62mm_MH' : generate_params(11, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806313', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTB_01x12_GF_7.62mm_MH' : generate_params(12, "GMSTB-GF", 7.62, True, True, OrderedDict([('1806326', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    ###################################################################################################################
    'GMSTBVA_01x02_G_7.62mm' : generate_params( 2, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766770', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x03_G_7.62mm' : generate_params( 3, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766783', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x04_G_7.62mm' : generate_params( 4, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766796', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x05_G_7.62mm' : generate_params( 5, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766806', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x06_G_7.62mm' : generate_params( 6, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766819', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x07_G_7.62mm' : generate_params( 7, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766822', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x08_G_7.62mm' : generate_params( 8, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766835', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x09_G_7.62mm' : generate_params( 9, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766848', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x10_G_7.62mm' : generate_params(10, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766851', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x11_G_7.62mm' : generate_params(11, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766864', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBVA_01x12_G_7.62mm' : generate_params(12, "GMSTBVA-G", 7.62, False, False, OrderedDict([('1766877', '12A 630V')]), side_to_pin=3.81, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    ###################################################################################################################
    'GMSTBV_01x02_GF_7.62mm' : generate_params( 2, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829154', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x03_GF_7.62mm' : generate_params( 3, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829167', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x04_GF_7.62mm' : generate_params( 4, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829170', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x05_GF_7.62mm' : generate_params( 5, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829183', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x06_GF_7.62mm' : generate_params( 6, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829196', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x07_GF_7.62mm' : generate_params( 7, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829206', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x08_GF_7.62mm' : generate_params( 8, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829219', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x09_GF_7.62mm' : generate_params( 9, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829222', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x10_GF_7.62mm' : generate_params(10, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829235', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x11_GF_7.62mm' : generate_params(11, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829248', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x12_GF_7.62mm' : generate_params(12, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829251', '12A 630V')]), mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    ###################################################################################################################
    'GMSTBV_01x02_GF_7.62mm_MH' : generate_params( 2, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829154', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x03_GF_7.62mm_MH' : generate_params( 3, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829167', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x04_GF_7.62mm_MH' : generate_params( 4, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829170', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x05_GF_7.62mm_MH' : generate_params( 5, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829183', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x06_GF_7.62mm_MH' : generate_params( 6, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829196', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x07_GF_7.62mm_MH' : generate_params( 7, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829206', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x08_GF_7.62mm_MH' : generate_params( 8, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829219', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x09_GF_7.62mm_MH' : generate_params( 9, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829222', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x10_GF_7.62mm_MH' : generate_params(10, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829235', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x11_GF_7.62mm_MH' : generate_params(11, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829248', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance),
    'GMSTBV_01x12_GF_7.62mm_MH' : generate_params(12, "GMSTBV-GF", 7.62, False, True, OrderedDict([('1829251', '12A 630V')]), mount_hole=True, mount_hole_to_pin=6.1, side_to_pin=9.1, min_pad_to_pad_clearance=seriesParams.GMSTB_min_pad_to_pad_clearance)
}

#lock_cutout=

def dimensions(params):
    lenght = (params.num_pins-1)*params.pin_pitch + 2*params.side_to_pin
    width = 12 if params.angled else 8.6
    upper_to_pin = -2 if params.angled else -8.6+3.8
    left_to_pin = -params.side_to_pin
    mount_hole_y = 2.5 if params.angled else 0.0
    mount_hole_left = [-params.mount_hole_to_pin,mount_hole_y]
    mount_hole_right = [(params.num_pins-1)*params.pin_pitch+params.mount_hole_to_pin,mount_hole_y]
    inner_len = params.num_pins*params.pin_pitch-1.6 + (0 if params.pin_pitch>5.08 else 2)
    return lenght, width, upper_to_pin, left_to_pin,\
        mount_hole_left, mount_hole_right, inner_len

def generate_description(params):
    d = "Generic Phoenix Contact connector footprint for series: " + params.series_name + "; number of pins: " + ("%02d" %params.num_pins) + "; pin pitch: " + (('%.2f' % params.pin_pitch))\
        +"mm" + ('; Angled' if params.angled else '; Vertical')\
        + ('; threaded flange' + ('; footprint includes mount hole for mounting screw: ' + seriesParams.mount_screw_info if params.mount_hole else '') if params.flanged else '')
    for order_num, info in params.order_info.items():
        d += " || order number: " + order_num + " " + info
    return d
