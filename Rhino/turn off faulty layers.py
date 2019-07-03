import rhinoscriptsyntax as rs


layers = rs.LayerNames()

for l in layers:
    if "REMEDIATION" in l.upper():
        print l
        rs.LayerVisible(l, False)