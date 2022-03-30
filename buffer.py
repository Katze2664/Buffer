import math
import numpy as np
from decimal import *

class AcidBase:
    def __init__(self, species_names, pKa, initial_conc, volume=None, volume_list=None):
        self.species_names = species_names
        self.pKa = pKa

        if volume == None:
            if volume_list == None:
                print("Error: no volume", self.species_names)
                exit()
            else:
                self.volume = sum(volume_list)

                if self.volume != 0:
                    self.initial_conc = []
                    for i in range(len(initial_conc)):
                        self.initial_conc.append(initial_conc[i] * volume_list[i] / self.volume)
                else:
                    self.initial_conc = initial_conc
        else:
            if volume_list == None:
                self.volume = volume
                self.initial_conc = initial_conc
            else:
                print("Error: volume double specified", self.species_names)
                exit()


def release(pH_guess, acidbase, volume_total, printer=False):
    protons = list(range(len(acidbase.species_names) - 1, -1, -1))
    if printer:
        print("protons", protons)

    diluted_conc = []
    for conc in acidbase.initial_conc:
        diluted_conc.append(conc * acidbase.volume / volume_total)
    if printer:
        print("diluted conc", diluted_conc)

    total_conc = sum(diluted_conc)
    if printer:
        print("total conc", total_conc)

    base_acid = []
    for i in range(len(diluted_conc) - 1):
        base_acid.append(10 ** (pH_guess - acidbase.pKa[i]))
    if printer:
        print("base_acid", base_acid)

    ratios = [1]
    for i in base_acid:
        ratios.append(ratios[-1] * i)
    if printer:
        print("ratios", ratios)

    ratio_sum = sum(ratios)
    if printer:
        print("ratio_sum", ratio_sum)

    equilibrium_conc = []
    for ratio in ratios:
        equilibrium_conc.append(total_conc * ratio / ratio_sum)
    if printer:
        print("equilibrium conc", equilibrium_conc)

    diff_conc = []
    for i in range(len(diluted_conc)):
        diff_conc.append(equilibrium_conc[i] - diluted_conc[i])
    if printer:
        print("diff conc", diff_conc)

    H_released = 0
    for i in range(len(diff_conc)):
        H_released += -1 * diff_conc[i] * protons[i]
    if printer:
        print("H released", H_released)
    return H_released


def pH_calc(H_released, printer=False):
    K_w = 1e-14
    OH_conc = (Decimal(-1 * H_released) + Decimal.sqrt(
        Decimal(H_released) * Decimal(H_released) + 4 * Decimal(K_w))) / 2
    H_conc = Decimal(OH_conc) + Decimal(H_released)
    pH = Decimal(-1) * Decimal.log10(Decimal(H_conc))
    if printer:
        print("OH conc", OH_conc)
        print("H conc", H_conc)
        print("Calculated pH: ", pH)
    return float(pH)


def diff(pH_guess, acidBases, printer=False):
    volume_total = 0
    for acidBase in acidBases:
        volume_total += acidBase.volume

    H_release = 0
    for acidBase in acidBases:
        H_release += release(pH_guess, acidBase, volume_total)
    pH_calculated = pH_calc(H_release, printer)
    return pH_guess - pH_calculated


def acidbase_objects_list(chemical_list):
    acidbase_list = []
    for chem_dict in chemical_list:
        acidbase = AcidBase(chem_dict["species_names"],
                            chem_dict["pKa"],
                            chem_dict["initial_conc"],
                            chem_dict["volume"],
                            chem_dict["volume_list"])
        acidbase_list.append(acidbase)
    return acidbase_list


def search(chemical_list, printer=False, precision=0.000001, rounded=2):

    acidBases = acidbase_objects_list(chemical_list)

    lowerbound = 0
    upperbound = 14

    while diff(lowerbound, acidBases) > 0:
        lowerbound += -1

    while diff(upperbound, acidBases) < 0:
        upperbound += 1

    diff_lower = diff(lowerbound, acidBases)
    diff_upper = diff(upperbound, acidBases)
    gradient = (diff_upper - diff_lower) / (upperbound - lowerbound)
    guess = upperbound - (diff_upper / gradient)
    diff_guess = diff(guess, acidBases)

    while not Decimal(-precision) < diff_guess < Decimal(precision):
        if diff_guess < 0:
            lowerbound = guess
            diff_lower = diff(lowerbound, acidBases)
        else:
            upperbound = guess
            diff_upper = diff(upperbound, acidBases)

        gradient = (diff_upper - diff_lower) / (upperbound - lowerbound)
        guess = upperbound - (diff_upper / gradient)
        diff_guess = diff(guess, acidBases)

    result = round(guess, rounded)
    if printer:
        print("pH = ", result)

    return result
