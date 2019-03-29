import os
import pandas as pd
import datetime
import uuid
from PIL import Image
import tkinter
from tkinter import filedialog


def get_path(_title=None, default_dir=r"V:\Sample Data"):
    """
    brings up a dialog to search for directory
    """
    tkinter.Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    path = filedialog.askdirectory(title=_title,
                                   initialdir=default_dir)  # show an "Open" dialog box and return the path to the selected file
    msg = f"Found this path: {path}"
    print(msg)
    return path


def get_pics(path):
    """
    finds any .jpg in a given directory and returns a list of pics
    """
    pics = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.upper().endswith("JPG"):
                full = os.path.join(root, name)
                pics.append(full)
    print(f"Found {len(pics)} photos")
    return pics


def get_date_taken(path):
    """gets the date a photo was taken"""
    return Image.open(path)._getexif()[36867]


def get_filename(path):
    # check if path exists
    if not os.path.exists(path):
        print(f"Path does not exist: {path}")
        return None

    first = os.path.splitext(path)[0]
    result = os.path.basename(first)
    print(result)
    return result


def create_report(path):
    """
    after looking through the names of log photos,
    a framework is created in pandas.  A pandas
    data frame is created to correlate pictures to
    date taken, flags present, what project you are looking at,
    the Crate/Pallet/Unit you are looking at etc.
    """
    pics = get_pics(path)
    print("Setting up dataframe")
    df = pd.DataFrame(pics)
    df.columns = ["path"]

    base = [get_filename(x) for x in pics]
    dt = [get_date_taken(x) for x in pics]
    qr = [str(uuid.uuid4()) for x in pics]
    df["pic"] = base
    df["datetime"] = dt
    df["tbr"] = None
    df["color_sample"] = None
    df["broken"] = None
    df["group"] = None
    df["qr"] = qr
    df["project"] = None
    df["crate"] = None
    df["unit"] = None
    df["pallet"] = None

    df = df.sort_values(by="datetime")
    df = df.reset_index(drop=True)
    df["flags"] = df['pic'].apply(find_flags)
    df["crate"] = assign_labels("Crate", df["flags"])
    df["project"] = assign_labels("Project", df["flags"])
    df["pallet"] = assign_labels("Pallet", df["flags"])
    data = df[["pic", "flags", "unit"]]

    df["unit"] = data["pic"][data["flags"].isnull()]

    # TODO add checklist for tbr, color sample, broken piece

    return df


def find_flags(search):
    """searches for flags in list, returns results"""
    flags = ["Crate",
             "Pallet",
             "Broken",
             "Project",
             "Color"]
    for flag in flags:
        if flag.upper() in search.upper():
            return search


def assign_labels(flag, series):
    """labels cells of given column if necessary column contains proper flag"""
    label = None
    result = []
    search = series.tolist()
    for s in search:
        # print(f"flag: {flag}, search: {s}")
        try:
            if flag.upper() in s.upper():
                a = s.upper().replace(".JPG", "")
                b = a.upper().replace(flag.upper(), "")
                label = f"{b.title()}"
            result.append(label)

        except:
            result.append(label)
            continue
    return result


def format_file(folder):
    ext = ".xlsx"
    timestamp = str(datetime.datetime.now()).replace(":", "_")
    excel = timestamp + ext
    result = os.path.join(folder, "Sample_Report_" + excel)
    print(f"Formatted report: {result}")
    return result


def create_excel(path, df):
    writer = pd.ExcelWriter(path)
    df.to_excel(writer, 'Sheet1')
    writer.save()
    print(f"Created excel report: {path}")


def run():
    print("Selecting folder...")
    prompt = "Select the folder which contains log photos:"
    path = get_path(_title=prompt)
    # path = r"V:\Sample Data\Chatsworth Apartments\log photos"
    print("Creating report...")
    report = create_report(path)
    print("Formatting report...")
    report_path = format_file(path)
    print("Saving Excel Spreadsheet...")
    create_excel(report_path, report)
    print("Report: ")
    print(report)


def main():
    run()


if __name__ == "__main__":
    main()
