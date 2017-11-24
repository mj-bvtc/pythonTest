from reportlab.pdfgen import canvas


def hello(c):
    from reportlab.lib.units import inch
    c.translate(inch, inch)
    c.setFont("Helvetica", 14)
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.setFillColorRGB(1, 0, 1)
    # draw some lines
    c.line(0, 0, 0, 1.7 * inch)
    c.line(0, 0, 1 * inch, 0)
    # draw a rectangle
    c.rect(0.2 * inch, 0.2 * inch, 1 * inch, 1.5 * inch, fill=1)
    # make text go straight up
    c.rotate(90)
    # change color
    c.setFillColorRGB(0, 0, 0.77)
    # say hello (note after rotate the y coord needs to be negative!)
    c.drawString(0.3*inch, -inch, "Hello World")


c = canvas.Canvas("hello.pdf")
hello(c)
c.showPage()
c.save()
