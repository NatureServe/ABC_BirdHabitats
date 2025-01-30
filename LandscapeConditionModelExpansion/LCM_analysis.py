## Data prep for running LCM Analysis
## This was developed for FY25 ABC project where we need to expand the LCM to arctic Canada, Alaska, and Hawaii
## Some data prep was done manually and will be outlined below:
## - downloaded and rasterized the Canadian Road Network data to get anthropogenic lands in arctic Canada
## - built a polygon mask for arctic Canada, AK and HI


# Import system modules
import os, arcpy, config
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

###############################
def dataprep ():
    config.log_message("Starting data prep")
    # mask suburban, urban and cropland habitat types from ABC map
    print("Masking ABC input to project boundary")
    ABC_landcov_mask = os.path.join(config.intGDB, "ABCmap_SuburbanUrbanCroplands_mask")
    outExtractByMask = ExtractByMask(config.ABC_landcov, config.LCMmask)
    outExtractByMask.save(ABC_landcov_mask)
    
    # extract by attribute ABC development land types
    print("Extracting individual habitat types")
    where_clause = "Primary_ = 'Cropland'"
    outExtractByAtt = ExtractByAttributes(ABC_landcov_mask, where_clause)
    outExtractByAtt.save(config.Croplands)
    print("Croplands prepped and ready")

    where_clause = "Primary_ = 'Urban'"
    outExtractByAtt = ExtractByAttributes(ABC_landcov_mask, where_clause)
    outExtractByAtt.save(config.Urban)
    print("Urban areas prepped and ready")

    where_clause = "Primary_ = 'Suburban'"
    Suburban_int = os.path.join(config.outFolder, "ABCmap_SuburbanExtract.tif")
    outExtractByAtt = ExtractByAttributes(ABC_landcov_mask, where_clause)
    outExtractByAtt.save(Suburban_int)
    print("Intermediate Suburban layer saved: ", Suburban_int)
    out_raster = arcpy.sa.CellStatistics(
        in_rasters_or_constants= [Suburban_int, config.CanRoadNet],
        statistics_type="MAXIMUM",
        ignore_nodata="DATA",
        process_as_multiband="SINGLE_BAND",
        percentile_value=90,
        percentile_interpolation_type="AUTO_DETECT"
    )
    out_raster.save(config.Suburban)
    print("Suburban areas prepped and ready")
    config.log_message("Data prep complete")

    # Mosaic Suburban rasters together
    

###################################
def creatdist():

    config.log_message("Calculating Distance Accumulation rasters")
    
    print("- Creating Distance Raster for Croplands")
    with arcpy.EnvManager(mask=config.LCMmask):
        out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation(config.Croplands, None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
        out_distance_accumulation_raster.save(config.Croplands_DA)
     
    print("- Creating Distance Raster for Urban lands")
    with arcpy.EnvManager(mask=config.LCMmask):
        out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation(config.Urban, None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
        out_distance_accumulation_raster.save(config.Urban_DA)

    print("- Creating Distance Raster for Suburban lands in Hawaii")
    with arcpy.EnvManager(mask=os.path.join(config.intGDB, "HI_boundary")):
        out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation(config.Sub_HI, None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
        out_distance_accumulation_raster.save(config.Sub_HI_DA)
        config.log_message("Hawaiian Suburban Distance Accumulation complete")

    print("- Creating Distance Raster for Suburban lands in Alaska")
    with arcpy.EnvManager(mask=os.path.join(config.intGDB, "AK_boundary")):
        out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation(config.Sub_AK, None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
        out_distance_accumulation_raster.save(config.Sub_AK_DA)
        config.log_message("Alaskan Suburban Distance Accumulation complete")    

    print("- Creating Distance Raster for Suburban lands in Arctic Canada")
    with arcpy.EnvManager(mask=os.path.join(config.intGDB, "ArcticCanada_noLCM")):
        out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation(config.Sub_ArcCan, None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
        out_distance_accumulation_raster.save(config.Sub_ArcCan_DA)
        config.log_message("Arctic Canadian Suburban Distance Accumulation complete")

#####################################################
# create the weights
def inputweights():

    config.log_message("Creating the distance decay rasters")

    fTable = config.LCM_weights
    fields = ['Category','InputTheme','DistFilename','FunctionType','a','b','c','w','DecayDistance'] # need to add a use column

    with arcpy.da.SearchCursor(fTable, fields) as cursor:
        for row in cursor:
            
            # these are variables holding individual field values from {sub_row}
            val_cat = row[0]
            val_inputtheme = row[1]
            val_fn = row[2]
            val_type = row[3]
            val_a = row[4]
            val_b = row[5]
            val_c = row[6]
            val_w = row[7]
            val_decay = row[8]

            val_fn = val_fn.replace('Dist_','')
            print(val_fn)
            weighted_output = os.path.join(config.outFolder, "Wgt_"+val_fn+".tif")
            print("Saving to: ", weighted_output)

            theDivide = Divide(os.path.join(config.intGDB, val_fn), val_c)
            theDivMinus = Minus(theDivide, val_a)
            theTimes = Times(theDivMinus,val_b)
            theExp = Exp(theTimes)
            thePlus = Plus(theExp, 1)
            theDivide2 = Divide(1,thePlus)
            theTimes2 = Times(theDivide2,val_w)
            theTimes2.save(weighted_output)
            print("Completed weight calculation for " + val_fn)

######################################################
# sum all the rasters
def rastersum():
    config.log_message("Summing all the rasters")

    arcpy.env.workspace = config.intGDB
    rastlist = arcpy.ListRasters("Wgt__*")
    print(rasterlist)
    
    outfile = "LCM_ArcticCanadaAKHI.tif"
    pixeltype = "32_BIT_FLOAT"
    numberbands = 1
    arcpy.management.MosaicToNewRaster(rastlist, config.outFolder, outfile, \
                                       'PROJCS["USA_Contiguous_Albers_Equal_Area_Conic_USGS_version",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-96.0],PARAMETER["Standard_Parallel_1",29.5],PARAMETER["Standard_Parallel_2",45.5],PARAMETER["Latitude_Of_Origin",23.0],UNIT["Meter",1.0]]', \
                                       pixeltype, None, numberbands, "SUM", "FIRST")

    intLCM = os.path.join(config.outFolder, outfile)
    config.log_message("Working on scaling "+ intLCM)
    maxvalue = float(arcpy.GetRasterProperties_management (intLCM, "MAXIMUM").getOutput (0))
    print(maxvalue)

    scaled_output = Times(Divide(intLCM, maxvalue), 100)
    scaled_output1 = Abs(Minus(scaled_output, 100))
    scaled_output1.save(os.path.join(config.intGDB, "ScaledOutput_LCM"))
    config.log_message("Script complete")

######################################################
# Run the script

#dataprep()
#creatdist()
#inputweights()
rastersum()
