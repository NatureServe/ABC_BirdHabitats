# config.py
# this loads in the paths and settings so all ABC_RSR_Calculation and ABC_PA scripts are using the same values

import arcpy
import os
from arcpy.sa import *
import pandas as pd

# environments

arcpy.env.overwriteOutput = True

# Enable the Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

print("Environments set from config file.")

# paths

projectName_final = "finalABC_y2025"
projectName_int = "intermediateABC_y2025"
data_final = r"S:\Projects\ABC\y2025\Data\Final"
data_int = r"S:\Projects\ABC\y2025\Data\Intermediate"
project_folder_final = os.path.join(data_final, projectName_final)
project_folder_int = os.path.join(data_int, projectName_int)
gdb_final = "ABC_final" # .gdb
gdb_int = "ABC_intermediate" # .gdb

print("Paths set from config file.")


# file and variable names 

input_csv = r"S:\Projects\ABC\y2025\Data\Source\HabitatMap\ABC_HabitatMap_comb41_PolarDesertFix_EXPORT.csv" #Need to recreate and update path when there are map changes
output_table = "ABCrsr_table"
ABC_Analysis_Table = "ABC_y2025"
output_int_PA = "ABCpa_table"
output_int_PA123 = "ABCpa123_table"
HabMap_tif = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\ABC_HabitatMap_comb41_PolarDesertFix.tif"
PA_1_2 = r"S:\Projects\ABC\y2025\Pro\Draft\ABC_RSR_Calculation_Pro\ABC_RSR_Calculation\ABC_RSR_Calculation.gdb\Protected_Areas_GAP_1_2 "
PA_1_2_3 = r"S:\Projects\ABC\y2025\Pro\Draft\ABC_RSR_Calculation_Pro\ABC_RSR_Calculation\ABC_RSR_Calculation.gdb\Protected_Areas_1_2_3"
LCVC_Lookup = r"S:\Projects\ABC\y2025\Pro\Draft\ABC_RSR_Calculation_Pro\ABC_RSR_Calculation\ABC_RSR_Calculation.gdb\LCVC_Canada_USA_Albers_Lookup_30m"
wheel_grid = r"S:\Projects\ABC\y2025\Pro\Draft\ABC_RSR_Calculation_Pro\ABC_RSR_Calculation\ABC_RSR_Calculation.gdb\nhf_wheels_Merge"
LCVC_table = "ABC_LCVC_ZonalStats"
LCVC_subtype_table = "ABC_LCVC_Subtype_ZonalStats"
LCM_data = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\ABC_fy25.gdb\LCM_NorthAmerica_30m"
LCM_subtype_table = "ABC_LCM_ZonalStats"
CV_data = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\FWVel_allNA.tif"
CV_subtype_table = "ABC_CV_ZonalStats"
Subtype_Merged_Raster = r"S:\Projects\ABC\y2025\Data\Final\SubtypeHabRangeMaps_fin.gdb\SubtypeHabitat_RangeMapsDissolve_20250128"


cfact030 = 0.0009  # Area of 30-m cell in Albers Conic Equal Area is 899.972796 m2 (0.0009 km2)

print("File and variable names set from config file.")
