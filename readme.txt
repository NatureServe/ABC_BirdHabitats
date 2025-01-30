ABC map has been created, tif ready for processing
1. primary habitat range map - tab area
2. primary habitat range map - map creation
3. subtype habitat range map - tab area
4. subtype habitat range map - map creation
5. LCM assessment
6. Conversion assessment
7. JOIN results of habitat threat scoring to subtype, dissolved range maps


ABC Threats Analysis:
1. 1_create_geodatabase *takes only minutes to run
  a. This creates the gdbs and folders (if they don’t already exist – the scripts check for their existence first), reads in the Habitat Map EXPORT CSV as a table, creates an empty final table to output results to and populates it with the fields from the EXPORT CSV.
2. 2_tabulate_rsr *takes only minutes to run
  a. Calculates range size rarity, hectares, and sqkm per subtype. Populates those values to the final table.
  b. I have a code cell in this notebook that clears the contents of these values in case they need to be rerun for some reason. It should be skipped otherwise.
3. 3_tabulate_area *takes roughly 2 hours to run
  a. Calculates the proportion of each habitat that is protected using PAD-US and equivalent Canadian datasets.
4. 4_zonal_stats *takes 4+ hours to run. 
  a. This script is to calculate the average LCVC stat for every 49sqmi hex, the average LCVC stat for every subtype, and the average LCM stat for every subtype.
  b. IF RERUNNING SCRIPT FOR A MAP UPDATE: Don’t run the cell that calculates the average LCVC score for each 49sqmi hexagon. None of the inputs have changed.
  c. NOTE: I added a code cell for calculating the zonal stats for Climate Velocity within my script. Last time, Chris calculated this, and I had a code cell to pull the values from his table and populate my final table.
  d. Review Values of the final table looking for zeros. 
      1. NOTE FROM LAST RERUN END OF JAN 2025: Atlantic Coral Reefs has a Conversion Mean of 0. Hannah C reminded me that we deleted some habitats altogether and Atlantic Coral Reefs was one of those. I need to add code to remove these habitats from the final table.
      2. NOTE FROM LAST RERUN END OF JA 2025: Nearctic Boggy Tundra has a Protected Area US GAP3 score of 0. This is an arctic habitat that has no protection overlapping so it is fine to leave this as is. This will result with this subtype being in the highest decile for that category.
      3. FYIs
          a. Polar Desert & General Sagebrush Shrubland were reclassified in the mapping updates.
          b. Montane Spruce-fir Forest was renamed to something else.
5. 5_deciles
  a. Calculates the deciles for each score.
  b. Remember to join the 'Raw Obligation scores' and 'Raw conservation Concern scores' sent by David from ABC to the final table prior to running the deciles for those categories.
      1. Replace the null values in each of these categories with zero prior to running the deciles.
