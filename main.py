# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import sys
import MainWindowDesign
import SelectDataWindowDesign
from buildPointCloudThread import *
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
            self.read_dialog1()
        except:
            pass

        self.browseButton1.clicked.connect(self.browse1)
        self.browseButton2.clicked.connect(self.browse2)
        self.browseButton3.clicked.connect(self.browse3)
        self.buttonBox.accepted.connect(self.save_dialog1)

    def save_dialog1(self):
        global dir_data_f, dir_extr_f, dir_models_f, dir_ins, dir_lidar, dir_camera, start_time, end_time
        dir_data_f = self.chooseDataFolder.text()
        dir_extr_f = self.chooseExtrFolder.text()
        dir_models_f = self.chooseModelsFolder.text()
        start_time = self.startTimeF.text()
        end_time = self.endTimeF.text()

        dir_data_f = dir_data_f.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_extr_f = dir_extr_f.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_models_f = dir_models_f.replace('\r', "").replace('\n', "").replace('file://', "")
        start_time = start_time.replace('\r', "").replace('\n', "")
        end_time = end_time.replace('\r', "").replace('\n', "")

        dir_lidar = dir_data_f + "/" + self.chooseLidar.currentText()
        dir_camera = dir_data_f + "/" + self.chooseCamera.currentText()
        if self.choosePoseF.currentIndex() == 1:
            dir_ins = dir_data_f + "/gps/ins.csv"
        else:
            dir_ins = dir_data_f + "/vo/vo.csv"

        f = open('defaultDir.txt', 'w')
        lines = [dir_data_f, "\n", dir_extr_f, "\n", dir_models_f, "\n", str(self.chooseLidar.currentIndex()), "\n",
                 str(self.chooseCamera.currentIndex()), "\n", str(self.choosePoseF.currentIndex()), "\n", start_time, "\n", end_time]
        f.writelines(lines)
        f.close()
        self.count_time()

    def count_time(self):
        global real_end_time, real_start_time
        path = dir_lidar + '.timestamps'
        f = open(path, 'r')
        x = f.readline()
        real_start_time = int(x.split()[0]) + int(start_time) * 1000  # [0]index elementu który ma zostać po splicie
        f.close()
        real_end_time = int(real_start_time) + int(end_time) * 1000  # 1418381798086398, 1418381817118734

    def read_dialog1(self):
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
        self.pointcloudButton.clicked.connect(self.build_pointcloud)
        self.selectDataButton.clicked.connect(self.open_select_data)
        #self.settingButton.clicked.connect(self.drawme)            do testów czegoś
        self.simulationButton.clicked.connect(self.build_pointcloud_live)

    def open_select_data(self):
        self.dialog = SelectDataWindow()
        self.dialog.show()

    def build_pointcloud(self):
        self.new_thread = BuildPointcloudThread(    str(dir_lidar),
                                                   str(dir_ins),
                                                   str(dir_extr_f),
                                                   real_start_time, real_end_time)
        self.connect(self.new_thread, SIGNAL("drawPointcloud(PyQt_PyObject)"), self.draw_pointcloud)
        self.new_thread.start()
        self.pointcloudButton.setEnabled(False)
        self.pointcloudButton.setText("Building pointcloud...")

    def draw_pointcloud(self, pointcloud):
        pointcloud = pointcloud[0:3, :].transpose()
        print pointcloud
        pointcloud = np.array(-pointcloud)

        plot_item = gl.GLScatterPlotItem(pos=pointcloud, size=1, color=[0.7, 0.7, 0.7, 1], pxMode=True)
        plot_item.translate(5, 5, 0)
        #clear pointcloud area
        if self.pointcloudArea.items.__len__() > 0:
            for i in range(0,self.pointcloudArea.items.__len__()):
                self.pointcloudArea.items.__delitem__(i)

        self.pointcloudArea.addItem(plot_item)

        self.pointcloudButton.setEnabled(True)
        self.pointcloudButton.setText("Build and draw sample pointcloud")

    def build_pointcloud_live(self):
        #Nie działa
        self.new_thread2 = BuildPointcloudThreadLive(str(dir_lidar),
                                               str(dir_ins),
                                               str(dir_extr_f),
                                               real_start_time, real_end_time)
        #self.connect(self.newThread2, SIGNAL("drawPointcloud(PyQt_PyObject)"), self.drawPointcloud)
        self.new_thread2.start()


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = Application()                # We set the form to be our Application (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
