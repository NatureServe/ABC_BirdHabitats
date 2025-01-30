## Landscape Condition Assessment:
## Calculates the average landscape condition model value in hexagons across IVC groups of interest
## This code is developed as part of a series of scripts, and should be performed after a results table is built in a previous step
## Originally developed by Chris Tracey, edited by Hannah Ceasar in aug 2024
## * side note: we used to incorporate invasive risk scores into this analysis, no longer doing this as the ruderal type
##   that analysis is based upon needs to be updated

## Process:
## 1. Loop through group map and extract by attribute each group, extract by mask the LCM for each group
## 2. Using the hexagon based range map developed in the previous step for each indv group, perform zonal statistics to get the average LCM score by hex for the groups. Join this information back to the hex range map for that group
## 3. Merge all individual hex range maps together 


import arcpy, os, re, config
from arcpy.sa import *
import numpy as np
import datetime

arcpy.CheckOutExtension("spatial")

#print start time
config.log_message("starting script")

# List of HabitatCods to exclude
excluded_habcode_list = [117639, 117638, 117637, 128200, 128300, 128400, 128445, 128500, 128600]

# # Extract unique Habitat Code values from group map
# habcode_list = []
# with arcpy.da.SearchCursor(config.habmap, ["HabitatCod"]) as cursor:
#     for row in cursor:
#         habcode = row[0]
#         if habcode not in habcode_list and habcode not in excluded_habcode_list:
#             habcode_list.append(habcode)

# Extract unique Habitat Code values from SUBSET OF HABITATS THAT HAVE BEEN UPDATED:-- use when updating a subset of the map
habcode_list = []
with arcpy.da.SearchCursor(config.updated_subtypes_csv, ["HabitatCod"]) as cursor:
    for row in cursor:
        habcode = row[0]
        if habcode not in habcode_list and habcode not in excluded_habcode_list:
            habcode_list.append(habcode)

# Begin loop to calculate zonal statistics on LCM
for habcode in habcode_list:
    if habcode is not None:  # Skip any NoData values
        config.log_message(f"Working on HabitatCod: " + str(habcode))

        ### Prep for analysis ###
        zone_feature_class = os.path.join(config.subtype_output_gdb, "Subtype" + str(habcode))

        # Set the processing extent to the extent of the zone_feature_class
        arcpy.env.extent = arcpy.Describe(zone_feature_class).extent        

        # Construct the path to check if the file already exists
        extracted_habcode_path = os.path.join(config.subtype_extracts_gdb, "Extract"+str(habcode))

        # Check if the extracted habitat code already exists
        if arcpy.Exists(extracted_habcode_path):
            config.log_message(f"{extracted_habcode_path} already exists, skipping extraction for this habitat code.")
        else:
            # Perform Extract by Attributes to select the current Subtype
            print("Processing... " + str(habcode))
            habcode_query = f"HabitatCod = {habcode}"
            extracted_habcode = ExtractByAttributes(config.habmap, habcode_query)
            
            # Save the extracted Subtype raster
            extracted_habcode.save(extracted_habcode_path)
            config.log_message(f"{habcode} extracted and saved to {extracted_habcode_path}")

        # Construct the path to check if masked output exists
        output_path = os.path.join(config.LCMextracts_gdb, "LCM_"+str(habcode))

        # Check if file already exists
        if arcpy.Exists(output_path):
            config.log_message(f"{output_path} already exists, skipping this habitat code.")
        else:
            # Perform Extract by Mask to extract the LCM across the habitat range
            config.log_message("Extracting LCM for "+ str(habcode))
            masked_raster = ExtractByMask(config.LCM, extracted_habcode_path)

            # Save the extracted LCM raster
            masked_raster.save(output_path)
            config.log_message(str(habcode) + " saved here: " + output_path)

        ### Perform Zonal Statistics ###
        # Path to the output table for zonal statistics
        zonal_stats_table = os.path.join(config.zonal_output_gdb, f"ZonalStats_{habcode}")
        
        # Check if file already exists
        if arcpy.Exists(zonal_stats_table):
            config.log_message(f"{zonal_stats_table} already exists, skipping this.")
        else:
            #Perform Zonal Statistics as Table
            # Path to the feature class for this Subtype
            
            zone_feature_class = os.path.join(config.subtype_output_gdb, "Subtype"+str(habcode))
            print(f"performing zonal stats for {zone_feature_class}")
            arcpy.sa.ZonalStatisticsAsTable(zone_feature_class, "wheel_id", output_path, zonal_stats_table, "DATA", "MEAN")

            print(f"Zonal stats complete for " + str(habcode) + ", performing data clean up and join back to range map")

        # Reset the processing extent to default (None) after extraction
        arcpy.env.extent = None
        
        # Join zonal stats results to Subtype range map and clean up field name
        zone_feature_class = os.path.join(config.subtype_output_gdb, "Subtype"+str(habcode))
        arcpy.management.JoinField(in_data = zone_feature_class, in_field = "wheel_id", join_table = zonal_stats_table, join_field = "wheel_id", fields=["MEAN"])[0]
        arcpy.management.CalculateField(in_table=zone_feature_class, field="scoreLCM", expression="round(!MEAN!,1)", field_type="DOUBLE")
        arcpy.management.DeleteField(zone_feature_class, "MEAN")
        arcpy.management.AlterField(zone_feature_class, "scoreLCM", "scoreLCM", "LCM Score")

        # Reassign null LCM values to zero
##        print("reassigning NULL LCM values to 0")
##        with arcpy.da.UpdateCursor(zone_feature_class, "scoreLCM") as cursor:
##            for row in cursor:
##                for  i in range(len(row)):
##                    if row[i] is None:
##                        row[i] = 0
##                cursor.updateRow(row)
##        config.log_message("LCM clean up complete")

        ### Add and Calculate LCM_Index Field with Natural Breaks ###
        arcpy.management.AddField(zone_feature_class, "LCM_Index", "TEXT")

        # Assign categories based on scoreLCM ranges (Low < 33, Medium 33-66, High > 66)
        with arcpy.da.UpdateCursor(zone_feature_class, ["scoreLCM", "LCM_Index"]) as cursor:
            for row in cursor:
                score = row[0]
                if score is None:
                    row[1] = None  # Leave null values as null
                elif score < 33:
                    row[1] = "Low"
                elif 33 <= score <= 66:
                    row[1] = "Medium"
                else:
                    row[1] = "High"
                cursor.updateRow(row)

        config.log_message(f"LCM_Index field calculated for {habcode}")
config.log_message("All subtypes processed successfully.")


## Uncomment and run the following section if you are not also calculating LCVC (Conversion threat)

### Loop through the IVC group hex maps and merge them together
##print("- Merging IVC groups")
##arcpy.env.workspace = config.subtype_output_gdb
##feature_classes = arcpy.ListFeatureClasses()
##
##g_fcs = [fc for fc in feature_classes if fc.startswith('G')]
##
### Check if there are any feature classes to merge
##if g_fcs:
##    
##    # Merge the filtered feature classes
##    arcpy.management.Merge(g_fcs, config.SubtpeFinalOutput)
##    
##    print(f"Merged {len(g_fcs)} feature classes into {merged_output}")
##else:
##    print("No feature classes found that start with 'G'.")
##
### Print end time
config.log_message("Script complete")
