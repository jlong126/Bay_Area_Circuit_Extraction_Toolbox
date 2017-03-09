import arcpy, os ,sys, itertools


## GW Import

try:
    arcpy.ImportToolbox("C:/Program Files (x86)/ET SpatialTechniques/ET GeoWizards 10.2 Concurrent for ArcGIS 10.1/ET GeoWizards.tbx")
    arcpy.gp.toolbox = "C:/Program Files (x86)/ET SpatialTechniques/ET GeoWizards 10.2 Concurrent for ArcGIS 10.1/ET GeoWizards.tbx"
except:
    try:
        arcpy.ImportToolbox("C:/Program Files (x86)/ET SpatialTechniques/ET GeoWizards 11.0 Concurrent for ArcGIS 10.2/ET GeoWizards.tbx")
        arcpy.gp.toolbox = "C:/Program Files (x86)/ET SpatialTechniques/ET GeoWizards 11.0 Concurrent for ArcGIS 10.2/ET GeoWizards.tbx"
    except:
        arcpy.AddError("\n~~~~ ~~~~ YOU MUST HAVE ET GEOWIZARDS INSTALLED AND LICENSED TO RUN THIS STEP! ~~~~ ~~~~\n")
        sys.exit()


arcpy.env.overwriteOutput = 1
arcpy.Delete_management("in_memory")

FINAL_DEL_TARGET_CIRCUIT = arcpy.GetParameterAsText(0)
FINAL_DEL_APPEND_CIRCUITS = arcpy.GetParameterAsText(1)

FINAL_inSITE_TARGET_CIRCUIT = arcpy.GetParameterAsText(2)
FINAL_inSITE_APPEND_CIRCUITS = arcpy.GetParameterAsText(3)

OutFolder = arcpy.GetParameterAsText(4)
Delivery = arcpy.GetParameterAsText(5)


def split_following_num(s):
    prev_char = ''
    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char

## PREP FINAL inSITE CIRCUIT

arcpy.AddMessage("...Creating New inSITE Circuit GDB in  inSITE_APPENDED_CIRCUITS Folder...")

if os.path.exists(FINAL_inSITE_TARGET_CIRCUIT):
    inSITE_MergeFolder = os.path.join(OutFolder,"%s_inSITE_APPENDED_CIRCUITS"%(Delivery))

    if not os.path.exists(inSITE_MergeFolder):
        os.makedirs(inSITE_MergeFolder)
else:
    pass

inSITE_MERGE_CIRCUITS = FINAL_inSITE_APPEND_CIRCUITS.split(";")

inSITE_MERGE_CIRCUITS_LIST =[]

for cir in inSITE_MERGE_CIRCUITS:
    inSITE_MERGE_CIRCUITS_LIST.append(cir)

inSITE_MERGE_CIRCUITS_LIST.append(FINAL_inSITE_TARGET_CIRCUIT)





cirNAME = split_following_num(os.path.basename(FINAL_inSITE_TARGET_CIRCUIT))

if os.path.exists(FINAL_inSITE_TARGET_CIRCUIT):
    arcpy.CreateFileGDB_management(inSITE_MergeFolder, cirNAME + "_inSITE_Ready_BAY_AREA_2016")

    inSITE_TARGET_MERGE_GDB = []
    arcpy.env.workspace = inSITE_MergeFolder
    for file in arcpy.ListFiles("*.gdb"):
        inSITE_TARGET_MERGE_GDB.append(file)

else:
    pass




## inSITE SPANS
if os.path.exists(FINAL_inSITE_TARGET_CIRCUIT):
    arcpy.AddMessage("...APPENDING inSITE SPANS....")

    inSITE_Spans_feature_classes = []


    for GDB in inSITE_MERGE_CIRCUITS_LIST:
        walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                if filename.endswith("Spans"):
                    inSITE_Spans_feature_classes.append(os.path.join(dirpath, filename))

    for f in inSITE_TARGET_MERGE_GDB:
        outSpans = os.path.join(f, "%s_inSITE_Ready_BAY_AREA_2016_Spans" % (cirNAME))

        arcpy.Merge_management(inSITE_Spans_feature_classes, outSpans)
else:
    pass
## inSITE TOWERS
if os.path.exists(FINAL_inSITE_TARGET_CIRCUIT):

    arcpy.AddMessage("...APPENDING inSITE TOWERS....")

    inSITE_Towers_feature_classes = []

    for GDB in inSITE_MERGE_CIRCUITS_LIST:
        walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                if filename.endswith("Towers"):
                    inSITE_Towers_feature_classes.append(os.path.join(dirpath, filename))

    for f in inSITE_TARGET_MERGE_GDB:
        outTowers = os.path.join(f, "%s_inSITE_Ready_BAY_AREA_2016_Towers" % (cirNAME))

        arcpy.Merge_management(inSITE_Towers_feature_classes, outTowers)
else:
    pass

## inSITE TreeTops

if os.path.exists(FINAL_inSITE_TARGET_CIRCUIT):

    arcpy.AddMessage("...APPENDING inSITE TreeTops....")

    inSITE_TTs_feature_classes = []

    for GDB in inSITE_MERGE_CIRCUITS_LIST:
        walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                if filename.endswith("TreeTops_AF"):
                    inSITE_TTs_feature_classes.append(os.path.join(dirpath, filename))

    for f in inSITE_TARGET_MERGE_GDB:
        outTTs = os.path.join(f, "%s_inSITE_Ready_BAY_AREA_2016_TreeTops_AF" % (cirNAME))

        arcpy.Merge_management(inSITE_TTs_feature_classes, outTTs)
else:
    pass

## inSITE VegPolys

if os.path.exists(FINAL_inSITE_TARGET_CIRCUIT):

    arcpy.AddMessage("...APPENDING inSITE VegPolys....")

    inSITE_VPs_feature_classes = []

    for GDB in inSITE_MERGE_CIRCUITS_LIST:
        walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                if filename.endswith("VegPolys"):
                    inSITE_VPs_feature_classes.append(os.path.join(dirpath, filename))

    for f in inSITE_TARGET_MERGE_GDB:
        outVPs = os.path.join(f, "%s_inSITE_Ready_BAY_AREA_2016_VegPolys" % (cirNAME))

        arcpy.Merge_management(inSITE_VPs_feature_classes, outVPs)

else:
    pass
















## PREP FINAL CIRCUIT DEL





arcpy.AddMessage("...Creating New Circuit GDB in APPENDED_CIRCUITS Folder...")

FINAL_DEL_MergeFolder = os.path.join(OutFolder,"%s_FINAL_DELIVERY_APPENDED_CIRCUITS"%(Delivery))

FINAL_DEL_MERGE_CIRCUITS = FINAL_DEL_APPEND_CIRCUITS.split(";")

FINAL_DEL_MERGE_CIRCUITS_LIST =[]

for cir in FINAL_DEL_MERGE_CIRCUITS:
    FINAL_DEL_MERGE_CIRCUITS_LIST.append(cir)

FINAL_DEL_MERGE_CIRCUITS_LIST.append(FINAL_DEL_TARGET_CIRCUIT)


if not os.path.exists(FINAL_DEL_MergeFolder):
    os.makedirs(FINAL_DEL_MergeFolder)




cirNAME = split_following_num(os.path.basename(FINAL_DEL_TARGET_CIRCUIT))

arcpy.CreateFileGDB_management(FINAL_DEL_MergeFolder, cirNAME + "_BAY_AREA_2016")

FINAL_TARGET_MERGE_GDB = []
arcpy.env.workspace = FINAL_DEL_MergeFolder
for file in arcpy.ListFiles("*.gdb"):
    FINAL_TARGET_MERGE_GDB.append(file)

## SPANS
SPAN_FIELDS = ['SPAN_TAG', 'BST_TAG', 'AST_TAG', 'GCC200', 'SPAN_ID', 'SPAN_LGTH', 'LATITUDE', 'LONGITUDE', 'VOLTAGE',
               'LINE_ID', 'LINE_NAME', 'LINE_NBR', 'PMD','Shape_Length', 'CIRCUIT_1',
               'CIRCUIT_2', 'CIRCUIT_3']


arcpy.AddMessage("...APPENDING SPANS....")

Spans_feature_classes = []


for GDB in FINAL_DEL_MERGE_CIRCUITS_LIST:
    walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            if filename.endswith("Spans"):
                Spans_feature_classes.append(os.path.join(dirpath, filename))

x = "ERROR"
for spans in Spans_feature_classes:

    fieldnames_Spans = [field.name for field in arcpy.ListFields(spans)]

    for field, s_fields in zip(SPAN_FIELDS, fieldnames_Spans):
        if s_fields in SPAN_FIELDS:
            arcpy.AddMessage("%s  FOUND " % (s_fields))
        else:

            spans_dif_A = list(set(SPAN_FIELDS) - set(fieldnames_Spans))
            spans_dif_D = (list(set(fieldnames_Spans) - set(SPAN_FIELDS)))

            for add_field in spans_dif_A:
                arcpy.AddError("'{0}' FIELD is not present in Tree Tops Spans Feature classes, Please Run GDBs through Step 0 for correct formatting ".format(
                        add_field))
                raise sys.exit("Error: " + arcpy.GetMessages(x))

            for del_field in spans_dif_D:
                if del_field not in ['Shape', 'OBJECTID']:
                    arcpy.AddError("'{0}' is not a required FIELD in Tree Tops Spans Feature classes, Please Run GDBs through Step 0 for correct formatting ".format(del_field))
                    raise sys.exit("Error: " + arcpy.GetMessages(x))


for f in FINAL_TARGET_MERGE_GDB:
    outSpans = os.path.join(f, "%s_BAY_AREA_2016_Spans" % (cirNAME))

    arcpy.Merge_management(Spans_feature_classes, outSpans)


## TOWERS

arcpy.AddMessage("...APPENDING TOWERS....")

Towers_feature_classes = []

for GDB in FINAL_DEL_MERGE_CIRCUITS_LIST:
    walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            if filename.endswith("Towers"):
                Towers_feature_classes.append(os.path.join(dirpath, filename))

for f in FINAL_TARGET_MERGE_GDB:
    outTowers = os.path.join(f, "%s_BAY_AREA_2016_Towers" % (cirNAME))

    arcpy.Merge_management(Towers_feature_classes, outTowers)

## TreeTops

TTs_FIELDS = ['OFF', 'Z', 'OVR', 'Y', 'D2W_AF', 'HEIGHT', 'X', 'OH',
              'SPAN_TAG',
              'BST_TAG', 'AST_TAG', 'SPAN_ID', 'LATITUDE', 'LONGITUDE', 'VOLTAGE', 'LINE_ID', 'LINE_NAME',
              'PMD', 'REGION', 'TREEID', 'ACQ_DATE', 'HEALTH','DC_AF', 'DC_FI',
              'DC_VENDOR', 'PMD', 'APN_NUMBER', 'STREET_NUM', 'STREET', 'CUSTOMER_P', 'CUSTOMER_N',
              'CUSTOMER_1', 'CITY', 'COUNTY', 'DIVISION', 'GCC200', 'FALL_IN', 'SRA_LRA']

try:

    fieldMappings = arcpy.FieldMappings()

    arcpy.AddMessage("...APPENDING TreeTops....")

    TTs_feature_classes = []

    for GDB in FINAL_DEL_MERGE_CIRCUITS_LIST:
        walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

        for dirpath, dirnames, filenames in walk:
            for filename in filenames:
                if filename.endswith("TreeTops_AF"):
                    TTs_feature_classes.append(os.path.join(dirpath, filename))


    ## TreeTops Field Map
    for fc_tt in TTs_feature_classes:

        fieldnames_TTs = [field.name for field in arcpy.ListFields(fc_tt)]

        for field, c_fields in zip(TTs_FIELDS, fieldnames_TTs):
            if c_fields in TTs_FIELDS:
                pass
            else:
                tts_dif_A = list(set(TTs_FIELDS) - set(fieldnames_TTs))
                tts_dif_D = (list(set(fieldnames_TTs) - set(TTs_FIELDS)))
                for add_field in tts_dif_A:
                    arcpy.AddError("'{0}' FIELD is not present in Tree Tops AF Feature classes, Please Run GDBs through Step 0 for correct formatting ".format(add_field))
                    raise sys.exit("Error: " + arcpy.GetMessages(x))
                for del_field in tts_dif_D:
                    if del_field not in ['Shape', 'OBJECTID']:
                        arcpy.AddError("'{0}' is not a required FIELD in Tree Tops AF Feature classes, Please Run GDBs through Step 0 for correct formatting ".format(del_field))
                        raise sys.exit("Error: " + arcpy.GetMessages(x))




        """# 33. APN_Number field
        fldMap_APN_Num = arcpy.FieldMap()
        fldMap_APN_Num.addInputField(fc_tt, "APN_NUMBER")

        APN_Num_field = fldMap_APN_Num.outputField
        APN_Num_field.name = "APN_NUMBER"
        fldMap_APN_Num.outputField = APN_Num_field

        fieldMappings.addFieldMap(fldMap_APN_Num)

        # 34. STREET_num field
        fldMap_STREET_num = arcpy.FieldMap()
        fldMap_STREET_num.addInputField(fc_tt, "STREET_NUM")

        STREET_num_field = fldMap_STREET_num.outputField
        STREET_num_field.name = "STREET_NUM"
        fldMap_STREET_num.outputField = STREET_num_field

        fieldMappings.addFieldMap(fldMap_STREET_num)

        # 35. STREET field
        fldMap_STREET = arcpy.FieldMap()
        fldMap_STREET.addInputField(fc_tt, "STREET")

        STREET_field = fldMap_STREET.outputField
        STREET_field.name = "STREET"
        fldMap_STREET.outputField = STREET_field

        fieldMappings.addFieldMap(fldMap_STREET)

        # 37.  CUSTOMER Name field
        fldMap_CUST_NAME = arcpy.FieldMap()
        fldMap_CUST_NAME.addInputField(fc_tt, "CUSTOMER_NAME")

        CUST_NAME_field = fldMap_CUST_NAME.outputField
        CUST_NAME_field.name = "CUSTOMER_NAME"
        fldMap_CUST_NAME.outputField = CUST_NAME_field

        fieldMappings.addFieldMap(fldMap_CUST_NAME)

        # 38. CUSTOMER_NAME1 field
        fldMap_CUST_NAME1 = arcpy.FieldMap()
        fldMap_CUST_NAME1.addInputField(fc_tt, "CUSTOMER_NAME_1")

        CUST_NAME1_field = fldMap_CUST_NAME1.outputField
        CUST_NAME1_field.name = "CUSTOMER_NAME_1"
        fldMap_CUST_NAME1.outputField = CUST_NAME1_field

        fieldMappings.addFieldMap(fldMap_CUST_NAME1)

        # 39. CITY field

        fldMap_CITY = arcpy.FieldMap()
        fldMap_CITY.addInputField(fc_tt, "CITY")

        CITY_field = fldMap_CITY.outputField
        CITY_field.name = "CITY"
        fldMap_CITY.outputField = CITY_field

        fieldMappings.addFieldMap(fldMap_CITY)

        # 40. COUNTY field
        fldMap_COUNTY = arcpy.FieldMap()
        fldMap_COUNTY.addInputField(fc_tt, "COUNTY")

        COUNTY_field = fldMap_COUNTY.outputField
        COUNTY_field.name = "COUNTY"
        fldMap_COUNTY.outputField = COUNTY_field

        fieldMappings.addFieldMap(fldMap_COUNTY)

        # 41. DIVISION field
        fldMap_DIV = arcpy.FieldMap()
        fldMap_DIV.addInputField(fc_tt, "DIVISION")

        DIV_field = fldMap_DIV.outputField
        DIV_field.name = "DIVISION"
        fldMap_DIV.outputField = DIV_field

        fieldMappings.addFieldMap(fldMap_DIV)

        # 19. LINE_NAME field
        fldMap_LINE_NAME = arcpy.FieldMap()
        fldMap_LINE_NAME.addInputField(fc_tt, "LINE_NAME")

        LINE_NAME_field = fldMap_LINE_NAME.outputField
        LINE_NAME_field.name = "LINE_NAME"
        fldMap_LINE_NAME.outputField = LINE_NAME_field

        fieldMappings.addFieldMap(fldMap_LINE_NAME)

        # SRA/LRA Field
        fldMap_SRA = arcpy.FieldMap()
        fldMap_SRA.addInputField(fc_tt, "SRA_LRA")

        SRA_field = fldMap_SRA.outputField
        SRA_field.name = "SRA_LRA"
        fldMap_SRA.outputField = SRA_field

        fieldMappings.addFieldMap(fldMap_SRA)

        # 3. D2W_AF
        fldMap_DTW = arcpy.FieldMap()
        fldMap_DTW.addInputField(fc_tt, "D2W_AF")

        DTW_field = fldMap_DTW.outputField
        DTW_field.name = "D2W_AF"
        fldMap_DTW.outputField = DTW_field

        fieldMappings.addFieldMap(fldMap_DTW)

        # 1. OFF_ field

        fldMap_OFF = arcpy.FieldMap()
        fldMap_OFF.addInputField(fc_tt, "OFF_")

        OFF_field = fldMap_OFF.outputField
        OFF_field.name = "OFF_"
        fldMap_OFF.outputField = OFF_field

        fieldMappings.addFieldMap(fldMap_OFF)

        # 2 .GEOTAG field
        fldMap_GT = arcpy.FieldMap()
        fldMap_GT.addInputField(fc_tt, "GEOTAG_1")

        GT_field = fldMap_GT.outputField
        GT_field.name = "GEOTAG_1"
        fldMap_GT.outputField = GT_field

        fieldMappings.addFieldMap(fldMap_GT)

        # 8. H field
        fldMap_H = arcpy.FieldMap()
        fldMap_H.addInputField(fc_tt, "H")

        H_field = fldMap_H.outputField
        H_field.name = "H"
        fldMap_H.outputField = H_field

        fieldMappings.addFieldMap(fldMap_H)

        # FALL_IN field
        fldMap_FI = arcpy.FieldMap()
        fldMap_FI.addInputField(fc_tt, "FALL_IN")

        FI_field = fldMap_FI.outputField
        FI_field.name = "FALL_IN"
        fldMap_FI.outputField = FI_field

        fieldMappings.addFieldMap(fldMap_FI)

        # 4. OVR field
        fldMap_OVR = arcpy.FieldMap()
        fldMap_OVR.addInputField(fc_tt, "OVR")

        OVR_field = fldMap_OVR.outputField
        OVR_field.name = "OVR"
        fldMap_OVR.outputField = OVR_field

        fieldMappings.addFieldMap(fldMap_OVR)

        # 15. LATITUDE field
        fldMap_LAT = arcpy.FieldMap()
        fldMap_LAT.addInputField(fc_tt, "LATITUDE")

        LAT_field = fldMap_LAT.outputField
        LAT_field.name = "LATITUDE"
        fldMap_LAT.outputField = LAT_field

        fieldMappings.addFieldMap(fldMap_LAT)

        # 16. LONGITUTDE field
        fldMap_LAT = arcpy.FieldMap()
        fldMap_LAT.addInputField(fc_tt, "LONGITUDE")

        LAT_field = fldMap_LAT.outputField
        LAT_field.name = "LONGITUDE"
        fldMap_LAT.outputField = LAT_field

        fieldMappings.addFieldMap(fldMap_LAT)

        # 18. LINE_ID field
        fldMap_LINE_ID = arcpy.FieldMap()
        fldMap_LINE_ID.addInputField(fc_tt, "LINE_ID")

        LINE_ID_field = fldMap_LINE_ID.outputField
        LINE_ID_field.name = "LINE_ID"
        fldMap_LINE_ID.outputField = LINE_ID_field

        fieldMappings.addFieldMap(fldMap_LINE_ID)

        # 25. TREE_ID field
        fldMap_TREE_ID = arcpy.FieldMap()
        fldMap_TREE_ID.addInputField(fc_tt, "TREEID")

        TREE_ID_field = fldMap_TREE_ID.outputField
        TREE_ID_field.name = "TREEID"
        fldMap_TREE_ID.outputField = TREE_ID_field

        fieldMappings.addFieldMap(fldMap_TREE_ID)

        # 26. ACQ_DATE field
        fldMap_ACQ_DATE = arcpy.FieldMap()
        fldMap_ACQ_DATE.addInputField(fc_tt, "ACQ_DATE")

        ACQ_DATE_field = fldMap_ACQ_DATE.outputField
        ACQ_DATE_field.name = "ACQ_DATE"
        fldMap_ACQ_DATE.outputField = ACQ_DATE_field

        fieldMappings.addFieldMap(fldMap_ACQ_DATE)

        # 29. DC_AF field
        fldMap_DC_AF = arcpy.FieldMap()
        fldMap_DC_AF.addInputField(fc_tt, "DC_AF")

        DC_AF_field = fldMap_DC_AF.outputField
        DC_AF_field.name = "DC_AF"
        fldMap_DC_AF.outputField = DC_AF_field

        fieldMappings.addFieldMap(fldMap_DC_AF)

        # 30. DC_FI field
        fldMap_DC_FI = arcpy.FieldMap()
        fldMap_DC_FI.addInputField(fc_tt, "DC_FI")

        DC_FI_field = fldMap_DC_FI.outputField
        DC_FI_field.name = "DC_FI"
        fldMap_DC_FI.outputField = DC_FI_field

        fieldMappings.addFieldMap(fldMap_DC_FI)

        # 31. DC_VENDOR field
        fldMap_DC_VEN = arcpy.FieldMap()
        fldMap_DC_VEN.addInputField(fc_tt, "DC_VENDOR")

        DC_VEN_field = fldMap_DC_VEN.outputField
        DC_VEN_field.name = "DC_VENDOR"
        fldMap_DC_VEN.outputField = DC_VEN_field

        fieldMappings.addFieldMap(fldMap_DC_VEN)

        # 9. OH field
        fldMap_OH = arcpy.FieldMap()
        fldMap_OH.addInputField(fc_tt, "OH")

        OH_field = fldMap_OH.outputField
        OH_field.name = "OH"
        fldMap_OH.outputField = OH_field

        fieldMappings.addFieldMap(fldMap_OH)

        # 5. X field
        fldMap_X = arcpy.FieldMap()
        fldMap_X.addInputField(fc_tt, "X")

        X_field = fldMap_X.outputField
        X_field.name = "X"
        fldMap_X.outputField = X_field

        fieldMappings.addFieldMap(fldMap_X)

        # 6. Y field
        fldMap_Y = arcpy.FieldMap()
        fldMap_Y.addInputField(fc_tt, "Y")

        Y_field = fldMap_Y.outputField
        Y_field.name = "Y"
        fldMap_Y.outputField = Y_field

        fieldMappings.addFieldMap(fldMap_Y)

        # 7. Z field
        fldMap_Z = arcpy.FieldMap()
        fldMap_Z.addInputField(fc_tt, "Z")

        Z_field = fldMap_Z.outputField
        Z_field.name = "Z"
        fldMap_Z.outputField = Z_field

        fieldMappings.addFieldMap(fldMap_Z)

        # 10. SPAN_TAG field
        fldMap_ST = arcpy.FieldMap()
        fldMap_ST.addInputField(fc_tt, "SPAN_TAG")

        ST_field = fldMap_ST.outputField
        ST_field.name = "SPAN_TAG"
        fldMap_ST.outputField = ST_field

        fieldMappings.addFieldMap(fldMap_ST)

        # 11. BST_TAG field
        fldMap_BST = arcpy.FieldMap()
        fldMap_BST.addInputField(fc_tt, "BST_TAG")

        BST_field = fldMap_BST.outputField
        BST_field.name = "BST_TAG"
        fldMap_BST.outputField = BST_field

        fieldMappings.addFieldMap(fldMap_BST)

        # 12. AST_TAG field
        fldMap_AST = arcpy.FieldMap()
        fldMap_AST.addInputField(fc_tt, "AST_TAG")

        AST_field = fldMap_AST.outputField
        AST_field.name = "AST_TAG"
        fldMap_AST.outputField = AST_field

        fieldMappings.addFieldMap(fldMap_AST)

        # 13. GCC200 field
        fldMap_GCC = arcpy.FieldMap()
        fldMap_GCC.addInputField(fc_tt, "GCC200")

        GCC_field = fldMap_GCC.outputField
        GCC_field.name = "GCC200"
        fldMap_GCC.outputField = GCC_field

        fieldMappings.addFieldMap(fldMap_GCC)

        # 14. SPAN_ID field
        fldMap_SPAN_ID = arcpy.FieldMap()
        fldMap_SPAN_ID.addInputField(fc_tt, "SPAN_ID")

        SPAN_ID_field = fldMap_SPAN_ID.outputField
        SPAN_ID_field.name = "SPAN_ID"
        fldMap_SPAN_ID.outputField = SPAN_ID_field

        fieldMappings.addFieldMap(fldMap_SPAN_ID)

        # 17. VOLTAGE field
        fldMap_V = arcpy.FieldMap()
        fldMap_V.addInputField(fc_tt, "VOLTAGE")

        V_field = fldMap_V.outputField
        V_field.name = "VOLTAGE"
        fldMap_V.outputField = V_field

        fieldMappings.addFieldMap(fldMap_V)

        # 20. PMD1 field
        fldMap_PMD1 = arcpy.FieldMap()
        fldMap_PMD1.addInputField(fc_tt, "PMD_1")

        PMD1_field = fldMap_PMD1.outputField
        PMD1_field.name = "PMD_1"
        fldMap_PMD1.outputField = PMD1_field

        fieldMappings.addFieldMap(fldMap_PMD1)

        # 21. PMD2 field
        fldMap_PMD2 = arcpy.FieldMap()
        fldMap_PMD2.addInputField(fc_tt, "PMD_2")

        PMD2_field = fldMap_PMD2.outputField
        PMD2_field.name = "PMD_2"
        fldMap_PMD2.outputField = PMD2_field

        fieldMappings.addFieldMap(fldMap_PMD2)

        # 22. PMD3 field
        fldMap_PMD3 = arcpy.FieldMap()
        fldMap_PMD3.addInputField(fc_tt, "PMD_3")

        PMD3_field = fldMap_PMD3.outputField
        PMD3_field.name = "PMD_3"
        fldMap_PMD3.outputField = PMD3_field

        fieldMappings.addFieldMap(fldMap_PMD3)

        # 23. PMD4 field
        fldMap_PMD4 = arcpy.FieldMap()
        fldMap_PMD4.addInputField(fc_tt, "PMD_4")

        PMD4_field = fldMap_PMD4.outputField
        PMD4_field.name = "PMD_4"
        fldMap_PMD4.outputField = PMD4_field

        fieldMappings.addFieldMap(fldMap_PMD4)

        # 27. HEALTH field
        fldMap_ACQ_DATE = arcpy.FieldMap()
        fldMap_ACQ_DATE.addInputField(fc_tt, "HEALTH")

        ACQ_DATE_field = fldMap_ACQ_DATE.outputField
        ACQ_DATE_field.name = "HEALTH"
        fldMap_ACQ_DATE.outputField = ACQ_DATE_field

        fieldMappings.addFieldMap(fldMap_ACQ_DATE)

        # 28. SPECIES field
        fldMap_ACQ_DATE = arcpy.FieldMap()
        fldMap_ACQ_DATE.addInputField(fc_tt, "SPECIES")

        ACQ_DATE_field = fldMap_ACQ_DATE.outputField
        ACQ_DATE_field.name = "SPECIES"
        fldMap_ACQ_DATE.outputField = ACQ_DATE_field

        fieldMappings.addFieldMap(fldMap_ACQ_DATE)

        # 32. PMD field
        fldMap_PMD = arcpy.FieldMap()
        fldMap_PMD.addInputField(fc_tt, "PMD")

        PMD_field = fldMap_PMD.outputField
        PMD_field.name = "PMD"
        fldMap_PMD.outputField = PMD_field

        fieldMappings.addFieldMap(fldMap_PMD)

        # 24. Region field
        fldMap_Region = arcpy.FieldMap()
        fldMap_Region.addInputField(fc_tt, "REGION")

        Region_field = fldMap_Region.outputField
        Region_field.name = "REGION"
        fldMap_Region.outputField = Region_field

        fieldMappings.addFieldMap(fldMap_Region)

        # 36. CUSTOMER PHONE field
        fldMap_CUST_PH = arcpy.FieldMap()
        fldMap_CUST_PH.addInputField(fc_tt, "CUSTOMER_PHONE")

        CUST_PH_field = fldMap_CUST_PH.outputField
        CUST_PH_field.name = "CUSTOMER_PHONE"
        fldMap_CUST_PH.outputField = CUST_PH_field

        fieldMappings.addFieldMap(fldMap_CUST_PH)"""

        for f in FINAL_TARGET_MERGE_GDB:
            outTTs = os.path.join(f, "%s_BAY_AREA_2016_TreeTops_AF" % (cirNAME))

            arcpy.Merge_management(TTs_feature_classes, outTTs)      #  , fieldMappings)

        #for field in Delete_List:
            #arcpy.DeleteField_management(outTTs,field)


except:
    pass



## VegPolys

arcpy.AddMessage("...APPENDING VegPolys....")

VPs_feature_classes = []

for GDB in FINAL_DEL_MERGE_CIRCUITS_LIST:
    walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            if filename.endswith("VegPolys"):
                VPs_feature_classes.append(os.path.join(dirpath, filename))

for f in FINAL_TARGET_MERGE_GDB:
    outVPs = os.path.join(f, "%s_BAY_AREA_2016_VegPolys" % (cirNAME))

    arcpy.Merge_management(VPs_feature_classes, outVPs)

































