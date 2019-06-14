import rhinoscriptsyntax as rs


obs = rs.GetObjects()

for o in obs:
    print o