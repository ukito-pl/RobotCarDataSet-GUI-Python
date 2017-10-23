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



class SelectDataWindow(QtGui.QDialog, SelectDataWindowDesign.Ui_Dialog):
    def __init__(self):
        # Using super allows us to
        # access variables, methods etc in the MainWindowDesign.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in MainWindowDesign.py file automatically
                            # It sets up layout and widgets that are defined


class Application(QtGui.QMainWindow, MainWindowDesign.Ui_MainWindow):
    def __init__(self):
        # Using super allows us to
        # access variables, methods etc in the MainWindowDesign.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in MainWindowDesign.py file automatically
                            # It sets up layout and widgets that are defined
        self.pointcloudButton.clicked.connect(self.buildPointcloud)
        self.selectDataButton.clicked.connect(self.openSelectData)


    def openSelectData(self):
        self.dialog = SelectDataWindow()
        self.dialog.open()


    def buildPointcloud(self):
        dirDataF = self.dialog.chooseDataFolder.text()
        dirDataF = dirDataF.replace('\r', "").replace('\n', "").replace('file://',"")
        dirExtrF = self.dialog.chooseExtrFolder.text()
        dirExtrF = dirExtrF.replace('\r', "").replace('\n', "").replace('file://', "")
        dirModelsF = self.dialog.chooseModelsFolder.text()
        dirModelsF = dirModelsF.replace('\r', "").replace('\n', "").replace('file://', "")
        dirIns = dirDataF + "/gps/ins.csv"
        dirLidar = dirDataF + "/" + self.dialog.chosseLidar.currentText()
        #dirCamera = dirFolder + "/sample/" + self.dialog.chooseCamera.currentText()
        startTime = self.dialog.startTime.text()
        endTime = self.dialog.endTime.text()




        #"/home/qahu/Documents/inz"
        #"1418381798086398, 1418381817118734"
        #int(startTime), int(endTime)

        self.newThread = buildPointcloudThread(    str(dirLidar),
                                                   str(dirIns),
                                                   str(dirExtrF),
                                                   1418381798086398, 1418381817118734)
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
