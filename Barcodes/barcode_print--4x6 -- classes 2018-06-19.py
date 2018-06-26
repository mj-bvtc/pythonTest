from reportlab.pdfgen import canvas
import os
import qrcode
import uuid
import win32api
import win32print
import datetime
import socket
import getpass
import time
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfile
import pandas as pd


class Common:
    def __init__(self):
        self.datetime_created = datetime.datetime.now()
        self.id = uuid.uuid4()
        self.hostname = socket.gethostname()
        self.username = getpass.getuser()

    @property
    def user_at_host(self):
        return f"{self.username}@{self.hostname}"


class Barcode(Common):
    """
    BVTC QR code sticker for Sample/Survey

    -mjk
    """

    def __init__(self):
        super().__init__()
        self.project_name = None
        self.project_number = None                      # required
        self.dt_received = None
        self.dt_printed = datetime.datetime.now()
        self.location = None
        self.quantity = None
        self.instance = None
        self.crate = None
        self.pallet = None
        self.block_style = None
        self.style_instance = None
        self.orientation = None
        self.notes = None
        self.sample_id = None
        self.color_sample = None
        self.logged_in = None
        self.to_be_returned = None
        self.scanned_in = None
        self.block_id = None
        self.pdf_path = None
        self.folder = None
        self.qr = None
        self.img_path = None
        self.path_base = None
        self.df = None
        self.estimating_block_id = None
        self.estimating_description = None
        self.number_shop_dwg = None
        self.forming_method = None
        self.quote = None

    def get_folder(self):
        dial = tk.Tk()
        dial.withdraw()
        target = askdirectory()
        self.folder = target
        print(f"Chose folder: {target}")
        return target

    def format_path(self):
        pass

    def get_sample_name(self):
        name = input("Type in sample name:  ")
        self.sample_id = name
        print(f"Sample id set to : {self.sample_id}")

    @staticmethod
    def create_id():
        code = uuid.uuid4()
        return

    def get_data(self):
        pass

    def draw_qr(self):
        # draw QR
        qr = qrcode.QRCode()
        pnum = self.project_number
        code = self.id
        pnum_code = f"{pnum}_{code}"
        self.path_base = os.path.join(self.folder, pnum_code)
        qr_data = pnum_code
        self.img_path = os.path.join(self.folder, qr_data) + ".jpg"
        qr.add_data(qr_data)
        img = qr.make_image().save(self.img_path)
        self.qr = img
        print(f"Created QR image here: {self.img_path}")

    def build_sticker(self):
        # format names
        pdf_path = self.path_base + ".pdf"
        print(f"pdf_path: {pdf_path}")
        img_path = self.img_path

        # draw pdf
        dt = datetime.datetime.now()
        c = canvas.Canvas(pdf_path)

        c.setFont("Helvetica-Bold", 9)

        c.setPageSize((576, 384))  # 4x6 in pixels

        # ----make labels----

        # project: ***THIS NEEDS TO BE PROGRAMMED
        project = self.project_name
        p_num = self.project_number
        proj = f"{p_num},  {project}"
        c.drawString(33, 282, "PROJECT:")
        c.setFont("Helvetica", 9)
        c.drawString(33, 268, proj)

        # date received: ****this needs to be input somehow
        c.setFont("Helvetica-Bold", 9)
        c.drawString(33, 246, "DATE RECEIVED:")
        c.setFont("Helvetica", 9)
        c.drawString(33, 232, str(self.dt_received))

        # date printed:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(33, 209, "DATE PRINTED:")
        c.setFont("Helvetica", 9)
        c.drawString(33, 198, str(self.datetime_created))

        # guid:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(33, 174, "GUID:")
        c.setFont("Helvetica", 9)
        c.drawString(33, 162, str(self.id))

        # LOCATION: ***PROGRAM THIS
        c.setFont("Helvetica-Bold", 9)
        c.drawString(33, 140, "LOCATION:")
        c.setFont("Helvetica", 9)
        # c.drawString(33, 128, "E25-14A-BK49R-COLOR")
        c.drawString(33, 128, self.location)

        # Sample ID: ***PROGRAM THIS
        c.setFont("Helvetica-Bold", 9)
        c.drawString(215, 140, "SAMPLE ID:")
        c.setFont("Helvetica", 9)
        c.drawString(215, 128, str(self.sample_id))

        # quantity
        c.setFont("Helvetica-Bold", 9)
        c.drawString(33, 107, "QUANTITY:")
        c.setFont("Helvetica", 9)
        c.drawString(33, 95, str(self.quantity))

        # NUMBERS
        c.setFont("Helvetica-Bold", 9)
        c.drawString(96, 107, "INSTANCE:")
        c.drawString(160, 107, "CRATE:")
        c.drawString(215, 107, "PALLET:")
        c.setFont("Helvetica", 9)
        c.drawString(96, 95, str(self.instance))
        c.drawString(160, 95, str(self.crate))
        c.drawString(215, 95, str(self.pallet))

        # BLOCK ID ***HAND INPUT
        c.setFont("Helvetica-Bold", 9)
        c.drawString(33, 75, "BLOCK ID:")

        c.setFont("Helvetica", 40)
        c.drawString(31, 37, str(self.block_id))

        # -------drawing---------
        # draw the QR code
        c.drawInlineImage(img_path, 300, 7, width=274, height=281)

        # draw the logo
        c.drawInlineImage(r"C:\Users\mkreidler\Desktop\BVTC-Logo-BLACK-horizontal.jpg",
                          285, 300, width=274, height=66)

        # rectangles
        from reportlab.lib.units import inch
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(33, 332, .105 * inch, .105 * inch, stroke=1, fill=0)
        c.rect(185, 332, .105 * inch, .105 * inch, stroke=1, fill=0)
        c.rect(33, 310, .105 * inch, .105 * inch, stroke=1, fill=0)
        c.rect(185, 310, .105 * inch, .105 * inch, stroke=1, fill=0)
        c.rect(185, 288, .105 * inch, .105 * inch, stroke=1, fill=0)  # DIGITAL SCULPTURE CHECKBOX
        c.setFont("Helvetica", 9.7)
        c.drawString(44, 332.213, "LOGGED IN")
        c.drawString(196, 332.213, "SCANNED")
        c.drawString(44, 310, "TO BE RETURNED")
        c.drawString(196, 310, "COLOR SAMPLE")
        c.drawString(196, 288, "DIGITAL SCULPTURE")
        c.save()

        # delete .jpeg
        os.remove(img_path)

        print(f"Built sticker here: {pdf_path}")
        self.pdf_path = pdf_path
        return pdf_path

    def print_sticker(self):

        win32api.ShellExecute(
            0,
            "print",
            self.pdf_path,
            #
            # If this is None, the default printer will
            # be used anyway.
            #
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0
        )
        print(f"Printed pdf_path: {self.pdf_path}")

    def print_sticker_list(self, sticker_list):
        pass


class Quote(Common):
    def __init__(self):
        super().__init__()
        self.path = None
        self.quote = None
        self.blocks = []
        self.barcodes = []
        self.quote_to_pandas()
        self.report_path = None
        self.report_data = None

    def quote_to_pandas(self, path=r"C:\Users\mkreidler\Desktop\Shell_House.xlsx"):
        df = pd.read_excel(path)
        df = df[["Block ID", "Description", "No. of Shop Dwgs.", "Form Method", "Qty of Units"]]
        df.rename(columns={"Block ID": "estimating_id",
                           "Description": "block_description",
                           "No. of Shop Dwgs.": "number_shops",
                           "Form Method": "form_method",
                           "Qty of Units": "block_quantity"}, inplace=True)

        # recreate df to contain only rows without section totals
        df = df[df.block_description.str.strip() != "Section Totals"]
        self.quote = df
        return df

    def make_barcodes(self):
        for i in range(len(self.quote)):
            b = Barcode()
            row = self.quote.iloc[[i]]
            b.estimating_description = row.block_description.values[0]
            b.quantity = row.block_quantity.values[0]
            b.block_id = row.estimating_id.values[0]                    # this should be b.estimating id
            b.forming_method = row.form_method.values[0]
            b.number_shop_dwg = row.number_shops.values[0]

            self.barcodes.append(b)

    def create_block_report(self):
        df = pd.DataFrame([vars(x) for x in self.barcodes])
        return df

    def save_block_report(self):
        dial = tk.Tk()
        dial.withdraw()
        target = asksaveasfile(defaultextension=".xlsx")

        if target.name is None:
            return
        df = pd.DataFrame([vars(x) for x in self.barcodes])

        df.to_excel(target.name)
        self.report_path = target.name
        self.report_data = df
        print(f"Saved barcode report here: {target.name}")

    def print_beginning(self, num, _print=False):
        for i in range(num):
            bc = self.barcodes[i]

            bc.project_number = "P12-3456"
            bc.location = "-----"
            bc.dt_received = datetime.datetime(2018, 3, 12)
            bc.project_name = "451 Broome"
            bc.color_sample = True

            bc.folder = r"C:\Users\mkreidler\Desktop\test"

            bc.draw_qr()

            bc.build_sticker()

            if print is not False:
                bc.print_sticker()
                time.sleep(5)

    def print_all(self):
        num = len(self.barcodes)
        self.print_beginning(num)


def test_barcode():
    # instantiate barcode class
    bc = Barcode()
    dd = Barcode()
    group = [bc, dd]

    # input data values
    bc.project_number = "P12-3456"
    bc.quantity = 12
    bc.location = "E14-5-H12R"
    bc.dt_received = datetime.datetime(2018, 3, 12)
    bc.project_name = "451 Broome"
    bc.color_sample = True

    # choose a folder to save in
    # bc.get_folder()                                               # this is a dialog box based folder search
    bc.folder = r"C:\Users\mkreidler\Desktop\New pdf exports"       # hard coded in for convenience

    # get sample id from user
    # bc.get_sample_name()                                          # user input
    bc.sample_id = str(123)                                              # hard coded in for convenience

    # draw QR
    bc.draw_qr()

    # build sticker
    bc.build_sticker()

    # physically print sticker
    # bc.print_sticker()

    # record data in database/spreadsheet
    df = pd.DataFrame([vars(f) for f in group])
    timestamp = str(datetime.datetime.now()).replace(":", "_")
    name = f"Report_{timestamp}.csv"

    root = r"C:\Users\mkreidler\Desktop\test"
    rpt = f"{root}\\{name}"
    df.to_csv(rpt)


def test_quote():
    qt = Quote()
    qt.make_barcodes()
    qt.create_block_report()
    qt.save_block_report()


def test_print_barcode_from_quote():
    qt = Quote()
    qt.make_barcodes()
    qt.create_block_report()
    qt.print_beginning(3, _print=True)


def main():
    test_print_barcode_from_quote()


if __name__ == "__main__":
    main()

