import rhinoscriptsyntax as rs


obs = rs.GetObjects("Get objects to label")

num = len(obs)
prefix = raw_input("Type in prefix")
for i,o in enumerate(obs):
    i += 1
    msg = "{}{}".format(prefix,i)
    pt = rs.GetPoint("Pick point")
    rs.AddTextDot(msg, pt)