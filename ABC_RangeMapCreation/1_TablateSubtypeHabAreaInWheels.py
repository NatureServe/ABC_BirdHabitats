"""Script Summary: This script is designed to perform habitat analysis using ArcGIS tools. It logs each step of the
process with timestamps. The main functions include listing field names in a raster dataset, tabulating the area of
each habitat group by a hex grid, and calculating additional fields for hectares and density.

Inputs:
- hexgrid: Path to hexgrid (D:\SGITemp.gdb\Hexes)
- WorkingHabitat: Path to habitat raster (D:\SGITemp.gdb\BPS_Raster20200606)

Outputs:
- output_table: Path for GroupAreaTable (D:\SGITemp.gdb\BPSGroupAreaTable)
- Intermediate and final output paths for habitat feature classes and tables

Script created on 20240611 by Kevin Knight
Last modified on 20240611 by Kevin Knight
"""

import arcpy
import os
import config
import pandas as pd

# from arcpy.sa import *

# Start script
config.log_message("Script started")

### The following block of code is useful when updating the ABC map results in just a handful of
### habitat types being updated. Allows for a faster processing time to subset to just that list
### of updated habitats.
# Load the list of updated subtypes from the CSV -- use when updating a subset of the map
try:
    updated_subtypes = pd.read_csv(config.updated_subtypes_csv)  # Read the CSV
    updated_subtypes_list = updated_subtypes['Subtype'].unique().tolist()  # Get a list of unique subtypes
    config.log_message(f"Loaded {len(updated_subtypes_list)} updated subtypes from CSV.")
except Exception as e:
    config.log_message(f"Error loading updated subtypes from CSV: {e}")
    raise

# check to make sure the required fields are in the raster
fields_to_check = ["HabitatCod", "Subtype"]  # Fields to check
fields = arcpy.ListFields(config.habmap)  # Get the list of fields in the table
for field in fields_to_check:  # Check if each field exists
    if any(f.name == field for f in fields):
        print(f"- field '{field}' exists in the table.")
    else:
        print(f"- field '{field}' does not exist in the table.")


# Tabulate area of each habitat group by 1sqmi hex
config.log_message("Starting Tabulate Area on subtypes")
try:
    ### The following two blocks of code should only be applied when updating a subset of habitat types
    # Create a SQL query to filter the subtypes
    subtype_query = f"Subtype IN ({','.join([repr(s) for s in updated_subtypes_list])})"
    config.log_message(f"Using SQL query: {subtype_query}")

    # Apply the SQL query to extract relevant subtypes -- use when updating a subset of the map
    filtered_habmap = arcpy.sa.ExtractByAttributes(config.habmap, subtype_query)
    config.log_message("Subtype filtering completed successfully.")

    # perform tabulate area
    arcpy.sa.TabulateArea(config.hex49, "wheel_id",
                          #config.habmap, ## -- use when rerunning on entire map
                          filtered_habmap, ## -- use when updating a subset of the map
                          "HabitatCod", config.SubtypeHab_OutputTbl,
                          #config.habmap, ## -- use when rerunning on entire map
                          filtered_habmap, ## -- use when updating a subset of the map
                          "CLASSES_AS_ROWS")
    config.log_message("TabulateArea completed successfully.")
except Exception as e:
    config.log_message(f"Error in TabulateArea: {e}")
    raise

config.log_message("Script completed")
