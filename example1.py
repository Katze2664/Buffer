from buffer import search

# According to an online phosphate buffer calculator, to make a 0.1M pH 6 phosphate buffer requires:
# H2PO4- concentration = 0.08631 M
# HPO4 2- concentration = 0.01369 M
# https://www.aatbio.com/resources/buffer-preparations-and-recipes/phosphate-buffer-ph-5-8-to-7-4

# Modify chemical dictionaries to represent your desired solutions.
phosphoric_dict = {"species_names": ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"],
                   "pKa": [2.15, 6.86, 12.32],  # literature values
                   "initial_conc": [0, 0.08631, 0.01369, 0],
                   "volume": 1.0,
                   "volume_list": None}

hydrochloric_dict = {"species_names": ["HCl", "Cl-"],
                     "pKa": [-6.3],  # literature value
                     "initial_conc": [0.1, 0],
                     "volume": 0.1,
                     "volume_list": None}

# Add each dictionary to a list to include it in the calculation.
# pH for each list will be calculated for the final solution created by mixing all chemicals in the list.

chemical_list1 = [phosphoric_dict]
print("1L Phosphate buffer (intended pH = 6)")
print("Calculated pH:", search(chemical_list1))
# Expected result: pH = 6.06
# This is pretty close to what was calculated by the online buffer calculator.

chemical_list2 = [hydrochloric_dict]
print("\n0.1L of 0.1M hydrochloric acid")
print("Calculated pH:", search(chemical_list2))
# Expected result: pH = 1.0

chemical_list3 = [phosphoric_dict, hydrochloric_dict]
print("\n1L Phosphate buffer + 0.1L of 0.1M hydrochloric acid")
print("Calculated pH:", search(chemical_list3))
# Expected result: pH = 5.45
# The purpose of a buffer is to ensure that the pH does not change much when acid or base is added.
# Notice how adding the hydrochloric acid to the phosphate buffer only changed the pH by a small amount
# (from 6.06 to 5.45) even though the hydrochloric acid by itself has a very low pH of 1.0
# This indicates the phosphate buffer is doing a good job of stabilising the pH.





