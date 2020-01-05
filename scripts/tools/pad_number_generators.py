"""
Pad number generator functions.

Some ICs have a non-standard pin numbering scheme.
Using the generators an iterable is generated following the scheme.

Available generators:
----------------------
- increment: Is a simple generator that increments the pin number by one.
- cw_dual: Generates pin numbers counting clockwise from the starting position
- ccw_dual: Generates pin numbers counting counter-clockwise from the starting position

Examples:
---------
To use a generator add the following to the device config:

  pad_numbers:
    generator: 'ccw_dual'
    axis: 'x'

"""


def increment(pincount, init=1, **kwargs):
    i = init
    while i <= pincount:
        yield i
        i += 1


def _get_pin_cw(pincount, loc):
    """Helper function to locate pin number for cw_dual.

    Args:
        pincount: Total number of pins
        loc: Starting location

    Returns:
        pin_number: Starting pin number
    """
    pins_per_side = pincount // 2
    if loc == "top_left":
        return 0
    elif loc == "bottom_left":
        return pins_per_side * 2 + 1
    elif loc == "bottom_right":
        return pins_per_side
    elif loc == "top_right":
        return pins_per_side + 1
    return 0


def _get_pin_ccw(pincount, loc):
    """Helper function to locate pin number for ccw_dual.

        Args:
            pincount: Total number of pins
            loc: Starting location

        Returns:
            pin_number: Starting pin number
    """
    pins_per_side = pincount // 2
    if loc == "top_left":
        return 0
    elif loc == "bottom_left":
        return pins_per_side + 1
    elif loc == "bottom_right":
        return pins_per_side
    elif loc == "top_right":
        return pins_per_side * 2 + 1
    return 0


def clockwise_dual(pincount, init=1, start="top_left", axis="x", **kwargs):
    """Generator for dual row packages counting clockwise.

    Args:
        pincount: Total number of pins
        init: Initial starting count (default: 1)
        start: The starting corner, top/bottom - left/right
        axis: Pin axis, either x or y. Is depended on num_pins_{x,y}
        **kwargs: Other keyword arguments

    Returns:
        Iterator
    """
    i = _get_pin_cw(pincount, start)

    if axis == "y":
        pins = iter(range(pincount, 0, -1))
    else:
        pins = iter(range(pincount))

    for ind in pins:
        yield ((i + ind) % pincount) + init


def counter_clockwise_dual(pincount, init=1, start="top_left", axis="x", **kwargs):
    """Generator for dual row packages counting counter clockwise.

     Args:
         pincount: Total number of pins
         init: Initial starting count (default: 1)
         start: The starting corner, top/bottom - left/right
         axis: Pin axis, either x or y. Is depended on num_pins_{x,y}
         **kwargs: Other keyword arguments

     Returns:
         Iterator
     """
    i = _get_pin_ccw(pincount, start)

    if axis == "x":
        pins = iter(range(pincount, 0, -1))
    else:
        pins = iter(range(pincount))

    for ind in pins:
        yield ((i + ind) % pincount) + init


# Add available generators to the dictionary
generators = {
    "increment": increment,
    "cw_dual": clockwise_dual,
    "ccw_dual": counter_clockwise_dual,
}


def get_generator(device_params):
    """Returns a pad number iterator based on device_params and selected generator.
    Fallback to plain increment.

    Args:
        device_params: Device parameters dictionary 

    Returns:
        Pad number iterator

    Raises:
        KeyError: If generator not available
    """
    # Fallback to plain increment
    pincount = device_params["num_pins_x"] * 2 + device_params["num_pins_y"] * 2
    pad_nums = device_params.get("pad_numbers")

    if not pad_nums:
        return generators["increment"](pincount)

    init = pad_nums.get("init", 1)

    gen = generators.get(pad_nums.get("generator"))
    if not gen:
        gens = ", ".join(generators.keys())
        pad_generator = pad_nums.get("generator")
        raise KeyError("{}: Use one of [{}]".format(pad_generator, gens))

    iterator = gen(pincount, init, **pad_nums)
    return iterator
