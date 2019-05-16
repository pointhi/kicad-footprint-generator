from __future__ import division
import math
import re

def roundToBase(value, base):
    return round(value/base) * base

class TolerancedSize():
    def to_metric(value, unit):
        if unit == "inch":
            factor = 25.4
        elif unit == "mil":
            factor = 25.4/1000
        else:
            factor = 1
        return value * factor

    def __init__(self, minimum=None, nominal=None, maximum=None, tolerance=None, unit=None):


        if nominal is not None:
            self.nominal = nominal
        else:
            if minimum is None or maximum is None:
                raise KeyError("Either nominal or minimum and maximum must be given")
            self.nominal = (minimum + maximum)/2

        if minimum is not None and maximum is not None:
            self.minimum = minimum
            self.maximum = maximum
        elif tolerance is not None:
            if type(tolerance) in [int, float]:
                self.minimum = self.nominal - tolerance
                self.maximum = self.nominal + tolerance
            elif len(tolerance) == 2:
                if tolerance[0] < 0:
                    self.minimum = self.nominal + tolerance[0]
                    self.maximum = self.nominal + tolerance[1]
                elif tolerance[1] < 0:
                    self.minimum = self.nominal + tolerance[1]
                    self.maximum = self.nominal + tolerance[0]
                else:
                    self.minimum = self.nominal - tolerance[0]
                    self.maximum = self.nominal + tolerance[1]
        else:
            self.minimum = self.nominal
            self.maximum = self.nominal

        if self.maximum < self.minimum:
            raise ValueError("Maximum is smaller than minimum. Tolerance ranges given wrong or parameters confused.")

        self.minimum = TolerancedSize.to_metric(self.minimum, unit)
        self.nominal = TolerancedSize.to_metric(self.nominal, unit)
        self.maximum = TolerancedSize.to_metric(self.maximum, unit)

        self.ipc_tol = self.maximum - self.minimum
        self.ipc_tol_RMS = self.ipc_tol
        self.maximum_RMS = self.maximum
        self.minimum_RMS = self.minimum

    def updateRMS(self, tolerances):
        ipc_tol_RMS = 0
        for t in tolerances:
            ipc_tol_RMS += t**2

        self.ipc_tol_RMS = math.sqrt(ipc_tol_RMS)
        if self.ipc_tol_RMS > self.ipc_tol:
            if roundToBase(self.ipc_tol_RMS, 1e-6) > roundToBase(self.ipc_tol, 1e-6):
                raise ValueError(
                    "RMS tolerance larger than normal tolerance. Did you give the wrong tolerances?\ntol(RMS): {} tol: {}"\
                    .format(self.ipc_tol_RMS, self.ipc_tol))
            # the discrepancy most likely comes from floating point errors. Ignore it.
            self.ipc_tol_RMS = self.ipc_tol

        self.maximum_RMS = self.maximum - (self.ipc_tol - self.ipc_tol_RMS)/2
        self.minimum_RMS = self.minimum + (self.ipc_tol - self.ipc_tol_RMS)/2

    def __add__(self, other):
        if type(other) in [int, float]:
            result = TolerancedSize(
                minimum = self.minimum + other,
                maximum = self.maximum + other
                )
            return result

        result = TolerancedSize(
            minimum = self.minimum + other.minimum,
            maximum = self.maximum + other.maximum
            )
        result.updateRMS([self.ipc_tol_RMS, other.ipc_tol_RMS])
        return result

    def __sub__(self, other):
        if type(other) in [int, float]:
            result = TolerancedSize(
                minimum = self.minimum - other,
                maximum = self.maximum - other
                )
            return result

        result = TolerancedSize(
            minimum = self.minimum - other.maximum,
            maximum = self.maximum - other.minimum
            )
        result.updateRMS([self.ipc_tol_RMS, other.ipc_tol_RMS])
        return result

    def __mul__(self, other):
        if type(other) not in [int, float]:
            raise NotImplementedError("Only multiplication with int and float is implemented right now.")
        result = TolerancedSize(
            minimum = self.minimum*other,
            maximum = self.maximum*other
            )
        result.updateRMS([self.ipc_tol_RMS*math.sqrt(other)])
        return result

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        if type(other) not in [int, float]:
            raise NotImplementedError("Only multiplication with int and float is implemented right now.")
        result = TolerancedSize(
            minimum = self.minimum/other,
            maximum = self.maximum/other
            )
        result.updateRMS([self.ipc_tol_RMS/math.sqrt(other)])
        return result

    def __floordiv__(self, other):
        if type(other) not in [int, float]:
            raise NotImplementedError("Only multiplication with int and float is implemented right now.")
        result = TolerancedSize(
            minimum = self.minimum//other,
            maximum = self.maximum//other
            )
        result.updateRMS([self.ipc_tol_RMS//math.sqrt(other)])
        return result

    @staticmethod
    def fromString(input, unit=None):
        minimum = None
        nominal = None
        maximum = None
        tolerance = None

        s = re.sub(r'\s+', '', str(input))
        if type(input) in [int, float]:
            nominal = input
        elif "+/-" in s:
            tokens = s.split("+/-")
            nominal = float(tokens[0])
            tolerance = float(tokens[1])
        elif '+' in s and '-' in s:
            if s.count('+') > 1 or s.count('-') > 1:
                raise ValueError("Illegal dimension specifier: {}\n\tToo many tolerance specifiers. Expected nom+tolp-toln".format(input))
            idxp = s.find('+')
            idxn = s.find('-')

            nominal = float(s[0:min(idxp, idxn)])
            tolerance=[
                float(s[idxn : idxp if idxn<idxp else None]),
                float(s[idxp : idxn if idxn>idxp else None])]
        elif '...' in s or '..' in s:
            s = s.replace('...', '..')
            tokens = s.split('..')
            if len(tokens) > 3:
                raise ValueError("Illegal dimension specifier: {}\n\tToo many tokens seperated by '...' (Valid options are min...max or min...nom...max)".format(input))
            minimum = float(tokens[0])
            maximum = float(tokens[-1])
            if len(tokens) == 3:
                nominal = float(tokens[1])
        else:
            try:
                nominal = float(s)
            except Exception as e:
                raise ValueError("Dimension specifier not recogniced: {}\n\t Valid options are nom, nom+/-tol, nom+tolp-toln, min...max or min...nom...max".format(input)) from e

        return TolerancedSize(
            minimum=minimum,
            nominal=nominal,
            maximum=maximum,
            tolerance=tolerance,
            unit=unit
            )

    @staticmethod
    def fromYaml(yaml, base_name=None, unit=None):
        if base_name is not None:
            if base_name+"_min" in yaml or base_name+"_max" in yaml or base_name+"_tol" in yaml:
                return TolerancedSize(
                    minimum=yaml.get(base_name+"_min"),
                    nominal=yaml.get(base_name),
                    maximum=yaml.get(base_name+"_max"),
                    tolerance=yaml.get(base_name+"_tol")
                    )
            return TolerancedSize.fromYaml(yaml.get(base_name), unit=unit)

        elif type(yaml) is dict:
            return TolerancedSize(
                minimum=yaml.get("minimum"),
                nominal=yaml.get("nominal"),
                maximum=yaml.get("maximum"),
                tolerance=yaml.get("tolerance"),
                unit=unit
                )
        else:
            return TolerancedSize.fromString(yaml, unit)

    def __str__(self):
        return 'nom: {}, min: {}, max: {}  | min_rms: {}, max_rms: {}'.format(self.nominal, self.minimum, self.maximum, self.minimum_RMS, self.maximum_RMS)

def ipc_body_edge_inside(ipc_data, ipc_round_base, manf_tol, body_size, lead_width,
        lead_len=None, lead_inside=None, heel_reduction=0):
    pull_back = TolerancedSize(nominal=0)

    return ipc_body_edge_inside_pull_back(
                ipc_data, ipc_round_base, manf_tol, body_size, lead_width,
                lead_len=lead_len, lead_inside=lead_inside, pull_back=pull_back,
                heel_reduction=heel_reduction
                )

def ipc_body_edge_inside_pull_back(ipc_data, ipc_round_base, manf_tol, body_size, lead_width,
        lead_len=None, lead_inside=None, body_to_inside_lead_edge=None, pull_back=None, lead_outside=None, heel_reduction=0):
    # Zmax = Lmin + 2JT + √(CL^2 + F^2 + P^2)
    # Gmin = Smax − 2JH − √(CS^2 + F^2 + P^2)
    # Xmax = Wmin + 2JS + √(CW^2 + F^2 + P^2)

    # Some manufacturers do not list the terminal spacing (S) in their datasheet but list the terminal lenght (T)
    # Then one can calculate
    # Stol(RMS) = √(Ltol^2 + 2*^2)
    # Smin = Lmin - 2*Tmax
    # Smax(RMS) = Smin + Stol(RMS)

    F = manf_tol.get('manufacturing_tolerance', 0.1)
    P = manf_tol.get('placement_tolerance', 0.05)

    if lead_outside is None:
        if pull_back is None:
            raise KeyError("Either lead outside or pull back distance must be given")
        lead_outside = body_size - pull_back*2

    if lead_inside is not None:
        S = lead_inside
    elif lead_len is not None:
        S = lead_outside - lead_len*2
    elif body_to_inside_lead_edge is not None:
        S = body_size - body_to_inside_lead_edge*2
    else:
        raise KeyError("either lead inside distance, lead to body edge or lead lenght must be given")

    Gmin = S.maximum_RMS - 2*ipc_data['heel'] + 2*heel_reduction - math.sqrt(S.ipc_tol_RMS**2 + F**2 + P**2)

    Zmax = lead_outside.minimum_RMS + 2*ipc_data['toe'] + math.sqrt(lead_outside.ipc_tol_RMS**2 + F**2 + P**2)
    Xmax = lead_width.minimum_RMS + 2*ipc_data['side'] + math.sqrt(lead_width.ipc_tol_RMS**2 + F**2 + P**2)

    Zmax = roundToBase(Zmax, ipc_round_base['toe'])
    Gmin = roundToBase(Gmin, ipc_round_base['heel'])
    Xmax = roundToBase(Xmax, ipc_round_base['side'])

    return Gmin, Zmax, Xmax

def ipc_gull_wing(ipc_data, ipc_round_base, manf_tol, lead_width, lead_outside,
        lead_len=None, lead_inside=None, heel_reduction=0):
    # Zmax = Lmin + 2JT + √(CL^2 + F^2 + P^2)
    # Gmin = Smax − 2JH − √(CS^2 + F^2 + P^2)
    # Xmax = Wmin + 2JS + √(CW^2 + F^2 + P^2)

    # Some manufacturers do not list the terminal spacing (S) in their datasheet but list the terminal lenght (T)
    # Then one can calculate
    # Stol(RMS) = √(Ltol^2 + 2*^2)
    # Smin = Lmin - 2*Tmax
    # Smax(RMS) = Smin + Stol(RMS)

    F = manf_tol.get('manufacturing_tolerance', 0.1)
    P = manf_tol.get('placement_tolerance', 0.05)

    if lead_inside is not None:
        S = lead_inside
    elif lead_len is not None:
        S = lead_outside - lead_len*2
    else:
        raise KeyError("either lead inside distance or lead lenght must be given")

    Gmin = S.maximum_RMS - 2*ipc_data['heel'] + 2*heel_reduction - math.sqrt(S.ipc_tol_RMS**2 + F**2 + P**2)

    Zmax = lead_outside.minimum_RMS + 2*ipc_data['toe'] + math.sqrt(lead_outside.ipc_tol_RMS**2 + F**2 + P**2)
    Xmax = lead_width.minimum_RMS + 2*ipc_data['side'] + math.sqrt(lead_width.ipc_tol_RMS**2 + F**2 + P**2)

    Zmax = roundToBase(Zmax, ipc_round_base['toe'])
    Gmin = roundToBase(Gmin, ipc_round_base['heel'])
    Xmax = roundToBase(Xmax, ipc_round_base['side'])

    return Gmin, Zmax, Xmax

def ipc_pad_center_plus_size(ipc_data, ipc_round_base, manf_tol,
        center_position, lead_length, lead_width):
    F = manf_tol.get('manufacturing_tolerance', 0.1)
    P = manf_tol.get('placement_tolerance', 0.05)

    S = center_position*2 - lead_length
    lead_outside = center_position*2 + lead_length

    Gmin = S.maximum_RMS - 2*ipc_data['heel'] - math.sqrt(S.ipc_tol_RMS**2 + F**2 + P**2)
    Zmax = lead_outside.minimum_RMS + 2*ipc_data['toe'] + math.sqrt(lead_outside.ipc_tol_RMS**2 + F**2 + P**2)

    Xmax = lead_width.minimum_RMS + 2*ipc_data['side'] + math.sqrt(lead_width.ipc_tol_RMS**2 + F**2 + P**2)

    Zmax = roundToBase(Zmax, ipc_round_base['toe'])
    Gmin = roundToBase(Gmin, ipc_round_base['heel'])
    Xmax = roundToBase(Xmax, ipc_round_base['side'])

    return Gmin, Zmax, Xmax
