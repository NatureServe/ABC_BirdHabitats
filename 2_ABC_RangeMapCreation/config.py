# config.py
# this loads in the paths and settings needed to create habitat range maps and perform a landscape condition assessment

import arcpy
import os
import datetime
arcpy.env.overwriteOutput = True

############## Paths variables needed for range map creation: #########################
# paths
project_folder = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25"
primary_output_gdb = r"S:\Projects\ABC\y2025\Data\Final\PrimaryHabRangeMaps_fin.gdb"
subtype_output_gdb = r"S:\Projects\ABC\y2025\Data\Final\SubtypeHabRangeMaps_fin.gdb"
int_tbl_path = r"D:\ABC_fy25\RangeMapDevelopment\temp_tbls.gdb"  # Intermediate output path for habitat tables and feature classes
int_tbl_path_subtype = r"D:\ABC_fy25\RangeMapDevelopment\temp_tbls_subtype.gdb"
int_range_path = r"D:\ABC_fy25\RangeMapDevelopment\int_rangemaps.gdb" # Intermediate output path for habitat range maps before dissolve
updated_subtypes_csv = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\UpdatedSubtypes_20250126.csv"

## Hexagon data inputs
hex49 = r"S:\Projects\ABC\y2025\Pro\Draft\ABC_RSR_Calculation_Pro\ABC_RSR_Calculation\ABC_RSR_Calculation.gdb\nhf_wheels_Merge"
hex49smooth = r"S:\Projects\ABC\y2025\Pro\Draft\ABC_RSR_Calculation_Pro\ABC_RSR_Calculation\ABC_RSR_Calculation.gdb\nhf_wheels_smoothed_Merge"
# Variables
habmap = os.path.join(project_folder, "ABC_HabitatMap_comb41_PolarDesertFix.tif")
PrimaryHab_OutputTbl = os.path.join(primary_output_gdb, "PrimaryHab_tabarea_out_20241018")
SubtypeHab_OutputTbl = os.path.join(subtype_output_gdb, "SubHab_tabarea_out_20250127")
SubtpeFinalOutput = os.path.join(subtype_output_gdb, "SubtypeHabitat_RangeMapsMerge_wLCM")

# For building results table
#results_table_name = "AnalysisTable_202409"
#results_table = os.path.join(output_gdb, results_table_name)

########### Paths variables needed for landscape condition assessment: #################

# For LCM stats
LCM = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\ABC_fy25.gdb\LCM_NorthAmerica_30m"
zonal_output_gdb = r"S:\Projects\ABC\y2025\Data\Intermediate\LCM_ZonalStats_bySubtype.gdb"
LCMextracts_gdb = r"S:\Projects\ABC\y2025\Data\Intermediate\LCM_ExtractbySubtype.gdb"
subtype_extracts_gdb = r"S:\Projects\ABC\y2025\Data\Intermediate\Subtypes_Extracts.gdb"

# for LCVC stats
LCVC = r"S:\Projects\ABC\y2025\Pro\Draft\ABC_RSR_Calculation_Pro\ABC_RSR_Calculation\ABC_RSR_Calculation.gdb\LCVC_Canada_USA_Albers_Lookup_30m"
LCVC_zonal_output_gdb = r"S:\Projects\ABC\y2025\Data\Intermediate\LCVC_ZonalStats_bySubtype.gdb"
LCVCextracts_gdb = r"S:\Projects\ABC\y2025\Data\Intermediate\LCVC_ExtractbySubtype.gdb"
log_file_path = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\HabitatThreatScoring\ABC_HabRangeMaps_Wheels\script_log.log"

# functions #################################################

# Function to log messages with timestamp
def log_message(message):
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")
