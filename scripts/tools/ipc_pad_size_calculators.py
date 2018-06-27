from __future__ import division
import math

def roundToBase(value, base):
    return round(value/base) * base

class TolerancedSize():
    def __init__(self, minimum=None, nominal=None, maximum=None, tolerance=None):
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
                self.minimum = self.nominal - tolerance[0]
                self.maximum = self.nominal + tolerance[1]
        else:
            self.minimum = self.nominal
            self.maximum = self.nominal

        if self.maximum < self.minimum:
            raise ValueError("Maximum is smaller than minimum. Tolerance ranges given wrong or parameters confused.")

        self.ipc_tol = self.maximum - self.minimum

    @staticmethod
    def fromYaml(yaml, base_name=None):
        if base_name is not None:
            if type(yaml.get(base_name)) is dict:
                dim = yaml.get(base_name)
                return TolerancedSize(
                    minimum=dim.get("minimum"),
                    nominal=dim.get("nominal"),
                    maximum=dim.get("maximum"),
                    tolerance=dim.get("tolerance")
                    )

            return TolerancedSize(
                minimum=yaml.get(base_name+"_min"),
                nominal=yaml.get(base_name),
                maximum=yaml.get(base_name+"_max"),
                tolerance=yaml.get(base_name+"_tol")
                )
        else:
            return TolerancedSize(
                minimum=yaml.get("minimum"),
                nominal=yaml.get("nominal"),
                maximum=yaml.get("maximum"),
                tolerance=yaml.get("tolerance")
                )

def ipc_body_edge_inside(ipc_data, ipc_round_base, manf_tol, body_size, lead_width,
        lead_len=None, lead_inside=None):
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
        Stol_RMS = lead_inside.ipc_tol
        Smax_RMS = lead_inside.maximum
    elif lead_len is not None:
        Smin = body_size.minimum - 2*lead_len.maximum
        Smax = body_size.maximum - 2*lead_len.minimum
        Stol = Smax - Smin
        Stol_RMS = math.sqrt(body_size.ipc_tol**2+2*(lead_len.ipc_tol**2))
        Smax_RMS = Smax - (Stol - Stol_RMS)/2
    else:
        raise KeyError("either lead inside distance or lead lenght must be given")

    Gmin = Smax_RMS - 2*ipc_data['heel'] - math.sqrt(Stol_RMS**2 + F**2 + P**2)

    Zmax = body_size.minimum + 2*ipc_data['toe'] + math.sqrt(body_size.ipc_tol**2 + F**2 + P**2)
    Xmax = lead_width.minimum + 2*ipc_data['side'] + math.sqrt(lead_width.ipc_tol**2 + F**2 + P**2)

    Zmax = roundToBase(Zmax, ipc_round_base['toe'])
    Gmin = roundToBase(Gmin, ipc_round_base['heel'])
    Xmax = roundToBase(Xmax, ipc_round_base['side'])

    return Gmin, Zmax, Xmax
