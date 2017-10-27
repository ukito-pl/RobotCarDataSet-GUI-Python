# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import sys
import MainWindowDesign
import SelectDataWindowDesign
from buildPointCloudThread import buildPointcloudThread
import numpy as np
from Tkinter import *



class SelectDataWindow(QtGui.QDialog, SelectDataWindowDesign.Ui_Dialog):
    def __init__(self):
        # Using super allows us to
        # access variables, methods etc in the MainWindowDesign.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in MainWindowDesign.py file automatically
                            # It sets up layout and widgets that are defined
        try:
            self.readDialog1()
        except:
            pass

        self.browseButton1.clicked.connect(self.browse1)
        self.browseButton2.clicked.connect(self.browse2)
        self.browseButton3.clicked.connect(self.browse3)
        self.buttonBox.accepted.connect(self.saveDialog1)

    def saveDialog1(self):
        global dirDataF, dirExtrF, dirModelsF, dirIns, dirLidar, dirCamera, startTime, endTime
        dirDataF = self.chooseDataFolder.text()
        dirExtrF = self.chooseExtrFolder.text()
        dirModelsF = self.chooseModelsFolder.text()
        startTime = self.startTimeF.text()
        endTime = self.endTimeF.text()

        dirDataF = dirDataF.replace('\r', "").replace('\n', "").replace('file://', "")
        dirExtrF = dirExtrF.replace('\r', "").replace('\n', "").replace('file://', "")
        dirModelsF = dirModelsF.replace('\r', "").replace('\n', "").replace('file://', "")
        startTime = startTime.replace('\r', "").replace('\n', "")
        endTime = endTime.replace('\r', "").replace('\n', "")

        dirLidar = dirDataF + "/" + self.chooseLidar.currentText()
        dirCamera = dirDataF + "/" + self.chooseCamera.currentText()
        if self.choosePoseF.currentIndex() == 1:
            dirIns = dirDataF + "/gps/ins.csv"
        else:
            dirIns = dirDataF + "/vo/vo.csv"

        f = open('defaultDir.txt', 'w')
        lines = [dirDataF, "\n", dirExtrF, "\n", dirModelsF, "\n", str(self.chooseLidar.currentIndex()), "\n",
                 str(self.chooseCamera.currentIndex()), "\n", str(self.choosePoseF.currentIndex()), "\n", startTime, "\n", endTime]
        f.writelines(lines)
        f.close()
        self.countTime()


    def countTime(self):
        global realEndTime, realStartTime
        path = dirLidar + '.timestamps'
        f = open(path, 'r')
        x = f.readline()
        realStartTime = int(x.split()[0]) + int(startTime)*1000  # [0]index elementu który ma zostać po splicie
        f.close()
        realEndTime = int(realStartTime) + int(endTime)*1000  # 1418381798086398, 1418381817118734


    def readDialog1(self):
        f = open('defaultDir.txt', 'r')
        self.chooseDataFolder.setText(f.readline())
        self.chooseExtrFolder.setText(f.readline())
        self.chooseModelsFolder.setText(f.readline())
        self.chooseLidar.setCurrentIndex(int(f.readline()))
        self.chooseCamera.setCurrentIndex(int(f.readline()))
        self.choosePoseF.setCurrentIndex(int(f.readline()))
        self.startTimeF.setText(f.readline())
        self.endTimeF.setText(f.readline())
        f.close()


    def browse1(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.chooseDataFolder.setText(directory)

    def browse2(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.chooseExtrFolder.setText(directory)

    def browse3(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.chooseModelsFolder.setText(directory)




class Application(QtGui.QMainWindow, MainWindowDesign.Ui_MainWindow):
    def __init__(self):
        # Using super allows us to
        # access variables, methods etc in the MainWindowDesign.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in MainWindowDesign.py file automatically
                            # It sets up layout and widgets that are defined
        self.pointcloudButton.clicked.connect(self.buildPointcloud)
        self.selectDataButton.clicked.connect(self.openSelectData)
        #self.settingButton.clicked.connect(self.drawme)            do testów czegoś
        #self.simulationButton.clicked.connect(self.trawme)         do testów czegoś


    def openSelectData(self):
        self.dialog = SelectDataWindow()
        self.dialog.show()


    def buildPointcloud(self):
        self.newThread = buildPointcloudThread(    str(dirLidar),
                                                   str(dirIns),
                                                   str(dirExtrF),
                                                   realStartTime, realEndTime)
        self.connect(self.newThread, SIGNAL("drawPointcloud(PyQt_PyObject)"), self.drawPointcloud)
        self.newThread.start()
        self.pointcloudButton.setEnabled(False)
        self.pointcloudButton.setText("Building pointcloud...")


    def drawPointcloud(self,pointcloud):
        pointcloud = pointcloud[0:3, :].transpose()
        print pointcloud
        pointcloud = np.array(-pointcloud)

        self.plotItem = gl.GLScatterPlotItem(pos=pointcloud, size=1, color=[0.7, 0.7, 0.7, 1], pxMode=True)
        self.plotItem.translate(5, 5, 0)
        if self.pointcloudArea.items.__len__() == 0:
            self.pointcloudArea.addItem(self.plotItem)

        self.pointcloudButton.setEnabled(True)
        self.pointcloudButton.setText("Build and draw sample pointcloud")



def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = Application()                # We set the form to be our Application (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
