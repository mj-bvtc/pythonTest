import tkinter
from tkinter import filedialog
import os
from shutil import copyfile
import datetime
import datetime
import socket
import getpass
import subprocess


class Common:
    def __init__(self):
        self.created_datetime = datetime.datetime.now()
        self.hostname = socket.gethostname()
        self.username = getpass.getuser()
        self.user_host = f"{self.username}@{self.hostname}"

    def copy(self):
        print("Copy Function: We are working on this...")


class Report(Common):
    def __init__(self, folder):
        super().__init__()
        self.path = None
        self.file = None
        self.folder = folder
        self.format_name()

    def format_name(self):
        dt = str(self.created_datetime).replace(":","_")
        self.path = os.path.join(self.folder,
                                 f"Agisoft Report {dt}.txt")

    def create(self):
        self.file = open(self.path, "w+")


def get_path(_title=None, default_dir=r"V:\Sample Data"):
    tkinter.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    path = filedialog.askdirectory(title=_title,
                                   initialdir=default_dir) # show an "Open" dialog box and return the path to the selected file
    msg = f"Found this path: {path}"
    print(msg)
    return path


def find_files(extensions, path):
    files = []
    dirs = set()

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            ext = filename.split(".")[-1]
            if ext in extensions:
                full_path = os.path.join(dirpath, filename)
                files.append(full_path)
                # print(f"Added {full_path} to list")
    return files


def copy_files(src, dst, files, report=None):
    for f in files:
        base = os.path.basename(f)
        folder = os.path.basename(os.path.dirname(f))
        new_folder = os.path.join(dst, folder)
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        d = os.path.join(new_folder, base)
        if not os.path.exists(d):
            copyfile(f, d)
            print(f"Copied file from {f} to {d}")
            report.file.write(f"Copied file from {f} to {d}\n")
        else:
            print(f"Skipped file {d}, already exists")
            report.file.write(f"Skipped file {d}, already exists\n")

    report.file.write(f"\nNumber of Files Compared: {len(files)}\n")


def main():

    try:
        src_dir = get_path("Select Folder to Copy From",
                           default_dir="S:")
        dst_dir = get_path("Select Folder to Copy To")
        rpt = Report(dst_dir)
        rpt.create()
        f = rpt.file
        f.write(str(rpt.created_datetime) + "\n")
        f.write(str(rpt.user_host) + "\n")
        f.write("\n")

        f.write(f"Copied From: {src_dir}\n")
        f.write(f"Copied To: {dst_dir}\n")

        extensions = ["3dm", "pdf"]
        f.write(f"Extensions: {extensions}\n")

        files = find_files(extensions, src_dir)

        copy_files(src_dir, dst_dir, files, rpt)

    finally:
        f.close()
        print(f"Closed file: {rpt.file}")
        #byte_file = str(rpt.file.name)
        #subprocess.check_call("attrib", "+H", byte_file)


if __name__ == "__main__":
    main()
