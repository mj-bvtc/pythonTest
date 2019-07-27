import pandas as pd
import re
import datetime
import os
from reportlab.pdfgen import canvas
import qrcode
import uuid
from natsort import natsorted, ns
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import random


# CLASSES
class Block():
    """A single piece of terracotta, with all of its attributes
    compiled in a data class"""

    def __init__(self):
        self.guid = None
        self.name = None
        self.point = None
        self.layer = None
        self.zones = None
        self.x = None
        self.y = None
        self.z = None
        self.floor = None
        self.swing_drop = None
        self.elevation = None
        self.priority = None
        self.phase = None


# SETTINGS
class Settings():
    """The general locations of files and
    values that can be modified"""
    # file = r"C:\Users\mkreidler\Desktop\Multisheet_export.xlsx"
    # save = r"C:\Users\mkreidler\Desktop\Block Grouping Scatter Plots.pdf"
    # ONLY USE reportlab version 3.5.20, later versions fail
    # pip install reportlab==3.5.20
    logo_path = r"C:\Users\mkreidler\Desktop\Test Setting Folder\BVTC-Logo-BLACK-horizontal.png"
    pdf_prefix = r"C:\Users\mkreidler\Desktop\Test Setting Folder\\"
    chart_save = r"C:\Users\mkreidler\Desktop\Test Setting Folder\Graphs_export.pdf"
    save_path = r"C:\Users\mkreidler\Desktop\Test Setting Folder\Multisheet_export.xlsx"
    folder = r"C:\Users\mkreidler\Desktop\Test Setting Folder\\"
    radius = 34


# Functions
def rand_color(x):
    """Takes some number and returns a random color"""
    random.seed(x)
    color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    color = '#%02x%02x%02x' % color
    return color


def my_round(x, base=10):
    """Takes some floating point number
        and rounds to closest base"""
    return base * round(x / base)


def nat_sort(x, df):
    """sort swingdrops alphanumerically the way a human reads numbers/letters"""
    unordered = df.swing_drop.tolist()
    reordered = natsorted(unordered, alg=ns.IGNORECASE)
    return reordered.index(x)


def find_floor(x):
    """Use re to search zone text for floor numbers"""
    pat = r"floor\s*(\d*)"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return int(result.group(1))


def find_phase(x):
    """Use re to search zone text for phase number, either Base or CO1, 2, 3...
    Generally we will be getting this from the layer structure in rhino"""
    if "BASE" in x.upper():
        return 0
    else:
        pat = r"CO\s*(\d*)"
        result = re.search(pat, str(x), flags=re.IGNORECASE)
        if result:
            return int(result.group(1))


def find_priority(x):
    """Use re to search zone text for priority"""
    pat = r"priority\s*(\d*)"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return int(result.group(1))


def find_elevation(x):
    """Use re to find elevation in zones"""
    pat = r"([a-zA-Z\s]*)\s*ELEVATION"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return result.group(1)


def get_drop(x):
    """Use re to find drop names in zones"""
    pat = r"drop\s*([a-z]*\d*)"
    match = re.search(pat, str(x), flags=re.IGNORECASE)

    if match:
        return match.group(1)
    else:
        return None


def get_access(x):
    """Use re to find access type in zones"""
    pat = r"access\s*([\w\s]*)"
    match = re.search(pat, str(x), flags=re.IGNORECASE)

    if match:
        return match.group(1)
    else:
        return "Boom Lift"


def get_survey(x):
    """Use re to find survey priority number in zones"""
    pat = r"Survey\s*([\d]*)"
    match = re.search(pat, str(x), flags=re.IGNORECASE)

    if match:
        return int(match.group(1))
    else:
        return 3


def find_qmark(x):
    """Use re to find question marks in zone text"""
    if "?" in x:
        return 1
    else:
        return 0


def format_path(folder, project_name="FCCH", ext=".xlsx"):
    """format path with prefix and timestamp"""
    timestamp = str(datetime.datetime.now()).replace(":", "_")
    path = f"{folder}Project {project_name} Report_{timestamp}.{ext}"
    return path


def sort_groups(x, group_order):
    """Sort groups in df based on an ordered list"""
    for i, g in enumerate(group_order):
        if g == x:
            return i + 1


def sort_drops(x, alphabetical=True):
    """Needs work.  Defaults to alphabetical sorting"""
    if alphabetical != True:
        drop_sort = {"W1": 1, "W2": 2, "W3": 3, "W4": 4, "W5": 5, "W6": 6, "S1": 7, "S2": 8, "S3": 9, "S4": 10}
        return drop_sort[x]
    else:
        pass


def start_dataframe(block_zones, block_guid, block_name, block_pt, block_layer):
    """Create the standard dataframe from rhino dots, rhino zones,
    and various attributes"""
    # make an empty list to populate with block objects
    blocks = []
    # connect gh wires to python block classes
    for i, z in enumerate(block_zones):
        b = Block()
        b.guid = block_guid[i]
        b.name = block_name[i]
        b.point = block_pt[i]
        b.layer = block_layer[i]
        b.phase = find_phase(b.layer)
        b.zones = z
        b.x = b.point[0]
        b.y = b.point[1]
        b.z = b.point[2]
        b.floor = find_floor(str(z))
        b.elevation = find_elevation(str(z))
        b.swing_drop = get_drop(str(z))
        b.priority = find_priority(str(z))
        b.access = get_access(str(z))
        b.survey = get_survey(str(z))

        # populate list of blocks
        blocks.append(b)

    # turn the above list to a pandas dataframe
    df = pd.DataFrame([vars(f) for f in blocks])

    # append a columns to df to track drop sort order
    df["drop_sort"] = df.swing_drop.apply(lambda x: nat_sort(x, df))

    # further specify dataframe sort order
    df = df.sort_values(["access", "survey", "elevation", "floor", "drop_sort", "y", "x"],
                        ascending=[False, True, True, False, True, False, True])
    df.reset_index(inplace=True, drop=True)
    df["new_order"] = df.index + 1

    # append columns
    df["instance"] = df.groupby("name").cumcount() + 1
    df["sample"] = 0
    df.loc[df.instance == 1, "sample"] = 1

    # create the survey name/bumper sticker name
    df["survey_name"] = df.swing_drop + "-" + df.floor.map(str) + "-" + df.name + "[" + df.new_order.map(str) + "]"
    # df["survey_name"] = f"{df.swing_drop}-{df.floor.map(str)-{df.name}[{df.new_order.map(str)}]}"
    return df


def make_groups(df, radius=34):
    """Use DBSCAN to find point clusters, add them to df"""
    # df = pd.read_excel(path, sheet_name="Main")
    coords = df[["x", "y"]]
    coords = np.array(coords)
    X = coords

    # perform DBSCAN grouping
    clustering = DBSCAN(eps=radius, min_samples=1).fit(X)

    # add column db to df
    df["db"] = clustering.labels_

    # get the number of groups in df
    size = len(df.groupby("db"))

    # Adjacency groups will be the same color, make new column
    df["color"] = df.db.apply(rand_color)

    # order groups
    ordered_groups_copies = df.db.tolist()
    group_order = []
    for g in ordered_groups_copies:
        if g in group_order:
            pass
        else:
            group_order.append(g)

    df["group_order"] = df["db"].apply(lambda x: sort_groups(x, group_order=group_order))
    return df


def make_summary(df, save_path):
    """Create a multi-page excel file summarizing
    standard data frame information"""
    # first survey blocks
    style_list = df.name.unique()

    # summary data
    num_styles = len(style_list)
    num_units = df.guid.count()
    num_floors = len(df.floor.unique())
    num_phases = len(df.phase.unique())
    num_priority = len(df.priority.unique())
    num_swings = len(df.swing_drop.unique())
    num_groups = len(df.db.unique())
    group_totals = df[["db", "guid"]].groupby("db").count()
    group_totals.reset_index(inplace=True)
    loners = len(group_totals.loc[group_totals.guid == 1, "db"].tolist())
    assemblies = len(group_totals.loc[group_totals.guid != 1, "db"].tolist())

    summary = {"Total_Styles": num_styles,
               "Total_Units": num_units,
               "Total_Floors": num_floors,
               "Total_Phases": num_phases,
               "Total_Priorities": num_priority,
               "Total_Drops": num_swings,
               "Total_Groups": num_groups,
               "Total_Loners": loners,
               "Total_Assemblies": assemblies}
    summary_df = pd.DataFrame(summary, index=[0])
    summary_df = summary_df.T

    # print(assemblies)
    # print(loners)
    # print(num_units)
    # print(list(df))

    # first groups
    # print(df[["group","group_order"]])
    # print(list(df))

    # reports
    floor_counts = df[["floor", "guid"]].groupby("floor").count()
    floor_counts.reset_index(inplace=True)
    # print(floor_counts)

    elevations = df[["elevation", "guid"]].groupby("elevation").count()
    elevations.reset_index(inplace=True)
    # (list(df))

    names = df[["name", "guid"]].groupby("name").count()
    names.reset_index(inplace=True)
    # print(names)

    priorities = df[["priority", "guid"]].groupby("priority").count()
    priorities.reset_index(inplace=True)
    # print(priorities)

    swing = df[["swing_drop", "guid"]].groupby("swing_drop").count()
    swing.reset_index(inplace=True)
    # print(swing)

    phase = df[["phase", "guid"]].groupby("phase").count()
    phase.reset_index(inplace=True)
    # print(phase)

    group_rpt = df[["db", "guid"]].groupby("db").count()
    group_rpt.reset_index(inplace=True)
    # print(group_rpt)

    group_odr = df[["name", "group_order", "guid"]].groupby(["group_order", "name"]).count()
    group_odr.reset_index(inplace=True)
    # print(group_odr)

    samples = df.loc[df.instance == 1, ["survey_name", "priority", "phase"]]
    # print(firsts)




    df["qmarks"] = df.name.apply(find_qmark)
    qmarks = df.loc[df.qmarks == 1, ["name", "guid"]]
    qmarks.reset_index(drop=True, inplace=True)
    qmarks = qmarks.groupby("name").count()

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(S.save_path, engine='xlsxwriter')

    # Write each dataframe to a different worksheet.

    summary_df.to_excel(writer, sheet_name='Summary')
    df.to_excel(writer, sheet_name='Main')
    floor_counts.to_excel(writer, sheet_name='Floors')
    names.to_excel(writer, sheet_name='Names')
    elevations.to_excel(writer, sheet_name='Elevations')
    priorities.to_excel(writer, sheet_name='Priorities')
    swing.to_excel(writer, sheet_name='Drops')
    phase.to_excel(writer, sheet_name='Phases')
    group_rpt.to_excel(writer, sheet_name='Groups')
    group_odr.to_excel(writer, sheet_name='Group Order')
    samples.to_excel(writer, sheet_name='Samples Trimmed')
    # first_styles_survey.to_excel(writer, sheet_name='Primary Styles Detail')
    qmarks.to_excel(writer, sheet_name="Question Marks")

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print("Summaries done!")
    # os.startfile(save_path)
    return df


def make_dataframe(block_zones, block_guid, block_name, block_pt, block_layer):
    df = start_dataframe(block_zones, block_guid, block_name, block_pt, block_layer)
    df = make_groups(df)
    df = make_summary(df, S.save_path)
    return df


def make_qr(df):
    """make pdf qr code sheet, 3 columns by 8 rows"""
    stuff = df.survey_name.tolist()
    df = pd.DataFrame({'stuff': stuff})
    df["num"] = df.index + 1
    df["c"] = df.num % 3
    df.c = df.c.replace(0, 3)
    df["page"] = ((df.num + 23) // 24)
    df["r"] = (((df.num - 1) // 3) + 1) % 8
    df.r = df.r.replace(0, 8)

    dt = str(datetime.datetime.now()).replace(":", "_")
    ext = ".pdf"
    pdf_path = f"{S.pdf_prefix}QR_codes{ext}"

    # MAKE CANVAS
    c = canvas.Canvas(pdf_path)
    c.setPageSize((612, 792))
    last_page = None

    # SPLIT INTO PAGES, COLUMNS, ROWS
    for index, row in df.iterrows():
        page = row["page"]
        if page != last_page:
            if last_page == None:
                last_page = page

            else:
                c.showPage()
                last_page = page

        col = row["c"]
        _row = row["r"]
        i = row["stuff"]
        code = f"{i}"

        # print(f"page {page} row {_row} column {col} info {i}")

        # DRAW QR
        def draw_qr(data, base=r"C:\Users\mkreidler\Desktop\pdf print barcodes\\"):
            # draw QR
            dt = str(datetime.datetime.now()).replace(":", "_")
            random = uuid.uuid4()
            img_path = f"{base}{dt}{random}.png"  ##can't write file paths with certain characters, removing 'i' variable here

            qr = qrcode.QRCode()
            qr.add_data(data)
            img = qr.make_image().save(img_path)
            return img_path

        # DRAW 1 TAG
        def draw_tag(x_num, y_num, code):
            flip_y = {1: 8,
                      2: 7,
                      3: 6,
                      4: 5,
                      5: 4,
                      6: 3,
                      7: 2,
                      8: 1}

            y_num = flip_y[y_num]

            qr = draw_qr(code)
            x_increment = 204
            y_increment = 99

            x = x_increment * (x_num - 1)
            y = y_increment * (y_num - 1)

            c.drawString(102.5491 + x, 33.7174 + y, code)
            c.drawInlineImage(qr, 0 + x, 0 + y, width=99, height=99)
            os.remove(qr)
            c.drawInlineImage(S.logo_path, 102.5491 + x, 71.2396 + y, width=84.2926,
                              height=14.0488)  # replace maroon with bnw later

        draw_tag(col, _row, code)

    # SAVE DOCUMENT
    c.save()
    print("QR codes done!")
    return pdf_path


def static_exports(df):
    """This needs work, static meaning grasshopper will always
    be displaying data values.  Need to arrange this in a way
    where calculations are minimal"""
    bumper = str(df["survey_name"].tolist())
    survey = df["new_order"].tolist()
    x = df["x"].tolist()
    y = df["y"].tolist()
    z = df["z"].tolist()
    sorted_guid = df["guid"].tolist()
    return bumper, x, y, z, survey, sorted_guid


def make_pdf_reports(df, path):
    """Use dataframe to create and save pdf reports using matplotlib"""
    with PdfPages(path) as pdf:
        # settings for the file
        base = 10  # threshold for grouping points
        page_size = (11, 8.5)
        point_size = 1.5  # scatter plot point size

        df["color"] = df.db.apply(rand_color)  # adjacency color
        df["fuzzy_y"] = df.y.apply(my_round)  # horizontal group color
        df["y_color"] = df.fuzzy_y.apply(rand_color)
        df["fuzzy_x"] = df.x.apply(my_round)  # vertical group color
        df["x_color"] = df.fuzzy_x.apply(rand_color)

        # Add title and axis names
        plt.figure(figsize=page_size)
        plt.title('Horizontal Grouping Scatter Plot')
        plt.xlabel('x distance')
        plt.ylabel('y distance')
        plt.scatter(df.x, df.y, c=df.y_color, s=point_size)
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

        plt.figure(figsize=page_size)
        plt.title('Vertical Grouping Scatter Plot')
        plt.xlabel('x distance')
        plt.ylabel('y distance')
        plt.scatter(df.x, df.y, c=df.x_color, s=point_size)
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

        plt.figure(figsize=page_size)
        plt.title('Block Adjacency Grouping Scatter Plot')
        plt.xlabel('x distance')
        plt.ylabel('y distance')
        plt.scatter(df.x, df.y, c=df.color, s=point_size)
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

        data1 = df[["floor", "swing_drop", "name"]]
        data = data1.groupby(["floor", "swing_drop"]).count()
        data = data.reset_index()
        data.head()
        data = data.fillna(0)
        pivot = data.pivot(index="floor", columns="swing_drop", values="name")
        pivot = pivot.fillna(0)
        order = sorted(df.floor.unique(), reverse=True)
        pivot = pivot.reindex(order)
        plt.figure(figsize=page_size)
        ax = sns.heatmap(pivot, cmap="BuPu")
        ax.set_title("Block Qty Heatmap")
        pdf.savefig()
        plt.close()

        # bar chart
        plt.rcParams.update({'font.size': 5})
        plt.figure(figsize=page_size)
        plt.title('Block Style Bar Graph')
        plt.xlabel('Names')
        plt.xticks(rotation=90)
        plt.ylabel('Quantities')
        dd = df[['name', "guid"]].groupby("name").count()
        dd = dd.reset_index()
        dd = dd.sort_values("guid")
        plt.bar(dd.name, dd.guid)
        # plt.show()
        pdf.savefig()
        plt.close()

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = 'Multipage PDF Example'
        d['Author'] = 'Matthew Kreidler'
        d['Subject'] = 'How to create a multipage pdf file and set its metadata'
        d['Keywords'] = 'PdfPages multipage keywords author title subject'
        d['CreationDate'] = datetime.datetime.today()
        d['ModDate'] = datetime.datetime.today()

    print("Graphs and Charts finished!")
    return path


def show_report(*args):
    """Open list of reports in the program the windows
    default program (excel, bluebeam, etc...)"""
    for report in args:
        os.startfile(report)


def main():
    start = datetime.datetime.now()
    print("Working...")
    df = make_dataframe(block_zones, block_guid, block_name, block_pt, block_layer)
    make_qr(df)
    make_pdf_reports(df, S.chart_save)

    stop = datetime.datetime.now()
    duration = stop - start
    print(f"Duration {duration}")


S = Settings()
if run == True:
    main()



