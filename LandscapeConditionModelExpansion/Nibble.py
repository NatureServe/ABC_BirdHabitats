# Nibble

import arcpy, os

LCM = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\ABC_fy25.gdb\LCM_NorthAmerica_30m"
NullValues = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\ABC_fy25.gdb\LCM_NorthAmerica_NullValues_ONLY"

print("working on Nibble")
with arcpy.EnvManager(extent="MAXOF", cellSize=LCM, scratchWorkspace=r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\ABC_fy25.gdb"):
    out_raster = arcpy.sa.Nibble(
        in_raster=LCM,
        in_mask_raster=NullValues,
        nibble_values="ALL_VALUES",
        nibble_nodata="PRESERVE_NODATA",
        in_zone_raster=None
    )
    out_raster.save(r"S:\Projects\ABC\y2025\Data\Final\LCM_NorthAmerica_30m_fillholes.tif")

print("Nibble complete")
