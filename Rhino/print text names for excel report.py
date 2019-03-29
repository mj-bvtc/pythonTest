import rhinoscriptsyntax as rs


obs = rs.GetObjects("Select text to report on", filter=rs.filter.annotation)
for o in obs:
    text = rs.TextObjectText(o)
    print text.strip()