# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import sys
import MainWindowDesign
from buildPointCloudThread import buildPointcloudThread
import numpy as np




class Application(QtGui.QMainWindow, MainWindowDesign.Ui_MainWindow):
    def __init__(self):
        # Using super allows us to
        # access variables, methods etc in the MainWindowDesign.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in MainWindowDesign.py file automatically
                            # It sets up layout and widgets that are defined
        self.pointcloudButton.clicked.connect(self.buildPointcloud)



    def buildPointcloud(self):
        # Performed when pointcloudButton has been clicked
        self.newThread = buildPointcloudThread("/home/ukito/Documents/inżynierka/sample/lms_front",
                                                   "/home/ukito/Documents/inżynierka/sample/gps/ins.csv",
                                                   "/home/ukito/Documents/inżynierka/robotcar-dataset-sdk-2.0.1/extrinsics",
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
