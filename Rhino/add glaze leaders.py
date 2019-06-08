import rhinoscriptsyntax as rs

rs.Command("-_Leader _pause _pause _pause _enter GLAZE _enter ")

rs.Command("-_Leader _pause _pause _pause _enter GLAZELINE")
obj = rs.LastCreatedObjects()
rs.LeaderText(obj, text= "GLAZE LINE")