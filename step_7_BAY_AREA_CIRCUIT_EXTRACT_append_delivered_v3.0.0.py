import arcpy,os

arcpy.env.overwriteOutput = True

INPUT_master = arcpy.GetParameterAsText(0)
INPUT_gdbs = arcpy.GetParameterAsText(1)


GDBs = sorted(INPUT_gdbs.split(";"))

GDBs_append_List =[]

for GDB in GDBs:
    GDBs_append_List.append(GDB)



# utlities

def split_following_num(s):
    prev_char = ''
    for i, char in enumerate(s):
        if char == '_' and prev_char in '0123456789':
            return s[:i]
        prev_char = char

# Duplicates Prevention
DELIVERED = []

master_spans = os.path.join(INPUT_master, "BAY_AREA_2016_Delivered_Spans")

with arcpy.da.SearchCursor(master_spans,["LINE_NAME"]) as sCur:
    for row in sCur:
        DELIVERED.append(row[0])

# Append only these circuits
append_list = []

for GDB in GDBs_append_List:
    if not split_following_num(os.path.basename(GDB)) in DELIVERED:
        append_list.append(GDB)


## Hold FCs

feature_classes = []

for GDB in append_list:
    walk = arcpy.da.Walk(GDB, datatype="FeatureClass")

    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            #if filename.endswith("Spans"):
            feature_classes.append(os.path.join(dirpath, filename))

for i in feature_classes:
    arcpy.AddMessage(i)

# Spans
spans_L = []

try:
    for spans in feature_classes:
        if spans.endswith("Spans"):
            spans_L.append(spans)

    master_spans = os.path.join(INPUT_master, "BAY_AREA_2016_Delivered_Spans")

    arcpy.Append_management(spans_L, master_spans, "NO_TEST","","")

except:
    for GDB in GDBs_append_List:
        if split_following_num(os.path.basename(GDB)) in DELIVERED:
            arcpy.AddError("%s SPANS HAS ALREADY BEEN DELIVERED, CAN NOT APPEND"%split_following_num(os.path.basename(GDB)))

# Towers
Towers_L = []

try:
    for i in feature_classes:
        if i.endswith("Towers"):
            Towers_L.append(i)

    master_Towers = os.path.join(INPUT_master, "BAY_AREA_2016_Delivered_Towers")

    arcpy.Append_management(Towers_L, master_Towers, "NO_TEST","","")

except:
    for GDB in GDBs_append_List:
        if split_following_num(os.path.basename(GDB)) in DELIVERED:
            arcpy.AddError("%s TOWERS HAS ALREADY BEEN DELIVERED, CAN NOT APPEND"%split_following_num(os.path.basename(GDB)))

# TreeTops
TTs_L = []

try:
    for i in feature_classes:
        if i.endswith("TreeTops_AF"):
            TTs_L.append(i)

    master_TTs = os.path.join(INPUT_master, "BAY_AREA_2016_Delivered_TreeTops_AF")

    arcpy.Append_management(TTs_L, master_TTs, "NO_TEST","","")

except:
    for GDB in GDBs_append_List:
        if split_following_num(os.path.basename(GDB)) in DELIVERED:
            arcpy.AddError("%s TREE TOPS HAS ALREADY BEEN DELIVERED, CAN NOT APPEND"%split_following_num(os.path.basename(GDB)))

# VPs
VPs_L = []

try:
    for i in feature_classes:
        if i.endswith("TreePolys_AF") or i.endswith("VegPolys"):
            VPs_L.append(i)

    master_VPs = os.path.join(INPUT_master, "BAY_AREA_2016_Delivered_VegPolys")

    arcpy.Append_management(VPs_L, master_VPs, "NO_TEST","","")

except:
    for GDB in GDBs_append_List:
        if split_following_num(os.path.basename(GDB)) in DELIVERED:
            arcpy.AddError("%s VEG POLYS HAS ALREADY BEEN DELIVERED, CAN NOT APPEND"%split_following_num(os.path.basename(GDB)))

















































