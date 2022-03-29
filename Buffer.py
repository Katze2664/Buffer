import math
import numpy as np
import matplotlib.pyplot as plt
from decimal import *

# You may modify the section below to enter you desired data for calculation.

# Specify the desired precision of the calculation.
precision = 0.00001

# Enter chemical data in the form of dictionaries.
# "species_names" (list[str]) contains names for the conjugate acids and bases in a series of deprotonations
# "pKa" (list[float]) contains literature pKa values for each deprotonation step
# "initial_conc" (list[float]) contains concentrations (in molar) for each chemical in "species_names"
# "volume" (float) contains the total volume of solution (in litres)
# "volume_list" (list[float]) contains the volume (in litres) of each chemical in "species_names"
# use "volume" or "volume_list" but not both. Leave the unused one as None

# Example values are included below to demonstrate how enter data.
# The default values create a 2L of phosphate buffer containing 0.073M H2PO4- and 0.027M HPO4 2-.
# This default buffer has a pH of 6.43
phosphoric_dict = {"species_names": ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"],
                   "pKa": [2.15, 6.86, 12.32],  # literature values
                   "initial_conc": [0, 0.073, 0.027, 0],
                   "volume": 2,
                   "volume_list": None}

# The default values create a mixture of 0.1L of 0.2M HCl and 0.5L of 0.1M Cl- (total volume 0.6L).
# The addition of this solution to the phosphate buffer above gives a pH of 6.17
hydrochloric_dict = {"species_names": ["HCl", "Cl-"],
                     "pKa": [-6.3],  # literature value
                     "initial_conc": [0.2, 0.1],
                     "volume": None,
                     "volume_list": [0.1, 0.5]}

# The default values create a mixture of 1L of water (H2O) and 0.4L of 0.5M OH- (total volume 1.4L).
# The addition of this solution to the phosphate buffer along with the hydrochloric acid gives a pH of 11.39
hydroxide_dict = {"species_names": ["H2O", "OH-"],
                  "pKa": [14],  # literature value
                  "initial_conc": [1, 0.5],
                  "volume": None,
                  "volume_list": [1, 0.4]}

# The default values create a 0.1L of 1M acetic acid (CH3COOH) solution.
# The addition of this solution to the phosphate buffer above gives a pH of 4.8
acetic_dict = {"species_names": ["CH3COOH", "CH3COO-"],
               "pKa": [4.75],  # literature value
               "initial_conc": [1, 0],
               "volume": 0.1,
               "volume_list": None}

# Add each dictionary to a list to include it in the calculation.
# pH for each list will be calculated for the final solution created by mixing all chemicals in the list.
chemical_list1 = [phosphoric_dict]
chemical_list2 = [phosphoric_dict, hydrochloric_dict]
chemical_list3 = [phosphoric_dict, hydrochloric_dict, hydroxide_dict]
chemical_list4 = [phosphoric_dict, acetic_dict]

# Set this to True to run an example titration of H3PO4 with NaOH and graph the output
titration_example = True

# Do not modify below here.

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


def release(pH_guess, acidbase, volume_total, printer=0):
    protons = list(range(len(acidbase.species_names) - 1, -1, -1))
    if printer == 1:
        print("protons", protons)

    diluted_conc = []
    for conc in acidbase.initial_conc:
        diluted_conc.append(conc * acidbase.volume / volume_total)
    if printer == 1:
        print("diluted conc", diluted_conc)

    total_conc = sum(diluted_conc)
    if printer == 1:
        print("total conc", total_conc)

    base_acid = []
    for i in range(len(diluted_conc) - 1):
        base_acid.append(10 ** (pH_guess - acidbase.pKa[i]))
    if printer == 1:
        print("base_acid", base_acid)

    ratios = [1]
    for i in base_acid:
        ratios.append(ratios[-1] * i)
    if printer == 1:
        print("ratios", ratios)

    ratio_sum = sum(ratios)
    if printer == 1:
        print("ratio_sum", ratio_sum)

    equilibrium_conc = []
    for ratio in ratios:
        equilibrium_conc.append(total_conc * ratio / ratio_sum)
    if printer == 1:
        print("equilibrium conc", equilibrium_conc)

    diff_conc = []
    for i in range(len(diluted_conc)):
        diff_conc.append(equilibrium_conc[i] - diluted_conc[i])
    if printer == 1:
        print("diff conc", diff_conc)

    H_released = 0
    for i in range(len(diff_conc)):
        H_released += -1 * diff_conc[i] * protons[i]
    if printer == 1:
        print("H released", H_released)
    return H_released


def pH_calc(H_released, printer=0):
    K_w = 1e-14
    OH_conc = (Decimal(-1 * H_released) + Decimal.sqrt(
        Decimal(H_released) * Decimal(H_released) + 4 * Decimal(K_w))) / 2
    H_conc = Decimal(OH_conc) + Decimal(H_released)
    pH = Decimal(-1) * Decimal.log10(Decimal(H_conc))
    if printer == 1:
        print("OH conc", OH_conc)
        print("H conc", H_conc)
        print("Calculated pH: ", pH)
    return float(pH)


def diff(pH_guess, acidBases, printer=0):
    volume_total = 0
    for acidBase in acidBases:
        volume_total += acidBase.volume

    H_release = 0
    for acidBase in acidBases:
        H_release += release(pH_guess, acidBase, volume_total)
    pH_calculated = pH_calc(H_release, printer)
    return pH_guess - pH_calculated


def search(precision, chemical_list):

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

    return guess

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


print("Chemical list 1: just phosphate buffer")
print("pH", round(search(precision, chemical_list1), 2))

print("Chemical list 2: phosphate buffer plus hydrochloric acid")
print("pH", round(search(precision, chemical_list2), 2))

print("Chemical list 3: phosphate buffer plus hydrochloric acid plus hydroxide")
print("pH", round(search(precision, chemical_list3), 2))

print("Chemical list 3: phosphate buffer plus acetic acid")
print("pH", round(search(precision, chemical_list4), 2))


if titration_example:
    x_list = np.linspace(0, 3, 101)
    y_list = []

    for x in x_list:

        phosphoric_dict = {"species_names": ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"],
                           "pKa": [2.15, 6.86, 12.32],
                           "initial_conc": [1, 0, 0, 0],
                           "volume": 1,
                           "volume_list": None}

        hydroxide_dict = {"species_names": ["H2O", "OH-"],
                          "pKa": [14],
                          "initial_conc": [0, 1],
                          "volume": x,
                          "volume_list": None}

        chemical_list = [phosphoric_dict, hydroxide_dict]

        pH = search(precision, chemical_list)
        y_list.append(pH)

    plt.scatter(x_list, y_list, marker=".")
    plt.title("1M H3PO4 titrated with 1M NaOH")
    plt.xlabel("1M NaOH (L)")
    plt.ylabel("pH")
    plt.show()
