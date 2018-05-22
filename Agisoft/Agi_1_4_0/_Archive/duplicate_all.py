import PhotoScan
import os

doc = PhotoScan.app.document


def get_save():
    path = PhotoScan.app.getSaveFileName("Save project as")
    try:
        doc.save(path)

    except RuntimeError:
        PhotoScan.app.messageBox("Can't Save Project")


def check_save():
    if doc.path is not "":
        print("save exists")
    else:
        print("no save file")
        get_save()


def align(chunk):
    chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy,
                      generic_preselection=True,
                      reference_preselection=False,
                      keypoint_limit=55000,
                      tiepoint_limit=5000
                      )
    chunk.alignCameras()


def align_all():
    for chunk in doc.chunks:
        align(chunk)
    doc.save()


def duplicate(chunk):
    name = chunk.label
    new = chunk.copy()
    new.label = "{}_3D-PDF".format(name)


def duplicate_all(export=True):
    for chunk in doc.chunks:

        # Max
        name = chunk.label
        #chunk.label = "{}_8-Mill".format(name)
        #chunk.decimateModel(8000000)

        # Rhino
        rhino = chunk.copy()
        rhino.label = "{}_Rhino".format(name)
        rhino.decimateModel(1500000)
        rhino.buildUV(mapping=PhotoScan.GenericMapping)
        rhino.buildTexture(blending=PhotoScan.MosaicBlending,
                           size=4096)
        if export is True:
            ext = ".obj"
            file = format_file(ext, rhino)
            rhino.exportModel(file)

        # PDF
        pdf = chunk.copy()
        pdf.label = "{}_3D-PDF".format(name)
        pdf.decimateModel(100000)
        pdf.buildUV(mapping=PhotoScan.GenericMapping)
        pdf.buildTexture(blending=PhotoScan.MosaicBlending,
                         size=4096)
        if export is True:
            ext = ".pdf"
            file = format_file(ext, pdf)
            pdf.exportModel(file)
        doc.save()


def process(chunk):
    chunk.buildDepthMaps(quality=PhotoScan.MediumQuality,
                         filter=PhotoScan.AggressiveFiltering)
    chunk.buildDenseCloud()
    chunk.buildModel(surface=PhotoScan.Arbitrary,
                     interpolation=PhotoScan.EnabledInterpolation,
                     face_count=0)
    #chunk.buildUV(mapping=PhotoScan.GenericMapping)
    #chunk.buildTexture(blending=PhotoScan.MosaicBlending,
                       #size=4096)
    doc.save()


def process_all():
    for chunk in doc.chunks:
        process(chunk)


def decimate_pdf(chunk):
    chunk.decimateModel(100000)


def get_folder(chunk):
    pic = chunk.cameras[0].photo.path
    path = os.path.dirname(pic)
    return path


def format_file(ext, chunk):
    path = get_folder(chunk)
    file = "{}/{}{}".format(path, chunk.label, ext)
    return file


def main():
    #check_save()
    #align_all()
    #process_all()
    duplicate_all()


if __name__ == "__main__":
    main()
