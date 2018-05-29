import rhinoscriptsyntax as rs



zones = rs.GetObjects("Select Zones", filter=4)

for z in zones:
    print z