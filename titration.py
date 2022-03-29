import numpy as np
from buffer import search
import matplotlib.pyplot as plt


def titration_example(precision):
    """Hard-coded example of titration of 1M H3PO4 with 1M OH-"""
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

        pH = search(chemical_list, rounded=3)
        y_list.append(pH)

    plt.scatter(x_list, y_list, marker=".")
    plt.title("1M H3PO4 titrated with 1M NaOH")
    plt.xlabel("1M NaOH (L)")
    plt.ylabel("pH")
    plt.show()