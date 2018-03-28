import os
import collections
import HiddenFiles
import datetime
import tkinter as tk
from tkinter.filedialog import askdirectory


def rhino_report(target):
    """
    Walks through provided target path and reports
    on the quantities of different file types

    parameter: target

    returns: None
    """

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report_name = "RhinoReport_" + timestamp + ".txt"
    report_path = os.path.join(target, report_name)
    report = open(report_path, "w")
    report.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    dir_count = 0
    found_rhino = 0
    found_obj = 0
    count_global = collections.Counter()  # built-in counting object, used globally
    print(f"Report for path: {target}\n", file=report)

    # walk the tree of the specified target path
    for root, dirs, files in os.walk(target):

        # remove hidden files, .psx extensions, and directories that end in .files
        files[:] = [f for f in files if not (HiddenFiles.is_hidden(os.path.join(root, f)))]
        files[:] = [f for f in files if not (f.endswith(".psx") or
                    f.endswith(".3dmbak") or f.endswith(".txt"))]
        dirs[:] = [d for d in dirs if not d.endswith(".files")]

        # only concerned with areas that contain files

        if files:
            dir_count += 1
            count = collections.Counter()   # instantiate local counter
            new_root = root.replace(target+"\\", "")
            print(f"{new_root} contains: ", file=report)

            # search and count file extensions
            for file in files:
                name, ext = os.path.splitext(file)
                if ext.upper() == ".3DM":
                    found_rhino += 1
                if ext.upper() == ".OBJ":
                    found_obj += 1
                count[ext] += 1         # increment local count
                count_global[ext] += 1  # increment global count
                # print(file)            # if interested, uncomment this to see files
            print(count, file=report)

        print("\n", file=report)                     # create a visual space between directories

    # print summary to report, .txt
    print("\n***\n", file=report)
    print("Global counts: ", file=report)
    print(count_global, file=report)
    missing_rhino = dir_count - found_rhino
    missing_obj = dir_count - found_obj
    print(f"\n\nSummary:\nNumber of Directories: {dir_count}\n"
          f"Number of missing Rhino files: {missing_rhino}"
          f"\nNumber of missing OBJ files: {missing_obj}", file=report)

    # print the following to console
    print(f"Searching this directory {target}")
    print(f"\n\nSummary:\nNumber of Directories: {dir_count}\n"
          f"Number of missing Rhino files: {missing_rhino}"
          f"\nNumber of missing OBJ files: {missing_obj}")
    report.close()


def main():
    dial = tk.Tk()
    dial.withdraw()
    target = askdirectory()
    rhino_report(target)


if __name__ == "__main__":
    main()