from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QGridLayout
from PySide2.QtWidgets import QPushButton

import sys
import csv
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Neware Data Logger")
        self.input = QLineEdit()
        self.input.setText("proj_cell_xxx_test_xxx.csv")
        # self.input.textChanged.connect(self.label.setText)
        self.l1 = QLabel("Ch:3411")
        self.l2 = QLabel()
        self.b1 = QPushButton("Start/Stop")
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.b1.clicked.connect(self.btnstate)

        layout = QGridLayout()
        layout.addWidget(self.l1,0,0)
        layout.addWidget(self.input,0,1)
        layout.addWidget(self.l2,0,2)
        layout.addWidget(self.b1,0,3)
        
        self.l2.setText("Stopped")
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    
    def log_data(self):
        f=open(self.input.text(),"a", newline='')
        writer = csv.writer(f,delimiter=",")
        writer.writerow(['col1,col2']) 
        f.flush()
        while self.b1.isChecked():
            writer.writerow([0,1])
            time.sleep(5)

    
    def btnstate(self):
        if self.b1.isChecked():
            self.l2.setText("Running")
            f_name = self.input.text()
            print('File name: ' + f_name)
            self.log_data()
        else:
            self.l2.setText("Stopped")
    
    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit( app.exec_() )