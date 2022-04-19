# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""


class Hedge:
    def __init__(self, lowerValue, middleValue, upperValue):
        self.lowerValue = lowerValue
        self.middleValue = middleValue
        self.upperValue = upperValue


def solver(t, w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
    
    None :if we have a division by zero

    """

    thetaClasses = {
        "NVB": Hedge(-50, -40, -25),
        "NB": Hedge(-40, -25, -10),
        "N": Hedge(-20, -10, 0),
        "ZO": Hedge(-5, 0, 5),
        "P": Hedge(0, 10, 20),
        "PB": Hedge(10, 25, 40),
        "PVB": Hedge(25, 40, 50)
    }

    omegaClasses = {
        "NB": Hedge(-10, -8, -3),
        "N": Hedge(-6, -3, 0),
        "ZO": Hedge(-1, 0, 1),
        "P": Hedge(0, 3, 6),
        "PB": Hedge(3, 8, 10)
    }

    forceClasses = {
        "NVVB": Hedge(-40, -32, -24),
        "NVB": Hedge(-32, -24, -16),
        "NB": Hedge(-24, -16, -8),
        "N": Hedge(-16, -8, 0),
        "Z": Hedge(-8, 0, 8),
        "P": Hedge(0, 8, 16),
        "PB": Hedge(8, 16, 24),
        "PVB": Hedge(16, 24, 32),
        "PVVB": Hedge(24, 32, 40)
    }

    fuzzyControlTable = {
        "NVB-NB": "NVVB", "NVB-N": "NVVB", "NVB-ZO": "NVB", "NVB-P": "NB", "NVB-PB": "N",
        "NB-NB": "NVVB", "NB-N": "NVB", "NB-ZO": "NB", "NB-P": "N", "NB-PB": "Z",
        "N-NB": "NVB", "N-N": "NB", "N-ZO": "N", "N-P": "Z", "N-PB": "P",
        "ZO-NB": "NB", "ZO-N": "N", "ZO-ZO": "Z", "ZO-P": "P", "ZO-PB": "PB",
        "P-NB": "N", "P-N": "Z", "P-ZO": "P", "P-P": "PB", "P-PB": "PVB",
        "PB-NB": "Z", "PB-N": "P", "PB-ZO": "PB", "PB-P": "PVB", "PB-PB": "PVVB",
        "PVB-NB": "P", "PVB-N": "PB", "PVB-ZO": "PVB", "PVB-P": "PVVB", "PVB-PB": "PVVB",
    }

    thetaMemberships = computeMembership(t, thetaClasses)
    omegaMemberships = computeMembership(w, omegaClasses)

    forceMemberships = computeForceMemberships(fuzzyControlTable, thetaMemberships, omegaMemberships)
    FMembership = computeForceMembership(forceMemberships)

    numerator = 0
    denominator = 0
    for label in forceMemberships:
        numerator = numerator + forceClasses[label].middleValue * FMembership[label]
        denominator = denominator + FMembership[label]

    return numerator / denominator if denominator != 0 else 0


def computeForceMembership(forceMemberships):
    FMembership = {
        "NVVB": 0,
        "NVB": 0,
        "NB": 0,
        "N": 0,
        "Z": 0,
        "P": 0,
        "PB": 0,
        "PVB": 0,
        "PVVB": 0
    }

    for label in forceMemberships:
        maximum = 0
        for val in forceMemberships[label]:
            maximum = max(maximum, val)
        FMembership[label] = maximum

    return FMembership


def computeForceMemberships(fuzzyControlTable, thetaMemberships, omegaMemberships):
    forceMemberships = {
        "NVVB": [],
        "NVB": [],
        "NB": [],
        "N": [],
        "Z": [],
        "P": [],
        "PB": [],
        "PVB": [],
        "PVVB": []
    }

    for thetaLabel in thetaMemberships:
        for omegaLabel in omegaMemberships:
            compositeLabel = thetaLabel + '-' + omegaLabel
            fLabel = fuzzyControlTable[compositeLabel]
            forceMemberships[fLabel].append(min(thetaMemberships[thetaLabel], omegaMemberships[omegaLabel]))

    return forceMemberships


def computeMembership(x, values):
    memberships = dict()

    for key in values:
        a = values[key].lowerValue
        b = values[key].middleValue
        c = values[key].upperValue
        memberships[key] = max(0,
                               min((x - a) / (b - a),
                                   1,
                                   (c - x) / (c - b))
                               )

    return memberships
