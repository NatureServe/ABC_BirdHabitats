# The purpose of this script is to QC the working habitats for the 2022 ABC project
# Below outlines the steps as I see them playing out as I am developing the script and are subject to change
# 1.) Tabulate area of habitat codes in each 343 sq mi hex
# 2.) Extract individual tables by habitat code - listing hexids that overlap that habitat --> this area of the script can probably be improved upon
# 3.) Loop through habitat code tables and select hexgrid layer by attribute, feature class to feature class to return
#     hexes where each habitat is found.

import arcpy, os, re
from arcpy.sa import *
import datetime

current_datetime = datetime.datetime.now()
timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print("Script started at: " + timestamp)

# Check out any necessary licenses.
arcpy.CheckOutExtension("spatial")

## Input Variables
hexgrid = r"S:\Projects\ABC\y2022\Pro\Draft\QC_Efforts\QC_Efforts\Default.gdb\nhf_summary_hexes_l1" ## UPDATE: with entire 343 hex grid, or extract of area of interest
WorkingHabitat = r"S:\Projects\ABC\y2022\Pro\FinalMapAssembly\combined29_HoleFillingPartial_LU.tif" ## UPDATE: with entire habtiat layer or extract of area of interest

## Set environments
intWorkspace = r"S:\Projects\ABC\y2022\Pro\Draft\QC_Efforts\QC_Efforts\IntermediateTables.gdb" #UPDATE
finalOutputs = r"S:\Projects\ABC\y2022\Pro\Draft\QC_Efforts\QC_Efforts\ExtractedHabitats.gdb"#UPDATE
finalOutputs_dslv = r"S:\Projects\ABC\y2022\Pro\Draft\QC_Efforts\QC_Efforts\ExtractedHabitats_dslv.gdb"
arcpy.env.workspace =  r"S:\Projects\ABC\y2022\Pro\Draft\QC_Efforts\QC_Efforts\Default.gdb" #UPDATE
arcpy.env.overwriteOutput =  True

value_list = [] 
with arcpy.da.SearchCursor(WorkingHabitat, ["HabitatCod","Primary_"]) as cursor:
    for row in cursor:
        value_list.append(row)

col_idx = 1
        
print("Tabulate area of " + str(len(value_list)) + " NVC groups by 343sqmi hex")
print("===============================================================================")

###Tabulate area
HabitatTable = r"S:\Projects\ABC\y2022\Symbology\PrimaryHabitatMapping\PrimaryHabitatSymbology_202311.csv"
TabArea_out = fr"TabArea_HabinHex"
arcpy.sa.TabulateArea(hexgrid, "summary_hex_l1_id", WorkingHabitat, "HabitatCod", TabArea_out, WorkingHabitat, "CLASSES_AS_ROWS")
arcpy.management.JoinField(TabArea_out, "HabitatCod", HabitatTable, "HabitatCode", "MajorGrp_Flat;MajorGrp_Code;Primary_;Primary_Code;Subtype;Subtype_Code;Reference;ClassName;Red;Green;Blue")

print("1) Looping through and extracting tables of habitats by hex")
print("===============================================================================")

 Get a list of unique habitat codes
TabArea_out = r"S:\Projects\ABC\y2022\Pro\Draft\QC_Efforts\QC_Efforts\Default.gdb\TabArea_HabinHex"
habitat_codes = set(row[0] for row in arcpy.da.SearchCursor(TabArea_out, "Primary_"))

for habcode in habitat_codes:
    print(f"Working on {habcode}")
    
    # select hexids for each habitat code
    w_clause = "Primary_ = '{}'".format(habcode)

    cleaned_string = re.sub(re.compile(r'[^a-zA-Z0-9]'), '', habcode)

    table_export = arcpy.conversion.TableToTable(TabArea_out, out_path = intWorkspace, out_name =f"{cleaned_string}", where_clause = w_clause)
    print(str(habcode) + " Table exported")

print("2) Looping through habitat tables and creating individual habitat/hex outputs")
print("===============================================================================")

 create a list of tables
arcpy.env.workspace = intWorkspace
habitat_tables = arcpy.ListTables()

# loop through tables and join them to hexgrid
for table in habitat_tables:
    output_name = f"{table}"
    link_field = "summary_hex_l1_id"

    #get a list of hex ids from the table
    hexid = []
    with arcpy.da.SearchCursor(table, [link_field]) as cursor:
        for row in cursor:
            hexid.append(row[0])
            
    # Create a query string to use in the selection
    query = "{} IN ({})".format(link_field, ', '.join(map(str, hexid)))

    # Escape single quotes if the field's data type is string/text
    if arcpy.ListFields(hexgrid, link_field)[0].type == "String":
        query = "{} IN ({})".format(link_field, ', '.join(map(lambda x: f"'{x}'", hexid)))

    print("working on" + table)
    #perform selection based on query
    selected_features = arcpy.SelectLayerByAttribute_management(in_layer_or_view=hexgrid, where_clause = query)

    #create new feature class from selected features
    arcpy.FeatureClassToFeatureClass_conversion(in_features = selected_features, out_path = finalOutputs, out_name =output_name)
    print(table + " complete")
##

print("3) Looping through individual habitat outputs and dissolving hexes")
print("===============================================================================")

# create a list of feature classes
arcpy.env.workspace = finalOutputs
habitat_hexes = arcpy.ListFeatureClasses()

# loop through final feature classes and dissolve hexes into one feature class
for fc in habitat_hexes:
    finalOutput_dslv = f"{finalOutputs_dslv}\\{fc}"

    #Dissolve hexes into one feature class
    arcpy.management.Dissolve(fc, finalOutput_dslv,None, None, "MULTI_PART", "DISSOLVE_LINES")
    print(fc + " dissolved")

    #Create Display field
    expression = f'"{fc}"'
    arcpy.management.AddField(finalOutput_dslv, "Display", "TEXT")
    arcpy.management.CalculateField(finalOutput_dslv, "Display", expression)
    print("Display field created")

current_datetime = datetime.datetime.now()
timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print("Script complete at: " + timestamp)
