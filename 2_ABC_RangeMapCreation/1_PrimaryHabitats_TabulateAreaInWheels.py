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

# from arcpy.sa import *

# Start script
config.log_message("Script started")

# check to make sure the required fields are in the raster
fields_to_check = ["Primary_Co", "Primary_"]  # Fields to check
fields = arcpy.ListFields(config.habmap)  # Get the list of fields in the table
for field in fields_to_check:  # Check if each field exists
    if any(f.name == field for f in fields):
        print(f"- field '{field}' exists in the table.")
    else:
        print(f"- field '{field}' does not exist in the table.")


# Tabulate area of each habitat group by 1sqmi hex
config.log_message("Starting Tabulate Area on Primary habitats")
try:
    arcpy.sa.TabulateArea(config.hex49, "wheel_id", config.habmap,
                          "Primary_Co", config.PrimaryHab_OutputTbl, config.habmap, "CLASSES_AS_ROWS")
    config.log_message("TabulateArea completed successfully.")
except Exception as e:
    config.log_message(f"Error in TabulateArea: {e}")
    raise

config.log_message("Script completed")
