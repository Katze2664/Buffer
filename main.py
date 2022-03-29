from buffer import search
from titration import titration_example

# Specify the desired precision of the calculation.
precision = 0.00001

# Modify chemical dictionaries to represent your desired solutions.
phosphoric_dict = {"species_names": ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"],
                   "pKa": [2.15, 6.86, 12.32],  # literature values
                   "initial_conc": [0, 0.1, 0.4, 0],
                   "volume": 1.5,
                   "volume_list": None}

hydrochloric_dict = {"species_names": ["HCl", "Cl-"],
                     "pKa": [-6.3],  # literature value
                     "initial_conc": [0.2, 0.1],
                     "volume": None,
                     "volume_list": [0.1, 0.5]}

hydroxide_dict = {"species_names": ["H2O", "OH-"],
                  "pKa": [14],  # literature value
                  "initial_conc": [1, 0.5],
                  "volume": None,
                  "volume_list": [1, 0.4]}

acetic_dict = {"species_names": ["CH3COOH", "CH3COO-"],
               "pKa": [4.75],  # literature value
               "initial_conc": [1, 0],
               "volume": 0.1,
               "volume_list": None}

# Add each dictionary to a list to include it in the calculation.
# pH for each list will be calculated for the final solution created by mixing all chemicals in the list.
chemical_list = [phosphoric_dict, hydrochloric_dict, hydroxide_dict, acetic_dict]

print("Phosphate + Hydrochloric + Hydroxide + Acetic")
search(chemical_list, printer=1, precision=precision)

titration_example(precision)
