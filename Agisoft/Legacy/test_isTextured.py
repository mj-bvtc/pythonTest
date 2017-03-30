import PhotoScan
import os
import math
import itertools

doc = PhotoScan.app.document

def isTextured(_CurrentChunk):


    try:
        texture = _CurrentChunk.model.meta['atlas/atlas_blend_mode']
        if texture is None:
            print("This chunk does not have a texture:  " + _CurrentChunk.label)
            return False

        else:
            print("This chunk already has a texture:  " + _CurrentChunk.label)
            return True

    except AttributeError:
        print("This chunk does not have a texture:  " + _CurrentChunk.label)
        return False

def main():
    for _CurrentChunk in doc.chunks:
        isTextured(_CurrentChunk)

if __name__ == "__main__":
    main()














