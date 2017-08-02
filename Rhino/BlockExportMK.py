import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

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
        doc.Objects.Add(geo)

def main():
    #selection
    objs = rs.GetObjects("Select objects")

    #add faces to document
    breps = [x for x in objs if get_type(x) == Rhino.DocObjects.ObjectType.Brep]
    for brep in breps:
        add_faces(brep)

    #get back surface info
    back = rs.GetObject("Select back face")
    back_face = get_face(back)
    back_vector = get_normal(back_face)
    back_centroid = get_centroid(back_face)    
    back_plane = Rhino.Geometry.Plane(back_centroid, back_vector)

    #get orientation surface info
    top = rs.GetObject("Select top face")
    top_face = get_face(top)
    top_vector = get_normal(top_face)
    top_centroid = get_centroid(top_face)

    #project centroid to make new axes perpendicular
    projected_point = back_plane.ClosestPoint(top_centroid)
    projected_vector = Rhino.Geometry.Vector3d(
            projected_point.X - back_centroid.X,
            projected_point.Y - back_centroid.Y,
            projected_point.Z - back_centroid.Z)
    line = Rhino.Geometry.Line(back_centroid, projected_vector, 20) #line to show you projection result
    Rhino.RhinoDoc.ActiveDoc.Objects.AddLine(line)

    #create transformation
    yz = rg.Plane(rg.Point3d.Origin, rg.Vector3d.YAxis, rg.Vector3d.ZAxis)
    start = rg.Plane(back_centroid, back_vector, projected_vector)
    remap = rg.Transform.PlaneToPlane(start, yz)

    #transform objects and redraw
    transform_objects(objs, remap)
    doc.Views.Redraw()


if __name__ == "__main__":
    main()