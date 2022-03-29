import numpy as np
from buffer import search
import matplotlib.pyplot as plt

# Titration example: run this script to plot the pH curve of the titration of 1M H3PO4 with 1M NaOH.
# The result closely matches the literature:
# https://www.researchgate.net/profile/Walter-Cisneros-Yupanqui/post/What_happens_when_the_buffer_capacity_is_exceeded_in_the_case_of_PBS_pH742/attachment/5f4a083fed60840001c96a8d/AS%3A929776059568128%401598687295154/image/Tritation+curve+of+phosphoric+acid+3.jpg

def titration_example(precision=0.000001):
    """Hard-coded example of titration of 1M H3PO4 with 1M NaOH"""
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

titration_example()