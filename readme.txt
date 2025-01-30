## American Bird Conservancy Bird Habitats of North America
This analysis was developed for the American Bird Conservancy project in FY2025 by Hannah Ceasar, Jordana Anderson, Sara DeCaro and Chris Tracey
The purpose of this analysis is as follows:
- Calculate habtiat threat scores for all bird habitats (at the subtype level) included in the Bird Habitats of North America map
- Create 49 square mile (wheel) hexagon based range maps for both primary and subtype habitats for display in the ABC app
- Calculate for each subtype two spatially explicit threat metrics at the wheel level: Land Cover Vulnerability Change (LCVC) and Landscape Condition Model (LCM)

Important things to note:
- To increase efficiency processes within both folders can be run simultaneously, the final step of 2_ABC_RangeMapCreation requires the output of 1_ABC_HabitatThreatsAnalysis
- When small updates are made to the ABC habitat map (ex. updating subtype names, extents etc.) 2_ABC_RangeMapCreation process can be modified to only run on a list of subtypes. Further details can be found in the 2_ABC_RangeMapCreation scripts.

# ABC Threats Analysis: 1_ABC_HabitatThreatsAnalysis
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

# ABC Range Map Creation: 2_ABC_RangeMapCreation
1. 1_PrimaryHabitats_TabulateAreaInWheels -- Calculates area of each primary habitat in each wheel
2. 2_PrimaryHabitats_CreateRangeMaps -- Creates wheel based range map for each primary habitat
3. 3_SubtypeHabitats_TabulateAreaInWheels -- Calculates area of each subtype habitat in each wheel
4. 4_SubtypeHabitats_CreateRangeMaps -- Creates wheel based range map for each subtype habitat
	* manually dissolve the output of this script - eventually add into the script
5. 5_SubtypeHabitats_LandscapeConditionAssessment -- extracts the extent of each subtype as a raster, extracts the LCM for that extent to calculate the average LCM score within each wheel
6. 6_SubtypeHabitats_ConversionAssessment -- extracts the extent of each subtype as a raster, extracts the LCVC for that extent to calculate the average LCVC score within each wheel
7. JOIN results of habitat threat scoring to subtype, dissolved range maps 
	* currently a manual step that can only be completed once threat analysis is complete
