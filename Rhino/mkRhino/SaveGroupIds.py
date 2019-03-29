import rhinoscriptsyntax as rs

def save_group():
    group_name = raw_input("Type in group name")
    group = rs.GetObjects("Select Group")
    if not group:
        print "Select Failed"
        return
    try:
        file = r"V:\Projects\35 East Wacker\Documents\011019 REMEDIATION MARKUPS\35 E Wacker West Elevation Survey\group selections\\" + group_name + ".txt"
        f = open(file, "w+")
        
        grp_len = len(group)
        print "Group length: " + str(grp_len)
        for g in group:
            f.write( str(g) + "\n")
            
    finally:
        f.close()
        print "File saved as: " + file 
        

save_group()


