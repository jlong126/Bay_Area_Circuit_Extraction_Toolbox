import arcpy, os, re

from collections import defaultdict

arcpy.env.overwriteOutput = 1
arcpy.Delete_management("in_memory")


PGE_MASTER = arcpy.GetParameterAsText(0)
CALIBRATION_MASTER = arcpy.GetParameterAsText(1)
INPUT_inSITE_Ready_GDBs = arcpy.GetParameterAsText(2)



circuit_inSITE_GDBs = sorted(INPUT_inSITE_Ready_GDBs.split(";"))

## Functions


## Get Cir Name
def split_following_num(s):
    prev_char = ''
    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char


## Get Acq Date

date_dict = {}

for circuit_GDB in circuit_inSITE_GDBs:

    cirNAME = split_following_num(os.path.basename(circuit_GDB))
    inSpans = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_Spans" % (cirNAME))

    arcpy.MakeFeatureLayer_management(CALIBRATION_MASTER, "PGE_MASTER_LYR")
    arcpy.SelectLayerByLocation_management("PGE_MASTER_LYR", "INTERSECT", inSpans,1000, "NEW_SELECTION")

    temp_lyr = r'in_memory\Dates'
    arcpy.MakeFeatureLayer_management("PGE_MASTER_LYR", temp_lyr)

    with arcpy.da.SearchCursor(temp_lyr,["FolderPath"]) as sCur:
        dates = []
        for row in sCur:
            dates.append(row[0])
        form_dates = []
        for i in dates:

            i = i.split("/")[2].split("_")[1]
            form_dates.append(i)

    rec_date = max(form_dates)
    formatted_date = rec_date[2:4]+"/"+rec_date[4:6]+"/"+rec_date[:2]

    date_dict[cirNAME] = formatted_date
    del temp_lyr

### circuit: circuit ID dictionary look up
fields = ['CircuitNam','Circuit_ID','PMD_ID']

info = {row[0]:dict(zip(fields,row[:])) for row in arcpy.da.SearchCursor(PGE_MASTER,fields)}

kv_dict = {04:4,11:12,22:21,21:21,12:12}
## will need to update SPAN_ID, LINE_ID, PMD_1 , LINE_NAME, VOLTAGE, LINE_NBR

for circuit_GDB in circuit_inSITE_GDBs:
    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    inSpans = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_Spans" % (cirNAME))

    cirPAT = str(re.findall('\d+', cirNAME)[:2])
    cirNUM = int(cirPAT[3:5])


    with arcpy.da.UpdateCursor(inSpans,["SPAN_ID","LINE_ID","LINE_NAME","LINE_NBR","PMD_1","VOLTAGE"]) as uCur:
        for row in uCur:
            
            real = re.sub('^([^+]*)+',info[cirNAME]["Circuit_ID"],str(row[0]))
           
            #row[0] =  row[0].replace(str(num),info[cirNAME]["Circuit_ID"])
            row[0] =  real
            row[2] = info[cirNAME]["CircuitNam"]
            row[1] = info[cirNAME]["Circuit_ID"]
            row[4] = info[cirNAME]["PMD_ID"]
            row[3] = info[cirNAME]["Circuit_ID"]
            row[5] = kv_dict[cirNUM]

            uCur.updateRow(row)

## Towers
for circuit_GDB in circuit_inSITE_GDBs:
    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    inSpans = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_Towers" % (cirNAME))

    cirPAT = str(re.findall('\d+', cirNAME)[:2])
    cirNUM = int(cirPAT[3:5])

    with arcpy.da.UpdateCursor(inSpans, ["LINEID_1", "LINE_NAME1", "PMD", "DATE1", "VOLTAGE"]) as uCur:
        for row in uCur:
            row[0] = info[cirNAME]["Circuit_ID"]
            row[1] = info[cirNAME]["CircuitNam"]
            row[2] = info[cirNAME]["PMD_ID"]
            row[3] = date_dict[cirNAME]
            row[4] = kv_dict[cirNUM]

            uCur.updateRow(row)


# TreeTops
for circuit_GDB in circuit_inSITE_GDBs:
    cirNAME = split_following_num(os.path.basename(circuit_GDB))

    inSpans = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_inSITE_Ready_TreeTops_AF" % (cirNAME))

    cirPAT = str(re.findall('\d+', cirNAME)[:2])
    cirNUM = int(cirPAT[3:5])

    with arcpy.da.UpdateCursor(inSpans, ["SPAN_ID", "LINE_ID", "LINE_NAME","LINE_NBR","PMD_1","PMD","SPECIES","LiDAR_Species","VOLTAGE","ACQ_DATE"]) as uCur:
        for row in uCur:
            
            real = re.sub('^([^+]*)+',info[cirNAME]["Circuit_ID"],str(row[0]))
            
            row[0] = real
            row[2] = info[cirNAME]["CircuitNam"]
            row[1] = info[cirNAME]["Circuit_ID"]
            row[3] = info[cirNAME]["Circuit_ID"]
            row[4] = info[cirNAME]["PMD_ID"]
            row[5] = info[cirNAME]["PMD_ID"]
            row[6] = "UNKN"
            row[7] = "UNKN"
            row[8] = kv_dict[cirNUM]
            row[9] = date_dict[cirNAME]
            uCur.updateRow(row)





































del info





