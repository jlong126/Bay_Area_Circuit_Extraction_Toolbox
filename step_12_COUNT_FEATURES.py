import arcpy, os 


Final_GDBs_in = arcpy.GetParameterAsText(0)

Final_GDBs = sorted(Final_GDBs_in.split(";"))


def split_following_num(s):
    prev_char = ''
    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char
        
        

for circuit_GDB in Final_GDBs:
    cirNAME = split_following_num(os.path.basename(circuit_GDB))
    
    arcpy.AddMessage(">%s< Final Geodatabase Counting...." % cirNAME)
    
    VPs = []
    
    TTs = []
    
    inTTs = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_TreeTops_AF" % (cirNAME))
    
    inVps = os.path.join(circuit_GDB, "%s_BAY_AREA_2016_VegPolys" % (cirNAME))
    
    with arcpy.da.SearchCursor(inTTs,["TREEID"]) as sCur:
        for row in sCur:
            TTs.append(row[0])
            
    with arcpy.da.SearchCursor(inVps,["TREEID"]) as sCur:
        for row in sCur:
            VPs.append(row[0])
    
    arcpy.AddMessage(">%s< VegPolys" %len(VPs))
    
    arcpy.AddMessage(">%s< TreeTops\n" %len(TTs))
    if not len(VPs) == len(TTs):
        arcpy.AddWarning("VegPolys and Treetops Do NOT MATCH PLEASE INSPECT")