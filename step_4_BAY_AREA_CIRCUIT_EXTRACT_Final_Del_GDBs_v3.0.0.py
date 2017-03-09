import arcpy, os, re

arcpy.env.overwriteOutput = 1
arcpy.Delete_management("in_memory")

INPUT_inSITE_Ready_GDBs = arcpy.GetParameterAsText(0)
Output_Folder = arcpy.GetParameterAsText(1)

circuit_inSITE_GDBs = sorted(INPUT_inSITE_Ready_GDBs.split(";"))


FinalDeliverable_GDBs = os.path.join(Output_Folder,"Final_Deliverable_GDBs")

if not os.path.exists(FinalDeliverable_GDBs):
    os.makedirs(FinalDeliverable_GDBs)


def split_following_num(s):
    prev_char = ''
    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char

arcpy.AddMessage("....CREATING FINAL GEODATABASES....")

for circuit_GDB in circuit_inSITE_GDBs:


    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    arcpy.AddMessage(">%s< Final Geodatabase Processing....\n" % cirNAME)

    if arcpy.Exists(os.path.join(FinalDeliverable_GDBs,cirNAME + "_BAY_AREA_2016.gdb")):
        arcpy.Delete_management(os.path.join(FinalDeliverable_GDBs,cirNAME + "_BAY_AREA_2016.gdb"))

    arcpy.CreateFileGDB_management(FinalDeliverable_GDBs, cirNAME + "_BAY_AREA_2016")


circuit_FINAL_GDBs_List = []
arcpy.env.workspace = FinalDeliverable_GDBs
for file in arcpy.ListFiles("*.gdb"):
    circuit_FINAL_GDBs_List.append(file)


## SPANS

arcpy.AddMessage("/n/n....CREATING FINAL SPANS..../n/n")

for circuit_GDB, Final_GDB in zip(circuit_inSITE_GDBs,circuit_FINAL_GDBs_List):

    delete_fields =["WIRES_PHS","PHASES","WIRES_TTL","SPAN_GUID","BST_ID","AST_ID",
                    "REGION","DivCode","SPAN_NAME","Span_NBR","Sect_Nbr","BST","AST","LENGTH",
                    "LENGTHS","Shape_Leng","Shape_Lengt","length_2","PMD_2","PMD_3","PMD_4"]

    add_fields = ["CIRCUIT_1","CIRCUIT_2","CIRCUIT_3"]

    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    arcpy.AddMessage(">%s< Spans Formatting Processing....\n" % cirNAME)

    inSpans = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_Spans" % (cirNAME))
    
    out_fc_Spans = ("%s_BAY_AREA_2016_Spans" % (cirNAME))
    
    outSpans = os.path.join(Final_GDB, "%s_BAY_AREA_2016_Spans" % (cirNAME))


    
    
    
    ##  MAKE arcpy.FeatureClassToFeatureClass_conversion()

    

    

    for field in add_fields:
        arcpy.AddField_management(inSpans,field,"TEXT","","",100)

    
    ## Spans Field Map
    
    # SPANS FIELD MAP
    fieldMappings_spans = arcpy.FieldMappings()

    # 1. BST TAG
    fldMap_BST_TAG_spans = arcpy.FieldMap()
    fldMap_BST_TAG_spans.addInputField(inSpans, "BST_TAG")

    BST_TAG_spans_field = fldMap_BST_TAG_spans.outputField
    BST_TAG_spans_field.name = "BST_TAG"
    fldMap_BST_TAG_spans.outputField = BST_TAG_spans_field

    fieldMappings_spans.addFieldMap(fldMap_BST_TAG_spans)

    # 2. AST TAG
    fldMap_AST_TAG_spans = arcpy.FieldMap()
    fldMap_AST_TAG_spans.addInputField(inSpans, "AST_TAG")

    AST_TAG_spans_field = fldMap_AST_TAG_spans.outputField
    AST_TAG_spans_field.name = "AST_TAG"
    fldMap_AST_TAG_spans.outputField = AST_TAG_spans_field

    fieldMappings_spans.addFieldMap(fldMap_AST_TAG_spans)

    # 3. SPAN TAG
    fldMap_SPAN_TAG_spans = arcpy.FieldMap()
    fldMap_SPAN_TAG_spans.addInputField(inSpans, "SPAN_TAG")

    SPAN_TAG_spans_field = fldMap_SPAN_TAG_spans.outputField
    SPAN_TAG_spans_field.name = "SPAN_TAG"
    fldMap_SPAN_TAG_spans.outputField = SPAN_TAG_spans_field

    fieldMappings_spans.addFieldMap(fldMap_SPAN_TAG_spans)

    # 4. SPAN ID
    fldMap_SPAN_ID_spans = arcpy.FieldMap()
    fldMap_SPAN_ID_spans.addInputField(inSpans, "SPAN_ID")

    SPAN_ID_spans_field = fldMap_SPAN_ID_spans.outputField
    SPAN_ID_spans_field.name = "SPAN_ID"
    fldMap_SPAN_ID_spans.outputField = SPAN_ID_spans_field

    fieldMappings_spans.addFieldMap(fldMap_SPAN_ID_spans)

    # 5. SPAN LGTH
    fldMap_SPAN_LGTH_spans = arcpy.FieldMap()
    fldMap_SPAN_LGTH_spans.addInputField(inSpans, "SPAN_LGTH")

    SPAN_LGTH_spans_field = fldMap_SPAN_LGTH_spans.outputField
    SPAN_LGTH_spans_field.name = "SPAN_LGTH"
    fldMap_SPAN_LGTH_spans.outputField = SPAN_LGTH_spans_field

    fieldMappings_spans.addFieldMap(fldMap_SPAN_LGTH_spans)

    # 6. VOLTAGE
    fldMap_VOLT_spans = arcpy.FieldMap()
    fldMap_VOLT_spans.addInputField(inSpans, "VOLTAGE")

    VOLT_spans_field = fldMap_VOLT_spans.outputField
    VOLT_spans_field.name = "VOLTAGE"
    fldMap_VOLT_spans.outputField = VOLT_spans_field

    fieldMappings_spans.addFieldMap(fldMap_VOLT_spans)

    # 7. LINE_ID
    fldMap_LINE_ID_spans = arcpy.FieldMap()
    fldMap_LINE_ID_spans.addInputField(inSpans, "LINE_ID")

    LINE_ID_spans_field = fldMap_LINE_ID_spans.outputField
    LINE_ID_spans_field.name = "LINE_ID"
    fldMap_LINE_ID_spans.outputField = LINE_ID_spans_field

    fieldMappings_spans.addFieldMap(fldMap_LINE_ID_spans)

    # 8. LINE_NAME
    fldMap_LINE_NAME_spans = arcpy.FieldMap()
    fldMap_LINE_NAME_spans.addInputField(inSpans, "LINE_NAME")

    LINE_NAME_spans_field = fldMap_LINE_NAME_spans.outputField
    LINE_NAME_spans_field.name = "LINE_NAME"
    fldMap_LINE_NAME_spans.outputField = LINE_NAME_spans_field

    fieldMappings_spans.addFieldMap(fldMap_LINE_NAME_spans)

    # 9. LINE_NBR
    fldMap_LINE_NBR_spans = arcpy.FieldMap()
    fldMap_LINE_NBR_spans.addInputField(inSpans, "LINE_NBR")

    LINE_NBR_spans_field = fldMap_LINE_NBR_spans.outputField
    LINE_NBR_spans_field.name = "LINE_NBR"
    fldMap_LINE_NBR_spans.outputField = LINE_NBR_spans_field

    fieldMappings_spans.addFieldMap(fldMap_LINE_NBR_spans)

    # 10. CIRCUIT 1
    fldMap_CIR_1_spans = arcpy.FieldMap()
    fldMap_CIR_1_spans.addInputField(inSpans, "CIRCUIT_1")

    CIR_1_spans_field = fldMap_CIR_1_spans.outputField
    CIR_1_spans_field.name = "CIRCUIT_1"
    fldMap_CIR_1_spans.outputField = CIR_1_spans_field

    fieldMappings_spans.addFieldMap(fldMap_CIR_1_spans)

    # 12. CIRCUIT 2
    fldMap_CIR_2_spans = arcpy.FieldMap()
    fldMap_CIR_2_spans.addInputField(inSpans, "CIRCUIT_2")

    CIR_2_spans_field = fldMap_CIR_2_spans.outputField
    CIR_2_spans_field.name = "CIRCUIT_2"
    fldMap_CIR_2_spans.outputField = CIR_2_spans_field

    fieldMappings_spans.addFieldMap(fldMap_CIR_2_spans)

    # 13. CIRCUIT 3
    fldMap_CIR_3_spans = arcpy.FieldMap()
    fldMap_CIR_3_spans.addInputField(inSpans, "CIRCUIT_3")

    CIR_3_spans_field = fldMap_CIR_3_spans.outputField
    CIR_3_spans_field.name = "CIRCUIT_3"
    fldMap_CIR_3_spans.outputField = CIR_3_spans_field

    fieldMappings_spans.addFieldMap(fldMap_CIR_3_spans)

    # 14. GCC 200
    fldMap_GCC_spans = arcpy.FieldMap()
    fldMap_GCC_spans.addInputField(inSpans, "GCC200")

    GCC_spans_field = fldMap_GCC_spans.outputField
    GCC_spans_field.name = "GCC200"
    fldMap_GCC_spans.outputField = GCC_spans_field

    fieldMappings_spans.addFieldMap(fldMap_GCC_spans)

    # 15. LATITUDE
    fldMap_LATITUDE_spans = arcpy.FieldMap()
    fldMap_LATITUDE_spans.addInputField(inSpans, "LATITUDE")

    LATITUDE_spans_field = fldMap_LATITUDE_spans.outputField
    LATITUDE_spans_field.name = "LATITUDE"
    fldMap_LATITUDE_spans.outputField = LATITUDE_spans_field

    fieldMappings_spans.addFieldMap(fldMap_LATITUDE_spans)

    # 16. LONGITUDE
    fldMap_LONGITUDE_spans = arcpy.FieldMap()
    fldMap_LONGITUDE_spans.addInputField(inSpans, "LONGITUDE")

    LONGITUDE_spans_field = fldMap_LONGITUDE_spans.outputField
    LONGITUDE_spans_field.name = "LONGITUDE"
    fldMap_LONGITUDE_spans.outputField = LONGITUDE_spans_field

    fieldMappings_spans.addFieldMap(fldMap_LONGITUDE_spans)

    # 17. PMD
    fldMap_PMD_spans = arcpy.FieldMap()
    fldMap_PMD_spans.addInputField(inSpans, "PMD_1")

    PMD_spans_field = fldMap_PMD_spans.outputField
    PMD_spans_field.name = "PMD"
    PMD_spans_field.aliasName = "PMD"
    fldMap_PMD_spans.outputField = PMD_spans_field

    fieldMappings_spans.addFieldMap(fldMap_PMD_spans)


    # 18. SHAPE_LENGTH
    fldMap_SL_spans = arcpy.FieldMap()
    fldMap_SL_spans.addInputField(inSpans, "Shape_Length")

    SL_spans_field = fldMap_SL_spans.outputField
    SL_spans_field.name = "Shape_Length"
    fldMap_SL_spans.outputField = SL_spans_field

    fieldMappings_spans.addFieldMap(fldMap_SL_spans)

    
    arcpy.FeatureClassToFeatureClass_conversion(inSpans, Final_GDB, out_fc_Spans, '#', fieldMappings_spans)
     
    [arcpy.DeleteField_management(outSpans,field) for field in delete_fields]
    
    with arcpy.da.UpdateCursor(outSpans,["CIRCUIT_1"]) as uCur:
        for row in uCur:
            row[0] = str(cirNAME)
            uCur.updateRow(row)

## TOWERS

arcpy.AddMessage("/n/n....CREATING FINAL TOWERS..../n/n")

for circuit_GDB, Final_GDB in zip(circuit_inSITE_GDBs, circuit_FINAL_GDBs_List):

    delete_fields = ["TEXT1","NUMBER1","NUMBER2","IS_SRA","IS_VELB","IS_HCP","HCP_AREA_NAME","ORD","STR_NUM","HEIGHT","STR_ID"]

    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    arcpy.AddMessage(">%s< Towers Formatting Processing....\n" % cirNAME)

    inTowers = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_Towers" % (cirNAME))
    
    out_towers_FC = ("%s_BAY_AREA_2016_Towers" % (cirNAME))
    
    outTowers = os.path.join(Final_GDB, "%s_BAY_AREA_2016_Towers" % (cirNAME))
    
    
    
    # TOWERS FIELD MAP

    fieldMappings_towers = arcpy.FieldMappings()

    # 1. STR GEOTAG
    fldMap_STR_TAG_towers = arcpy.FieldMap()
    fldMap_STR_TAG_towers.addInputField(inTowers, "STR_GEOTAG")

    STR_TAG_towers_field = fldMap_STR_TAG_towers.outputField
    STR_TAG_towers_field.name = "STR_GEOTAG"
    fldMap_STR_TAG_towers.outputField = STR_TAG_towers_field

    fieldMappings_towers.addFieldMap(fldMap_STR_TAG_towers)

    # 2. LONGITUDE
    fldMap_LONG_towers = arcpy.FieldMap()
    fldMap_LONG_towers.addInputField(inTowers, "LONGITUDE")

    LONG_towers_field = fldMap_LONG_towers.outputField
    LONG_towers_field.name = "LONGITUDE"
    fldMap_LONG_towers.outputField = LONG_towers_field

    fieldMappings_towers.addFieldMap(fldMap_LONG_towers)

    # 3. LONGITUDE
    fldMap_LAT_towers = arcpy.FieldMap()
    fldMap_LAT_towers.addInputField(inTowers, "LATITUDE")

    LAT_towers_field = fldMap_LAT_towers.outputField
    LAT_towers_field.name = "LATITUDE"
    fldMap_LAT_towers.outputField = LAT_towers_field

    fieldMappings_towers.addFieldMap(fldMap_LAT_towers)
    
    # 4. X
    fldMap_X_towers = arcpy.FieldMap()
    fldMap_X_towers.addInputField(inTowers, "X")

    X_towers_field = fldMap_X_towers.outputField
    X_towers_field.name = "X"
    fldMap_X_towers.outputField = X_towers_field

    fieldMappings_towers.addFieldMap(fldMap_X_towers)
    
    # 5. Y
    fldMap_Y_towers = arcpy.FieldMap()
    fldMap_Y_towers.addInputField(inTowers, "Y")

    Y_towers_field = fldMap_Y_towers.outputField
    Y_towers_field.name = "Y"
    fldMap_Y_towers.outputField = Y_towers_field

    fieldMappings_towers.addFieldMap(fldMap_Y_towers)

    # 6. ELEVATION
    fldMap_ELEVATION_towers = arcpy.FieldMap()
    fldMap_ELEVATION_towers.addInputField(inTowers, "ELEVATION")

    ELEVATION_towers_field = fldMap_ELEVATION_towers.outputField
    ELEVATION_towers_field.name = "ELEVATION"
    fldMap_ELEVATION_towers.outputField = ELEVATION_towers_field

    fieldMappings_towers.addFieldMap(fldMap_ELEVATION_towers)
    
    # 6. VOLTAGE
    fldMap_VOLTAGE_towers = arcpy.FieldMap()
    fldMap_VOLTAGE_towers.addInputField(inTowers, "VOLTAGE")

    VOLTAGE_towers_field = fldMap_VOLTAGE_towers.outputField
    VOLTAGE_towers_field.name = "VOLTAGE"
    fldMap_VOLTAGE_towers.outputField = VOLTAGE_towers_field

    fieldMappings_towers.addFieldMap(fldMap_VOLTAGE_towers)
    
    # 6. VOLTAGE
    fldMap_LINE_ID_towers = arcpy.FieldMap()
    fldMap_LINE_ID_towers.addInputField(inTowers, "LINEID_1")

    LINE_ID_towers_field = fldMap_LINE_ID_towers.outputField
    LINE_ID_towers_field.name = "LINE_ID"
    LINE_ID_towers_field.aliasName = "LINE_ID"
    fldMap_LINE_ID_towers.outputField = LINE_ID_towers_field

    fieldMappings_towers.addFieldMap(fldMap_LINE_ID_towers)
    
    # 6. VOLTAGE
    fldMap_LINE_NAME_towers = arcpy.FieldMap()
    fldMap_LINE_NAME_towers.addInputField(inTowers, "LINE_NAME1")

    LINE_NAME_towers_field = fldMap_LINE_NAME_towers.outputField
    LINE_NAME_towers_field.name = "LINE_NAME"
    LINE_NAME_towers_field.aliasName = "LINE_NAME"
    fldMap_LINE_NAME_towers.outputField = LINE_NAME_towers_field

    fieldMappings_towers.addFieldMap(fldMap_LINE_NAME_towers)
    
    # 6. VOLTAGE
    fldMap_PMD_towers = arcpy.FieldMap()
    fldMap_PMD_towers.addInputField(inTowers, "PMD")

    PMD_towers_field = fldMap_PMD_towers.outputField
    PMD_towers_field.name = "PMD"
    fldMap_PMD_towers.outputField = PMD_towers_field

    fieldMappings_towers.addFieldMap(fldMap_PMD_towers)
    
    # 6. VOLTAGE
    fldMap_DIVISION_towers = arcpy.FieldMap()
    fldMap_DIVISION_towers.addInputField(inTowers, "DIVISION")

    DIVISION_towers_field = fldMap_DIVISION_towers.outputField
    DIVISION_towers_field.name = "DIVISION"
    fldMap_DIVISION_towers.outputField = DIVISION_towers_field

    fieldMappings_towers.addFieldMap(fldMap_DIVISION_towers)
    
    # 6. VOLTAGE
    fldMap_REGION_towers = arcpy.FieldMap()
    fldMap_REGION_towers.addInputField(inTowers, "REGION")

    REGION_towers_field = fldMap_REGION_towers.outputField
    REGION_towers_field.name = "REGION"
    fldMap_REGION_towers.outputField = REGION_towers_field

    fieldMappings_towers.addFieldMap(fldMap_REGION_towers)
    
    # 6. VOLTAGE
    fldMap_COUNTY_towers = arcpy.FieldMap()
    fldMap_COUNTY_towers.addInputField(inTowers, "COUNTY")

    COUNTY_towers_field = fldMap_COUNTY_towers.outputField
    COUNTY_towers_field.name = "COUNTY"
    fldMap_COUNTY_towers.outputField = COUNTY_towers_field

    fieldMappings_towers.addFieldMap(fldMap_COUNTY_towers)

    # 6. VOLTAGE
    fldMap_CITY_towers = arcpy.FieldMap()
    fldMap_CITY_towers.addInputField(inTowers, "CITY")

    CITY_towers_field = fldMap_CITY_towers.outputField
    CITY_towers_field.name = "CITY"
    fldMap_CITY_towers.outputField = CITY_towers_field

    fieldMappings_towers.addFieldMap(fldMap_CITY_towers)
    
    # 6. VOLTAGE
    fldMap_ACQ_DATE_towers = arcpy.FieldMap()
    fldMap_ACQ_DATE_towers.addInputField(inTowers, "DATE1")

    ACQ_DATE_towers_field = fldMap_ACQ_DATE_towers.outputField
    ACQ_DATE_towers_field.name = "ACQ_DATE"
    ACQ_DATE_towers_field.aliasName = "ACQ_DATE"
    fldMap_ACQ_DATE_towers.outputField = ACQ_DATE_towers_field

    fieldMappings_towers.addFieldMap(fldMap_ACQ_DATE_towers)
    
    
    
    arcpy.FeatureClassToFeatureClass_conversion(inTowers, Final_GDB, out_towers_FC, '#', fieldMappings_towers)
    
    [arcpy.DeleteField_management(outTowers, field) for field in delete_fields]

    


## TTs

arcpy.AddMessage("/n/n....CREATING FINAL TREE TOPS..../n/n")

for circuit_GDB, Final_GDB in zip(circuit_inSITE_GDBs, circuit_FINAL_GDBs_List):

    delete_fields = ["TID","id","Join_Count","TARGET_FID","delta_h","Span_NBR","BST","AST","SECT_NBR","WIRES_PHS","PHASES","WIRES_TTL","LENGTH",
"SPAN_GUID","SPAN_NAME","SPAN_LGTH","BST_ID","AST_ID","LINE_NBR","DivCode","ASFLOWN","MODELED","D2W","FALLDIST","RD2W_AF","LiDAR_OVR",
"LiDAR_D2W","LiDAR_HT","LiDAR_Falldist","LiDAR_Health","LiDAR_Species","POLE_BEFORE","POLE_AFTER","IS_SRA","IS_VELB",
"IS_HCP","HCP_AREA_NAME","ttop_kind","LENGTHS","Shape_Lengt","Shape_Leng","SPECIES","PMD_1","PMD_2","PMD_3","PMD_4","GEOTAG_1"]

    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    arcpy.AddMessage(">%s< TreeTops Formatting Processing....\n" % cirNAME)

    inTTs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_TreeTops_AF" % (cirNAME))

    out_fc_TTs = ("%s_BAY_AREA_2016_TreeTops_AF" % (cirNAME))
    outTTs = os.path.join(Final_GDB, "%s_BAY_AREA_2016_TreeTops_AF" % (cirNAME))

    # FIELD MAP FOR ORGANIZATION

    fieldMappings = arcpy.FieldMappings()

    # 33. APN_Number field
    fldMap_APN_Num = arcpy.FieldMap()
    fldMap_APN_Num.addInputField(inTTs, "APN_NUMBER")

    APN_Num_field = fldMap_APN_Num.outputField
    APN_Num_field.name = "APN_NUMBER"
    fldMap_APN_Num.outputField = APN_Num_field

    fieldMappings.addFieldMap(fldMap_APN_Num)

    # 34. STREET_num field
    fldMap_STREET_num = arcpy.FieldMap()
    fldMap_STREET_num.addInputField(inTTs, "STREET_NUM")

    STREET_num_field = fldMap_STREET_num.outputField
    STREET_num_field.name = "STREET_NUM"
    fldMap_STREET_num.outputField = STREET_num_field

    fieldMappings.addFieldMap(fldMap_STREET_num)

    # 35. STREET field
    fldMap_STREET = arcpy.FieldMap()
    fldMap_STREET.addInputField(inTTs, "STREET")

    STREET_field = fldMap_STREET.outputField
    STREET_field.name = "STREET"
    fldMap_STREET.outputField = STREET_field

    fieldMappings.addFieldMap(fldMap_STREET)

    # 37.  CUSTOMER Name field
    fldMap_CUST_NAME = arcpy.FieldMap()
    fldMap_CUST_NAME.addInputField(inTTs, "CUSTOMER_NAME")

    CUST_NAME_field = fldMap_CUST_NAME.outputField
    CUST_NAME_field.name = "CUSTOMER_N"
    CUST_NAME_field.aliasName = "CUSTOMER_N"
    fldMap_CUST_NAME.outputField = CUST_NAME_field

    fieldMappings.addFieldMap(fldMap_CUST_NAME)

    # 38. CUSTOMER_NAME1 field
    fldMap_CUST_NAME1 = arcpy.FieldMap()
    fldMap_CUST_NAME1.addInputField(inTTs, "CUSTOMER_NAME_1")

    CUST_NAME1_field = fldMap_CUST_NAME1.outputField
    CUST_NAME1_field.name = "CUSTOMER_1"
    CUST_NAME1_field.aliasName = "CUSTOMER_1"
    fldMap_CUST_NAME1.outputField = CUST_NAME1_field

    fieldMappings.addFieldMap(fldMap_CUST_NAME1)

    # 39. CITY field

    fldMap_CITY = arcpy.FieldMap()
    fldMap_CITY.addInputField(inTTs, "CITY")

    CITY_field = fldMap_CITY.outputField
    CITY_field.name = "CITY"
    fldMap_CITY.outputField = CITY_field

    fieldMappings.addFieldMap(fldMap_CITY)

    # 40. COUNTY field
    fldMap_COUNTY = arcpy.FieldMap()
    fldMap_COUNTY.addInputField(inTTs, "COUNTY")

    COUNTY_field = fldMap_COUNTY.outputField
    COUNTY_field.name = "COUNTY"
    fldMap_COUNTY.outputField = COUNTY_field

    fieldMappings.addFieldMap(fldMap_COUNTY)

    # 41. DIVISION field
    fldMap_DIV = arcpy.FieldMap()
    fldMap_DIV.addInputField(inTTs, "DIVISION")

    DIV_field = fldMap_DIV.outputField
    DIV_field.name = "DIVISION"
    fldMap_DIV.outputField = DIV_field

    fieldMappings.addFieldMap(fldMap_DIV)

    # 19. LINE_NAME field
    fldMap_LINE_NAME = arcpy.FieldMap()
    fldMap_LINE_NAME.addInputField(inTTs, "LINE_NAME")

    LINE_NAME_field = fldMap_LINE_NAME.outputField
    LINE_NAME_field.name = "LINE_NAME"
    fldMap_LINE_NAME.outputField = LINE_NAME_field

    fieldMappings.addFieldMap(fldMap_LINE_NAME)

    # SRA/LRA Field
    fldMap_SRA = arcpy.FieldMap()
    fldMap_SRA.addInputField(inTTs, "SRA_LRA")

    SRA_field = fldMap_SRA.outputField
    SRA_field.name = "SRA_LRA"
    fldMap_SRA.outputField = SRA_field

    fieldMappings.addFieldMap(fldMap_SRA)

    # 3. D2W_AF
    fldMap_DTW = arcpy.FieldMap()
    fldMap_DTW.addInputField(inTTs, "D2W_AF")

    DTW_field = fldMap_DTW.outputField
    DTW_field.name = "D2W_AF"
    fldMap_DTW.outputField = DTW_field

    fieldMappings.addFieldMap(fldMap_DTW)

    # 1. OFF_ field

    fldMap_OFF = arcpy.FieldMap()
    fldMap_OFF.addInputField(inTTs, "OFF_")

    OFF_field = fldMap_OFF.outputField
    OFF_field.name = "OFF"
    OFF_field.aliasName = "OFF"
    fldMap_OFF.outputField = OFF_field

    fieldMappings.addFieldMap(fldMap_OFF)



    # 8. H field
    fldMap_H = arcpy.FieldMap()
    fldMap_H.addInputField(inTTs, "H")

    H_field = fldMap_H.outputField
    H_field.name = "HEIGHT"
    H_field.aliasName = "HEIGHT"
    fldMap_H.outputField = H_field

    fieldMappings.addFieldMap(fldMap_H)

    # FALL_IN field
    fldMap_FI = arcpy.FieldMap()
    fldMap_FI.addInputField(inTTs, "FALL_IN")

    FI_field = fldMap_FI.outputField
    FI_field.name = "FALL_IN"
    fldMap_FI.outputField = FI_field

    fieldMappings.addFieldMap(fldMap_FI)


    # 4. OVR field
    fldMap_OVR = arcpy.FieldMap()
    fldMap_OVR.addInputField(inTTs, "OVR")

    OVR_field = fldMap_OVR.outputField
    OVR_field.name = "OVR"
    fldMap_OVR.outputField = OVR_field

    fieldMappings.addFieldMap(fldMap_OVR)

    # 15. LATITUDE field
    fldMap_LAT = arcpy.FieldMap()
    fldMap_LAT.addInputField(inTTs, "LATITUDE")

    LAT_field = fldMap_LAT.outputField
    LAT_field.name = "LATITUDE"
    fldMap_LAT.outputField = LAT_field

    fieldMappings.addFieldMap(fldMap_LAT)

    # 16. LONGITUTDE field
    fldMap_LAT = arcpy.FieldMap()
    fldMap_LAT.addInputField(inTTs, "LONGITUDE")

    LAT_field = fldMap_LAT.outputField
    LAT_field.name = "LONGITUDE"
    fldMap_LAT.outputField = LAT_field

    fieldMappings.addFieldMap(fldMap_LAT)

    # 18. LINE_ID field
    fldMap_LINE_ID = arcpy.FieldMap()
    fldMap_LINE_ID.addInputField(inTTs, "LINE_ID")

    LINE_ID_field = fldMap_LINE_ID.outputField
    LINE_ID_field.name = "LINE_ID"
    fldMap_LINE_ID.outputField = LINE_ID_field

    fieldMappings.addFieldMap(fldMap_LINE_ID)

    # 25. TREE_ID field
    fldMap_TREE_ID = arcpy.FieldMap()
    fldMap_TREE_ID.addInputField(inTTs, "TREEID")

    TREE_ID_field = fldMap_TREE_ID.outputField
    TREE_ID_field.name = "TREEID"
    fldMap_TREE_ID.outputField = TREE_ID_field

    fieldMappings.addFieldMap(fldMap_TREE_ID)

    # 26. ACQ_DATE field
    fldMap_ACQ_DATE = arcpy.FieldMap()
    fldMap_ACQ_DATE.addInputField(inTTs, "ACQ_DATE")

    ACQ_DATE_field = fldMap_ACQ_DATE.outputField
    ACQ_DATE_field.name = "ACQ_DATE"
    fldMap_ACQ_DATE.outputField = ACQ_DATE_field

    fieldMappings.addFieldMap(fldMap_ACQ_DATE)

    # 29. DC_AF field
    fldMap_DC_AF = arcpy.FieldMap()
    fldMap_DC_AF.addInputField(inTTs, "DC_AF")

    DC_AF_field = fldMap_DC_AF.outputField
    DC_AF_field.name = "DC_AF"
    fldMap_DC_AF.outputField = DC_AF_field

    fieldMappings.addFieldMap(fldMap_DC_AF)

    # 30. DC_FI field
    fldMap_DC_FI = arcpy.FieldMap()
    fldMap_DC_FI.addInputField(inTTs, "DC_FI")

    DC_FI_field = fldMap_DC_FI.outputField
    DC_FI_field.name = "DC_FI"
    fldMap_DC_FI.outputField = DC_FI_field

    fieldMappings.addFieldMap(fldMap_DC_FI)

    # 31. DC_VENDOR field
    fldMap_DC_VEN = arcpy.FieldMap()
    fldMap_DC_VEN.addInputField(inTTs, "DC_VENDOR")

    DC_VEN_field = fldMap_DC_VEN.outputField
    DC_VEN_field.name = "DC_VENDOR"
    fldMap_DC_VEN.outputField = DC_VEN_field

    fieldMappings.addFieldMap(fldMap_DC_VEN)

    # 9. OH field
    fldMap_OH = arcpy.FieldMap()
    fldMap_OH.addInputField(inTTs, "OH")

    OH_field = fldMap_OH.outputField
    OH_field.name = "OH"
    fldMap_OH.outputField = OH_field

    fieldMappings.addFieldMap(fldMap_OH)

    # 5. X field
    fldMap_X = arcpy.FieldMap()
    fldMap_X.addInputField(inTTs, "X")

    X_field = fldMap_X.outputField
    X_field.name = "X"
    fldMap_X.outputField = X_field

    fieldMappings.addFieldMap(fldMap_X)

    # 6. Y field
    fldMap_Y = arcpy.FieldMap()
    fldMap_Y.addInputField(inTTs, "Y")

    Y_field = fldMap_Y.outputField
    Y_field.name = "Y"
    fldMap_Y.outputField = Y_field

    fieldMappings.addFieldMap(fldMap_Y)

    # 7. Z field
    fldMap_Z = arcpy.FieldMap()
    fldMap_Z.addInputField(inTTs, "Z")

    Z_field = fldMap_Z.outputField
    Z_field.name = "Z"
    fldMap_Z.outputField = Z_field

    fieldMappings.addFieldMap(fldMap_Z)


    # 10. SPAN_TAG field
    fldMap_ST = arcpy.FieldMap()
    fldMap_ST.addInputField(inTTs, "SPAN_TAG")

    ST_field = fldMap_ST.outputField
    ST_field.name = "SPAN_TAG"
    fldMap_ST.outputField = ST_field

    fieldMappings.addFieldMap(fldMap_ST)

    # 11. BST_TAG field
    fldMap_BST = arcpy.FieldMap()
    fldMap_BST.addInputField(inTTs, "BST_TAG")

    BST_field = fldMap_BST.outputField
    BST_field.name = "BST_TAG"
    fldMap_BST.outputField = BST_field

    fieldMappings.addFieldMap(fldMap_BST)

    # 12. AST_TAG field
    fldMap_AST = arcpy.FieldMap()
    fldMap_AST.addInputField(inTTs, "AST_TAG")

    AST_field = fldMap_AST.outputField
    AST_field.name = "AST_TAG"
    fldMap_AST.outputField = AST_field

    fieldMappings.addFieldMap(fldMap_AST)

    # 13. GCC200 field
    fldMap_GCC = arcpy.FieldMap()
    fldMap_GCC.addInputField(inTTs, "GCC200")

    GCC_field = fldMap_GCC.outputField
    GCC_field.name = "GCC200"
    fldMap_GCC.outputField = GCC_field

    fieldMappings.addFieldMap(fldMap_GCC)

    # 14. SPAN_ID field
    fldMap_SPAN_ID = arcpy.FieldMap()
    fldMap_SPAN_ID.addInputField(inTTs, "SPAN_ID")

    SPAN_ID_field = fldMap_SPAN_ID.outputField
    SPAN_ID_field.name = "SPAN_ID"
    fldMap_SPAN_ID.outputField = SPAN_ID_field

    fieldMappings.addFieldMap(fldMap_SPAN_ID)

    # 17. VOLTAGE field
    fldMap_V = arcpy.FieldMap()
    fldMap_V.addInputField(inTTs, "VOLTAGE")

    V_field = fldMap_V.outputField
    V_field.name = "VOLTAGE"
    fldMap_V.outputField = V_field

    fieldMappings.addFieldMap(fldMap_V)

    # 27. HEALTH field
    fldMap_ACQ_DATE = arcpy.FieldMap()
    fldMap_ACQ_DATE.addInputField(inTTs, "HEALTH")

    ACQ_DATE_field = fldMap_ACQ_DATE.outputField
    ACQ_DATE_field.name = "HEALTH"
    fldMap_ACQ_DATE.outputField = ACQ_DATE_field

    fieldMappings.addFieldMap(fldMap_ACQ_DATE)

 
    # 32. PMD field
    fldMap_PMD = arcpy.FieldMap()
    fldMap_PMD.addInputField(inTTs, "PMD")

    PMD_field = fldMap_PMD.outputField
    PMD_field.name = "PMD"
    fldMap_PMD.outputField = PMD_field

    fieldMappings.addFieldMap(fldMap_PMD)

    # 24. Region field
    fldMap_Region = arcpy.FieldMap()
    fldMap_Region.addInputField(inTTs, "REGION")

    Region_field = fldMap_Region.outputField
    Region_field.name = "REGION"
    fldMap_Region.outputField = Region_field

    fieldMappings.addFieldMap(fldMap_Region)

    # 36. CUSTOMER PHONE field
    fldMap_CUST_PH = arcpy.FieldMap()
    fldMap_CUST_PH.addInputField(inTTs, "CUSTOMER_PHONE")

    CUST_PH_field = fldMap_CUST_PH.outputField
    CUST_PH_field.name = "CUSTOMER_P"
    CUST_PH_field.aliasName = "CUSTOMER_P"
    fldMap_CUST_PH.outputField = CUST_PH_field

    fieldMappings.addFieldMap(fldMap_CUST_PH)





    arcpy.FeatureClassToFeatureClass_conversion(inTTs, Final_GDB, out_fc_TTs, '#', fieldMappings)

    [arcpy.DeleteField_management(outTTs, field)for field in delete_fields]
    
    with arcpy.da.UpdateCursor(outTTs,["D2W_AF","OFF"]) as uCur:
        for row in uCur:
            row[0] = str(row[0]).split(".")[0] + "." +str(row[0]).split(".")[1][:1]
            row[1] = str(row[1]).split(".")[0] + "." +str(row[1]).split(".")[1][:1]
            
            uCur.updateRow(row)
    
    




## VPs
arcpy.AddMessage("/n/n....CREATING FINAL VEG POLYS..../n/n")

for circuit_GDB, Final_GDB in zip(circuit_inSITE_GDBs, circuit_FINAL_GDBs_List):

    delete_fields = ["id","TID","delta_h","ttop_kind","OH","D2W_AF","OVR","Shape_Leng"]

    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    arcpy.AddMessage(">%s< VegPolys Formatting Processing....\n" % cirNAME)

    inVPs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_VegPolys" % (cirNAME))
    VPs_FC = ("%s_BAY_AREA_2016_VegPolys" % (cirNAME))
    
    outVPs = os.path.join(Final_GDB, "%s_BAY_AREA_2016_VegPolys" % (cirNAME))

    # VPs Field Map

    fieldMappings_VPs = arcpy.FieldMappings()

    # 1. X
    fldMap_X_VPs = arcpy.FieldMap()
    fldMap_X_VPs.addInputField(inVPs, "X")

    X_VPs_field = fldMap_X_VPs.outputField
    X_VPs_field.name = "X"
    fldMap_X_VPs.outputField = X_VPs_field

    fieldMappings_VPs.addFieldMap(fldMap_X_VPs)

    # 1. Y
    fldMap_Y_VPs = arcpy.FieldMap()
    fldMap_Y_VPs.addInputField(inVPs, "Y")

    Y_VPs_field = fldMap_Y_VPs.outputField
    Y_VPs_field.name = "Y"
    fldMap_Y_VPs.outputField = Y_VPs_field

    fieldMappings_VPs.addFieldMap(fldMap_Y_VPs)
    
    # 1. Z
    fldMap_Z_VPs = arcpy.FieldMap()
    fldMap_Z_VPs.addInputField(inVPs, "Z")

    Z_VPs_field = fldMap_Z_VPs.outputField
    Z_VPs_field.name = "Z"
    fldMap_Z_VPs.outputField = Z_VPs_field

    fieldMappings_VPs.addFieldMap(fldMap_Z_VPs)

    # 1. TREEID
    fldMap_GEOTAG_1_VPs = arcpy.FieldMap()
    fldMap_GEOTAG_1_VPs.addInputField(inVPs, "GEOTAG_1")

    GEOTAG_1_VPs_field = fldMap_GEOTAG_1_VPs.outputField
    GEOTAG_1_VPs_field.name = "TREEID"
    GEOTAG_1_VPs_field.aliasName = "TREEID"
    fldMap_GEOTAG_1_VPs.outputField = GEOTAG_1_VPs_field

    fieldMappings_VPs.addFieldMap(fldMap_GEOTAG_1_VPs)

    # 1. HEIGHT
    fldMap_HEIGHT_VPs = arcpy.FieldMap()
    fldMap_HEIGHT_VPs.addInputField(inVPs, "H")

    HEIGHT_VPs_field = fldMap_HEIGHT_VPs.outputField
    HEIGHT_VPs_field.name = "HEIGHT"
    HEIGHT_VPs_field.aliasName = "HEIGHT"
    fldMap_HEIGHT_VPs.outputField = HEIGHT_VPs_field

    fieldMappings_VPs.addFieldMap(fldMap_HEIGHT_VPs)
    
    # 1. Shape Length
    fldMap_Shape_Length_VPs = arcpy.FieldMap()
    fldMap_Shape_Length_VPs.addInputField(inVPs, "Shape_Length")

    Shape_Length_VPs_field = fldMap_Shape_Length_VPs.outputField
    Shape_Length_VPs_field.name = "Shape_Length"
    fldMap_Shape_Length_VPs.outputField = Shape_Length_VPs_field

    fieldMappings_VPs.addFieldMap(fldMap_Shape_Length_VPs)
    
    # 1. Shape_Area
    fldMap_Shape_Area_VPs = arcpy.FieldMap()
    fldMap_Shape_Area_VPs.addInputField(inVPs, "Shape_Area")

    Shape_Area_VPs_field = fldMap_Shape_Area_VPs.outputField
    Shape_Area_VPs_field.name = "Shape_Area"
    fldMap_Shape_Area_VPs.outputField = Shape_Area_VPs_field

    fieldMappings_VPs.addFieldMap(fldMap_Shape_Area_VPs)


    arcpy.FeatureClassToFeatureClass_conversion(inVPs, Final_GDB, VPs_FC,"#",fieldMappings_VPs)

    [arcpy.DeleteField_management(outVPs, field)for field in delete_fields]



