import rhinoscriptsyntax as rs



obs = rs.GetObjects("Select dimensions", filter=rs.filter.annotation)

for ob in obs:
    rs.DimensionUserText(ob, usertext="(        )")