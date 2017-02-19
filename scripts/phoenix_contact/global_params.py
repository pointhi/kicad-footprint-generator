
class globalParams():
    pin_layers = ['*.Cu', '*.Mask'] #, '*.Paste' through hole: no paste!
    mount_hole_layers = ['*.Cu', '*.Mask']
    manufacturer_tag = "phoenix_contact"

def generate_keyword_str(model):
    return manufacturer_tag + " connector " + model

def generate_footprint_name(series_name, num_pins, pin_pitch, angled, mount_hole, flanged):
    return "PhoenixContact_" + series_name + "_"+ ('%02d' % num_pins) + "x"\
    + ('%.2f' % pin_pitch) + "mm_" + ('Angled' if angled else 'Vertical')\
    + ('_ThreadedFlange' + ('_MountHole' if mount_hole else '') if flanged else '')

DRAW_PIN_1_MARKER = 1

def create_marker_poly(bottom_y, center_x=0):
    marker_width=0.6
    marker_height=0.6

    marker_top=bottom_y-marker_height
    marker_poly=[
        {'x':center_x, 'y':bottom_y},
        {'x':center_x+marker_width/2, 'y':marker_top},
        {'x':center_x-marker_width/2, 'y':marker_top},
        {'x':center_x, 'y':bottom_y}
    ]

    return marker_poly
