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

    outVPs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_VegPolys" % (cirNAME))

    # TTs
    fields = ["DC_AF","DC_VENDOR","OH","D2W_AF","OVR","DC_FI"]
    with arcpy.da.UpdateCursor(outTTs,fields) as uCur:
        for row in uCur:
            if row[2] == '_OH2':
                row[2] = '_OH1'
            elif row[2] == '_OH1':
                row[2] = '_OH2'

            if row[3] <= 2.0:
                row[0] = 'ZONE1'
            elif row[3] <= 4.0:
                row[0] = 'ZONE2'
            elif row[3] <= 6.0:
                row[0] = 'ZONE3'
            elif row[3] <= 15.0:
                row[0] = 'ZONE4'
            else:
                row[0] = None

            if row[2]:
                if row[0]:
                    row[0] += row[2]
                else:
                    row[0] = 'ZONE0_OH'

            row[1] = row[0].replace('ONE', '').replace('_', '') if row[0] else row[0]
            row[1] = row[1] + row[5] if (row[5] and row[1]) else filter(lambda r: r, (row[5], row[1]))[0]
            row[1] = row[1].replace('_', '')

            uCur.updateRow(row)

    with arcpy.da.UpdateCursor(outVPs, ["OH"]) as sCur:
        for row in sCur:
            if row[0] == '_OH2':
                row[0] = '_OH1'
            elif row[0] == '_OH1':
                row[0] = '_OH2'

            sCur.updateRow(row)
