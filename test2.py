from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QGridLayout
from PySide6.QtWidgets import QPushButton

import sys
import csv
import time
import threading

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

    
    def start_log(self):
        self.f=open(self.input.text(),"a", newline='')
        self.writer = csv.writer(self.f,delimiter=",")
        self.writer.writerow(['col1,col2']) 
        self.f.flush()
        self.stop_event=threading.Event()
        self.c_thread=threading.Thread(target=self.log_data, args=(self.stop_event,))
        self.c_thread.start()
    
    def log_data(self,stop_event):
        state=True
        while state and not stop_event.isSet():
            self.writer.writerow([0,1])
            time.sleep(5)

    def stop_log(self):
        self.stop_event.set()
        self.f.close()

    def btnstate(self):
        if self.b1.isChecked():
            self.l2.setText("Running")
            f_name = self.input.text()
            print('File name: ' + f_name)
            self.start_log()
        else:
            self.l2.setText("Stopped")
            self.stop_log()
    
    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit( app.exec_() )