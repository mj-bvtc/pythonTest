import rhinoscriptsyntax as rs

steal = rs.GetObject("Select dot to match", filter=rs.filter.textdot)
name = rs.TextDotText(steal)

texts = rs.GetObjects("Select text objects to apply to", filter=rs.filter.textdot)

rs.EnableRedraw(False)

for t in texts:
    rs.TextDotText(t, name)

rs.EnableRedraw(True)