# Working Qt code

from PySide6.QtWidgets import *

import sys
import csv
import time
import threading

import asyncio
import functools
import qasync

from qasync import asyncSlot, asyncClose, QApplication


class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.N_channels=8
        self.BattCelldata = [{'Datapoint Number':0,'Test Time':0,'Current':0,'Potential':0,'Timestamp':0,'LDC SENSOR':0,'LDC REF':0,'Ambient Temperature':0,'Ambient RH':0,'LDC N':0,'LDC STD':0,'REF N':0,'REF STD':0,'LDC scaled':0,'LDC status':0,'REF status':0,'Filename':0,'Start_Time':0,'New_data':0,'LogStatus':0} for i in range(self.N_channels)]

        self.setWindowTitle("Neware Data Logger")
        self.input = QLineEdit()
        self.input.setText("proj_cell_xxx_test_xxx.csv")
        # self.input.textChanged.connect(self.label.setText)
        self.l0 = QLabel("Channel #")
        self.l1 = QLabel("411")
        self.idx = 0
        self.l2 = QLabel()
        self.b1 = QPushButton("Start")
        self.b2 = QPushButton("Stop")
        self.b1.clicked.connect(self.b1_state)
        self.b2.clicked.connect(self.b2_state)
        self.b2.setEnabled(False)

        self.combobox = QComboBox()
        self.combobox.addItems(['411','412','413','414','415','416','417','418'])
        self.combobox.activated.connect(self.activated)
        self.combobox.currentTextChanged.connect(self.text_changed)
        # self.combobox.currentIndexChanged.connect(self.index_changed)

        layout = QGridLayout()
        ix=0
        iy=0
        layout.addWidget(self.l0,ix,0)
        iy+=1
        layout.addWidget(self.combobox,ix,iy)
        ix+=1
        iy=0
        layout.addWidget(self.l1,ix,iy)
        iy+=1
        layout.addWidget(self.input,ix,iy)
        iy+=1
        layout.addWidget(self.l2,ix,iy)
        iy+=1
        layout.addWidget(self.b1,ix,iy)
        iy+=1
        layout.addWidget(self.b2,ix,iy)
        
        self.l2.setText("Stopped")
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    
    @asyncSlot()
    async def start_log(self):
        Headerlist=['Datapoint Number','Test Time','Current','Potential','Timestamp','LDC SENSOR','LDC REF','Ambient Temperature','Ambient RH','LDC N','LDC STD','REF N','REF STD','LDC scaled','LDC status','REF status']
        SubHeader=['none','second','amp','volt','epoch','none','none','celsius','percent','none','none','none','none','none']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.BattCelldata[self.idx]['Filename']= 'proj_cell_xxx_test_xxx_'+timestr +'.csv'
        self.BattCelldata[self.idx]['LogStatus']= 1
        print('Log Status: ',self.BattCelldata[self.idx]['LogStatus'])
        with open(self.BattCelldata[self.idx]['Filename'], 'w',newline='') as file:
            headerwriter=csv.writer(file,delimiter='\t')
            headerwriter.writerow(Headerlist)
            headerwriter.writerow(SubHeader)
        self.l2.setText("Running")
        self.b1.setEnabled(False)
        self.b2.setEnabled(True)
        self.input.setText(self.BattCelldata[self.idx]['Filename'])
    
    # def log_data(self):
    #     state=True
    #     while state and not self.stop_event.wait(1):
    #         self.writer.writerow([0,1])
    #         time.sleep(5)
    
    @asyncSlot()
    async def stop_log(self):
        self.BattCelldata[self.idx]['LogStatus']= 0
        print('Log Status: ',self.BattCelldata[self.idx]['LogStatus'])
        self.l2.setText("Stopped")
        self.b2.setEnabled(False)
        self.b1.setEnabled(True)
        self.input.setText("proj_cell_xxx_test_xxx.csv")

    @asyncSlot()
    async def activated(self, index):
        print("Activated index:", index)
        self.idx=index
        print('Log Status: ',self.BattCelldata[self.idx]['LogStatus'])
        if self.BattCelldata[self.idx]['LogStatus']:
            self.l2.setText("Running")
            self.b1.setEnabled(False)
            self.b2.setEnabled(True)
            self.input.setText(self.BattCelldata[self.idx]['Filename'])
        else:
            self.l2.setText("Stopped")
            self.b2.setEnabled(False)
            self.b1.setEnabled(True)
            self.input.setText("proj_cell_xxx_test_xxx.csv")

    @asyncSlot()
    async def text_changed(self, s):
        # print("Text changed:", s)
        # self.l1 = QLabel(s)
        self.l1.setText(s)

    @asyncSlot()
    async def index_changed(self, index):
        print("Index changed", index)
    
    
    @asyncSlot()
    async def b1_state(self):
        
        f_name = self.input.text()
        print(f_name)
        self.start_log()
    
    @asyncSlot()
    async def b2_state(self):
        self.stop_log()
    
async def main():    

    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    window = MainWindow()
    window.show()

    await future
    return True

if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)