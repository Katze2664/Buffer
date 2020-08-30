import math
from decimal import *

class AcidBase:
    def __init__(self, species_names, initial_conc, pKa):
        self.species_names = species_names
        self.initial_conc = initial_conc
        self.pKa = pKa

phosphoric = AcidBase(["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"], [0, 0.0246, 0.0754, 0], [2.15, 6.86, 12.32])

#pKa = [2.14, 7.20, 12.37]

def release(pH_guess, acidbase, printer = 0):
    protons = range(len(acidbase.species_names)-1,-1,-1)


    total_conc = 0
    for i in acidbase.initial_conc:
        total_conc += i
    if printer == 1:
        print("total conc", total_conc)

    base_acid = []
    for i in range(len(acidbase.initial_conc) - 1):
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
    for i in range(len(acidbase.initial_conc)):
        diff_conc.append(equilibrium_conc[i] - acidbase.initial_conc[i])
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
        print("pH_calc", pH)
    return float(pH)

def diff(pH_guess, acidBases):
    H_release = 0
    for acidBase in acidBases:
        H_release += release(pH_guess, acidBase)
    pH_calculated = pH_calc(H_release)
    return pH_guess - pH_calculated

def search(precision, acidBases):
    lowerbound = 2
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

    print("Found")
    print("guess", guess)
    print("diff guess", diff_guess)
    H_release = 0
    for acidBase in acidBases:
        H_release += release(guess, acidBase)
    print("pH calc", pH_calc(H_release))


#pH_guess = 5

search(0.00001, [phosphoric])

#H_release = release(pH_guess, ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"], [0.1, 0.5, 0.2, 0.3], [2, 7, 12], [3, 2, 1, 0])
#pH_calc(H_release)