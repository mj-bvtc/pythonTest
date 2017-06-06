import Rhino
import rhinoscriptsyntax as rs

doc = Rhino.RhinoDoc.ActiveDoc

def get_type(obj):
    return Rhino.RhinoDoc.ActiveDoc.Objects.Find(obj).ObjectType

def get_geo(id):
    return doc.Objects.Find(id).Geometry

def get_types(objs):
    type_list = []
    for obj in objs:
        type_list.append(get_type(obj))
    return type_list

def add_faces(id):
    obj = doc.Objects.Find(id)
    faces = obj.Geometry.Faces
    for face in faces:
        doc.Objects.Add(face.DuplicateFace(False))

def get_face(id):
    return get_geo(id).Faces[0]

def get_centroid(face):
    amp = Rhino.Geometry.AreaMassProperties.Compute(face)
    return amp.Centroid

def get_normal(face):
    point = get_centroid(face)
    success, u, v = face.ClosestPoint(point)
    return face.NormalAt(u,v)

def pick_normal():
    obj = rs.GetObject("Select Object")
    face = get_face(obj)
    return get_normal(face)
    

def transform_objects(objects, xform):
    for obj in objects:
        geo = get_geo(obj)
        geo.Transform(xform)
        
def main():
    #selection
    #objs = rs.GetObjects("Select objects")
    #print get_types(objs)
    
    #breps = [x for x in objs if get_type(x) == Rhino.DocObjects.ObjectType.Brep]
    #for brep in breps:
    #    add_faces(brep)
    
    #get back
    back = rs.GetObject("Select back face")
    back_face = get_face(back)
    back_vector = get_normal(back_face)
    back_centroid = get_centroid(back_face)    
    back_plane = Rhino.Geometry.Plane(back_centroid, back_vector)

    #orientation axis
    top = rs.GetObject("Select top face")
    top_face = get_face(top)
    top_vector = get_normal(top_face)
    top_centroid = get_centroid(top_face)
    result = top_vector.PerpendicularTo(back_vector)
    #print result
    #line = Rhino.Geometry.Line(top_centroid, top_vector, 20)
    #Rhino.RhinoDoc.ActiveDoc.Objects.AddLine(line)
    projected_point = back_plane.ClosestPoint(top_centroid)
    projected_vector = Rhino.Geometry.Vector3d(
            projected_point.X - back_centroid.X,
            projected_point.Y - back_centroid.Y,
            projected_point.Z - back_centroid.Z)
    line = Rhino.Geometry.Line(back_centroid, projected_vector, 20)
    Rhino.RhinoDoc.ActiveDoc.Objects.AddLine(line)
if __name__ == "__main__":
    main()