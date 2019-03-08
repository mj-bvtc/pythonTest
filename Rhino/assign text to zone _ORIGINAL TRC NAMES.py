import rhinoscriptsyntax as rs

obs = rs.GetObjects("Select Text Objects", filter=rs.filter.annotation )
zones = rs.GetObjects("Select zones", filter=rs.filter.curve)

priorities = {
"64c0fe00-fa1a-4f36-9442-c33565d2c392": 12, #12
"15c5e770-6169-48ce-b1b8-463dd6edf7b2" : 11,#11
"0587314d-264d-48ac-8621-dcdb3c913314" : 10,#10
"39b43bfb-0e97-4a1a-914c-da2cd076b138" : 9,#9
"5e5b85f0-6012-482e-9515-7c098e6c2f44" : 7,#7
"fb07fdee-9cf3-4117-876b-621459d4a2d8" : 6,#6
"4bfa7d15-02e3-4afd-82c6-ccf8ce3f4722" : 5,#5
"cd281492-f9ae-4184-aad6-bb38265c6fff" : 4,#4
"daa675eb-7c85-4570-be4f-fa591d8029bc" : 3,#3
"1f1abb5b-5f3e-41c0-9e40-bb6b32940552" : 2,#2
"68bbde5f-da75-4bef-9202-5302220811d1" : 1,#1
"1da72715-3d7a-4cd5-8b82-ff7fb9f6ddbf" : "Ground",#G
"c0ae40b8-d8c6-4180-b6c5-bd28bf8819b2" : "Clock",#clock
"b5a9d0f5-634a-4f98-affa-0d1a9b1784b8" : 1,#1
"ea035395-0c4b-46b6-b1be-00eb4d2e2d18" : 7,#7
"d8a9ba22-1b67-4eca-b0e1-e7965cfcac7a" : "Ground"#7

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