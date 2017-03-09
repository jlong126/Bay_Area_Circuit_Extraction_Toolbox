## NOTES ##

'''want to be able to put all PROD SUB GROUP final spans shps in for the entire delivery'''


# IMPORTS
import arcpy, os ,sys
from collections import defaultdict


arcpy.env.overwriteOutput = 1
arcpy.Delete_management("in_memory")


# INPUTS

INPUT_FinalSpans_Sub_Group = arcpy.GetParameterAsText(0)
PGE_Master_Circuits = arcpy.GetParameterAsText(1)
outFolder = arcpy.GetParameterAsText(2)
SearchTolerance = arcpy.GetParameterAsText(3)
INPUT_adjusted_circuits = arcpy.GetParameterAsText(4)

adj_circuits = sorted(INPUT_adjusted_circuits.split(";"))


## HARDCODE INPUTS

'''FinalSpans_Sub_Group = "D:\\PROJECTS\\BAY_AREA_DISTRO\\01_DIVISIONS\\DELIVERIES\\DELIVERY1\\LLAGAS\\SHAPES\\LLAGAS_HOLLISTER_GREEN_VALLEY_FINAL_SPANS_161101_CASP3_USFT_2011_GCC_attributted.shp"
PGE_Master_Circuits = "D:\\SCRIPT_LIBRARY\\BAY_AREA_CIRCUIT_EXTRACTION_working\\TEST_SHAPES\\PG_E_BAY_AREA_CIRCUITS_161109_MF_v3.shp"
outFolder = "D:\\SCRIPT_LIBRARY\\BAY_AREA_CIRCUIT_EXTRACTION_working\\TEST_OUTPUT"
SearchTolerance = 500'''

## Make dir folder within output folders for REFERENCE circuit shapes and EXTRACT shps

ref = os.path.join(outFolder,"CIRCUIT_REFERENCE")
ex = os.path.join(outFolder,"CIRCUIT_EXTRACT_needs_edits")
edit = os.path.join(outFolder,"CIRCUIT_EXTRACT_edited")
sub_ref = os.path.join(outFolder,"SUB_GROUP_REF")

### Other Directories Create
if not os.path.exists(ref):
    os.makedirs(ref)
if not os.path.exists(ex):
    os.makedirs(ex)
if not os.path.exists(sub_ref):
    os.makedirs(sub_ref)
if not os.path.exists(edit):
    os.makedirs(edit)


######### FUNCTIONS ##########
sub_names = []

def split_following_num(s):
    prev_char = ''

    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char


# Production Subs Reference
def sub_prod_ref(SUB):

    arcpy.MakeFeatureLayer_management(PGE_Master_Circuits, "PGE_MASTER_LYR")

    arcpy.MakeFeatureLayer_management(PGE_Master_Circuits, "PGE_MASTER_ALL_LYR")

    arcpy.SelectLayerByLocation_management("PGE_MASTER_LYR", "INTERSECT", SUB,"", "NEW_SELECTION")

    tempsublyrOUT = r'in_memory\subprod_out'

    arcpy.Select_analysis("PGE_MASTER_LYR", tempsublyrOUT )

    with arcpy.da.SearchCursor(tempsublyrOUT, ["PROD_SUB"]) as sCur:
        [sub_names.append(row) for row in sCur]
        for S in sub_names:
            out_shp = sub_ref + r"\%s_REFERENCE_SUB.shp" % (S)
            arcpy.Select_analysis("PGE_MASTER_ALL_LYR", out_shp, ' "PROD_SUB" = ' +  "'%s'"%S)
    del tempsublyrOUT

### PGE Circuit extract Fucntion
def PGE_circuit_extract(PROD_SUB):
    arcpy.AddMessage("....STARTING REFERENCE CIRCUITS EXTRACTION....")
    for sub in PROD_SUB:
        Internal_circuits_prodSub_dict = defaultdict(list)

        with arcpy.da.SearchCursor(sub,["CircuitNam","PROD_SUB"]) as sCur:
            for row in sCur:
                Internal_circuits_prodSub_dict[row[0]]= (str(row[1]))
                Master_circuits_prodSub_dict[row[0]] = (str(row[1]))

            for CirName,subGroup in Internal_circuits_prodSub_dict.items():
                arcpy.AddMessage("Processing Reference Extraction of Circuit>{0}< in Sub Group >{1}<.......".format(CirName,subGroup))

                out_shp = ref + r"\%s_%s_PROD_SUB_GROUP_REFERENCE.shp" %(CirName.replace(" ",""),str(subGroup.replace(" ","")))
                arcpy.Select_analysis(sub, out_shp,  ' "CircuitNam" = ' +  "'%s'"%CirName)

### Prod Spans Circuit extract Fucntion
def CircuitExtractByFinalSpans(PROD_SPANS,REF_PROD_SUBS,cir_list):
    arcpy.MakeFeatureLayer_management(PROD_SPANS, "FinalSpansSubLYR")
    for f in cir_list:
        cir_name_split = os.path.split(f)

        out_shp = ex + r"\%s" %(os.path.split(f)[1].replace("_REFERENCE.shp","_FINAL_EXTRACT_NEEDS_EDITS.shp"))
        arcpy.AddMessage("Processing Production Sub Extraction of Circuit>{0}<.......".format(cir_name_split[1]))
        arcpy.SelectLayerByLocation_management("FinalSpansSubLYR", "INTERSECT",f , SearchTolerance, "NEW_SELECTION")
        arcpy.Select_analysis("FinalSpansSubLYR", out_shp)
        #else:
           # pass



###### FUNCTIONS FOR ADJUSTED ALIGNMENT ######

# Production Subs Reference
def sub_prod_ref_ADJ(SUB):

    arcpy.MakeFeatureLayer_management(PGE_Master_Circuits, "PGE_MASTER_LYR")

    arcpy.MakeFeatureLayer_management(PGE_Master_Circuits, "PGE_MASTER_ALL_LYR")

    arcpy.SelectLayerByLocation_management("PGE_MASTER_LYR", "INTERSECT", SUB,"", "NEW_SELECTION")

    tempsublyrOUT = r'in_memory\subprod_out'

    arcpy.Select_analysis("PGE_MASTER_LYR", tempsublyrOUT )

    with arcpy.da.SearchCursor(tempsublyrOUT, ["PROD_SUB"]) as sCur:
        [sub_names.append(row) for row in sCur]
        for S in sub_names:
            out_shp = sub_ref + r"\%s_REFERENCE_SUB_Q2.shp" % (S)
            arcpy.Select_analysis("PGE_MASTER_ALL_LYR", out_shp, ' "PROD_SUB" = ' +  "'%s'"%S)
    del tempsublyrOUT

### PGE Circuit extract Fucntion
def PGE_circuit_extract_ADJ(PROD_SUB):
    arcpy.AddMessage("....STARTING REFERENCE CIRCUITS EXTRACTION....")
    for sub in PROD_SUB:
        Internal_circuits_prodSub_dict = defaultdict(list)

        with arcpy.da.SearchCursor(sub,["CircuitNam","PROD_SUB"]) as sCur:
            for row in sCur:
                Internal_circuits_prodSub_dict[row[0]]= (str(row[1]))
                Master_circuits_prodSub_dict[row[0]] = (str(row[1]))

            for CirName,subGroup in Internal_circuits_prodSub_dict.items():
                arcpy.AddMessage("Processing Reference Q2 Extraction of Circuit>{0}< in Sub Group >{1}<.......".format(CirName,subGroup))

                out_shp = ref + r"\%s_%s_PROD_SUB_GROUP_REFERENCE_Q2.shp" %(CirName.replace(" ",""),str(subGroup.replace(" ","")))
                arcpy.Select_analysis(sub, out_shp,  ' "CircuitNam" = ' +  "'%s'"%CirName)

### Prod Spans Circuit extract Fucntion
def CircuitExtractByFinalSpans_ADJ(PROD_SPANS,REF_PROD_SUBS,cir_list):
    arcpy.MakeFeatureLayer_management(PROD_SPANS, "FinalSpansSubLYR")
    for f in cir_list:
        cir_name_split = os.path.split(f)

        out_shp = ex + r"\%s" %(os.path.split(f)[1].replace("_REFERENCE_Q2.shp","_EXTRACT_NEEDS_EDITS_Q2.shp"))
        arcpy.AddMessage("Processing Production Sub Extraction of Q2 Circuit>{0}<.......".format(cir_name_split[1]))
        arcpy.SelectLayerByLocation_management("FinalSpansSubLYR", "INTERSECT",f , SearchTolerance, "NEW_SELECTION")
        arcpy.Select_analysis("FinalSpansSubLYR", out_shp)
        #else:
           # pass


Master_circuits_prodSub_dict = defaultdict(list)

## seperate if using multipart(final spans) or single part(adjusted alignemtn) and convert to spans

desc = arcpy.Describe(INPUT_FinalSpans_Sub_Group)
shape_field = desc.ShapeFieldName

rows = arcpy.SearchCursor(INPUT_FinalSpans_Sub_Group)

Base_adj = os.path.basename(INPUT_FinalSpans_Sub_Group)
Adjusted_conversion = os.path.join(outFolder, os.path.splitext(Base_adj)[0] + "_MP_Converted_Q2.shp")



for row in rows:
    poly = row.getValue(shape_field)
    if poly.isMultipart == 1:
        if arcpy.CheckProduct("ArcInfo") == "AlreadyInitialized":
            arcpy.arcpy.AddWarning("ARC ADVANCED LICENSE DETECTED")

        else:
            arcpy.AddError("YOU NEED AN ARC ADVANCED LICENSE TO EXECUTE THIS STEP WITH AN ADJUSTED ALIGNMENT EXTRACTION")

        arcpy.SplitLine_management(INPUT_FinalSpans_Sub_Group, Adjusted_conversion)
    else:
        pass



if os.path.exists(Adjusted_conversion):
    arcpy.AddMessage("ADJUSTED ALIGNMENT DETECTED....CONVERTING ADJUSTED ALIGNMENT TO MULTI PART FEATURE(SPANS)....")
    sub_prod_ref_ADJ(Adjusted_conversion)
    sub_ref_shps_list = []
    for root, dirs, files in os.walk(sub_ref):
        for file in files:
            if file.endswith(".shp"):
                F = (os.path.join(root, file))
                sub_ref_shps_list.append(F)


    PGE_circuit_extract_ADJ(sub_ref_shps_list)

    cir_ref_shps_list = []
    for root, dirs, files in os.walk(ref):
        for file in files:
            if file.endswith(".shp"):
                F = (os.path.join(root, file))
                cir_ref_shps_list.append(F)

    arcpy.AddMessage("\n....STARTING PRODUCTION CIRCUITS EXTRACTION....")
    for sub in sub_ref_shps_list:
        CircuitExtractByFinalSpans_ADJ(Adjusted_conversion, sub, cir_ref_shps_list)


elif [os.path.exists(adj_circuit) for adj_circuit in adj_circuits if os.path.exists(adj_circuit) == True] :

    arcpy.AddMessage("\n....STARTING FINAL SPANS PRODUCTION CIRCUITS EXTRACTION....")

    FINAL_CIRCUITS_folder = os.path.join(outFolder, "FINAL_CIRCUIT_shapes")
    if not os.path.exists(FINAL_CIRCUITS_folder):
        os.makedirs(FINAL_CIRCUITS_folder)

    for adj_circuit in adj_circuits:

        arcpy.MakeFeatureLayer_management(INPUT_FinalSpans_Sub_Group, "FinalSpansSubLYR")

        cirNAME = split_following_num(os.path.basename(adj_circuit))

        arcpy.AddMessage("Processing Production Sub Extraction of Q2 Circuit >{0}<  .......".format(cirNAME))

        out_shp = r"%s_FINAL_SPANS_Q2.shp" % (cirNAME)

        arcpy.SelectLayerByLocation_management("FinalSpansSubLYR", "INTERSECT", adj_circuit, SearchTolerance,"NEW_SELECTION")

        arcpy.FeatureClassToFeatureClass_conversion("FinalSpansSubLYR", FINAL_CIRCUITS_folder, out_shp)



else:
    arcpy.AddWarning("....FINAL PRODUCTION SPANS SHAPE DETECTED....")

    sub_prod_ref(INPUT_FinalSpans_Sub_Group)
    sub_ref_shps_list = []
    for root, dirs, files in os.walk(sub_ref):
        for file in files:
            if file.endswith(".shp"):
                F = (os.path.join(root, file))
                sub_ref_shps_list.append(F)

    PGE_circuit_extract(sub_ref_shps_list)
    arcpy.AddMessage("\n....STARTING PRODUCTION CIRCUITS EXTRACTION....")

    cir_ref_shps_list = []
    for root, dirs, files in os.walk(ref):
        for file in files:
            if file.endswith(".shp"):
                F = (os.path.join(root, file))
                cir_ref_shps_list.append(F)

    for sub in sub_ref_shps_list:
        CircuitExtractByFinalSpans(INPUT_FinalSpans_Sub_Group, sub, cir_ref_shps_list)


del rows

## Adjusted Circuits to Final Circuits Extraction with minimal search tolerance





arcpy.AddMessage("\n\tEXTRACTION SUCESSFULLY COMPLETED..... please inspect shapes for manual edits")











































































