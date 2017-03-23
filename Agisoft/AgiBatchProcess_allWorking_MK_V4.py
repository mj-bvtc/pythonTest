import PhotoScan
import os
import math
import itertools

doc = PhotoScan.app.document
app = PhotoScan.app


class AgiChunk:
    """
    A collection of attributes and
    commands for processing agi chunks
    """

    def __init__(self, chunk, agi_doc):
        self.name = None
        self.agi_doc = agi_doc
        self.chunk = chunk
        self.error = None
        self.start_error = None
        self.exists = None
        self.enabled = None
        self.is_aligned = None
        self.is_dense = None
        self.is_meshed = None
        self.is_modeled = None
        self.is_textured = None
        self.is_marked = None
        self.is_obj = None
        self.obj_path = None
        self.is_enough_points = None
        self.initial_point_count = None
        self.final_point_count = None

    def align(self):
        chunk = self.chunk
        # initial alignment
        chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.GenericPreselection,
                          keypoint_limit=40000, tiepoint_limit=4000)
        chunk.alignCameras()
        self.initial_point_count = len(chunk.point_cloud.points)
        print(f"Original Point initialPointCount: {self.initial_point_count}")
        self.is_aligned = True
        return

    def adjust_error(self):
        # Reduces error without removing too many points, while loop
        chunk = self.chunk
        pt_list = chunk.point_cloud.points
        init_points = self.initial_point_count
        print(f"initial points: {str(init_points)}")

        # initial settings before loop\

        error1 = error(chunk)

        initial_pts = init_points
        current_pts = initial_pts
        count = 0
        while error1 >= 1.000:
            # prints current error as it goes through loop
            print("initial error: " + str(error1))

            # breaks if half points or more removed
            if initial_pts * .50 > current_pts:
                print("Percentage of points removed too high, I stopped it")
                break

            tie_point_count = len(chunk.point_cloud.points)
            # breaks if less than 40K points are left
            if tie_point_count < 5000:
                print("Point count almost went below 40,000, I stopped it")
                break

            # breaks if loop runs more than 1K times
            if count > 100:
                print("This may have ran forever, I stopped it")
                break

            # optimize camera alignment before removing points
            chunk.optimizeCameras(fit_f=True, fit_cxcy=True, fit_b1=True, fit_b2=True, fit_k1k2k3=True, fit_p1p2=True,
                                  fit_k4=True, fit_p3=True, fit_p4=True)

            # remove error by %, lower point count (for simulation only), advance count by 1
            error1 *= .80
            # current_pts -= 500
            count += 1
            chunk.buildPoints(error=(chunk.buildPoints(error1)))

        # prints total number of times loop ran
        print("While loop ran " + str(count) + " times")
        print("Number of points after gradual selection: ")
        print(len(chunk.point_cloud.points))
        self.final_point_count = len(chunk.point_cloud.points)
        return

    def camera_crop(self):
        chunk = self.chunk
        point_list = []
        combos = list(itertools.combinations(chunk.cameras, 2))

        cam_list = []
        for cam in chunk.cameras:
            if cam.center is not None:
                point_list.append(cam.center)
                cam_list.append(cam.label)

        pt_combos = list(itertools.combinations(point_list, 2))

        dist_list = []

        a = [0, 0, 0]
        b = [8, 0, 0]

        test_dist = pt_dist(a, b)

        for pt in pt_combos:
            dist = pt_dist(pt[0], pt[1])
            dist_list.append(dist)

        max_dist = max(dist_list)  # biggest distance
        print(max_dist)

        index = dist_list.index(max_dist)  # index of biggest distance
        # print(index)

        far_pts = pt_combos[index]
        f1 = far_pts[0]  # Coordinates of far camA
        f2 = far_pts[1]  # Coordinates of far camA

        cam_ind_a = point_list.index(far_pts[0])
        cam_ind_b = point_list.index(far_pts[1])

        cam1 = cam_list[cam_ind_a]  # name of farthest cameraA
        cam2 = cam_list[cam_ind_b]  # name of farthest cameraB

        tie_pts = []

        center = mid_pt(f1, f2)  # midpoint between 2 far points, center of selection sphere

        for pt in chunk.point_cloud.points:
            tie_pts.append(pt.coord)

        sel_pt_list = []

        for pt in chunk.point_cloud.points:
            if pt_dist(center, pt.coord) < max_dist * 1.15:
                pt.selected = True
                sel_pt_list.append(pt)
            else:
                pt.selected = False

        chunk.point_cloud.cropSelectedPoints()
        chunk.resetRegion()  # Helps gradual selection work only on points of interest
        cropped_points = len(chunk.point_cloud.points)

        print("After cropping points too far from cameras there were: ")
        print(cropped_points)

        message = cam1 + " and " + cam2 + " are the farthest photos apart from each other.  They are " + str(
            max_dist) + " units apart from one another."
        message += " They are located at " + str(f1) + " and " + str(f2)
        message += " Halfway between them is " + str(
            center) + " A selection of nearby points will be made, and those points will be cropped. Thanks, and have a greeeeat day"
        print(message)

    def export_obj(self):
        chunk = self.chunk
        # gets folder containing chunk pics/source folder instead of building it
        path_pic = chunk.cameras[0].photo.path
        pic_name = path_pic.split("/")[-1]
        folder_pic = path_pic.rstrip(pic_name)

        # naming the file
        folder = folder_pic
        label = chunk.label
        new_path = "C:\\Users\\peters\\Desktop\\"
        name = str(label).replace(" ", "_")
        full_path = ""
        full_path = folder + name + ".obj"

        if os.path.exists(folder):

            message1 = "Attempting to export:".rjust(150)
            message2 = full_path.rjust(150)
            message = message1 + "\n" + message2
            print(message)
            chunk.exportModel(full_path) 
            print("\n")
            self.obj_path = full_path
            self.is_obj = True
        else:
            self.is_obj = False
            message = "Failed to export: " + full_path
            print(message)
            print("\n")

    def process_chunk(self):
        # check that chunk exists and is enabled
        self.check_exists()
        self.check_enabled()
        if not (self.exists and self.enabled):
            return

        # run alignment and lower the error
        self.align()
        self.camera_crop()
        self.adjust_error()
        self.camera_crop()
        self.check_enough_points()
        if self.is_enough_points is False or None:
            return
        doc.save()

        # process chunk
        # build dense point cloud
        self.check_dense()
        if self.is_dense is False or None:
            chunk.buildDenseCloud(quality=PhotoScan.HighQuality)
            doc.save()

        # build mesh
        self.check_mesh()
        if self.is_meshed() is False or None:
            chunk.buildModel(surface=PhotoScan.Arbitrary,
                             interpolation=PhotoScan.EnabledInterpolation,
                             face_count=2000000)
            doc.save()

        # build texture
        self.check_texture()
        if self.is_textured() is False or None:
            chunk.buildUV(mapping=PhotoScan.GenericMapping)
            chunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)
            doc.save()
        
        # export obj
        self.export_obj()
        if self.is_obj is not False or None:
            print(f"Script ran successfully for {self.name}")
        return    

    def check_exists(self):
        if self.chunk is none:
            print("Error: chunk is none")
            self.exists = False
            return
        else:
            self.name = self.chunk.label
            print(f"Chunk {self.name} exists")
            self.exists = True
            return

    def check_enabled(self):
        if self.chunk.enabled is False:
            print("Error: chunk is not enabled, skipping")
            self.enabled = False
            return
        else:
            print("Chunk enabled")
            self.enabled = True
            return

    def check_alignment(self):
        if self.chunk.point_cloud is not None:
            print(f"This chunk already has a sparse cloud: {self.name} ")
            self.is_aligned = True
            return
        else:
            print(f"This chunk does not have a sparse cloud: {self.name} ")
            self.is_aligned = False
            return

    def check_error(self):
        # Compatibility - Agisoft PhotoScan Professional 1.2.4
        # saves reprojection error for the tie points in the sparse cloud      
        chunk = self.chunk
        M = chunk.transform.matrix
        point_cloud = chunk.point_cloud
        projections = point_cloud.projections
        points = point_cloud.points
        n_points = len(points)

        points_errors = {}
        error_list = []

        for photo in chunk.cameras:

            if not photo.transform:
                continue

            T = photo.transform.inv()
            calib = photo.sensor.calibration

            point_index = 0
            for proj in projections[photo]:
                track_id = proj.track_id
                while point_index < n_points and points[point_index].track_id < track_id:
                    point_index += 1
                if point_index < n_points and points[point_index].track_id == track_id:
                    if points[point_index].valid == False:
                        continue

                    coord = T * points[point_index].coord
                    coord.size = 3
                    dist = calib.error(coord, proj.coord).norm() ** 2
                    v = M * points[point_index].coord
                    v.size = 3

                    if point_index in points_errors.keys():
                        point_index = int(point_index)
                        points_errors[point_index].x += dist
                        points_errors[point_index].y += 1
                    else:
                        points_errors[point_index] = PhotoScan.Vector([dist, 1])

        for point_index in range(n_points):

            if points[point_index].valid is False:
                continue

            if chunk.crs:
                w = M * points[point_index].coord
                w.size = 3
                X, Y, Z = chunk.crs.project(w)
            else:
                X, Y, Z, w = M * points[point_index].coord

            error = math.sqrt(points_errors[point_index].x / points_errors[point_index].y)
            error_list.append(error)
            error_list.sort()

        ave_error = sum(error_list) / len(error_list)  # for original photos, no point manipulation recorded

        valid_pt_list = []

        for pt in chunk.point_cloud.points:  # Makes a list of points that are NOT deleted
            if pt.valid is True:
                valid_pt_list.append(pt)
            else:
                continue

        count = 0

        print(ave_error)
        print(max(error_list))
        self.error = ave_error
        if self.start_error is None:
            self.start_error = ave_error
        return

    def check_dense(self):
        if self.chunk.dense_cloud:
            print("This chunk already has a dense cloud:  " + self.chunk.label)
            self.is_dense = True
            return
        else:
            print("This chunk does not have a dense cloud:  " + self.chunk.label)
            self.is_dense = False
            return

    def check_mesh(self):
        if self.chunk.model is not None:
            print("This chunk already has a model:  " + self.chunk.label)
            self.is_meshed = True
            return
        else:
            print("This chunk does not have a model:  " + self.chunk.label)
            self.is_meshed = False
            return

    def check_model(self):
        chunk = self.chunk
        if chunk.model is not None:
            print("This model exists:  " + chunk.label)
            self.is_modeled = True
            return
        else:
            message = "This model DOES NOT exist:  " + chunk.label
            print(message)
            self.is_modeled = False
            return

    def check_texture(self):
        chunk = self.chunk
        try:
            texture = chunk.model.meta['atlas/atlas_blend_mode']
            if texture is None:
                print("This chunk does not have a texture:  " + chunk.label)
                self.is_textured = False
                return

            else:
                print("This chunk already has a texture:  " + chunk.label)
                self.is_textured = True
                return

        except AttributeError:
            print("This chunk does not have a texture:  " + chunk.label)
            self.is_textured = False
            return

    def check_markers(self):
        chunk = self.chunk
        if len(chunk.markers) > 0:
            print("Markers marked for:" + chunk.label)
            self.is_marked = True
            return
        else:
            print("No markers found: " + chunk.label)
            self.is_marked = False
            return

    def check_enough_points(self):
        chunk = self.chunk
        min_points = 2000
        points_in_chunk = len(chunk.point_cloud.points)
        name = chunk.label
        if points_in_chunk < min_points:
            print("Less than required number of points to generate good model")
            print(f"{min_points} required points, {points_in_chunk} points in chunk {self.name}  ")
            self.is_enough_points = False
        else:
            self.is_enough_points = True
        return
    
    def check_obj(self):
        pass


class Report:
    """Data logging tools for chunks"""

    def __init__(self):
        pass


class AgiDoc:
    """
    Tools for working with
    Agisoft documents
    """

    def __init__(self):
        self.doc = doc
        self.path = None
        self.is_saved = None
        self.is_saved()
        self.chunks = doc.chunks

    def get_path(self):
        path = app.getSaveFileName("Save Project As") + ".psx"
        doc.save(path)
        print("Saved to path:  " + path)
        self.path = path
        return

    def is_saved(self):
        if doc.path == "":
            print("File not saved")
            self.get_path()
            self.is_saved = False
            return
        else:
            print(f"File already Saved: {doc.path}")
            self.path = doc.path
            self.is_saved = True
            return

    def process_all_chunks(self):
        for chunk in self.chunks:
            agi = AgiChunk(chunk, self)
            agi.process_chunk()
        PhotoScan.app.messageBox("Script Complete! Hooray!!!")


def pt_dist( pta, ptb):
    x = ptb[0] - pta[0]
    y = ptb[1] - pta[1]
    z = ptb[2] - pta[2]
    distance = math.sqrt((x) ** 2 + (y) ** 2 + (z) ** 2)
    return distance


def mid_pt(ptA, ptB):
    x = (ptA[0] + ptB[0]) / 2
    y = (ptA[1] + ptB[1]) / 2
    z = (ptA[2] + ptB[2]) / 2
    return [x, y, z]

if __name__ == "__main__":
    pass
