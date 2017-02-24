
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
