import rhinoscriptsyntax as rs


obs = rs.GetObjects("select surfaces", filter=8)

rs.EnableRedraw(enable=False)

for count, ob in enumerate(obs):
    #count += 1
    #print count, ob
    layer = rs.ObjectLayer(ob, layer=None)
    point = rs.SurfaceAreaCentroid(ob)[0]
    msg = "{}-{}".format(layer, count)
    rs.AddTextDot(msg, point)



rs.EnableRedraw(enable=True)


