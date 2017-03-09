import arcpy, os, sys

# PARAMETERS AND DIRECTORIES



INPUT_GDBs = arcpy.GetParameterAsText(0)
Output_Folder = arcpy.GetParameterAsText(1)

OH_Reatrib_GDBs = sorted(INPUT_GDBs.split(";"))

INPUT_GDBs

#FinalDeliverable_GDBs = os.path.join(Output_Folder,"REATTRIBUTED_OH_GDBs")


# FUNCTIONS

def split_following_num(s):
    prev_char = ''

    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char



## Fields needing swap: OH , DC_VENDOR, DC_AF

for circuit_GDB in OH_Reatrib_GDBs :
    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    outTTs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_TreeTops_AF" % (cirNAME))

    delete_fields =["D2W_AF","OVR","OH","Shape_Leng"]

    outSpans = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_VegPolys" % (cirNAME))
    
    IN_Spans = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_Spans" % (cirNAME))

    [arcpy.DeleteField_management(outSpans,field) for field in delete_fields]
    
    # Spans
    
    [arcpy.DeleteField_management(IN_Spans,field) for field in ["length_2"]]
    
    with arcpy.da.UpdateCursor(IN_Spans,["SPAN_ID","SPAN_TAG","LINE_ID"]) as Cur:
        for row in Cur:
            row[0] = row[2] + "+" + row[1]
            
            Cur.updateRow(row)
        
    # TTs
    fields = ["SRA_LRA","SPAN_ID","SPAN_TAG","LINE_ID"]
    with arcpy.da.UpdateCursor(outTTs,fields) as uCur:
        for row in uCur:
        
            row[1] = row[3] + "+" + row[2]
        
            if row[0] == 'Yes':
                row[0] = 'SRA'
            

            uCur.updateRow(row)


    
