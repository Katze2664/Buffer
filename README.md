# Buffer

Calculates the pH of mixtures of buffers.

## Description

This program calculates the final pH of an aqueous solution containing any number 
of buffers or other chemicals. For each buffer or chemical, the required input
data is:
* name of chemicals
* pKa
* concentration (in molar, M)
* volume (in litres, L)

## Executing program
* In main.py, create a dictionary for each chemical solution you wish to mix together. 
  (See below for how to format the data in the dictionary.)
* Add each chemical dictionary to a chemical list.
* Put chemical list into search function to calculate the pH of the mixture.
Set printer=1 to print the result.
* Run main.py  
 
Run example1.py to see a demonstration of the pH calculation for a phosphate buffer being mixed 
with hydrochloric acid.  

Run example2.py to see a demonstration of plotting the pH of the titration of 1M H<sub>3</sub>PO<sub>4</sub>
with 1M NaOH.

## Formatting chemical dictionary
* "species_names" (list[str]) contains names for the conjugate acids and bases in a series of deprotonations.
* "pKa" (list[float]) contains literature pKa values for each deprotonation step.
* "initial_conc" (list[float]) contains concentrations (in molar, M) for each chemical in "species_names".
* "volume" (float) contains the total volume of solution (in litres, L).
* "volume_list" (list[float]) contains the volume (in litres, L) of each chemical in "species_names".
* use "volume" or "volume_list" but not both. Leave the unused one as None.

For example, to create 1.5L of phosphate buffer containing 0.1M H<sub>2</sub>PO<sub>4</sub><sup>-</sup> 
and 0.4M HPO<sub>4</sub><sup>2-</sup>, the required dictionary is:

phosphoric_dict1 =  
{"species_names": ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"],  
"pKa": [2.15, 6.86, 12.32],  # literature values  
"initial_conc": [0, 0.1, 0.4, 0],  
"volume": 1.5,  
"volume_list": None}  

Note that even though only H<sub>2</sub>PO<sub>4</sub><sup>-</sup> and HPO<sub>4</sub><sup>2-</sup> are 
present in the initial solution, all 4 protonation states of phosphoric acid must be listed since 
they are connected by the following equilibrium equations:  
H<sub>3</sub>PO<sub>4</sub> <---> H<sub>2</sub>PO<sub>4</sub><sup>-</sup> + H<sup>+</sup>, pK<sub>a</sub> = 2.15  
H<sub>2</sub>PO<sub>4</sub><sup>-</sup> <---> HPO<sub>4</sub><sup>2-</sup> + H<sup>+</sup>, pK<sub>a</sub> = 6.86  
HPO<sub>4</sub><sup>2-</sup> <---> PO<sub>4</sub><sup>3-</sup> + H<sup>+</sup>, pK<sub>a</sub> = 12.32  

"species_names" must contain all protonation states of the chemical, ordered from most protonated on the left (acidic)
to least protonated on the right (basic). If there are n protonation states, "species_names" will be a list of length n.

"pKa" must contain the literature pKa values of each successive deprotonation equation, with the lowest value on the
left and highest value on the right. "pKa" will contain a list of length n - 1.

"initial_conc" contains a list of the concentrations (in molar, M) of each chemical specified in "species_names" in order.

"volume" is the total volume of solution (in litres, L).  
Alternatively, you can specify "volume_list" which is a list (of length n) of the volumes (in litres, L) of each chemical in "species_names"
at the concentration specified in "initial_conc".  
If specifying "volume", leave "volume_list" as None.  
If specifying "volume_list", leave "volume" as None.  

For example, mixing 0.5L of 0.3M H<sub>2</sub>PO<sub>4</sub><sup>-</sup> with 1.0L of 0.6M HPO<sub>4</sub><sup>2-</sup> 
would be represented by the following dictionary.  
phosphoric_dict2 =  
{"species_names": ["H3PO4", "H2PO4 -", "HPO4 2-", "PO4 3-"],  
"pKa": [2.15, 6.86, 12.32],  # literature values  
"initial_conc": [0, 0.3, 0.6, 0],  
"volume": None,  
"volume_list": [0, 0.5, 1.0, 0]} 

phosphoric_dict2 is equivalent to phosphoric_dict1, since: 
* the total volume is the same: 0.5L + 1.0L = 1.5L
* the concentration of H<sub>2</sub>PO<sub>4</sub><sup>-</sup> is 0.3M * 0.5L / 1.5L = 0.1M
* the concentration of HPO<sub>4</sub><sup>2-</sup> is 0.6M * 1.0L / 1.5L = 0.4M

## Further notes

Calculations of pH by this program do not take into account the effects of ionic strength, nor does it account for
differences between activity and concentration.

## Authors

Ethan Watkins

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details

## Acknowledgements

"Quest Calculate™ Phosphate Buffer (pH 5.8 to 7.4) Preparation and Recipe." AAT Bioquest, Inc., 29 Mar. 2022, https://www.aatbio.com/resources/buffer-preparations-and-recipes/phosphate-buffer-ph-5-8-to-7-4.