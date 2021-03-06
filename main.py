from buffer import search

# Specify the desired precision of the calculation.
precision = 0.00001

# Modify the chemical dictionaries below to represent your desired solutions.

# Current dictionary represents 1.5L of phosphate buffer containing 0.1M H2PO4- and 0.4M HPO4 2-.
phosphoric_dict = {"species_names": ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"],
                   "pKa": [2.15, 6.86, 12.32],  # literature values
                   "initial_conc": [0, 0.1, 0.4, 0],
                   "volume": 1.5,
                   "volume_list": None}

# Current dictionary represents 0.1L of 0.2M HCl mixed with 0.5L of 0.1M NaCl to make 0.6L total.
hydrochloric_dict = {"species_names": ["HCl", "Cl-"],
                     "pKa": [-6.3],  # literature value
                     "initial_conc": [0.2, 0.1],
                     "volume": None,
                     "volume_list": [0.1, 0.5]}

# Current dictionary represents 0.8L of water (H2O) mixed with 0.4L of 0.5M NaOH to make 1.2L total.
hydroxide_dict = {"species_names": ["H2O", "OH-"],
                  "pKa": [14],  # literature value
                  "initial_conc": [1, 0.5],
                  "volume": None,
                  "volume_list": [0.8, 0.4]}

# Current dictionary represents 0.1L of 1M acetic acid (CH3COOH).
acetic_dict = {"species_names": ["CH3COOH", "CH3COO-"],
               "pKa": [4.75],  # literature value
               "initial_conc": [1, 0],
               "volume": 0.1,
               "volume_list": None}

# Add each dictionary to a list to include it in the calculation.
# pH will be calculated for the final solution created by mixing all chemicals in the list.
chemical_list = [phosphoric_dict, hydrochloric_dict, hydroxide_dict, acetic_dict]

# Pass the chemical list into the search function to calculate the pH.
print("Phosphate + Hydrochloric + Hydroxide + Acetic")
search(chemical_list, printer=True, precision=precision)
