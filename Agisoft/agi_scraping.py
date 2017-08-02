import PhotoScan
import os
import math
import itertools
import time
import datetime
from functools import wraps

doc = PhotoScan.app.document
app = PhotoScan.app


chunk = doc.chunks[0]


class Duration:
    def __init__(self, chunk):
        self.chunk = chunk

    @property
    def name(self):
        return self.chunk.label

    @property
    def align(self):
        for k, v in self.chunk.meta.items():
            if k == 'align/duration':
                return v

    @property
    def dense(self):
        for k, v in self.chunk.dense_cloud.meta.items():
            if k == 'dense_cloud/duration':
                return v


d = Duration(chunk)
print(d.dense)
print(d.align)

dense = chunk.dense_cloud.meta["dense_cloud/duration"]
print(dense)
print(d.name)




