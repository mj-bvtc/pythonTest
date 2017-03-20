import PhotoScan
import os
import math
import itertools

doc = PhotoScan.app.document

def isTextured(_CurrentChunk):

    #if not hasattr(_CurrentChunk.model, 'meta'):
       # print("This chunk does not have a texture:  " + _CurrentChunk.label)
        #return False
    try:
        print(_CurrentChunk.model.meta['atlas/atlas_blend_mode'])
        print("This chunk already has a texture:  " + _CurrentChunk.label)
        return True

    except AttributeError:
        print("This chunk does not have a texture:  " + _CurrentChunk.label)
        return False
    '''
    if _CurrentChunk.model.meta['atlas/atlas_blend_mode']:
        print("This chunk already has a texture:  " + _CurrentChunk.label)
        return True
    else:
        print("This chunk does not have a texture:  " + _CurrentChunk.label)
        return False
    '''

def main():
    for _CurrentChunk in doc.chunks:
        isTextured(_CurrentChunk)

if __name__ == "__main__":
    main()














