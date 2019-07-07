import pandas as pd
import re
import datetime
import os
from reportlab.pdfgen import canvas
import qrcode
import uuid
from natsort import natsorted, ns

class Block():
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

class Group():
    def __init__(self):
        self.group = None
        self.guid = None     

def find_floor(x):
    pat = r"floor\s*(\d*)"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return int(result.group(1))    

def find_phase(x):
    if "BASE" in x.upper():
        return 0
    else:
        pat = r"CO\s*(\d*)"
        result = re.search(pat, str(x), flags=re.IGNORECASE)
        if result:
            return int(result.group(1)) 

def find_priority(x):
    pat = r"priority\s*(\d*)"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return int(result.group(1))   

def find_elevation(x):
    pat = r"([a-zA-Z\s]*)\s*ELEVATION"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return result.group(1)

def get_drop(x):
    pat = r"drop\s*([a-z]*\d*)"
    match = re.search(pat, str(x), flags=re.IGNORECASE)

    if match:
        return match.group(1)
    else:
        return None



def sort_drops(x, alphabetical = True):
    if alphabetical != True:
        drop_sort = {   "W1":1,"W2":2,"W3":3, "W4":4, "W5":5, "W6":6, "S1":7, "S2":8, "S3":9, "S4":10}
        return drop_sort[x]
    else:
        pass
    

def make_barcodes(path):

    data = pd.read_excel(path)
    stuff = data.survey_name.tolist()
    df = pd.DataFrame({'stuff': stuff})
    df["num"] = df.index + 1
    df["c"] = df.num % 3
    df.c = df.c.replace(0, 3)
    df["page"] = ((df.num + 23) // 24)
    df["r"] = (((df.num - 1) // 3) + 1) % 8
    df.r = df.r.replace(0, 8)

    # FILE LOCATIONS
    logo_path = r"C:\Users\mkreidler\Desktop\pdf print barcodes\BVTC-Logo-BLACK-horizontal.png"
    pdf_suffix = r"C:\Users\mkreidler\Desktop\pdf print barcodes\\" ##actually this is a prefix
    dt = str(datetime.datetime.now()).replace(":", "_")
    ext = ".pdf"
    pdf_path = f"{pdf_suffix}{dt}{ext}"

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
        print(f"page {page} row {_row} column {col} info {i}")

        # DRAW QR
        def draw_qr(data, base=r"C:\Users\mkreidler\Desktop\pdf print barcodes\\"):
            # draw QR
            dt = str(datetime.datetime.now()).replace(":", "_")
            random = uuid.uuid4()
            img_path = f"{base}{dt}{random}.png" ##can't write file paths with certain characters, removing 'i' variable here

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
            c.drawInlineImage(logo_path, 102.5491 + x, 71.2396 + y, width=84.2926,
                              height=14.0488)  # replace maroon with bnw later


        draw_tag(col, _row, code)
    

    # SAVE DOCUMENT
    c.save()
    print()
    print("Done!")
    return pdf_path




#############################


def make_dataframe():
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

# populate list of blocks
        blocks.append(b)

# turn the above list to a pandas dataframe
    df = pd.DataFrame([vars(f) for f in blocks])

# make an empty list to populate groups
    groups = []

# connect groups classes to rhino ids
    for i, g in enumerate(group):
        gr = Group()
        gr.group = g
        gr.guid = id[i]
        groups.append(gr)

# make a separate dataframe with groups
    group_df = pd.DataFrame([vars(f) for f in groups])

# merge main dataframe with groups
    merge = df.merge(group_df, on="guid", how="outer")

# sort swingdrops alphanumerically the way a human reads numbers/letters
    def nat_sort(x):
        unordered = merge.swing_drop.tolist()
        reordered = natsorted(unordered,alg=ns.IGNORECASE)
        return reordered.index(x)

# append a columns to df to track drop sort order
    merge["drop_sort"] = merge.swing_drop.apply(nat_sort)

# further specify dataframe sort order
    merge = merge.sort_values(["elevation", "drop_sort", "floor", "z","x"], ascending=[True, True, False,False,True])
    merge.reset_index(inplace = True, drop=True )
    merge["new_order"] = merge.index + 1

# append columns 
    merge["instance"] = merge.groupby("name").cumcount() + 1

    # order groups
    ordered_groups_copies = merge.group.tolist()
    group_order = []
    for g in ordered_groups_copies:
        if g in group_order:
            pass
        else:
            group_order.append(g)
    def sort_groups(x):
        for i,g in enumerate(group_order):
            if g == x:
                return i + 1
    merge["group_order"] = merge["group"].apply(sort_groups)

# create the survey name/bumper sticker name
    merge["survey_name"] = merge.swing_drop +"-"+ merge.floor.map(str) +"-"+ merge.name + "[" +merge.new_order.map(str) +"]"
    return merge




def static_exports():
    merge = make_dataframe()
    bumper = str(merge["survey_name"].tolist())
    survey = merge["new_order"].tolist()
    x = merge["x"].tolist()
    y = merge["y"].tolist()
    z = merge["z"].tolist()
    sorted_guid = merge["guid"].tolist()

    return bumper, x,y,z,survey, sorted_guid
    
########################################





folder = r"V:\Field Survey\Moynihan Station Phase II\Moynihan Phase II CO17 + CO19\Deliverables\Setting Reports\\"
path = folder + "ProjectReport_" + str(datetime.datetime.now()).replace(":","_") + ".xlsx"

if show_barcodes == True:
    make_dataframe()
    barcodes = make_barcodes(path)
    os.startfile(barcodes)

if open_report == True:
    df = make_dataframe()
    df.to_excel(path)
    os.startfile(path) # open report after pressing button

if report == True:
    make_dataframe() # make report, do not open

if show_bc_rpt == True:
    df = make_dataframe()
    df.to_excel(path)
    os.startfile(path)
    barcodes = make_barcodes(path)
    os.startfile(barcodes)

if show_static == True:
    merge = make_dataframe()
    bumper = str(merge["survey_name"].tolist())
    survey_num = merge["new_order"].tolist()
    x = merge["x"].tolist()
    y = merge["y"].tolist()
    z = merge["z"].tolist()
    sorted_guid = merge["guid"].tolist()

# first survey blocks
df = make_dataframe()
first_styles_survey = df[df.instance == 1]
style_list = df.name.unique()

# summary data
num_styles = len(style_list)
num_units = df.guid.count()
num_floors = len(df.floor.unique())
num_phases = len(df.phase.unique())
num_priority = len(df.priority.unique())
num_swings = len(df.swing_drop.unique())
num_groups = len(df.group.unique())
group_totals = df[["group","guid"]].groupby("group").count()
group_totals.reset_index(inplace=True)
loners = len(group_totals.loc[group_totals.guid == 1, "group"].tolist())
assemblies = len(group_totals.loc[group_totals.guid != 1, "group"].tolist())


summary = { "Total_Styles":num_styles,
            "Total_Units":num_units,
            "Total_Floors":num_floors,
            "Total_Phases":num_phases,
            "Total_Priorities":num_priority,
            "Total_Drops":num_swings,
            "Total_Groups":num_groups,
            "Total_Loners":loners,
            "Total_Assemblies":assemblies}
summary_df = pd.DataFrame(summary, index=[0])
summary_df = summary_df.T

#print(assemblies)
#print(loners)
#print(num_units)
#print(list(df))

# first groups
#print(df[["group","group_order"]])
#print(list(df))

#reports
floor_counts = df[["floor","guid"]].groupby("floor").count()
floor_counts.reset_index(inplace=True)
#print(floor_counts)

elevations = df[["elevation","guid"]].groupby("elevation").count()
elevations.reset_index(inplace=True)
print(list(df))

names = df[["name","guid"]].groupby("name").count()
names.reset_index(inplace=True)
#print(names)

priorities = df[["priority","guid"]].groupby("priority").count()
priorities.reset_index(inplace=True)
#print(priorities)

swing = df[["swing_drop","guid"]].groupby("swing_drop").count()
swing.reset_index(inplace=True)
#print(swing)

phase = df[["phase","guid"]].groupby("phase").count()
phase.reset_index(inplace=True)
#print(phase)

group_rpt = df[["group","guid"]].groupby("group").count()
group_rpt.reset_index(inplace=True)
#print(group_rpt)

group_odr = df[["name","group_order","guid"]].groupby(["group_order","name"]).count()
group_odr.reset_index(inplace=True)
#print(group_odr)

firsts = df.loc[df.instance == 1,["survey_name", "priority", "phase" ]]
#print(firsts)


##########################

save_path = r"C:\Users\mkreidler\Desktop\35wacker_multisheet.xlsx"

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(save_path, engine='xlsxwriter')

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
firsts.to_excel(writer, sheet_name='Primary Styles Trimmed')
first_styles_survey.to_excel(writer, sheet_name='Primary Styles Detail')

# Close the Pandas Excel writer and output the Excel file.
writer.save()


##########################

print("Complete")




