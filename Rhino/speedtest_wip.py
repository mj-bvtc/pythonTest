import Rhino
#import rhinoscriptsyntax as rs
import time
#import LogStamp
#import os




doc = Rhino.RhinoDoc.ActiveDoc

start = time.time()

parameters = (500, True, 8, 6.2)
doc.Views.ActiveView.SpeedTest(*parameters)

end = time.time()

duration = end - start

#py_file =  os.path.realpath(__file__)


result = "Duration: {}\nParameters: {}".format(duration, parameters)
print "Document: {}".format(doc.Path)
#
print "Python file: {}".format(py_file)
#print "User: {}".format(LogStamp.get_log_stamp())
print "Rhino Version: {}".format(Rhino.RhinoApp.ExeVersion)
print(result)

