def roundToBase(value, base):
    if base == 0:
        return value
    return round(value/base) * base
