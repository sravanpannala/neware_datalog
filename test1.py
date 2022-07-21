# Basic Qt Window

import sys
from PySide2.QtWidgets import QApplication, QPushButton, QWidget, QFileDialog

app = QApplication(sys.argv)

w = QWidget()
w.resize(600, 400)
w.setWindowTitle("Hello, World!")
w.show()

sys.exit( app.exec_() )