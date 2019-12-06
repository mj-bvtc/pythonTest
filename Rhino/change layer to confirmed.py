import rhinoscriptsyntax as rs
import Rhino


obj = rs.GetObjects()

rs.ObjectLayer(obj, layer="CONFIRMED")