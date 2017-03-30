import PhotoScan
def reset_view():
    chunk = PhotoScan.app.document.chunk
    T = chunk.transform.matrix
    viewpoint = PhotoScan.app.viewpoint
    cx = viewpoint.width
    cy = viewpoint.height

    region = chunk.region
    r_center = region.center
    r_rotate = region.rot
    r_size = region.size
    r_vert = list()

    for i in range(8):   #bounding box corners
        r_vert.append(PhotoScan.Vector([0.5 * r_size[0] * ((i & 2) - 1), r_size[1] * ((i & 1) - 0.5), 0.25 * r_size[2] * ((i & 4) - 2)]))
        r_vert[i] = r_center + r_rotate * r_vert[i]

    height =  T.mulv(r_vert[1] - r_vert[0]).norm()
    width  = T.mulv(r_vert[2] - r_vert[0]).norm()

    if width / cx > height /cy:
        scale = cx / width
    else:
        scale = cy / height

    PhotoScan.app.viewpoint.coo = T.mulp(chunk.region.center)
    PhotoScan.app.viewpoint.mag = 80
    #PhotoScan.app.viewpoint.rot = chunk.transform.rotation * r_rotate

