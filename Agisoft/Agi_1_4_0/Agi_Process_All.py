import PhotoScan


doc = PhotoScan.app.document


def process(chunk):
    chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy,
                      generic_preselectio=True,
                      reference_preselection=False)

    chunk.alignCameras()


def align_all():
    for chunk in doc.chunks:
        process(chunk)


def main():
    align_all()
