"""
Tools for automating BVTC process with Agisoft PhotoScan
Compatible with Version 1.2.6
"""

import PhotoScan
import os
import math
import itertools
import time
import datetime
from functools import wraps

doc = PhotoScan.app.document
app = PhotoScan.app


def timer(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        # print("instance {} of class {} is decorated".format(self, self.__class__))
        # print("entering...")
        # print("running process...")
        start = time.time()
        result = fn(self, *args, **kwargs)
        end = time.time()
        # print("exiting...")
        dur = end - start
        msg = "'{}' function took {} seconds to run\n\n".format(fn.__name__, round(dur, 2))
        print(msg)
        self.log_list.append(msg)  # send log to class????
        return result
    return wrapper


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
        self.log_path = None
        self.log = None
        self.log_list = []
        self.indent = "\t"*5

    def create_log(self):
        # writes log file in folder with each chunk
        full_path = self.format_file_at_chunk(".txt", add_timestamp=True)
        report = open(full_path, "w")
        report.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        report.write("Project file path: {}\n".format(doc.path))
        report.write("Chunk: {}\n\n".format(self.name))
        for log in self.log_list:
            report.write(log)
        report.close()
        self.log_path = full_path
        self.log = report
        print("Created log file: {}\n".format(full_path))
        return

    @timer
    def align(self):
        chunk = self.chunk
        # initial alignment
        chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.GenericPreselection,
                          keypoint_limit=40000, tiepoint_limit=4000)
        chunk.alignCameras()
        self.initial_point_count = len(chunk.point_cloud.points)
        print("Original Point count: {}".format(self.initial_point_count))
        return

    @timer
    def adjust_error(self):
        # Reduces error without removing too many points, while loop
        chunk = self.chunk
        pt_list = chunk.point_cloud.points
        init_points = self.initial_point_count
        print("initial points: {}".format(str(init_points)))

        # initial settings before loop\

        error1 = self.check_error()

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
        self.is_aligned = True
        return

    @timer
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
        return

    def format_file_at_chunk(self, ext, add_timestamp=False):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        chunk = self.chunk
        # gets folder containing chunk pics/source folder instead of building it
        path_pic = chunk.cameras[0].photo.path
        pic_name = path_pic.split("/")[-1]
        folder_pic = path_pic.rstrip(pic_name)

        # naming the file
        folder = folder_pic
        label = chunk.label
        name = str(label).replace(" ", "_")
        if add_timestamp is True:
            full_path = folder + name + "_" + timestamp + ext
        else:
            full_path = folder + name + ext
        print("Formatted path {}".format(full_path))
        return full_path

    def export_obj(self):
        print("Exporting {}...".format(self.name))
        print(self.obj_path)
        self.chunk.exportModel(self.obj_path)
        print("\n")
        self.is_obj = True
        return

    @timer
    def run_verification(self):
        chunk = self.chunk
        # check that chunk exists and is enabled
        self.check_exists()
        self.check_enabled()
        if not (self.exists and self.enabled):
            return

    @timer
    def run_alignment(self):
        chunk = self.chunk
        # run alignment and lower the error
        self.check_alignment()
        if self.is_aligned is not True:
            self.align()
            self.camera_crop()
            self.adjust_error()
            self.camera_crop()
            self.check_enough_points()
            if self.is_enough_points is False or None:
                return
            doc.save()

    @timer
    def run_dense(self):
        # process chunk
        # build dense point cloud
        chunk = self.chunk

        self.check_dense()
        if self.is_dense is False or None:
            chunk.buildDenseCloud(quality=PhotoScan.HighQuality)
            doc.save()

    @timer
    def run_mesh(self):
        chunk = self.chunk
        # build mesh
        self.check_mesh()
        if self.is_meshed is False or None:
            chunk.buildModel(surface=PhotoScan.Arbitrary,
                             interpolation=PhotoScan.EnabledInterpolation,
                             face_count=2000000)
            doc.save()

    @timer
    def run_texture(self):
        chunk = self.chunk
        # build texture
        self.check_texture()
        if self.is_textured is False or None:
            chunk.buildUV(mapping=PhotoScan.GenericMapping)
            chunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)
            doc.save()

    @timer
    def run_obj(self):
        self.check_obj()

        # export obj
        if self.is_obj is False:
            self.export_obj()

    @timer
    def elapsed_time(self):
        chunk = self.chunk
        # process chunk
        self.run_verification()
        self.run_alignment()
        self.run_dense()
        self.run_mesh()
        self.run_texture()
        self.run_obj()
        self.export_report()
        return

    @timer
    def export_report(self):
        chunk = self.chunk
        path = self.format_file_at_chunk(".pdf", add_timestamp=True)
        if os.path.exists(path):
            return
        chunk.exportReport(path)
        return

    @timer
    def run_process(self):
        self.elapsed_time()
        # create log here
        self.create_log()

    def check_exists(self):
        chunk = self.chunk
        if self.chunk is None:
            print("Error: chunk is none")
            self.exists = False
            return
        else:
            self.name = self.chunk.label
            print("Chunk {} exists".format(self.name))
            self.exists = True
            return

    def check_enabled(self):
        if self.chunk.enabled is False:
            print("Error: chunk is not enabled, skipping\n\n\n")
            self.enabled = False
            return
        else:
            print("Chunk enabled")
            self.enabled = True
            return

    def check_alignment(self):
        if self.chunk.point_cloud is not None:
            print("This chunk already has a sparse cloud: {} ".format(self.name))
            self.is_aligned = True
            return
        else:
            print("This chunk does not have a sparse cloud: {} ".format(self.name))
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
        return ave_error

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
            print("{} required points, {} points in chunk {}".format(min_points, points_in_chunk, self.name))
            self.is_enough_points = False
        else:
            self.is_enough_points = True
        return
    
    def check_obj(self):
        full_path = self.format_file_at_chunk(".obj")

        if os.path.exists(full_path):
            print("{} already exists, skipping".format(full_path))
            self.obj_path = full_path
            self.is_obj = True
            return
        else:
            print("No obj in this chunks folder")
            self.is_obj = False
            self.obj_path = full_path
            return

    def reset_view(self, magnification=80):
        doc.chunk = self.chunk
        chunk = self.chunk
        T = chunk.transform.matrix
        viewpoint = PhotoScan.app.viewpoint
        cx = viewpoint.width
        cy = viewpoint.height

        region = chunk.region
        r_center = region.center
        r_rotate = region.rot
        r_size = region.size
        r_vert = list()

        for i in range(8):  # bounding box corners
            r_vert.append(PhotoScan.Vector(
                [0.5 * r_size[0] * ((i & 2) - 1), r_size[1] * ((i & 1) - 0.5), 0.25 * r_size[2] * ((i & 4) - 2)]))
            r_vert[i] = r_center + r_rotate * r_vert[i]

        height = T.mulv(r_vert[1] - r_vert[0]).norm()
        width = T.mulv(r_vert[2] - r_vert[0]).norm()

        if width / cx > height / cy:
            scale = cx / width
        else:
            scale = cy / height

        PhotoScan.app.viewpoint.coo = T.mulp(chunk.region.center)
        PhotoScan.app.viewpoint.mag = magnification
        # PhotoScan.app.viewpoint.rot = chunk.transform.rotation * r_rotate


class AgiDoc:
    """
    Tools for working with
    Agisoft documents
    """

    def __init__(self):
        self.doc = doc
        self.path = None
        self.is_saved = None
        self.chunks = doc.chunks

    def get_path(self):
        path = app.getSaveFileName("Save Project As") + ".psx"
        doc.save(path)
        print("Saved to path:  " + path)
        self.path = doc.path
        self.is_saved = True
        return

    def check_save(self):
        if doc.path is "" or None or False:
            self.is_saved = False
            print("File not saved")
            self.get_path()
            return
        else:
            print("File already Saved: {}".format(doc.path))
            self.path = doc.path
            self.is_saved = True
            return

    def process_all_chunks(self):
        print("\n\n\n")
        # Main project loop, iterate through all chunks + process them
        count = 0
        for chunk in self.chunks:
            try:
                agi = AgiChunk(chunk, self)
                if count > 0:
                    agi.reset_view()
                count += 1
                agi.run_process()
            except Exception:
                continue

        PhotoScan.app.messageBox("Script Complete! Hooray!!!")


class View:
    """Tools to manipulate agi viewpoints"""
    def __init__(self):
        self.doc = doc
        self.app = app
        self.view = PhotoScan.Viewpoint


def pt_dist(pt_a, pt_b):
    x = pt_b[0] - pt_a[0]
    y = pt_b[1] - pt_a[1]
    z = pt_b[2] - pt_a[2]
    distance = math.sqrt(x**2 + y**2 + z**2)
    return distance


def mid_pt(pt_a, pt_b):
    x = (pt_a[0] + pt_b[0]) / 2
    y = (pt_a[1] + pt_b[1]) / 2
    z = (pt_a[2] + pt_b[2]) / 2
    return [x, y, z]


def main():
    test = AgiDoc()
    test.check_save()
    test.process_all_chunks()


if __name__ == "__main__":
    main()
