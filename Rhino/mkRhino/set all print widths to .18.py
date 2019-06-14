import rhinoscriptsyntax as rs

width = .18

for id in rs.LayerIds():
    name = rs.LayerName(id)
    rs.LayerPrintWidth(name, width=width)
    print "Layer {} print width set to .{}".format(name, str(width))
    

print
print "Reset all layer widths"



