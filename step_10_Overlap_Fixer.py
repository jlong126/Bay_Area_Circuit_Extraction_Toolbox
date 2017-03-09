import arcpy, os, re

arcpy.env.overwriteOutput = 1
arcpy.Delete_management("in_memory")

Needs_update_GDB = arcpy.GetParameterAsText(0)
Bay_Ref = arcpy.GetParameterAsText(1)



ref_PGE = os.path.join(Bay_Ref, 'PG_E_BAY_AREA_INITIAL_CIRCUITS_JL_030717')

fields = ['CircuitNam','Circuit_ID','PMD_ID']
info = {row[0]:dict(zip(fields,row[:])) for row in arcpy.da.SearchCursor(ref_PGE,fields)}

kv_dict = {02: 2, 04: 4, 11: 12, 22: 21, 21: 21, 12: 12}

def split_following_num(s):
    prev_char = ''
    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char

cirNAME = split_following_num(os.path.basename(Needs_update_GDB))
cirPAT = str(re.findall('\d+', cirNAME)[:2])
cirNUM = int(cirPAT[3:5])

TTs_Fields = ["VOLTAGE","SPAN_ID","SPAN_TAG","LINE_ID","PMD","LINE_NAME"]  
inTTs = os.path.join(Needs_update_GDB, "%s_BAY_AREA_2016_TreeTops_AF" % (cirNAME))

sp_fields = ['VOLTAGE',"SPAN_ID","LINE_ID","PMD","LINE_NAME",'CIRCUIT_1','LINE_NBR','SPAN_TAG']
inSpans = os.path.join(Needs_update_GDB, "%s_BAY_AREA_2016_Spans" % (cirNAME))


towers_fields = ["LINE_ID","PMD","LINE_NAME",'VOLTAGE']
inTowers = os.path.join(Needs_update_GDB, "%s_BAY_AREA_2016_Towers" % (cirNAME))

with arcpy.da.UpdateCursor(inTTs,TTs_Fields) as uCur:
    for row in uCur:
        row[0] = kv_dict[cirNUM]
        row[1] = info[cirNAME]['Circuit_ID']+ '+' + row[2]
        
        row[3] = info[cirNAME]['Circuit_ID']
        row[4] = info[cirNAME]['PMD_ID']
        row[5] = info[cirNAME]['CircuitNam']
        uCur.updateRow(row)
with arcpy.da.UpdateCursor(inSpans, sp_fields) as uCur:
    for row in uCur:
        row[0] = kv_dict[cirNUM]
        row[1] = info[cirNAME]['Circuit_ID']+ '+' + row[7]
        
        row[2] = info[cirNAME]['Circuit_ID']
        row[3] = info[cirNAME]['PMD_ID']
        row[4] = info[cirNAME]['CircuitNam']
        row[5] = info[cirNAME]['CircuitNam']
        row[6] = info[cirNAME]['Circuit_ID']
        uCur.updateRow(row)
        
with arcpy.da.UpdateCursor(inTowers, towers_fields) as uCur:
    for row in uCur:
        row[3] = kv_dict[cirNUM]
        row[0] = info[cirNAME]['Circuit_ID']
        row[1] = info[cirNAME]['PMD_ID']
        row[2] = info[cirNAME]['CircuitNam']
        uCur.updateRow(row)


