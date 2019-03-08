import rhinoscriptsyntax as rs




obs = rs.GetObjects()
measures = []
text = []


for ob in obs:
    dim = rs.DimensionValue(ob)
    dt = rs.DimensionText(ob)
    text.append(dt)
    measures.append(dim)
    #print dim
    
 

total = sum(measures)
count = len(measures)
avg = total/count

print "Average = {}".format(avg)
print


def dec_to_frac(number):
    from fractions import Fraction
    
    number = abs(number)
    
    #result = round(number, 4)   ##no need to round
    
    #create a list of precision to use, use closest 16th
    fracts = [x/16 for x in range(1,17,1)]
    
    #find closest match to fractions
    close = min(fracts, key=lambda x:abs(x-number))
    
    #use the decimal equivalent
    result = str(Fraction.from_float(close))
    print result

for num, m in enumerate(measures):
    print text[num]
    print m
    delta = m- avg
    print delta
    
    dec_to_frac(delta)
    
    print