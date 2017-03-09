import os, arcpy, csv

arcpy.env.overwriteOutput = True
arcpy.Delete_management("in_memory")


Final_master_GDB= arcpy.GetParameterAsText(0)
Deliver_Name = arcpy.GetParameterAsText(1)
Symbology_LYR = arcpy.GetParameterAsText(2)
outFolder = arcpy.GetParameterAsText(3)


# DEL CSV
exclude_fields = ('FID', 'OBJECTID', 'Shape')

arcpy.AddMessage("Creating TreeTop Detection CSVs...\n")



del_csv = os.path.join(outFolder, Deliver_Name+"_BAY_AREA_2016_TreeTops_AF.csv")

try:

    inTTs = os.path.join(Final_master_GDB, "BAY_AREA_2016_Delivered_TreeTops_AF")

    fields = [field.name for field in arcpy.ListFields(inTTs) if field.name not in exclude_fields]

    QUERY = "'ZONE1','ZONE1_OH1','ZONE1_OH2'"

    arcpy.MakeFeatureLayer_management(inTTs, "BAY_AREA_2016_TreeTops_AF" )
    arcpy.SelectLayerByAttribute_management("BAY_AREA_2016_TreeTops_AF" , "NEW_SELECTION",' "DC_AF" IN (%s) ' % (QUERY))

    tempsublyrOUT = r'in_memory\TTs_Temp'

    arcpy.Select_analysis("BAY_AREA_2016_TreeTops_AF", tempsublyrOUT)

except:

    Arcpy.AddMessage("Your input GDB Treetops FC needs to be named:  >BAY_AREA_2016_Delivered_TreeTops_AF<")


with arcpy.da.SearchCursor(tempsublyrOUT, fields) as sCur, open(del_csv, 'wb') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(fields)
    for row in sCur:
        records = list(row)
        writer.writerow(records)

del tempsublyrOUT

# Del KML

composite = 'NO_COMPOSITE'
pixels = 1024
dpi = 96
clamped = 'CLAMPED_TO_GROUND'
QUERY = "'ZONE1','ZONE1_OH1','ZONE1_OH2'"


del_kml = os.path.join(outFolder, Deliver_Name+"_BAY_AREA_2016_TreeTops_AF.kmz")

inTTs = os.path.join(Final_master_GDB, "BAY_AREA_2016_Delivered_TreeTops_AF")


arcpy.MakeFeatureLayer_management(inTTs,"BAY_AREA_2016_TreeTops_AF_LYR")
arcpy.SelectLayerByAttribute_management("BAY_AREA_2016_TreeTops_AF_LYR", "NEW_SELECTION",' "DC_AF" IN (%s) ' %(QUERY))

arcpy.ApplySymbologyFromLayer_management("BAY_AREA_2016_TreeTops_AF_LYR", Symbology_LYR)

arcpy.LayerToKML_conversion("BAY_AREA_2016_TreeTops_AF_LYR", del_kml, '', '','', pixels, dpi, clamped)