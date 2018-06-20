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
        c.drawString(215, 128, self.sample_id)

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
        c.drawString(31, 37, "BK49R")

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


def main():

    # instantiate barcode class
    bc = Barcode()

    # input data values
    bc.project_number = "P12-3456"
    bc.quantity = 12
    bc.location = "E14-5-H12R"
    bc.dt_received = datetime.datetime(2018, 3, 12)
    bc.project_name = "451 Broome"
    bc.color_sample = True

    # choose a folder to save in
    bc.get_folder()

    # get sample id from user
    bc.get_sample_name()

    # draw QR
    bc.draw_qr()

    # build sticker
    bc.build_sticker()

    # physically print sticker
    bc.print_sticker()


if __name__ == "__main__":
    main()

