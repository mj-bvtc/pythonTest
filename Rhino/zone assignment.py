import rhinoscriptsyntax as rs



#zone = rs.GetObject("select zone")
#priority = raw_input("type in priority")

class Zone:
    def __init__(self):
        self.priority = None
        self.id = None
        

def set_priorities(num):
    for i in range(num):
        z = Zone()
        id = rs.GetObject("select zone")
        priority = raw_input("type in priority")
        z.id = id
        z.priority = priority
        print "{},{}".format(priority, id)



set_priorities(7)