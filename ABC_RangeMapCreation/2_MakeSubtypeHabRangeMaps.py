## The following code was modified from Chris Tracey by Hannah Ceasar in Sept 2024
## It maps individual 49 square mile hexagon based range maps for the ABC map
## then merges them together to support joining results of other spatial analyses to the ABC map (like LCM)

import config
import re, arcpy

# Start script
config.log_message("Script started")

# List all fields in groupmap raster to confirm their names
fields = arcpy.ListFields(config.habmap)
field_names = [field.name for field in fields]
config.log_message(f"Field names in ABC map: {field_names}")

# Extract and export tables for each habitat group
config.log_message("Extracting and exporting tables for all habitats")
try:
    hab_codes = list(set(row[0] for row in arcpy.da.SearchCursor(config.SubtypeHab_OutputTbl, "HabitatCod")))
    config.log_message(f"Habitat codes to process: {hab_codes}")

    for habcode in hab_codes:
        config.log_message(f"Working on hab_code: {habcode}")

        w_clause = f"HabitatCod = {habcode}"
        cleaned_string = re.sub(re.compile(r'[^a-zA-Z0-9]'), '', str(habcode))
        table_name = f"tbl_{cleaned_string}"

        if not cleaned_string:
            config.log_message("Skipping empty cleaned string")
            continue

        try:
            config.log_message(f"Exporting table for habitat: {habcode}")
            table_export = arcpy.conversion.TableToTable(config.SubtypeHab_OutputTbl, config.int_tbl_path_subtype, table_name, w_clause)
            config.log_message(f"{habcode} Table exported at: {config.int_tbl_path_subtype}\\{table_name}")
        except Exception as e:
            config.log_message(f"Error exporting table for hab_code {habcode}: {e}")

        # Process the specified habitat table and create individual habitat/hex outputs
        config.log_message("Starting habitat table processing")
        try:
            arcpy.env.workspace = config.int_tbl_path_subtype
            config.log_message(f"Current workspace: {arcpy.env.workspace}")

            habitat_tables = arcpy.ListTables()
            config.log_message(f"Habitat tables found: {habitat_tables}")

            if habitat_tables is None or not habitat_tables:
                config.log_message("No habitat tables found in the intermediate output path.")
                raise ValueError("No habitat tables found in the intermediate output path.")

            # Ensure we only process the specified habitat table
            if table_name not in habitat_tables:
                config.log_message(f"Specified habitat table {table_name} not found.")
                raise ValueError(f"Specified habitat table {table_name} not found.")

            table = table_name
            output_name = f"{table.replace('tbl_', 'Subtype')}"
            sub_code_int = f"{table.replace('Subtype','')}"
            sub_code = f"{table.replace('tbl_','')}"
            link_field = "wheel_id"

            hexid = []
            try:
                with arcpy.da.SearchCursor(table, [link_field]) as cursor:
                    hexid = [row[0] for row in cursor]
            except Exception as e:
                config.log_message(f"Error reading hex IDs from table {table}: {e}")

            hexid_str = ', '.join([f"'{x}'" for x in hexid])
            query = f"{link_field} IN ({hexid_str})"

            config.log_message(f"Creating hex poly layer for {table}")
            try:
                selected_features = arcpy.SelectLayerByAttribute_management(in_layer_or_view=config.hex49smooth, where_clause=query)
                arcpy.FeatureClassToFeatureClass_conversion(in_features=selected_features, out_path=config.subtype_output_gdb, out_name=output_name)
                config.log_message(f"{table} complete")

                # Add and calculate Primary Code field               
                arcpy.management.AddField(f"{config.subtype_output_gdb}\\{output_name}", "HabitatCod", "LONG")
                arcpy.management.CalculateField(f"{config.subtype_output_gdb}\\{output_name}", "HabitatCod", f'"{sub_code}"', "PYTHON3")
                config.log_message(f"Habitat Code field populated for {output_name}")

            except Exception as e:
                config.log_message(f"Error processing table {table}: {e}")

            # Add descriptive fields to feature classes
            config.log_message("Adding descriptive fields to feature classes")
            try:
                arcpy.env.workspace = config.subtype_output_gdb
                config.log_message(f"Current workspace: {arcpy.env.workspace}")

                # Process only the specific feature class that corresponds to the group code
                fc = output_name
                config.log_message(f"Processing feature class: {fc}")
                try:
                    # Log field names in the feature class to verify
                    fc_fields = arcpy.ListFields(fc)
                    fc_field_names = [field.name for field in fc_fields]
                    config.log_message(f"Field names in feature class {fc}: {fc_field_names}")

                    # Ensure 'Primary_Co' exists in the feature class before joining
                    if 'Primary_Co' in fc_field_names:
                        # Join specified fields from groupmap based on GroupKey
                        config.log_message(f"Joining fields from ABC map to feature class {fc}")
                        arcpy.management.JoinField(fc, "HabitatCod", config.habmap, "HabitatCod", fields =["Subtype","Primary_"])
                        config.log_message(f"Fields joined from groupmap to {fc}")
                        
                    else:
                        config.log_message(f"Field 'HabitatCod' does not exist in feature class {fc}. Skipping join.")
                except Exception as e:
                    config.log_message(f"Error processing feature class {fc}: {e}")

##                # Delete the intermediate table after all joins are completed
##                config.log_message(f"Deleting intermediate table: {table}")
##                config.arcpy.Delete_management(f"{intermediate_output_path}\\{table}")
##                config.log_message(f"Intermediate table {table} deleted")

            except Exception as e:
                config.log_message(f"Error adding descriptive fields: {e}")
                raise

        except Exception as e:
            config.log_message(f"Error during habitat table processing: {e}")
            raise

except Exception as e:
    config.log_message(f"Error extracting and exporting tables: {e}")
    raise


### Loop through all feature classes in the final output path and merge them together
##config.log_message("Starting merge of all feature classes in final output path")
##
##try:
##    arcpy.env.workspace = config.subtype_output_gdb
##    feature_classes = arcpy.ListFeatureClasses()
##    
##    if feature_classes:
##        merged_output = "SubtypeHabitat_RangeMapsMerge"
##        config.log_message(f"Merging the following feature classes: {feature_classes}")
##        
##        # Merge all feature classes into one
##        arcpy.management.Merge(feature_classes, f"{config.subtype_output_gdb}\\{merged_output}")
##        config.log_message(f"Merged feature class created at: {config.subtype_output_gdb}\\{merged_output}")
##    else:
##        config.log_message("No feature classes found to merge.")
##except Exception as e:
##    config.log_message(f"Error during merge operation: {e}")
##    raise

config.log_message("Script completed")

