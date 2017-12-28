import pyqrcode
import PIL
qr = pyqrcode.create("testing 1,2,3")
qr.png("test.png", scale=6)

# import qrtools

# qr = qrtools.QR()
# qr.decode("test.png")
# print(qr.data)

help(PIL)

