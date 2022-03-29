import math
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
# use "volume" or "volume_list" but not both. Leave the used one as None

phosphoric_dict = {"species_names": ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"],
                   "pKa": [2.15, 7.21, 12.32],
                   "initial_conc": [0, 0.06, 0.09, 0],
                   "volume": 1.5,
                   "volume_list": None}

hydrochloric_dict = {"species_names": ["HCl", "Cl-"],
                     "pKa": [-6.3],
                     "initial_conc": [0.2, 0.1],
                     "volume": None,
                     "volume_list": [0.5, 0.3]}

# Add each dictionary to this list to include it in the calculation.
# pH will be calculated for the final solution created by mixing all chemicals in this list.
chemical_list = [phosphoric_dict, hydrochloric_dict]

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
                self.volume = 0
                for i in volume_list:
                    self.volume += i

                self.initial_conc = []
                for i in range(len(initial_conc)):
                    self.initial_conc.append(initial_conc[i] * volume_list[i] / self.volume)
        else:
            if volume_list == None:
                self.volume = volume
                self.initial_conc = initial_conc
            else:
                print("Error: volume double specified", self.species_names)
                exit()


def release(pH_guess, acidbase, volume_total, printer = 0):
    protons = range(len(acidbase.species_names)-1, -1, -1)

    diluted_conc = []
    for conc in acidbase.initial_conc:
        diluted_conc.append(conc * acidbase.volume / volume_total)

    total_conc = 0
    for i in diluted_conc:
        total_conc += i
    if printer == 1:
        print("total conc", total_conc)

    base_acid = []
    for i in range(len(diluted_conc) - 1):
        base_acid.append(10**(pH_guess - acidbase.pKa[i]))
    if printer == 1:
        print("base_acid", base_acid)

    ratio = [1]
    for i in base_acid:
        ratio.append(ratio[-1]*i)
    if printer == 1:
        print("ratio", ratio)

    sum = 0
    for i in ratio:
        sum += i
    if printer == 1:
        print("sum", sum)

    equilibrium_conc = []
    for i in ratio:
        equilibrium_conc.append(total_conc*i/sum)
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

def pH_calc(H_released, printer = 0):
    K_w = 1e-14
    OH_conc = (Decimal(-1*H_released) + Decimal.sqrt(Decimal(H_released) * Decimal(H_released) + 4 * Decimal(K_w)))/2
    H_conc = Decimal(OH_conc) + Decimal(H_released)
    pH = Decimal(-1) * Decimal.log10(Decimal(H_conc))
    if printer == 1:
        print("Calculated pH: ", pH)
    return float(pH)

def diff(pH_guess, acidBases, printer = 0):
    volume_total = 0
    for acidBase in acidBases:
        volume_total += acidBase.volume

    H_release = 0
    for acidBase in acidBases:
        H_release += release(pH_guess, acidBase, volume_total)
    pH_calculated = pH_calc(H_release, printer)
    return pH_guess - pH_calculated

def search(precision, acidBases):
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


    diff(guess, acidBases, 1)
    print("Precision error: ", diff_guess)

acidbase_list = []
for chem_dict in chemical_list:
    acidbase = AcidBase(chem_dict["species_names"], chem_dict["pKa"], chem_dict["initial_conc"], chem_dict["volume"], chem_dict["volume_list"])
    acidbase_list.append(acidbase)

search(precision, acidbase_list)
