import PhotoScan


doc = PhotoScan.app.document

# Save current file if not saved yet
doc.open("project.psz")

# loop through all chunks in file
for chunk in doc.chunks:
    pre_process(chunk)


def pre_process(chunk):
    chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy,
                      generic_preselection=True,
                      reference_preselection=False)
    chunk.alignCameras()

# Pause here --- I want hand point selection
# crop sparse point cloud
# check points
# gradual selection

chunk.buildDepthMaps(quality=PhotoScan.MediumQuality,
                     filter=PhotoScan.AggressiveFiltering)
chunk.buildDenseCloud()
chunk.buildModel(surface=PhotoScan.Arbitrary,
                 interpolation=PhotoScan.EnabledInterpolation)
chunk.buildUV(mapping=PhotoScan.GenericMapping)
chunk.buildTexture(blending=PhotoScan.MosaicBlending,
                   size=4096)

# save document out
doc.save()
