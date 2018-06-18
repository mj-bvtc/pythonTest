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

    def get_data(self):
        pass

    def build_sticker(self):
        pass

    def print_sticker(self):
        pass

    def print_sticker_list(self, sticker_list):
        pass


def get_user_host():
    hostname = socket.gethostname()
    username = getpass.getuser()
    user_host = f"{username}@{hostname}"
    return user_host


def create_code():
    raw_code = uuid.uuid4()
    code = str(raw_code)
    return code


def make_pdf(code=None, path=None):
    # get code
    if code is None:
        code = create_code()

    # format names
    path = r"C:\Users\mkreidler\Desktop\pdf exports"  # this is hard coded in, this is BADDDD
    full_path = os.path.join(path, code)
    pdf_path = full_path + ".pdf"
    img_path = full_path + ".jpeg"

    # draw QR
    qr = qrcode.QRCode()
    pnum = "P12-3456"
    qr_data = f"{pnum}_{code}"
    qr.add_data(qr_data)
    img = qr.make_image().save(img_path)

    # draw pdf
    dt = datetime.datetime.now()
    c = canvas.Canvas(pdf_path)

    c.setFont("Helvetica-Bold", 9)

    c.setPageSize((576, 384))  # 4x6 in pixels

    # ----make labels----

    # project: ***THIS NEEDS TO BE PROGRAMMED
    project = "Moynihan Station Phase III"
    p_num = "P18-1234"
    proj = f"{p_num},  {project}"
    c.drawString(33, 282, "PROJECT:")
    c.setFont("Helvetica", 9)
    c.drawString(33, 268, proj)

    # date received: ****this needs to be input somehow
    c.setFont("Helvetica-Bold", 9)
    c.drawString(33, 246, "DATE RECEIVED:")
    c.setFont("Helvetica", 9)
    c.drawString(33, 232, str(dt))

    # date printed:
    c.setFont("Helvetica-Bold", 9)
    c.drawString(33, 209, "DATE PRINTED:")
    c.setFont("Helvetica", 9)
    c.drawString(33, 198, str(dt))

    # guid:
    c.setFont("Helvetica-Bold", 9)
    c.drawString(33, 174, "GUID:")
    c.setFont("Helvetica", 9)
    c.drawString(33, 162, str(code))

    # LOCATION: ***PROGRAM THIS
    c.setFont("Helvetica-Bold", 9)
    c.drawString(33, 140, "LOCATION:")
    c.setFont("Helvetica", 9)
    # c.drawString(33, 128, "E25-14A-BK49R-COLOR")
    c.drawString(33, 128, "----")

    # Sample ID: ***PROGRAM THIS
    c.setFont("Helvetica-Bold", 9)
    c.drawString(215, 140, "SAMPLE ID:")
    c.setFont("Helvetica", 9)
    c.drawString(215, 128, "23")

    # quantity ***HAND INPUT AT THE MOMENT
    c.setFont("Helvetica-Bold", 9)
    c.drawString(33, 107, "QUANTITY:")
    c.setFont("Helvetica", 9)
    c.drawString(33, 95, "256")

    # NUMBERS
    c.setFont("Helvetica-Bold", 9)
    c.drawString(33, 107, "QUANTITY:")
    c.drawString(96, 107, "INSTANCE:")
    c.drawString(160, 107, "CRATE:")
    c.drawString(215, 107, "PALLET:")
    c.setFont("Helvetica", 9)
    c.drawString(33, 95, "256")
    c.drawString(96, 95, "14")
    c.drawString(160, 95, "6")
    c.drawString(215, 95, "3")

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
    c.rect(33, 332, .105*inch, .105*inch, stroke=1, fill=0)
    c.rect(185, 332, .105 * inch, .105 * inch, stroke=1, fill=0)
    c.rect(33, 310, .105*inch, .105*inch, stroke=1, fill=0)
    c.rect(185, 310, .105 * inch, .105 * inch, stroke=1, fill=0)
    c.rect(185, 288, .105 * inch, .105 * inch, stroke=1, fill=0)        # DIGITAL SCULPTURE CHECKBOX
    c.setFont("Helvetica", 9.7)
    c.drawString(44, 332.213, "LOGGED IN")
    c.drawString(196, 332.213, "SCANNED")
    c.drawString(44, 310, "TO BE RETURNED")
    c.drawString(196, 310, "COLOR SAMPLE")
    c.drawString(196, 288, "DIGITAL SCULPTURE")
    c.save()

    # delete .jpeg
    os.remove(img_path)

    return pdf_path


def print_file(filename):
    win32api.ShellExecute(
        0,
        "print",
        filename,
        #
        # If this is None, the default printer will
        # be used anyway.
        #
        '/d:"%s"' % win32print.GetDefaultPrinter(),
        ".",
        0
    )


def print_label():
    file = make_pdf()
    print_file(file)


def print_labels(num=1, pause=0):
    for i in range(num):
        print_label()
        print(f"Printed {i+1}")
        time.sleep(pause)


class QR(Common):
    def __init__(self, name):
        super().__init__()
        self.name = name


def program():
    user = get_user_host()
    prompt = f"{user}"
    project = ""

    esc = 'X'
    name = "Walter"

    commands = [esc, name]

    while esc not in prompt:
        if project == "":
            project = input("Type in name of current project: ")
        cmd = input(f"Type in a command, {esc} to leave...")

        if cmd not in commands:
            print("Invalid command")
            cmd = ""

        prompt = f"[{project}] {user} {cmd}"
        print(prompt)


def main():
    print_labels(num=3, pause=5)


if __name__ == "__main__":
    main()

