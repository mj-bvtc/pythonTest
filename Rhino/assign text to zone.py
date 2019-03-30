import rhinoscriptsyntax as rs

obs = rs.GetObjects("Select Text Objects", filter=rs.filter.annotation )
zones = rs.GetObjects("Select zones", filter=rs.filter.curve)

priorities = {
"93f0feb7-87d5-4808-ac8f-1fbb14310a0d": 1,
"46a9fb38-2214-42b0-817d-92a280fe9fec" : 2,
"af77efbc-3ee4-4eee-a570-46916601f9c8" : 3,
"6331e8ee-8f24-4d07-b769-f2b4be6cccc2" : 4,
"d2a9c23b-8066-4d48-a5eb-2a7cdf9ba91d" : 5,
"d3efb5e0-f926-4773-af8a-3b0c25044228" : 6,
"b9d27469-64cd-40d4-8d48-3f03fa97f646" : 7,
"63184b31-266e-499e-ad0d-83e4e4b07fc3" : 8,
"64ed1001-3407-4544-be8a-bea5932580dd" : 9,
"9c175cb1-90b4-4721-994b-0a690da58f89" : 10,
"db51f08c-73ca-4b41-bdd8-3c0a275d9347" : 11,
"1416dee3-184d-4ffe-956a-5e03d7b207a6" : 12,
"3c900d30-9c17-4b98-be6e-7ab260bf4e39" : 13
}


rs.EnableRedraw(enable=False)

for o in obs:
    txt = rs.TextObjectText(o)
    pt = rs.TextObjectPoint(o)
    
    zone = None
    
    for z in zones:
        result = rs.PointInPlanarClosedCurve(pt, z)
        if result == 1:
            zone = priorities[str(z)]
    
    zmsg = "Zone = {}".format(zone)
    rs.AddTextDot(zmsg, pt)
    
    report = "{},{},{}".format(o,txt,zone)
    print report
    

rs.EnableRedraw(enable=True)