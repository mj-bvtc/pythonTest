import os
import math
import itertools
import time
import datetime
from functools import wraps


def timer(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        print("instance {} of class {} is decorated".format(self, self.__class__))
        print("entering...")
        print("running process...")
        start = time.time()
        result = fn(self, *args, **kwargs)
        end = time.time()
        print("exiting...")
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
        self.log_path = r"C:\Users\mkreidler\Desktop\test_logs"
        self.log_list = []
        self.indent = "\t" * 5

    def create_log(self):
        # writes log file in folder with each chunk
        name = r"\log_test"
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        ext = ".txt"
        full_path = self.log_path + name + timestamp + ext
        report = open(full_path, "w")
        report.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        for log in self.log_list:
            report.write(log)
        report.close()
        print("Created log file: {}\n".format(full_path))
        return

    @timer
    def run_process(self):
        for i in range(10):
            i * 300
        self.slow(2)
        return


    @timer
    def slow(self, sec):
        time.sleep(sec)
        return

    def run_all(self):
        self.run_process()
        self.create_log()


class AgiDoc:
    """
    Tools for working with
    Agisoft documents
    """

    def __init__(self):
        self.path = None
        self.is_saved = None
        self.chunks = [1,2,3]

    def get_path(self):
        path = app.getSaveFileName("Save Project As") + ".psx"
        doc.save(path)
        print("Saved to path:  " + path)
        self.path = doc.path
        self.is_saved = True
        return

    def check_save(self):
        return True

    def process_all_chunks(self):

        for chunk in self.chunks:
            agi = AgiChunk(chunk, self)
            agi.run_all()


def main():
    test = AgiDoc()
    test.check_save()
    test.process_all_chunks()


    #@timer
   # def slow(sec):
    #    print("Function executing")
    #    time.sleep(sec)

   # slow(1)


if __name__ == "__main__":
    main()
