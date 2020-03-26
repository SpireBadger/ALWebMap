# Project: AL Web Map - Annotations
# Create Date: 03/24/2020
# Last Updated: 03/26/2020
# Create by: Robert Domiano
# Updated by: 
# Purpose: To create a current copy of Spire AL annotation FC's and upgrade them using Pro's Upgrade Dataset tool.
# ArcGIS Version:   ArcGIS Pro 2.4.1 [Must use 2.1+]
# Python Version:   3.X
# For a changelog of updates, visit the github at: https://github.com/SpireBadger/XXX
# -----------------------------------------------------------------------

import arcpy
import os

arcpy.env.overwriteOutput=True        
    
# Set workspace, input and output names
ws = r"\\gisappser2\gis_coordinator\ArcGIS_Online\PublishedLayers_Portal\Alagasco\MAGI Online Gas Features"
# Set workspace gdb
wsGDB = r"\\gisappser2\gis_coordinator\ArcGIS_Online\PublishedLayers_Portal\Alagasco\MAGI Online Gas Features\ALWebViewer.gdb"
# Set project
project = r"C:\Users\GISADMIN\Documents\ArcGIS\Projects\ALWebViewer\ALWebViewer.aprx"
# Declare project as project
prj = arcpy.mp.ArcGISProject(project)
# set default gdb
prj.defaultGeodatabase = wsGDB
# set service variable for later use
service = "GasText_Published"
# Set map to use from project
annoMap = prj.listMaps(service)[0]

# Remove existing layers
for lyr in annoMap.listLayers():
    annoMap.removeLayer(lyr)

# Create a temporary SDE c onnection
sdeAL = arcpy.CreateDatabaseConnection_management(ws,'tempALServ.sde',\
                                                  'ORACLE',\
                                                 'xs-bhm-dgp-1.energen.com:1521/gsp',\
                                                 'DATABASE_AUTH', 'GISADMIN',\
                                                 'gisadmin','SAVE_USERNAME')
print("Database connection created at {0} to the Alabama Database.".format(ws))

# Copy all annotation features to the GDB, overwrite if already present
# The list below is the test list
gasList = ['ServiceText', 'MainText']
# gasList = ['ServiceText', 'MainText', 'CasingText','ValveText','FittingText',\
#           'RetiredMainText','RetiredServiceText','RegulatorStationText',\
#            'StopperFittingText','MainAuthorizationNumberText']
# landList = ['MiscellaneousText','LeaderLine','HookLeader','StationPlus',\
#            'DetailAnnotation','Notes','LocationMeasurement']
# project '\GISADMIN.ProjectData\GISADMIN.ProjectBoundary

# Iterate through all desired variables in gasList    
for item in gasList:
    # Set the input FC to be copied
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.' + item
    # If the input FC exists (this is for security in case afeature class name changes)
    if arcpy.Exists(inputFC):
        print("The annotation layer {0} was found at {1}.".format(item,inputFC))
        # Set output path
        outPath = os.path.join(wsGDB, item)
        # If the path exists, delete it first and then copy features
        if arcpy.Exists(outPath):
            print("The feature {0} already exists in the database and will be overwritten.".format(outPath))
            arcpy.Delete_management(outPath)
            outputFC = arcpy.CopyFeatures_management(inputFC, outPath)
        # If the path doesn't exist, copy features
        else:
            print("The feature {0} does not yet exist and will be created.".format(outPath))
            outputFC = arcpy.CopyFeatures_management(inputFC, outPath)
            print("A copy has been created at {0}.".format(outputFC))            
    else:
        print("The feature class {0} could not be found in the AL SDE. Verify the name is correct.")
        break
    annoMap.addLayer(outputFC)
    arcpy.UpgradeDataset_management(outputFC)     
   
arcpy.env.workspace = ""
print("Removing temporary SDE Connection Files.")
os.remove(sdeAL.getOutput(0))
        