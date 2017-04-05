import sys
from PyQt5 import QtWidgets, QtGui


def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    b = QtWidgets.QPushButton(w)
    l = QtWidgets.QLabel(w)
    b.setText("Push Me")
    l.setText("Look at Me")
    b.move(230, 200)
    label_1 = QtWidgets.QLabel(w)
    label_2 = QtWidgets.QLabel(w)
    label_2.setPixmap(QtGui.QPixmap(r"C:\Users\mkreidler\Desktop\Dump\Button-Next-icon.png"))
    label_1.setText("Hello World")
    label_1.move(100, 20)
    label_2.move(120, 90)
    w.setWindowTitle("Test Window for Matthew!")
    w.setGeometry(100, 100, 400, 350)
    w.show()
    sys.exit(app.exec_())

window()


