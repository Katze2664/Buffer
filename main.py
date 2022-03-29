from buffer import search
from titration import titration_example

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

print("Chemical list 1: just phosphate buffer")
search(chemical_list1, printer=1)

print("Chemical list 2: phosphate buffer plus hydrochloric acid")
search(chemical_list2, printer=1)

print("Chemical list 3: phosphate buffer plus hydrochloric acid plus hydroxide")
search(chemical_list3, printer=1)

print("Chemical list 4: phosphate buffer plus acetic acid")
search(chemical_list4, printer=1)

titration_example(precision)
