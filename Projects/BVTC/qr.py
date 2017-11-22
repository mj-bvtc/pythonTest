import qrcode
"""https://pypi.python.org/pypi/qrcode"""


def save_qr(data, path, name):
    qr = qrcode.QRCode(
        version=4,      # 1-40 controls size
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10, # pixel size
        border=6, #border size, min 4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    ext = ".png"
    path += name
    path += ext
    img.save(path)


def main():
    data = """guid: 45d31d7f-a6d7-4bfe-a510-b2a829e90c70
user: mkreidler
machine: BVTC-Render08
time_created: 2017-11-22 16:28:46.009735
style: ['Egg & Dart']
orientation: L
length_number: 4
style_number: 3
form_method: None
profile: None
deleted: None
phase: None
size: None
type: None
region: None
is_mirror_opposite: None
notes: None
repeat_number: ['5']
floor: 2
drop: S
drop_number: 1
floor_section: 
block: E3L4(5)
shorthand: S1-2-E3L-4(5)
sample: None"""
    save_qr(data, r"C:\Users\mkreidler\Desktop\\", "qr4")

    print("finished")

if __name__ == "__main__":
    main()


