def dec_to_frac(number):
    from fractions import Fraction
    
    
    #result = round(number, 4)   ##no need to round
    
    #create a list of precision to use, use closest 16th
    fracts = [x/16 for x in range(1,17,1)]
    
    #find closest match to fractions
    close = min(fracts, key=lambda x:abs(x-number))
    
    #use the decimal equivalent
    result = str(Fraction.from_float(close))
    print result
    

dec_to_frac(.125)