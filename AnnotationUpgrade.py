# Project: AL Web Map - Annotations
# Create Date: 03/24/2020
# Last Updated: 04/17/2020
# Create by: Robert Domiano
# Updated by: 
# Purpose: To create a current copy of Spire AL annotation FC's and upgrade them using Pro's Upgrade Dataset tool.
# ArcGIS Version:   ArcGIS Pro 2.4.1 [Must use 2.1+]
# Python Version:   3.X
# For a changelog of updates, visit the github at: https://github.com/SpireBadger/XXX
# -----------------------------------------------------------------------
##
import arcpy
import os, datetime, sys
 
arcpy.env.overwriteOutput=True        
    
# Set workspace, input and output names
ws = r"D:\GisServerManager\Data\ALWebViewer_Annotation"
# Set workspace gdb
wsGDB = r"D:\GisServerManager\Data\ALWebViewer_Annotation\ALWebViewer_Annotation.gdb"
# Set project
project = r"C:\Users\GISADMIN\Documents\ArcGIS\Projects\ALWebViewer\ALWebViewer.aprx"
# Declare project as project
prj = arcpy.mp.ArcGISProject(project)
# set default gdb
prj.defaultGeodatabase = wsGDB
# set service variable for later use
service = "GasText_Published"

# Create a text file to log the results
date = datetime.datetime.now()
logName = "LogFile.txt"
logPath = os.path.join(ws, logName)
log = open(logPath, "w")
print("Log:" + str(date))
log.write("Log: " + str(date) + "\n")
print("\n")

# Create a temporary SDE c onnection
sdeAL = arcpy.CreateDatabaseConnection_management(ws,'tempALServ.sde',\
                                                  'ORACLE',\
                                                 'xs-bhm-dgp-1.energen.com:1521/gsp',\
                                                 'DATABASE_AUTH', 'GISADMIN',\
                                                 'gisadmin','SAVE_USERNAME')
print("Database connection created at {0} to the Alabama Database.".format(ws))
print("\n")
log.write("Database connection created at " + str(ws) + "\n")

# Copy all annotation features to the GDB, overwrite if already present
# Test list for running with one annotation
#gasList = ['ServiceText']

#gasList = ['ServiceText', 'MainText', 'CasingText','ValveText','FittingText',\
#            'RetiredMainText','RetiredServiceText','RegulatorStationText',\
#            'StopperFittingText','MainAuthorizationNumberText', 'TownBorderStationText']
#landList = ['MiscellaneousText','LeaderLine','HookLeader','StationPlus',\
#            'DetailAnnotation','Notes','LocationMeasurement', 'DetailPolygon',\
#            'PavementText','MiscellaneousLines','ROWText']
##lotID = ['LotID']
#
## Iterate through all desired variables in gasList    
#for item in gasList:
#    # Set the input FC to be copied
#    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.' + item
#    # If the input FC exists (this is for security in case afeature class name changes)
#    if arcpy.Exists(inputFC):
#        print("The annotation layer {0} was found at {1}.".format(item,inputFC))
#        log.write("The annotation layer" + str(item) + "was found at " + str(inputFC) + "\n")
#        # Set output path
#        outPath = os.path.join(wsGDB, item)
#        outputFC = arcpy.CopyFeatures_management(inputFC, outPath)
#        dateLoop = datetime.datetime.now()
#        print("The feature {0} has been copied to {1} at {2}.".format(item, outPath, dateLoop))
#        log.write("The feature has been copied." + str(dateLoop) + "\n")
#        print("Upgrading the dataset now at {0}.".format(dateLoop))
#        print("\n")
#        arcpy.UpgradeDataset_management(outputFC)
#        dateLoop2 = datetime.datetime.now()
#        print("The dataset finished upgrading at {0}.".format(dateLoop2))
#        log.write("The dataset finished upgrading at " + str(dateLoop2) + "\n")
#        # If the path exists, delete it first and then copy features
##        if arcpy.Exists(outPath):
##            print("The feature {0} already exists in the database and will be overwritten.".format(outPath))
##            arcpy.Delete_management(outPath)
##            outputFC = arcpy.CopyFeatures_management(inputFC, outPath)
##            print("\n")
##        # If the path doesn't exist, copy features
##        else:
##            print("The feature {0} does not yet exist and will be created.".format(outPath))
##            outputFC = arcpy.CopyFeatures_management(inputFC, outPath)
##            print("A copy has been created at {0}.".format(outputFC))
##            print("\n")        
#    else:
#        print("The feature class {0} could not be found in the AL SDE. Verify the name is correct.".format(inputFC))
#        log.write("The feature class" + str(inputFC) + "could not be found in the AL SDE. Verify the name is correct." + "\n")
#        print("\n")
#
## This section goes through the LandList list of annotation features from the AL SDE.        
#for item in landList:
#    # Set the input FC to be copied
#    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.' + item
#    # If the input FC exists (this is for security in case afeature class name changes)
#    if arcpy.Exists(inputFC):
#        print("The annotation layer {0} was found at {1}.".format(item,inputFC))
#        log.write("The annotation layer" + str(item) + "was found at " + str(inputFC) + "\n")
#        # Set output path
#        outPath = os.path.join(wsGDB, item)
#        outputFC = arcpy.CopyFeatures_management(inputFC, outPath)
#        dateLoop = datetime.datetime.now()
#        print("The feature {0} has been copied to {1}.".format(item, outPath))
#        log.write("The feature has been copied." + str(dateLoop) + "\n")
#        desc = arcpy.Describe(outputFC)
#        if desc.featureType == 'Annotation':
#            print("Upgrading the dataset now...")
#            print("\n")
#            arcpy.UpgradeDataset_management(outputFC)
#            dateLoop2 = datetime.datetime.now()
#            print("The dataset finished upgrading at {0}.".format(dateLoop2))
#            log.write("The dataset finished upgrading at " + str(dateLoop2) + "\n")
#    else:
#        print("The feature class {0} could not be found in the AL SDE. Verify the name is correct.".format(inputFC))
#        log.write("The feature class" + item + "could not be found in the AL SDE. Verify the name is correct." + "\n")
#        print("\n")
        
#for item in lotID:
#    # Set the input FC to be copied
#    inputFC = "\\\\gisappser2\\GIS_Coordinator\\ArcGIS_Online\\PublishedLayers_Portal\\Spire_Gulf_MS_Portal\\Mobile_LotID.gdb\Data\\" + item
#    # If the input FC exists (this is for security in case afeature class name changes)
#    if arcpy.Exists(inputFC):
#        print("The annotation layer {0} was found at {1}.".format(item,inputFC))
#        # Set output path
#        outPath = os.path.join(wsGDB, item)
#        outputFC = arcpy.CopyFeatures_management(inputFC, outPath)
#        print("The feature {0} has been copied to {1}.".format(item, outPath))
#        print("Upgrading the dataset now...")
#        print("\n")
#        arcpy.UpgradeDataset_management(outputFC)
 
# Clear out the workspace, this allows os.remove to delete the SDE connection file created.
arcpy.env.workspace = ""
print("Removing temporary SDE Connection Files.")
log.write("Removing temporary SDE Connection Files." + "\n")
#Remove the SDE
os.remove(sdeAL.getOutput(0))
# Close the log file
log.close()

# Send Email
# List of people to email
recepientAddress = "robert.domiano@spireenergy.com"
# String as command line using the blat.exe SMTP program from www.blat.net to send email
command = 'D:\GisServerManager\ServiceMonitor\\bin\\blat.exe -f robert.domiano@spireenergy.com -to {} -s "Annotation Upgrade Script log" -body "New log from Annotation Upgrade Script. Please see attached report for more details.<br><br>This is an automated email. Please do not reply." -server emailserver.lac1.biz:25 -attach "{}" -html'.format(recepientAddress,logPath)
# Enter system command
os.system(command)        