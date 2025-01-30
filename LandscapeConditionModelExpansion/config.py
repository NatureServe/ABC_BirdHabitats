# config.py
# this loads in the paths and settings so all the MoBI code are using the same value

import arcpy
import os
import datetime

# paths
outFolder = r"D:\ABC_fy25\ExpandingLCM"
SoutFolder = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\LCM\Outputs"
intGDB = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\ABC_fy25.gdb"
LCMmask = os.path.join(intGDB, "ArcticCan_HI_AK_dslv")
ABC_landcov = os.path.join(intGDB, "ABCmap_SuburbanUrbanCroplands")
ABC_landcov_mask = os.path.join(intGDB, "ABCmap_SuburbanUrbanCroplands_mask")
Croplands = os.path.join(intGDB, "LCMinput_Croplands")
Croplands_DA = os.path.join(outFolder, "DAout_Croplands.tif")
#Suburban = os.path.join(outFolder, "LCMinput_Suburban.tif")
#Suburban_DA = os.path.join(outFolder, "DistAcc_Suburban.tif")
Sub_AK = os.path.join(outFolder, "Sub_AK.tif")
Sub_ArcCan = os.path.join(outFolder, "Sub_ArcticCan.tif")
Sub_HI = os.path.join(outFolder, "Sub_HI.tif")
Sub_HI_DA = os.path.join(SoutFolder, "DistAcc_Sub_HI.tif")
Sub_AK_DA = os.path.join(SoutFolder, "DistAcc_Sub_AK.tif")
Sub_ArcCan_DA = os.path.join(SoutFolder, "DistAcc_Sub_Can.tif")
Urban = os.path.join(intGDB, "LCMinput_Urban")
Urban_DA = os.path.join(outFolder, "DAout_Urban.tif")
CanRoadNet = r"S:\Projects\_Workspaces\Hannah_Hyatt\NatureServe_ExplorerPro\NSXpro\NSXpro_testing.gdb\CanadianRoadNetwork_ArcticCan"

LCM_weights = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\LCM\Inputs\LCM_weights_Urb_Crop.csv"
LCM_weights_sub = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\LCM\Inputs\LCM_weights_Sub.csv"
#LCM_weights_test = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\LCM\Inputs\LCM_weights_test.csv"
#LCM_weights_v2 = r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\LCM\Inputs\LCM_weights_v2.csv"

LCM_30m = r"S:\Data\NatureServe\Landscape_Condition\Americas_N_LCM_Cat100.tif"

### environments
##with arcpy.EnvManager(outputCoordinateSystem='PROJCS["North_America_Albers_Equal_Area_Conic",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-96.0],PARAMETER["Standard_Parallel_1",20.0],PARAMETER["Standard_Parallel_2",60.0],PARAMETER["Latitude_Of_Origin",40.0],UNIT["Meter",1.0]]',
##                      cellSize="Americas_N_LCM_Cat100_resample30m.tif",
##                      scratchWorkspace=r"S:\Projects\ABC\y2025\Workspace\Hannah_Ceasar\ABC_fy25\ABC_fy25.gdb"):


# functions #################################################

# Function to log messages with timestamp
def log_message(message):
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")
