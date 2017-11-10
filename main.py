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
import csv
from math import sin, cos
import numpy.matlib as ml



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
        global dir_data_f, dir_extr_f, dir_models_f, dir_lidar_data, dir_ins, dir_lidar, dir_camera, start_time, end_time
        dir_data_f = self.chooseDataFolder.text()
        dir_extr_f = self.chooseExtrFolder.text()
        dir_models_f = self.chooseModelsFolder.text()
        dir_lidar_data = self.chooseLidarDataFile.text()
        start_time = self.startTimeF.text()
        end_time = self.endTimeF.text()

        dir_data_f = dir_data_f.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_extr_f = dir_extr_f.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_models_f = dir_models_f.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_lidar_data = dir_lidar_data.replace('\r', "").replace('\n', "").replace('file://', "")
        start_time = start_time.replace('\r', "").replace('\n', "")
        end_time = end_time.replace('\r', "").replace('\n', "")

        dir_lidar = dir_data_f + "/" + self.chooseLidar.currentText()
        dir_camera = dir_data_f + "/" + self.chooseCamera.currentText()
        if self.choosePoseF.currentIndex() == 1:
            dir_ins = dir_data_f + "/gps/ins.csv"
        else:
            dir_ins = dir_data_f + "/vo/vo.csv"

        f = open('defaultDir.txt', 'w')
        lines = [dir_data_f, "\n", dir_extr_f, "\n", dir_models_f, "\n", dir_lidar_data, "\n",
                 str(self.chooseLidar.currentIndex()), "\n", str(self.chooseCamera.currentIndex()),
                 "\n", str(self.choosePoseF.currentIndex()), "\n", start_time, "\n", end_time]
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
        self.chooseLidarDataFile.setText(f.readline())
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
        self.settingButton.clicked.connect(self.drawme)
        self.simulationButton.clicked.connect(self.build_pointcloud_live)

    def open_select_data(self):
        self.dialog = SelectDataWindow()
        self.dialog.show()


#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
    def nic(self):
        path = dir_lidar_data
        dane_gps = []
        sensors_file = open(path + '/mystream_11_3_8_11_44.csv' , 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                txyzrpy = [float(line.split(',')[0])] + [float(x) for x in line.split(',')[2:5]] + [float(x) for x in
                                                                                                    line.split(',')[
                                                                                                    10:13]]
                dane_gps.append(txyzrpy)
        if len(dane_gps) == 0:
            raise ValueError("No GPS data found")
        sensors_file.close()

        gsp_file = open('daneGPS.csv', 'w')
        aaa = csv.writer(gsp_file)
        aaa.writerows(dane_gps)
        gsp_file.close()
        print 'Zakończono'

    def stepbystep(self):
        path = str(dir_lidar_data)
        dane_lidar = []
        lidar_data_file = open(path + '/dane.csv', 'r')
        for line in lidar_data_file:
            try:
                one_scan = [float(x) for x in line.split(',')[11:282]]
                dane_lidar.append(one_scan)
            except:
                pass
        lidar_data_file.close()

        f = open(path + '/daneLidar.csv', 'w')
        f_csv = csv.writer(f)
        f_csv.writerows(dane_lidar)
        f.close()
        print 'Zakończono'


        licznik = -50
        dane_pointcloud = []
        lidar_data_file = open(path + '/daneLidar.csv', 'r')
        for line in lidar_data_file:
            licznik = licznik + 0.06
            i = 45
            for x in line.split(','):
                s = np.pi / 180 * i
                a = float(x) * sin(s)
                b = float(x) * cos(s)
                c = licznik
                i = i + 1
                one_point = [c] + [a] + [b]
                dane_pointcloud.append(one_point)
        lidar_data_file.close()


        f = open(path + '/danePointcloud.csv', 'w')
        f_csv = csv.writer(f)
        f_csv.writerows(dane_pointcloud)
        f.close()
        print 'Zakończono'

        klaudzik = []
        klaudzik_file = open(path + '/danePointcloud.csv', 'r')
        for line in klaudzik_file:
            xyz = np.matrix([[float(x) for x in line.split(',')[0:3]]])
            klaudzik.append(xyz)
        klaudzik_file.close()

        print 'Zakończono'
        klaudzik = np.array(klaudzik)
        plot_item = gl.GLScatterPlotItem(pos=klaudzik, size=1, color=[0.7, 0.7, 0.7, 1], pxMode=True)
        plot_item.translate(5, 5, 0)
        if self.pointcloudArea.items.__len__() > 0:
            for i in range(0, self.pointcloudArea.items.__len__()):
                self.pointcloudArea.items.__delitem__(i)

        self.pointcloudArea.addItem(plot_item)
        print 'Zakończono :DDDD'


    def timestampy(self):
        dane = []
        f = open(dir_lidar_data + '/lms_front.timestamps', 'w')
        fc = csv.writer(f)
        for i in range(0, 1530, 1):
            dane.append([str(i * 66666 + 1000000) + ' 1'])
        fc.writerows(dane)
        f.close()
        print "koniec"


    def get_IMU(self):
        start = False
        path = dir_lidar_data
        dane_gps = []
        sensors_file = open(path + '/mystream_11_3_8_11_44.csv', 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                txyzrpy =  [float(x) for x in line.split(',')[10:13]]
                dane_gps.append(txyzrpy)
                start = True
            else:
                if start == True:
                    txyzrpy = [float(x) for x in line.split(',')[6:9]]
                    if txyzrpy != []:
                        dane_gps.append(txyzrpy)
        if len(dane_gps) == 0:
            raise ValueError("No GPS data found")
        sensors_file.close()

        gsp_file = open(path + '/daneIMU.csv', 'w')
        aaa = csv.writer(gsp_file)
        aaa.writerows(dane_gps)
        gsp_file.close()
        print 'Zakończono'

    def daneIMU15_GPS(self):
        path = dir_lidar_data
        dane_gps = []
        sensors_file = open(path + '/mystream_11_3_8_11_44.csv', 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                next_data = [float(x) for x in line.split(',')[2:5]]
                next_imu = [float(x) for x in line.split(',')[10:13]]
                try:
                    x = np.linspace(last_data[0], next_data[0], 15)
                    y = np.linspace(last_data[1], next_data[1], 15)
                    z = np.linspace(last_data[2], next_data[2], 15)
                    i = np.linspace(last_imu[0], next_imu[0], 15)
                    m = np.linspace(last_imu[1], next_imu[1], 15)
                    u = np.linspace(last_imu[2], next_imu[2], 15)
                    for j in range(0, 15, 1):
                        xyz = [x[j], y[j], z[j], i[j], m[j], u[j]]
                        dane_gps.append(xyz)
                    last_data = next_data
                    last_imu = next_imu
                except:
                    last_data = next_data
                    last_imu = next_imu
        if len(dane_gps) == 0:
            raise ValueError("No GPS data found")
        sensors_file.close()

        gsp_file = open(path + '/daneGPS+imu.csv', 'w')
        aaa = csv.writer(gsp_file)
        aaa.writerows(dane_gps)
        gsp_file.close()
        print 'Zakończono'


    def dane_do_build_scan(self):
        path = str(dir_lidar_data)
        dane_lidar = []
        lidar_data_file = open(path + '/dane.csv', 'r')
        for line in lidar_data_file:
            try:
                one_scan = [float(x) for x in line.split(',')[11:282]]
                dane_lidar.append(one_scan)
            except:
                pass
        lidar_data_file.close()

        f = open(path + '/daneLidar.csv', 'w')
        f_csv = csv.writer(f)
        f_csv.writerows(dane_lidar)
        f.close()
        print 'Zakończono'

        dane_pointcloud = []
        lidar_data_file = open(path + '/daneLidar.csv', 'r')
        for line in lidar_data_file:
            i = 45
            for x in line.split(','):
                s = np.pi / 180 * i
                a = float(x) * sin(s)
                b = float(x) * cos(s)
                i = i + 1
                one_point = [a] + [b] + [0]
                dane_pointcloud.append(one_point)
            dane_pointcloud = np.array(dane_pointcloud)
            dane_pointcloud = dane_pointcloud.transpose()
        lidar_data_file.close()


        def RPY_metoda_AKC_MAGN(self):
            path = dir_lidar_data
            dane_gps = []
            sensors_file = open(path + '/mystream_11_3_8_11_44.csv', 'r')
            for line in sensors_file:
                id = line.split(',')[1]
                if int(id) == 1:
                    next_data = [float(x) for x in line.split(',')[2:5]]
                    try:
                        x = np.linspace(last_data[0], next_data[0], 15)
                        y = np.linspace(last_data[1], next_data[1], 15)
                        z = np.linspace(last_data[2], next_data[2], 15)
                        for j in range(0, 15, 1):
                            xyz = [x[j], y[j], z[j]]
                            dane_gps.append(xyz)
                        last_data = next_data
                    except:
                        last_data = next_data
            if len(dane_gps) == 0:
                raise ValueError("No GPS data found")
            sensors_file.close()

            gsp_file = open(path + '/dane_sam_GPS.csv', 'w')
            aaa = csv.writer(gsp_file)
            aaa.writerows(dane_gps)
            gsp_file.close()
            print 'Zakończono'

            start = False
            i = 0
            path = dir_lidar_data
            dane_imu = []
            sensors_file = open(path + '/mystream_11_3_8_11_44.csv', 'r')
            for line in sensors_file:
                id = line.split(',')[1]
                if int(id) == 1:
                    start = True
                    imu = [float(x) for x in line.split(',')[6:9]] + [float(x) for x in line.split(',')[14:17]]
                    roll = np.arctan2((-imu[1]), imu[2])
                    pitch = np.arcsin(-imu[0] / 9.81)
                    yaw = np.arctan2((sin(roll) * imu[5] - cos(roll) * (-imu[4])),
                                     (cos(pitch) * imu[3] + sin(roll) * sin(pitch) * (-imu[4])) +
                                     cos(roll) * sin(pitch) * imu[5])
                    rpy = [roll * np.pi / 180, pitch * np.pi / 180, yaw * np.pi / 180]
                    dane_imu.append(rpy)
                if start == True and i >= 3 and int(id) != 1 and line.split(',')[10:13] != []:
                    imu = [float(x) for x in line.split(',')[2:5]] + [float(x) for x in line.split(',')[10:13]]
                    roll = np.arctan2((-imu[1]), imu[2])
                    pitch = np.arcsin(-imu[0] / 9.81)
                    yaw = np.arctan2((sin(roll) * imu[5] - cos(roll) * (-imu[4])),
                                     (cos(pitch) * imu[3] + sin(roll) * sin(pitch) * (-imu[4])) +
                                     cos(roll) * sin(pitch) * imu[5])
                    rpy = [roll * np.pi / 180, pitch * np.pi / 180, yaw * np.pi / 180]
                    dane_imu.append(rpy)
                    i = 0
                i = i + 1
            gsp_file = open(path + '/dane_RPY_AKC_MAG.csv', 'w')
            aaa = csv.writer(gsp_file)
            aaa.writerows(dane_imu)
            gsp_file.close()
            print 'Zakończono'


    def RPY_metoda_ZYRO(self):
        path = dir_lidar_data
        dane_gps = []
        sensors_file = open(path + '/mystream_11_3_8_11_44.csv', 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                next_data = [float(x) for x in line.split(',')[2:5]]
                try:
                    x = np.linspace(last_data[0], next_data[0], 15)
                    y = np.linspace(last_data[1], next_data[1], 15)
                    z = np.linspace(last_data[2], next_data[2], 15)
                    for j in range(0, 15, 1):
                        xyz = [x[j], y[j], z[j]]
                        dane_gps.append(xyz)
                    last_data = next_data
                except:
                    last_data = next_data
        if len(dane_gps) == 0:
            raise ValueError("No GPS data found")
        sensors_file.close()

        gsp_file = open(path + '/dane_sam_GPS.csv', 'w')
        aaa = csv.writer(gsp_file)
        aaa.writerows(dane_gps)
        gsp_file.close()
        print 'Zakończono'

        start = False
        i = 0
        path = dir_lidar_data
        dane_imu = []
        sensors_file = open(path + '/mystream_11_3_8_11_44.csv', 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                start = True
                imu = [float(x) for x in line.split(',')[10:13]]
                roll = np.arctan2((imu[0] * 0.06), 1)
                pitch = np.arcsin(-imu[1] * 0.06)
                yaw = np.arctan2((imu[2] * 0.06), 1)
                rpy = [roll * np.pi / 180, pitch * np.pi / 180, yaw * np.pi / 180]
                dane_imu.append(rpy)
            if start == True and i >= 3 and int(id) != 1 and line.split(',')[6:9] != []:
                imu = [float(x) for x in line.split(',')[6:9]]
                roll = np.arctan2((imu[0] * 0.06), 1)
                pitch = np.arcsin(-imu[1] * 0.06)
                yaw = np.arctan2((imu[2] * 0.06), 1)
                rpy = [roll * np.pi / 180, pitch * np.pi / 180, yaw * np.pi / 180]
                dane_imu.append(rpy)
                i = 0
            i = i + 1
        gsp_file = open(path + '/dane_RPY_ZYRO.csv', 'w')
        aaa = csv.writer(gsp_file)
        aaa.writerows(dane_imu)
        gsp_file.close()
        print 'Zakończono'


    def GPS_z_dwoch(self):
        dane_gps = []
        x = np.linspace(6027547.29171011, 6027597.66872427, 1530)
        y = np.linspace(345111.874480535, 345130.419515812, 1530)
        z = np.linspace(-40, -49, 1530)
        for j in range(0, 1530, 1):
            xyz = [x[j], y[j], z[j]]
            dane_gps.append(xyz)

        path = dir_lidar_data
        gsp_file = open(path + '/daneGPS_tylko_z_dwoch.csv', 'w')
        aaa = csv.writer(gsp_file)
        aaa.writerows(dane_gps)
        gsp_file.close()
        print 'Zakończono'
    #SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

    def drawme(self):
        path = str(dir_lidar_data)
        dane_lidar = []
        lidar_data_file = open(path + '/dane.csv', 'r')
        for line in lidar_data_file:
            try:
                one_scan = [float(x) for x in line.split(',')[11:282]]
                dane_lidar.append(one_scan)
            except:
                pass
        lidar_data_file.close()

        f = open(path + '/daneLidar.csv', 'w')
        f_csv = csv.writer(f)
        f_csv.writerows(dane_lidar)
        f.close()
        print 'Zakończono'

        licznik = -50
        dane_pointcloud = []
        lidar_data_file = open(path + '/daneLidar.csv', 'r')
        for line in lidar_data_file:
            licznik = licznik + 0.06
            i = 45
            for x in line.split(','):
                s = np.pi / 180 * i
                a = float(x) * sin(s)
                b = float(x) * cos(s)
                c = licznik
                i = i + 1
                one_point = [c] + [a] + [b]
                dane_pointcloud.append(one_point)
        lidar_data_file.close()

        f = open(path + '/danePointcloud.csv', 'w')
        f_csv = csv.writer(f)
        f_csv.writerows(dane_pointcloud)
        f.close()
        print 'Zakończono'

        klaudzik = []
        klaudzik_file = open(path + '/danePointcloud.csv', 'r')
        for line in klaudzik_file:
            xyz = np.matrix([[float(x) for x in line.split(',')[0:3]]])
            klaudzik.append(xyz)
        klaudzik_file.close()

        print 'Zakończono'
        klaudzik = np.array(klaudzik)
        plot_item = gl.GLScatterPlotItem(pos=klaudzik, size=1, color=[0.7, 0.7, 0.7, 1], pxMode=True)
        plot_item.translate(5, 5, 0)
        if self.pointcloudArea_2.items.__len__() > 0:
            for i in range(0, self.pointcloudArea_2.items.__len__()):
                self.pointcloudArea_2.items.__delitem__(i)

        self.pointcloudArea_2.addItem(plot_item)
        print 'Zakończono :DDDD'








    def build_pointcloud(self):
        self.new_thread = BuildPointcloudThread(   str(dir_lidar),
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

