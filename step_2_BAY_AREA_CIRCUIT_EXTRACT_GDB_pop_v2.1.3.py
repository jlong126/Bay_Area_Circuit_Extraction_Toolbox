T## NOTES ##

'''want to be able to put all PROD SUB GROUP final spans shps in for the entire delivery'''

# IMPORTS
import arcpy, os ,sys, re, glob

arcpy.env.overwriteOutput = True    
arcpy.Delete_management("in_memory")


INPUT_spans = arcpy.GetParameterAsText(0)
Prod_Sub_GDB = arcpy.GetParameterAsText(1)
working_Prod_Sub_GDB = arcpy.GetParameterAsText(2)
OutFolder = arcpy.GetParameterAsText(3)

## HARDCODE INPUTS
'''INPUT_spans = "D:\SCRIPT_LIBRARY\BAY_AREA_CIRCUIT_EXTRACTION_working\TEST_OUTPUT\CIRCUIT_EXTRACT_needs_edits\ALTAMONT 0201_ALTAMONT_PROD_SUB_GROUP_EXTRACT_NEEDS_EDITS.shp"
Prod_Sub_GDB = "D:\SCRIPT_LIBRARY\BAY_AREA_CIRCUIT_EXTRACTION_working\TEST_SHAPES\BAY_AREA_2016_inSITE_R4_ALTAMONT_SUB_GROUP_BAY_AREA_2016.gdb"
OutFolder = "D:\SCRIPT_LIBRARY\BAY_AREA_CIRCUIT_EXTRACTION_working\TEST_OUTPUT"'''

InSiteReadyFolder = os.path.join(OutFolder,"inSITE_Ready_CIRCUITS")

ref = os.path.join(OutFolder,"CIRCUIT_REFERENCE")
ex = os.path.join(OutFolder,"CIRCUIT_EXTRACT_needs_edits")
edit = os.path.join(OutFolder,"CIRCUIT_EXTRACT_edited")
sub_ref = os.path.join(OutFolder,"SUB_GROUP_REF")

if not os.path.exists(ref):
    os.makedirs(ref)
if not os.path.exists(ex):
    os.makedirs(ex)
if not os.path.exists(sub_ref):
    os.makedirs(sub_ref)
if not os.path.exists(edit):
    os.makedirs(edit)

if not os.path.exists(InSiteReadyFolder):
    os.makedirs(InSiteReadyFolder)

circuits = sorted(INPUT_spans.split(";"))


def split_following_num(s):
    prev_char = ''

    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char

#irNUM = split_following_num(circuit)

#arcpy.AddMessage(">%s< Creating Circuit inSITE Ready GDBs....\n" % cirNUM)


for circuit in circuits:
    cirNAME = split_following_num(os.path.basename(circuit))



for circuit in circuits:
    cirNAME = split_following_num(os.path.basename(circuit))

    #cir_FN_sep = os.path.split(circuit)
    #cirNUM = cir_FN_sep[1]

    arcpy.AddMessage(">%s< Creating Circuit inSITE Ready GDBs....\n" % cirNAME)

    arcpy.CreateFileGDB_management(InSiteReadyFolder, cirNAME+"_inSITE_Ready_BAY_AREA_2016")

circuit_GDBs_List = []
arcpy.env.workspace = InSiteReadyFolder
for file in arcpy.ListFiles("*.gdb"):
    circuit_GDBs_List.append(file)


### each EDIT span shape will need to have select by location analysis done on it against the inSIDE sub GDB
feature_classes = []
walk = arcpy.da.Walk(Prod_Sub_GDB, datatype="FeatureClass")

for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        #if filename.endswith("Spans"):
        feature_classes.append(os.path.join(dirpath, filename))

for prod_sub in feature_classes:
    if prod_sub.endswith("Spans"):
        arcpy.MakeFeatureLayer_management(prod_sub, "Prod_sub_spans_LYR")
        ## Circuit inSite Ready Spans extract from inSITE sub GDB
        for cir_edit,circuit_GDB in zip(circuits,circuit_GDBs_List):

            cirNAME = split_following_num(os.path.basename(cir_edit))

            arcpy.AddMessage(">%s< Spans Extraction Processing....\n" % cirNAME)

            #arcpy.MakeFeatureLayer_management(prod_sub, "Prod_sub_spans_LYR")
            arcpy.SelectLayerByLocation_management("Prod_sub_spans_LYR", "INTERSECT", cir_edit, "", "NEW_SELECTION")

            out_shp = InSiteReadyFolder + r"\%s_BAY_AREA_2016_inSITE_Ready_Spans.shp" %(cirNAME)

            arcpy.Select_analysis("Prod_sub_spans_LYR", out_shp )
            arcpy.FeatureClassToGeodatabase_conversion(out_shp, circuit_GDB)
            arcpy.Delete_management(out_shp)

### Circuit inSITE Ready Towers
for prod_sub in feature_classes:
    if prod_sub.endswith("Towers"):
        arcpy.MakeFeatureLayer_management(prod_sub, "Prod_sub_Towers_LYR")

        for circuit_GDB in circuit_GDBs_List:
            cirNAME = split_following_num(os.path.basename(circuit_GDB))


            arcpy.AddMessage(">%s< Towers Extraction Processing....\n" % cirNAME)

            inSpans = os.path.join(circuit_GDB,"%s_BAY_AREA_2016_inSITE_Ready_Spans"%(cirNAME))
            inTowers = os.path.join(circuit_GDB,"%s_BAY_AREA_2016_inSITE_Ready_Towers"%(cirNAME))
            arcpy.SelectLayerByLocation_management("Prod_sub_Towers_LYR", "INTERSECT", inSpans, "", "NEW_SELECTION")
            arcpy.Select_analysis("Prod_sub_Towers_LYR", inTowers)

### Circuit inSITE Ready TTs Extraction

for prod_sub in feature_classes:
    if prod_sub.endswith("TreeTops_AF"):
        arcpy.MakeFeatureLayer_management(prod_sub, "Prod_sub_TreeTops_AF_LYR")

        TreeTop_SpanTags = []

        with arcpy.da.SearchCursor(prod_sub, ["SPAN_TAG"]) as sCur:
            [TreeTop_SpanTags.append(row) for row in sCur]

        for circuit_GDB in circuit_GDBs_List:
            cirNAME = split_following_num(os.path.basename(circuit_GDB))

            arcpy.AddMessage(">%s< Tree Top Extraction Processing....\n"%cirNAME)

            CircuitSpan_SpanTags = []

            inSpans = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_Spans" % (cirNAME))
            inTTs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_TreeTops_AF" % (cirNAME))

            arcpy.CreateFeatureclass_management(circuit_GDB, os.path.basename(inTTs), 'Point')

            with arcpy.da.SearchCursor(inSpans, ["SPAN_TAG"]) as sCur:
                for row in sCur:
                    CircuitSpan_SpanTags.append(str(row[0]))

            #CircuitSpan_SpanTags_JOIN = ",".join(CircuitSpan_SpanTags)

            span_tags = ','.join(["'{}'".format(tag) for tag in CircuitSpan_SpanTags])

            arcpy.SelectLayerByAttribute_management("Prod_sub_TreeTops_AF_LYR", "NEW_SELECTION", ' "SPAN_TAG" in (%s) '%span_tags)
            arcpy.CopyFeatures_management("Prod_sub_TreeTops_AF_LYR",inTTs)

## Circuit inSITE TreePolys extract

VP_FC_List = []
working_walk = arcpy.da.Walk(working_Prod_Sub_GDB, datatype="FeatureClass")

for dirpath, dirnames, filenames in working_walk:
    for filename in filenames:
        if filename.endswith("tree_polys_attributed"):
            VP_FC_List.append(os.path.join(dirpath, filename))

for VP_FC in VP_FC_List:
    arcpy.MakeFeatureLayer_management(VP_FC, "VP_LYR")

    for circuit_GDB in circuit_GDBs_List:
        cirNAME = split_following_num(os.path.basename(circuit_GDB))


        arcpy.AddMessage(">%s< Vegetation Polys Extraction Processing....\n" % cirNAME)

        inTTs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_TreeTops_AF" % (cirNAME))
        outVPs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_VegPolys" % (cirNAME))

        arcpy.CreateFeatureclass_management(circuit_GDB, os.path.basename(outVPs), 'Polygon')
        arcpy.SelectLayerByLocation_management("VP_LYR","INTERSECT", inTTs, "", "NEW_SELECTION")

        arcpy.CopyFeatures_management("VP_LYR", outVPs)






















































