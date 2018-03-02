from reportlab.pdfgen import canvas
import re
import os
import qrcode
import uuid
import tempfile
import win32api
import win32print
import datetime
import socket
import getpass


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
    qr.add_data(code)
    img = qr.make_image().save(img_path)

    # draw pdf
    dt = datetime.datetime.now()
    c = canvas.Canvas(pdf_path)

    c.setFont("Helvetica", 10)

    c.setPageSize((288, 96))  # (288,96)
    c.drawString(85, 60, code)
    c.drawString(85, 40, str(dt))
    # c.drawString(85, 20, get_user_host())
    c.drawString(85, 20, "Project: Old Main Post Office")
    c.drawInlineImage(img_path, 5, 10, width=80, height=80)
    c.drawInlineImage(r"C:\Users\mkreidler\Desktop\BVTC-Logo-BLACK-horizontal.jpg",
                      205, 70, width=75, height=20)
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


def print_labels(num=1):
    for i in range(num):
        print_label()


def main():
    # print_labels(20)
    pdf = make_pdf()
    print(pdf)


main()
