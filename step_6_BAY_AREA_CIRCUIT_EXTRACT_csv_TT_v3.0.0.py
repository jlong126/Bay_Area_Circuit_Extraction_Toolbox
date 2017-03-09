import csv, arcpy, os, sys

arcpy.env.overwriteOutput = True
arcpy.Delete_management("in_memory")

# INPUTS

INPUT_Final_Del_GDBs= arcpy.GetParameterAsText(0)
Symbology_LYR = arcpy.GetParameterAsText(1)
outFolder = arcpy.GetParameterAsText(2)


FINAL_XLSX = os.path.join(outFolder,"Final_Deliverable_CSVs")

FINAL_KMZ = os.path.join(outFolder,"Final_Deliverable_KMZ")

if not os.path.exists(FINAL_XLSX):
    os.makedirs(FINAL_XLSX)

if not os.path.exists(FINAL_KMZ):
    os.makedirs(FINAL_KMZ)



GDB_SPLIT = sorted(INPUT_Final_Del_GDBs.split(";"))

def split_following_num(s):
    prev_char = ''
    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char



exclude_fields = ('FID', 'OBJECTID', 'Shape')

arcpy.AddMessage("Creating TreeTop Detection CSVs...\n")

for i, circuit_GDB in enumerate(GDB_SPLIT):

    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    cir_csv = os.path.join(FINAL_XLSX, "%s_BAY_AREA_2016_TreeTops_AF.csv" % (cirNAME))

    inTTs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_TreeTops_AF" % (cirNAME))

    fields = [field.name for field in arcpy.ListFields(inTTs) if field.name not in exclude_fields]

    arcpy.AddMessage("{0:<60} ({1} of {2})".format(os.path.basename(cir_csv), i + 1, len(GDB_SPLIT)))

    with arcpy.da.SearchCursor(inTTs, fields) as sCur, open(cir_csv, 'wb') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(fields)
        for row in sCur:
            records = list(row)
            writer.writerow(records)


arcpy.AddMessage("\nCreating Urgent TreeTop Detection KMZs...\n")

## KML Creation

composite = 'NO_COMPOSITE'
pixels = 1024
dpi = 96
clamped = 'CLAMPED_TO_GROUND'
QUERY = "'ZONE1','ZONE1_OH1','ZONE1_OH2'"




for i, circuit_GDB in enumerate(GDB_SPLIT):

    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    outKML = os.path.join(FINAL_KMZ, "%s_BAY_AREA_2016_TreeTops.kmz"%(cirNAME))
    inTTs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_TreeTops_AF"%(cirNAME))

    arcpy.MakeFeatureLayer_management(inTTs,"%s_BAY_AREA_2016_TreeTops_AF"%(cirNAME))
    arcpy.SelectLayerByAttribute_management("%s_BAY_AREA_2016_TreeTops_AF"%(cirNAME), "NEW_SELECTION",' "DC_AF" IN (%s) ' %(QUERY))


    result = arcpy.GetCount_management("%s_BAY_AREA_2016_TreeTops_AF"%(cirNAME))
    count = int(result.getOutput(0))

    if (count) > 0:


        arcpy.ApplySymbologyFromLayer_management("%s_BAY_AREA_2016_TreeTops_AF"%(cirNAME), Symbology_LYR)

        arcpy.LayerToKML_conversion("%s_BAY_AREA_2016_TreeTops_AF"%(cirNAME), outKML,'', '',
                                '', pixels, dpi, clamped)

        arcpy.AddMessage("CREATING KMZ for {0}".format(os.path.basename(outKML)))
    else:
        arcpy.AddMessage("NO ZONE1 DETECTIONS, NO KMZ CREATED for {0}".format(os.path.basename(outKML)))
        pass


