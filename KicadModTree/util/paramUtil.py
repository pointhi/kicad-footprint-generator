# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016-2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
# (C) 2018 by Rene Poeschl, github @poeschlr


from KicadModTree.Vector import *


def toNumberArray(value, length=2, min_value=1, member_type=int):
    r""" Convert value into an array of given type with given length

    :param value:
        Possible input types:
          * numnber (int or float) -> returns array filled with copies of value
          * dict -> arreay created with values for keys 'x', 'y', 'z'.
            dict only supported for len 2 and 3
          * list or tuple -> truncated to length
          * Vector -> truncated to lenght

    :param length: (``int``) -- default: 2
        Defines the length of the resulting array

    :min_value: (``int``) -- default: 1
        Defines the minimum alowed value (raise value error if too low)
        None -> No check

    :param mamber_type: (``type``) -- default: <type: int>
        all members of the array will be converted to this type
    """
    if type(value) in [int, float]:
        result = [value for i in range(length)]
    elif type(value) is dict:
        if length in [2, 3]:
            KEYS = ['x', 'y', 'z']
            result = [value[KEYS[i]] for i in range(length)]
        else:
            raise TypeError('Dict only supported for length 2 or 3.')
    elif type(value) in [list, tuple]:
        if len(value) >= length:
            result = value[:length]
    elif type(value) in [Vector2D, Vector3D]:
        if len(value) < length:
            raise TypeError(
                'Vector dimensions ({}) are too low. Must be at least {}'.format(len(value), length))
        result = list(value)
    else:
        raise TypeError('Unsupported type: {}'.format(type(value)))

    result = [member_type(v) for v in result]

    if min_value is not None and isAnyLarger(result, min_value, False):
        raise ValueError(
            "At least one value in ({}) too small. Linit is {}.".format(result, min_value))

    return result


def toIntArray(value, length=2, min_value=1):
    r""" Convert value into an array of ints of given length

    :param value:
        Possible input types:
          * numnber (int or float) -> returns array filled with copies of value
          * dict -> arreay created with values for keys 'x', 'y', 'z'.
            dict only supported for len 2 and 3
          * list or tuple -> truncated to length
          * Vector -> truncated to lenght

    :param length: (``int``) -- default: 2
        Defines the length of the resulting array

    :min_value: (``int``) -- default: 1
        Defines the minimum alowed value (raise value error if too low)
        None -> No check
    """
    return toNumberArray(value, length, min_value, member_type=int)


def toFloatArray(value, length=2, min_value=1):
    r""" Convert value into an array of floats of given length

    :param value:
        Possible input types:
          * numnber (int or float) -> returns array filled with copies of value
          * dict -> arreay created with values for keys 'x', 'y', 'z'.
            dict only supported for len 2 and 3
          * list or tuple -> truncated to length
          * Vector -> truncated to lenght

    :param length: (``int``) -- default: 2
        Defines the length of the resulting array

    :min_value: (``int``) -- default: 1
        Defines the minimum alowed value (raise value error if too low)
        None -> No check
    """
    return toNumberArray(value, length, min_value, member_type=float)


def isAnyLarger(values, low_limits, must_be_larger=False):
    r"""Check if any value in the source array is larger than its respective limit

    :param value: (``itterable``) --
        The values to check.

    :param low_limit: (``int``)
        Defines the minimum alowed value (raise value error if too low)
        None -> No check

    :param must_be_larger: (``bool``) -- default: True
       Defines if the number must be larger than the limit or if the limit is
       the minimum value.
    """
    limits = toFloatArray(low_limits, len(values), min_value=None)
    for v, l in zip(values, limits):
        if v < l or (v <= l and must_be_larger):
            return True
    return False


def toVectorUseCopyIfNumber(value, length=2, low_limit=None, must_be_larger=True):
    r""" Convert value into an vector of given dimension

    :param value:
        The value to convert.
        Supported types are all types allowed for vector constructor plus int/float.
        If int/float vector will be initialized with the correct number of copies.

    :param length: (2 or 3) -- default: 2
        Defines the dimension of the resulting vector

    :param low_limit: (``int``) -- default: None
        Defines the minimum alowed value (raise value error if too low)
        None -> No check

    :param must_be_larger: (``bool``) -- default: True
       Defines if the number must be larger than the limit or if the limit is
       the minimum value.
    """

    if type(value) in [int, float]:
        result = [value for i in range(length)]
    else:
        result = value

    if length == 2:
        result = Vector2D(result)
    elif length == 3:
        result = Vector3D(result)
    else:
        raise ValueError("length must be 2 or 3")

    if low_limit is not None and isAnyLarger(result, low_limit, must_be_larger):
        raise ValueError("One value in ({}) too small. Limit is {}.".format(result, low_limit))

    return result


def getOptionalNumberTypeParam(
        kwargs, param_name, default_value=None,
        low_limit=None, high_limit=None, allow_equal_limit=True):
    r""" Get a named parameter from packed dict and guarantee it is a number (float or int)

    :param param_name:
        The name of the parameter (=key)

    :param default_value: -- default: None
        The value to be used if the parameter is not in the dict

    :param low_limit: -- default: None
        The minimum allowable value

    :param high_limit: -- default: None
        The maximum allowable value

    :param allow_equal_limit: -- default: True
        Limits are included in range of allowable values
        (min <= x <= max if true else min < x < max)

    :param **kwargs:
        The parameters as packed dict
    """
    val = kwargs.get(param_name, default_value)
    if val is not None:
        if type(val) not in [int, float]:
            raise TypeError('{} needs to be of type int or float'.format(param_name))
        if low_limit is not None:
            if val < low_limit or (val == low_limit and not allow_equal_limit):
                raise ValueError(
                    '{} with value {} violates the low limit of {}'
                    .format(param_name, val, low_limit))
        if high_limit is not None:
            if val > high_limit or (val == low_limit and not allow_equal_limit):
                raise ValueError(
                    '{} with value {} violates the high limit of {}'
                    .format(param_name, val, high_limit))
    return val


def round_to(value, base):
    r""" Round a value to a given base value

    :param value:
        The value to round

    :param base:
        The base value. The resulting value will be rounded to a multiple of it

    :return:
        The rounded value
    """

    return round(value/base) * base
