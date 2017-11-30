# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import sys
import MainWindowDesign
import SelectDataWindowDesign
import ViewSettingWindowDesign
from buildPointCloudThread import *
import numpy as np
from Tkinter import *
import csv
from math import sin, cos, atanh, asinh, sqrt, pi, tan, sinh, atan, cosh
from transform import so3_to_euler
from image import*
from camera_model import *
from datetime import datetime as dt
from view_images_threads import *
from matplotlib import pyplot

import warnings
from numpy.linalg import norm
from quaternion import Quaternion


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class MadgwickAHRS:
    samplePeriod = 1./50
    quaternion = Quaternion(1, 0, 0, 0)
    beta = 0.3

    def __init__(self, sampleperiod=None, quaternion=None, beta=None):
        """
        Initialize the class with the given parameters.
        :param sampleperiod: The sample period
        :param quaternion: Initial quaternion
        :param beta: Algorithm gain beta
        :return:
        """
        if sampleperiod is not None:
            self.samplePeriod = sampleperiod
        if quaternion is not None:
            self.quaternion = quaternion
        if beta is not None:
            self.beta = float(beta)

    def update(self, gyroscope, accelerometer, magnetometer):
        """
        Perform one update step with data from a AHRS sensor array
        :param gyroscope: A three-element array containing the gyroscope data in radians per second.
        :param accelerometer: A three-element array containing the accelerometer data. Can be any unit since a normalized value is used.
        :param magnetometer: A three-element array containing the magnetometer data. Can be any unit since a normalized value is used.
        :return:
        """
        q = self.quaternion

        gyroscope = np.array(gyroscope, dtype=float).flatten()
        accelerometer = np.array(accelerometer, dtype=float).flatten()
        magnetometer = np.array(magnetometer, dtype=float).flatten()

        # Normalise accelerometer measurement
        if norm(accelerometer) is 0:
            warnings.warn("accelerometer is zero")
            return
        accelerometer /= norm(accelerometer)

        # Normalise magnetometer measurement
        if norm(magnetometer) is 0:
            warnings.warn("magnetometer is zero")
            return
        magnetometer /= norm(magnetometer)

        h = q * (Quaternion(0, magnetometer[0], magnetometer[1], magnetometer[2]) * q.conj())
        b = np.array([0, norm(h[1:3]), 0, h[3]])

        # Gradient descent algorithm corrective step
        f = np.array([
            2*(q[1]*q[3] - q[0]*q[2]) - accelerometer[0],
            2*(q[0]*q[1] + q[2]*q[3]) - accelerometer[1],
            2*(0.5 - q[1]**2 - q[2]**2) - accelerometer[2],
            2*b[1]*(0.5 - q[2]**2 - q[3]**2) + 2*b[3]*(q[1]*q[3] - q[0]*q[2]) - magnetometer[0],
            2*b[1]*(q[1]*q[2] - q[0]*q[3]) + 2*b[3]*(q[0]*q[1] + q[2]*q[3]) - magnetometer[1],
            2*b[1]*(q[0]*q[2] + q[1]*q[3]) + 2*b[3]*(0.5 - q[1]**2 - q[2]**2) - magnetometer[2]
        ])
        j = np.array([
            [-2*q[2],                  2*q[3],                  -2*q[0],                  2*q[1]],
            [2*q[1],                   2*q[0],                  2*q[3],                   2*q[2]],
            [0,                        -4*q[1],                 -4*q[2],                  0],
            [-2*b[3]*q[2],             2*b[3]*q[3],             -4*b[1]*q[2]-2*b[3]*q[0], -4*b[1]*q[3]+2*b[3]*q[1]],
            [-2*b[1]*q[3]+2*b[3]*q[1], 2*b[1]*q[2]+2*b[3]*q[0], 2*b[1]*q[1]+2*b[3]*q[3],  -2*b[1]*q[0]+2*b[3]*q[2]],
            [2*b[1]*q[2],              2*b[1]*q[3]-4*b[3]*q[1], 2*b[1]*q[0]-4*b[3]*q[2],  2*b[1]*q[1]]
        ])
        step = j.T.dot(f)
        step /= norm(step)  # normalise step magnitude

        # Compute rate of change of quaternion
        qdot = (q * Quaternion(0, gyroscope[0], gyroscope[1], gyroscope[2])) * 0.5 - self.beta * step.T

        # Integrate to yield quaternion
        q += qdot * self.samplePeriod
        self.quaternion = Quaternion(q / norm(q))  # normalise quaternion

    def update_imu(self, gyroscope, accelerometer):
        """
        Perform one update step with data from a IMU sensor array
        :param gyroscope: A three-element array containing the gyroscope data in radians per second.
        :param accelerometer: A three-element array containing the accelerometer data. Can be any unit since a normalized value is used.
        """
        q = self.quaternion

        gyroscope = np.array(gyroscope, dtype=float).flatten()
        accelerometer = np.array(accelerometer, dtype=float).flatten()

        # Normalise accelerometer measurement
        if norm(accelerometer) is 0:
            warnings.warn("accelerometer is zero")
            return
        accelerometer /= norm(accelerometer)

        # Gradient descent algorithm corrective step
        f = np.array([
            2*(q[1]*q[3] - q[0]*q[2]) - accelerometer[0],
            2*(q[0]*q[1] + q[2]*q[3]) - accelerometer[1],
            2*(0.5 - q[1]**2 - q[2]**2) - accelerometer[2]
        ])
        j = np.array([
            [-2*q[2], 2*q[3], -2*q[0], 2*q[1]],
            [2*q[1], 2*q[0], 2*q[3], 2*q[2]],
            [0, -4*q[1], -4*q[2], 0]
        ])
        step = j.T.dot(f)
        step /= norm(step)  # normalise step magnitude

        # Compute rate of change of quaternion
        qdot = (q * Quaternion(0, gyroscope[0], gyroscope[1], gyroscope[2])) * 0.5 - self.beta * step.T

        # Integrate to yield quaternion
        q += qdot * self.samplePeriod
        self.quaternion = Quaternion(q / norm(q))  # normalise quaternion


class SelectDataWindow(QtGui.QDialog, SelectDataWindowDesign.Ui_Dialog):
    def __init__(self):
        # Using super allows us to
        # access variables, methods etc in the MainWindowDesign.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in MainWindowDesign.py file automatically
                            # It sets up layout and widgets that are defined
        try:
            self.read_dialog1()      # Jak nie ma jeszcze default.txt
        except:
            pass
        self.browseButton1.clicked.connect(self.browse1)
        self.browseButton2.clicked.connect(self.browse2)
        self.browseButton3.clicked.connect(self.browse3)
        self.browseButton4.clicked.connect(self.browse4)
        self.browseButton5.clicked.connect(self.browse5)
        self.browseButton6.clicked.connect(self.browse6)
        self.browseButton7.clicked.connect(self.browse7)
        self.browseButton8.clicked.connect(self.browse8)
        self.browseButton9.clicked.connect(self.browse9)
        self.browseButton10.clicked.connect(self.browse10)
        self.buttonBoxDataSet.accepted.connect(self.wersja_sdk)
        self.buttonBoxCustom.accepted.connect(self.wersja_custom)
        self.pointToImageBox.clicked.connect(self.point3d_checked)
        self.choosePoseKind.currentIndexChanged.connect(self.disable_or_enable)
        self.disable_or_enable(self.choosePoseKind.currentIndex())


    def point3d_checked(self):
        self.startTimeImg.setText("0")

    def disable_or_enable(self, id):
        if id == 1:
            self.choosePoseDataImu.setDisabled(True)
            self.choosePoseExtrImu.setDisabled(True)
            self.choosePoseDataVo.setEnabled(True)
            self.choosePoseExtrVo.setEnabled(True)
            self.skalaVO.setEnabled(True)
            self.beta.setDisabled(True)
        elif id == 3:
            self.choosePoseDataImu.setEnabled(True)
            self.choosePoseExtrImu.setEnabled(True)
            self.choosePoseDataVo.setDisabled(True)
            self.choosePoseExtrVo.setDisabled(True)
            self.skalaVO.setDisabled(True)
            self.beta.setEnabled(True)
        elif id == 2:
            self.choosePoseDataImu.setEnabled(True)
            self.choosePoseExtrImu.setDisabled(True)
            self.choosePoseDataVo.setEnabled(True)
            self.choosePoseExtrVo.setEnabled(True)
            self.skalaVO.setEnabled(True)
            self.beta.setEnabled(True)
        else:
            self.choosePoseDataImu.setEnabled(True)
            self.choosePoseExtrImu.setEnabled(True)
            self.choosePoseDataVo.setEnabled(True)
            self.choosePoseExtrVo.setEnabled(True)
            self.skalaVO.setEnabled(True)
            self.beta.setEnabled(True)

    def wersja_sdk(self):
        global sdk
        sdk = True
        self.save_dialog1()

    def wersja_custom(self):
        global sdk
        sdk = False
        self.save_dialog1()

    # Oczyszczanie i zapisywanie wszystkich danych z tzw. "formularzy" do pliku "defaultDir.txt"
    def save_dialog1(self):
        global dir_data_f, dir_extr_f, dir_models_f, dir_ins, dir_lidar, dir_camera, start_time, end_time, ki
        global dir_lidar_data_custom, dir_lidar_extr, lidar_synch_time, dir_pose_data_vo, dir_pose_extr_vo, pose_kind
        global skala_vo, clear_h, clear_roll, clear_pitch, pose_synch_time, start_time_custom, end_time_custom
        global camera, undistort, point3d, img_start_time, img_end_time, dir_image_custom, img_start_time_custom
        global img_end_time_custom, point3d_custom, beta_value, dir_pose_extr_imu, dir_pose_data_imu

        ki = 1
        dir_data_f = self.chooseDataFolder.text()
        dir_extr_f = self.chooseExtrFolder.text()
        dir_models_f = self.chooseModelsFolder.text()
        start_time = self.startTimeF.text()
        end_time = self.endTimeF.text()
        img_start_time = self.startTimeImg.text()
        img_end_time = self.endTimeImg.text()
        img_start_time_custom = self.startTimeImgCustom.text()
        img_end_time_custom = self.endTimeImgCustom.text()

        dir_lidar_data_custom = self.chooseLidarData.text()
        dir_lidar_extr = self.chooseLidarExtr.text()
        lidar_synch_time = self.synchLidarTime.text()
        dir_pose_data_vo = self.choosePoseDataVo.text()
        dir_pose_extr_vo = self.choosePoseExtrVo.text()
        dir_pose_data_imu = self.choosePoseDataImu.text()
        dir_pose_extr_imu = self.choosePoseExtrImu.text()
        dir_image_custom = self.chooseImgData.text()
        pose_synch_time = self.synchPoseTime.text()
        skala_vo = self.skalaVO.text()
        start_time_custom = self.startTimeCustom.text()
        end_time_custom = self.endTimeCustom.text()
        beta_value = self.beta.text()

        dir_data_f = dir_data_f.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_extr_f = dir_extr_f.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_models_f = dir_models_f.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_lidar_data_custom = dir_lidar_data_custom.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_lidar_extr = dir_lidar_extr.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_pose_data_vo = dir_pose_data_vo.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_pose_extr_vo = dir_pose_extr_vo.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_pose_data_imu = dir_pose_data_imu.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_pose_extr_imu = dir_pose_extr_imu.replace('\r', "").replace('\n', "").replace('file://', "")
        dir_image_custom = dir_image_custom.replace('\r', "").replace('\n', "").replace('file://', "")
        start_time = start_time.replace('\r', "").replace('\n', "")
        end_time = end_time.replace('\r', "").replace('\n', "")
        img_start_time = img_start_time.replace('\r', "").replace('\n', "")
        img_end_time = img_end_time.replace('\r', "").replace('\n', "")
        img_start_time_custom = img_start_time_custom.replace('\r', "").replace('\n', "")
        img_end_time_custom = img_end_time_custom.replace('\r', "").replace('\n', "")
        lidar_synch_time = lidar_synch_time.replace('\r', "").replace('\n', "")
        pose_synch_time = pose_synch_time.replace('\r', "").replace('\n', "")
        skala_vo = skala_vo.replace('\r', "").replace('\n', "")
        start_time_custom = start_time_custom.replace('\r', "").replace('\n', "")
        end_time_custom = end_time_custom.replace('\r', "").replace('\n', "")
        beta_value = beta_value.replace('\r', "").replace('\n', "")

        camera = self.chooseCamera.currentText()
        dir_lidar = dir_data_f + "/" + self.chooseLidar.currentText()
        dir_camera = dir_data_f + "/" + self.chooseCamera.currentText()
        undistort = self.distortBox.isChecked()
        point3d = self.pointToImageBox.isChecked()
        point3d_custom = self.pointToImageBoxCustom.isChecked()
        if self.choosePoseF.currentIndex() == 1:
            dir_ins = dir_data_f + "/gps/ins.csv"
        else:
            dir_ins = dir_data_f + "/vo/vo.csv"
        pose_kind = self.choosePoseKind.currentIndex()
        clear_h = self.clearHeight.isChecked()
        clear_roll = self.clearRoll.isChecked()
        clear_pitch = self.clearPitch.isChecked()

        f = open('defaultDir.txt', 'w')
        lines = [dir_data_f, "\n", dir_extr_f, "\n", dir_models_f, "\n",
                 str(self.chooseLidar.currentIndex()), "\n", str(self.chooseCamera.currentIndex()),
                 "\n", str(undistort),"\n",str(point3d),"\n", str(point3d_custom), "\n", str(self.choosePoseF.currentIndex()), "\n", start_time,
                 "\n", end_time,"\n", img_start_time,"\n", img_end_time, "\n", img_start_time_custom, "\n", img_end_time_custom, "\n",
                 dir_lidar_data_custom, "\n", dir_lidar_extr, "\n", dir_pose_data_vo, "\n", dir_pose_extr_vo,"\n", dir_pose_data_imu, "\n",
                 dir_pose_extr_imu, "\n", dir_image_custom, "\n", lidar_synch_time, "\n", pose_synch_time,"\n", skala_vo, "\n", str(pose_kind),
                 "\n", str(clear_h),"\n", str(clear_roll), "\n", str(clear_pitch), "\n", start_time_custom, "\n", end_time_custom, "\n", beta_value]
        f.writelines(lines)
        f.close()
        try:
            self.count_time()
        except:
            pass

    # Dla danych z SDK - wyliczanie potrzebnych "czasów" jakby ktoś ograniczył zakres wyświetlania pointclouda
    def count_time(self):
        global real_end_time, real_start_time, real_img_start_time, real_img_end_time
        path = dir_lidar + '.timestamps'
        f = open(path, 'r')
        x = f.readline()
        real_start_time = int(x.split()[0]) + int(start_time) * 1000
        real_img_start_time = real_start_time + int(img_start_time) * 1000
        f.close()
        real_end_time = int(real_start_time) + int(end_time) * 1000
        real_img_end_time = int(real_img_start_time) + int(img_end_time) * 1000

    # Czytanie i wypisywanie danych z pliku "defaultDir.txt" do tzw. "formularzy"
    def read_dialog1(self):
        f = open('defaultDir.txt', 'r')
        self.chooseDataFolder.setText(f.readline())
        self.chooseExtrFolder.setText(f.readline())
        self.chooseModelsFolder.setText(f.readline())
        self.chooseLidar.setCurrentIndex(int(f.readline()))
        self.chooseCamera.setCurrentIndex(int(f.readline()))
        if f.readline().replace('\n',"") == 'True':
            self.distortBox.setChecked(True)
        else:
            self.distortBox.setChecked(False)
        if f.readline().replace('\n',"") == 'True':
            self.pointToImageBox.setChecked(True)
        else:
            self.pointToImageBox.setChecked(False)
        if f.readline().replace('\n',"") == 'True':
            self.pointToImageBoxCustom.setChecked(True)
        else:
            self.pointToImageBoxCustom.setChecked(False)
        self.choosePoseF.setCurrentIndex(int(f.readline()))
        self.startTimeF.setText(f.readline())
        self.endTimeF.setText(f.readline())
        self.startTimeImg.setText(f.readline())
        self.endTimeImg.setText(f.readline())
        self.startTimeImgCustom.setText(f.readline())
        self.endTimeImgCustom.setText(f.readline())
        self.chooseLidarData.setText(f.readline())
        self.chooseLidarExtr.setText(f.readline())
        self.choosePoseDataVo.setText(f.readline())
        self.choosePoseExtrVo.setText(f.readline())
        self.choosePoseDataImu.setText(f.readline())
        self.choosePoseExtrImu.setText(f.readline())
        self.chooseImgData.setText(f.readline())
        self.synchLidarTime.setText(f.readline())
        self.synchPoseTime.setText(f.readline())
        self.skalaVO.setText(f.readline())
        self.choosePoseKind.setCurrentIndex(int(f.readline()))
        if f.readline().replace('\n',"") == 'True':
            self.clearHeight.setChecked(True)
        else:
            self.clearHeight.setChecked(False)
        if f.readline().replace('\n',"") == 'True':
            self.clearRoll.setChecked(True)
        else:
            self.clearRoll.setChecked(False)
        if f.readline().replace('\n',"") == 'True':
            self.clearPitch.setChecked(True)
        else:
            self.clearPitch.setChecked(False)
        self.startTimeCustom.setText(f.readline())
        self.endTimeCustom.setText(f.readline())
        self.beta.setText(f.readline())
        f.close()

    # Masa guzików "browse" - najprościej jak umiałem nie chciałem się zastanawiać godzinami
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

    def browse4(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.chooseLidarData.setText(directory)

    def browse5(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.chooseLidarExtr.setText(directory)

    def browse6(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.choosePoseDataVo.setText(directory)

    def browse7(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.choosePoseExtrVo.setText(directory)

    def browse8(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.chooseImgData.setText(directory)

    def browse9(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.choosePoseDataImu.setText(directory)

    def browse10(self):
        from tkFileDialog import askdirectory
        Tk().withdraw()
        directory = askdirectory()
        self.choosePoseExtrImu.setText(directory)


class SettingsWindow(QtGui.QDialog, ViewSettingWindowDesign.Ui_Dialog):
    def __init__(self):
        # Using super allows us to
        # access variables, methods etc in the MainWindowDesign.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in MainWindowDesign.py file automatically
                            # It sets up layout and widgets that are defined
        try:
            self.read_dialog2()
        except:
            pass
        self.buttonBox.accepted.connect(self.save_dialog2)


    def save_dialog2(self):
        global uw, pixel_mode, points_colour, points_size

        uw = self.checkBoxUW.isChecked()
        pixel_mode = self.checkBoxPixel.isChecked()
        points_colour = self.checkBoxColors.isChecked()
        points_size = self.choosePointsSize.text()

        points_size = points_size.replace('\r', "").replace('\n', "")

        f = open('defaultSettings.txt', 'w')
        lines = [str(uw), "\n", str(pixel_mode), "\n", str(points_colour), "\n", points_size]
        f.writelines(lines)
        f.close()

    def read_dialog2(self):
        f = open('defaultSettings.txt', 'r')
        if f.readline().replace('\n',"") == 'True':
            self.checkBoxUW.setChecked(True)
        else:
            self.checkBoxUW.setChecked(False)
        if f.readline().replace('\n',"") == 'True':
            self.checkBoxPixel.setChecked(True)
        else:
            self.checkBoxPixel.setChecked(False)
        if f.readline().replace('\n',"") == 'True':
            self.checkBoxColors.setChecked(True)
        else:
            self.checkBoxColors.setChecked(False)
        self.choosePointsSize.setText(f.readline())
        f.close()


class Application(QtGui.QMainWindow, MainWindowDesign.Ui_MainWindow):
    def __init__(self):
        pg.setConfigOptions(imageAxisOrder='row-major')
        # Using super allows us to
        # access variables, methods etc in the MainWindowDesign.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in MainWindowDesign.py file automatically
                            # It sets up layout and widgets that are defined
        self.pointcloudButton.clicked.connect(self.build_pointcloud)
        self.selectDataButton.clicked.connect(self.open_select_data)
        self.settingButton.clicked.connect(self.open_settings)
        self.imageButton.clicked.connect(self.view_images)
        self.lidarDataButton.clicked.connect(self.show_lidar_data)
        self.pointcloud = None

        #Ukryj niepotrzebne przyciski
        self.imageView.ui.roiBtn.hide()
        self.imageView.ui.menuBtn.hide()
        #Ukryj histogram
        self.imageView.ui.histogram.item.close()
        self.imageView.ui.histogram.setFixedWidth(1)

        try:
            SettingsWindow().save_dialog2()                         # Zapisanie ustawień defaultSettings.txt
        except:
            pass


    def open_select_data(self):
        self.dialog = SelectDataWindow()
        self.dialog.show()

    def open_settings(self):
        self.dialog = SettingsWindow()
        self.dialog.show()



#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

    # Wyświetla dane z lidaru w linii prostej aż do "Zakończono funkcję step by step :DDDD"
    def show_lidar_data(self):

        path = os.path.split(str(dir_lidar_data_custom))[0]
        dane_lidar = []
        lidar_data_file = open(dir_lidar_data_custom, 'r')
        for line in lidar_data_file:
            try:
                one_scan = [float(x) for x in line.split(',')[11:282]]
                dane_lidar.append(one_scan)
            except:
                pass
        lidar_data_file.close()

        f = open(path + '/dane_odleglosci_lidar.csv', 'w')
        f_csv = csv.writer(f)
        f_csv.writerows(dane_lidar)
        f.close()
        print 'Utworzono plik dane_odległosci_lidar.csv'

        licznik = -50
        dane_pointcloud = []
        lidar_data_file = open(path + '/dane_odleglosci_lidar.csv', 'r')
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
        print 'Utworzono plik danePointcloud.csv'

        klaudzik = []
        klaudzik_file = open(path + '/danePointcloud.csv', 'r')
        for line in klaudzik_file:
            xyz = np.matrix([[float(x) for x in line.split(',')[0:3]]])
            klaudzik.append(xyz)
        klaudzik_file.close()


        klaudzik = np.array(klaudzik)
        plot_item = gl.GLScatterPlotItem(pos=klaudzik, size=1, color=[0.7, 0.7, 0.7, 1], pxMode=True)
        plot_item.translate(5, 5, 0)
        if self.pointcloudArea.items.__len__() > 0:
            for i in range(0, self.pointcloudArea.items.__len__()):
                self.pointcloudArea.items.__delitem__(0)

        self.pointcloudArea.addItem(plot_item)
        print 'Zakończono funkcję step by step :DDDD'

    # Działa bardzo dobrze
    def madgwick_gyro_akc(self):
        k0 = 0.9996
        e = 0.081819
        AA = 6367449.15
        alpha1 = 0.0008377318
        alpha2 = 7.60852780571568E-07
        alpha3 = 1.19764551083372E-09
        alpha4 = 2.42917070093028E-12
        alpha5 = 5.71181842951141E-15
        alpha6 = 1.47999804582115E-17
        zone = 21

        dane_gps = []
        sensors_file = open(dir_pose_data_imu, 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                next_data = [float(x) for x in line.split(',')[2:5]]
                try:
                    x = np.linspace(last_data[0], next_data[0], 15)
                    y = np.linspace(last_data[1], next_data[1], 15)
                    # z = np.linspace(last_data[2], next_data[2], 15)
                    for j in range(0, 15, 1):
                        kH = (y[j] - zone) * np.pi / 180
                        kJ = x[j] * np.pi / 180
                        kM = sinh(e * atanh(e * tan(kJ) / sqrt(1 + tan(kJ) * tan(kJ))))
                        kO = atan(tan(kJ) * sqrt(1 + kM * kM) - kM * sqrt(1 + tan(kJ) * tan(kJ)))
                        kQ = atan(tan(kO) / cos(kH))
                        kR = asinh(sin(kH) / sqrt(tan(kO) * tan(kO) + (cos(kH) * cos(kH))))
                        kS = kQ + alpha1 * sin(2 * kQ) * cosh(2 * kR) + alpha2 * sin(4 * kQ) * cosh(
                            4 * kR) + alpha3 * sin(6 * kQ) * cosh(6 * kR) + alpha4 * sin(8 * kQ) * cosh(
                            8 * kR) + alpha5 * sin(10 * kQ) * cosh(10 * kR) + alpha6 * sin(12 * kQ) * cosh(12 * kR)
                        kT = kR + alpha1 * cos(2 * kQ) * sinh(2 * kR) + alpha2 * cos(4 * kQ) * sinh(
                            4 * kR) + alpha3 * cos(6 * kQ) * sinh(6 * kR) + alpha4 * cos(8 * kQ) * sinh(
                            8 * kR) + alpha5 * cos(10 * kQ) * sinh(10 * kR) + alpha6 * cos(12 * kQ) * sinh(12 * kR)
                        kU = k0 * AA * kT
                        kV = k0 * AA * kS
                        kW = 500000
                        easting = kU + kW
                        if kV > 0:
                            northing = kV
                        else:
                            northing = kV + 10000000
                        xyz = [northing, easting, 0]
                        dane_gps.append(xyz)
                    last_data = next_data
                except:
                    last_data = next_data
        if len(dane_gps) == 0:
            raise ValueError("No GPS data found")
        sensors_file.close()
        print 'Ilość pozycji z GPS:'
        len(dane_gps)


        start = False
        dane_akc = []
        dane_gyro = []
        sensors_file = open(dir_pose_data_imu, 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                start = True
                akc = [-(float(line.split(',')[7]))] + [-(float(line.split(',')[6]))] + [float(line.split(',')[8])]
                gyro = [-(float(line.split(',')[11]))] + [-(float(line.split(',')[10]))] + [float(line.split(',')[12])]
                dane_akc.append(akc)
                dane_gyro.append(gyro)
            if start == True and int(id) != 1 and line.split(',')[6:9] != [] and line.split(',')[
                                                                                 6:9] != ['', '', '']:
                akc = [-(float(line.split(',')[3]))] + [-(float(line.split(',')[2]))] + [float(line.split(',')[4])]
                gyro = [-(float(line.split(',')[7]))] + [-(float(line.split(',')[6]))] + [float(line.split(',')[8])]
                dane_akc.append(akc)
                dane_gyro.append(gyro)
        sensors_file.close()


        euler = []
        AHRS = MadgwickAHRS(None, None, beta_value)
        for i in range(len(dane_akc)):
            AHRS.update_imu(dane_gyro[i], dane_akc[i])
            euler.append(Quaternion.to_euler123(Quaternion.conj(AHRS.quaternion)))

        # Do wykreślenia kąta yaw na wykresie
        yaw = []
        for i in range(len(euler)):
            yaw.append(-euler[i][2] * 180 / pi)
        #pyplot.plot(range(len(yaw)), yaw)
        #pyplot.grid()
        #pyplot.show()

        j = 0
        dane_imu = []
        for i in range(len(euler)):
            if j >= 3:
                dane_imu.append([euler[i][0], euler[i][1], -euler[i][2]])
                j = 0
            j = j + 1
        if clear_roll == True:
            for i in range(len(dane_imu)):
                dane_imu[i][0] = 0
        if clear_pitch == True:
            for i in range(len(dane_imu)):
                dane_imu[i][1] = 0

        # Czas do poses.csv
        dane_time = []
        for i in range(0, len(dane_gps), 1):
            dane_time.append([str(i * 66666)])


        # Stworzenie poses i obciecie ewentualnych poczatkowycyh pomiarow
        dane = []
        poses_file = open('poses.csv', 'w')
        csv_poses_file = csv.writer(poses_file)
        odjemnik = 0
        for i in range(0, len(dane_time), 1):
            if float(dane_time[i][0]) < float(pose_synch_time) * 1000:
                odjemnik = float(dane_time[i][0])
            else:
                dane.append([float(dane_time[i][0]) - odjemnik] + dane_gps[i] + dane_imu[i])
        csv_poses_file.writerows(dane)
        poses_file.close()
        print 'Utworzono plik poses.csv'

    # Sprawdzone
    def marek_wersja_1(self):
        skala = float(skala_vo)
        dane_xyz = []
        dane_imu = []
        poses_times = []
        sensors_file = open(dir_pose_data_vo, 'r')  ##ścieżka do pliku vo
        for line in sensors_file:
            try:

                vector = [float(x) for x in line.split(',')[0:13]]
                macierzR = np.matrix([vector[4:7], vector[7:10], vector[10:13]])
                #print macierzR
                rpy = so3_to_euler(macierzR)
                if clear_h == True:
                    vector[2] = 0
                if clear_roll == True:
                    rpy[0,2] = 0
                if clear_pitch == True:
                    rpy[0,0] = 0
                dane_xyz.append([vector[1]*skala, vector[2]*skala, vector[3]*skala])
                dane_imu.append([rpy[0,0], rpy[0, 1], rpy[0,2]])
                poses_times.append([vector[0]*1000000])
            except:
                pass
        if len(dane_xyz) == 0:
            raise ValueError("No VO data found")
        sensors_file.close()

        # stworzenie poses i obciecie ewentualnych poczatkowycyh pomiarow
        dane = []
        poses_file = open('poses.csv', 'w')
        csv_poses_file = csv.writer(poses_file)
        if len(dane_xyz) >= poses_times:
            t = len(poses_times)
        else:
            t = len(dane_xyz)
        odjemnik = 0
        for i in range(0, t, 1):
            if poses_times[i][0] < float(pose_synch_time)*1000:
                odjemnik = poses_times[i][0]
            else:
                dane.append([poses_times[i][0]-odjemnik] + dane_xyz[i] + dane_imu[i])
        csv_poses_file.writerows(dane)
        poses_file.close()
        print 'Utworzono plik poses.csv'

    # Trajektoria vo kąty IMU
    def vo_imu(self):
        skala = float(skala_vo)
        dane_xyz = []
        dane_imu = []
        poses_times = []
        sensors_file = open(dir_pose_data_vo, 'r')  ##ścieżka do pliku vo
        for line in sensors_file:
            try:
                vector = [float(x) for x in line.split(',')[0:13]]
                macierzR = np.matrix([vector[4:7], vector[7:10], vector[10:13]])
                #print macierzR
                rpy = so3_to_euler(macierzR)
                if clear_h == True:
                    vector[2] = 0
                if clear_roll == True:
                    rpy[0,2] = 0
                if clear_pitch == True:
                    rpy[0,0] = 0
                dane_xyz.append([vector[1]*skala, vector[2]*skala, vector[3]*skala])
                dane_imu.append([rpy[0,0], rpy[0, 1], rpy[0,2]])
                poses_times.append([vector[0]*1000000])
            except:
                pass
        if len(dane_xyz) == 0:
            raise ValueError("No VO data found")
        sensors_file.close()

        print len(dane_xyz)

        start = False
        dane_akc = []
        dane_gyro = []
        sensors_file = open(dir_pose_data_imu, 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                start = True
                akc = [-(float(line.split(',')[7]))] + [-(float(line.split(',')[6]))] + [float(line.split(',')[8])]
                gyro = [-(float(line.split(',')[11]))] + [-(float(line.split(',')[10]))] + [float(line.split(',')[12])]
                dane_akc.append(akc)
                dane_gyro.append(gyro)
            if start == True and int(id) != 1 and line.split(',')[6:9] != [] and line.split(',')[
                                                                                 6:9] != ['', '', '']:
                akc = [-(float(line.split(',')[3]))] + [-(float(line.split(',')[2]))] + [float(line.split(',')[4])]
                gyro = [-(float(line.split(',')[7]))] + [-(float(line.split(',')[6]))] + [float(line.split(',')[8])]
                dane_akc.append(akc)
                dane_gyro.append(gyro)
        sensors_file.close()

        euler = []
        AHRS = MadgwickAHRS(None, None, beta_value)
        for i in range(len(dane_akc)):
            AHRS.update_imu(dane_gyro[i], dane_akc[i])
            euler.append(Quaternion.to_euler123(Quaternion.conj(AHRS.quaternion)))

        # Do wykreślenia kąta yaw na wykresie
        yaw = []
        for i in range(len(euler)):
            yaw.append(euler[i][2] * 180 / pi)
        #pyplot.plot(range(len(yaw)), yaw)
        #pyplot.grid()
        #pyplot.show()

        j = 0
        dane_imu = []
        for i in range(len(euler)):
            if j >= 11:
                dane_imu.append([euler[i][0], euler[i][2], euler[i][1]])
                j = 0
            j = j + 1
        if clear_roll == True:
            for i in range(len(dane_imu)):
                dane_imu[i][0] = 0
        if clear_pitch == True:
            for i in range(len(dane_imu)):
                dane_imu[i][2] = 0


        # stworzenie poses i obciecie ewentualnych poczatkowycyh pomiarow
        dane = []
        poses_file = open('poses.csv', 'w')
        csv_poses_file = csv.writer(poses_file)
        if len(dane_xyz) >= poses_times:
            t = len(poses_times)
        else:
            t = len(dane_xyz)
        odjemnik = 0
        for i in range(0, t, 1):
            if poses_times[i][0] < float(pose_synch_time)*1000:
                odjemnik = poses_times[i][0]
            else:
                dane.append([poses_times[i][0]-odjemnik] + dane_xyz[i] + dane_imu[i])
        csv_poses_file.writerows(dane)
        poses_file.close()
        print 'Utworzono plik poses.csv'


# ^^^^^^^^^^^^^^^ Używane funkcje do oblicznia pliku poses.csv ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS


    # Obliczanie Yaw na podstawie GPS-a, działa dobrze, efekt taki sobie
    def gps15_yaw(self):
        k0 = 0.9996
        e = 0.081819
        AA = 6367449.15
        alpha1 = 0.0008377318
        alpha2 = 7.60852780571568E-07
        alpha3 = 1.19764551083372E-09
        alpha4 = 2.42917070093028E-12
        alpha5 = 5.71181842951141E-15
        alpha6 = 1.47999804582115E-17
        zone = 21

        dane_gps = []
        sensors_file = open(dir_pose_data_imu, 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                next_data = [float(x) for x in line.split(',')[2:5]]
                try:
                    x = np.linspace(last_data[0], next_data[0], 15)
                    y = np.linspace(last_data[1], next_data[1], 15)
                    # z = np.linspace(last_data[2], next_data[2], 15)
                    for j in range(0, 15, 1):
                        kH = (y[j] - zone) * np.pi / 180
                        kJ = x[j] * np.pi / 180
                        kM = sinh(e * atanh(e * tan(kJ) / sqrt(1 + tan(kJ) * tan(kJ))))
                        kO = atan(tan(kJ) * sqrt(1 + kM * kM) - kM * sqrt(1 + tan(kJ) * tan(kJ)))
                        kQ = atan(tan(kO) / cos(kH))
                        kR = asinh(sin(kH) / sqrt(tan(kO) * tan(kO) + (cos(kH) * cos(kH))))
                        kS = kQ + alpha1 * sin(2 * kQ) * cosh(2 * kR) + alpha2 * sin(4 * kQ) * cosh(
                            4 * kR) + alpha3 * sin(6 * kQ) * cosh(6 * kR) + alpha4 * sin(8 * kQ) * cosh(
                            8 * kR) + alpha5 * sin(10 * kQ) * cosh(10 * kR) + alpha6 * sin(12 * kQ) * cosh(12 * kR)
                        kT = kR + alpha1 * cos(2 * kQ) * sinh(2 * kR) + alpha2 * cos(4 * kQ) * sinh(
                            4 * kR) + alpha3 * cos(6 * kQ) * sinh(6 * kR) + alpha4 * cos(8 * kQ) * sinh(
                            8 * kR) + alpha5 * cos(10 * kQ) * sinh(10 * kR) + alpha6 * cos(12 * kQ) * sinh(12 * kR)
                        kU = k0 * AA * kT
                        kV = k0 * AA * kS
                        kW = 500000
                        easting = kU + kW
                        if kV > 0:
                            northing = kV
                        else:
                            northing = kV + 10000000
                        xyz = [northing, easting, 0]
                        dane_gps.append(xyz)
                    last_data = next_data
                except:
                    last_data = next_data
        if len(dane_gps) == 0:
            raise ValueError("No GPS data found")
        sensors_file.close()
        print 'Ilość pozycji z GPS:'
        print len(dane_gps)

        ### Obliczanie YAW na podstawie GPS-a
        dane_imu = []
        prosta_odniesienia = (0 - 0) / (0 - 5)
        for i in range(len(dane_gps) - 1):
            try:
                [xA, yA, zA] = dane_gps[i]
                [xB, yB, zB] = dane_gps[i + 1]
                a2 = (yA - yB) / (xA - xB)
                yaw = np.arctan(((prosta_odniesienia - a2) / (1 + prosta_odniesienia * a2)))
            except:
                pass
            dane_imu.append([0, 0, -yaw])
        dane_imu.append([0, 0, 0])

        if clear_roll == True:
            for i in range(len(dane_imu)):
                dane_imu[i][0] = 0
        if clear_pitch == True:
            for i in range(len(dane_imu)):
                dane_imu[i][1] = 0


            ### Czas do poses.csv
        dane_time = []
        for i in range(0, len(dane_gps), 1):
            dane_time.append([str(i * 66666)])


            ### Stworzenie poses i obciecie ewentualnych poczatkowycyh pomiarow
        dane = []
        poses_file = open('poses.csv', 'w')
        csv_poses_file = csv.writer(poses_file)
        odjemnik = 0
        for i in range(0, len(dane_time), 1):
            if float(dane_time[i][0]) < float(pose_synch_time) * 1000:
                odjemnik = float(dane_time[i][0])
            else:
                dane.append([float(dane_time[i][0]) - odjemnik] + dane_gps[i] + dane_imu[i])
        csv_poses_file.writerows(dane)
        poses_file.close()
        print 'Utworzono plik poses.csv'

    # Wersja 2 jest podobna do 1, zmienione tylko że linspacem żeby było więcej danych z pozycji bez interpolacji, na razie nie działa
    def marek_wersja_2(self):
        path = os.path.split(str(dir_lidar_data_custom))[0]  ### ścieżka w Custom do danych z lidaru (nieobrobionych)
        dane_xyz = []
        dane_time = []
        dane_imu = []

        sensors_file = open(dir_pose_data, 'r')  ##ścieżka do pliku vo
        for line in sensors_file:
            try:
                vector = [float(x) for x in line.split(',')[0:13]]
                macierzR = np.matrix([vector[4:7], vector[7:10], vector[10:13]])
                print macierzR
                rpy = so3_to_euler(macierzR)

                roll = np.arctan2(vector[11], vector[12])
                pitch = np.arcsin(-vector[10])
                yaw = np.arctan2(vector[7], vector[4])
                if clear_h == True:
                    vector[2] = 0
                if clear_roll == True:
                    rpy[0, 2] = 0
                if clear_pitch == True:
                    rpy[0, 0] = 0

                next_data =[vector[1], vector[2], vector[3]]
            except:
                pass
            try:
                x = np.linspace(last_data[0], next_data[0], 3)
                y = np.linspace(last_data[1], next_data[1], 3)
                z = np.linspace(last_data[2], next_data[2], 3)
                for j in range(0, 3, 1):
                    xyz = [x[j], y[j], z[j]]
                    dane_xyz.append([vector[1], vector[2], vector[3]])
                    dane_imu.append([rpy[0, 0], rpy[0, 1], rpy[0, 2]])
            except:
                pass
            try:
                last_data = next_data
            except:
                pass
        if len(dane_xyz) == 0:
            raise ValueError("No VO data found")
        sensors_file.close()
        print 'Ilość pozycji XYZ:'
        print len(dane_xyz)

        pierwsza_wartosc = True
        time_file = open(str(dir_lidar_data_custom), 'r')
        for line in time_file:
            try:
                dane_time.append(float(line.split(',')[0]))
                if pierwsza_wartosc == True:
                    odjemnik = line.split(',')[0]
                    pierwsza_wartosc = False
            except:
                pass
        for i in range(len(dane_time)):
            dane_time[i] = [int(dane_time[i] - float(odjemnik))]

        time_file = open('plik.timestamps', 'w')
        csv_time_file = csv.writer(time_file)
        csv_time_file.writerows(dane_time)
        time_file.close()
        print "Utworzono plik.timestamps"

        dane = []
        ins_file = open('ins.csv', 'w')
        csv_ins_file = csv.writer(ins_file)
        if len(dane_xyz) >= dane_time:
            t = len(dane_time)
        else:
            t = len(dane_xyz)
        for i in range(0, t, 1):
            dane.append(dane_time[i] + dane_xyz[i] + dane_imu[i])
        csv_ins_file.writerows(dane)
        ins_file.close()
        print 'Utworzone plik ins.csv'

    # Dla mnie do testowania
    def test_ukl_wsp_scanu_lidaru(self):
        dane_lidar = []
        lidar_data_file = open(str(dir_lidar_data_custom), 'r')
        for line in lidar_data_file:
            try:
                one_scan = [float(x) for x in line.split(',')[11:282]]
                dane_lidar.append(one_scan)
            except:
                pass
        lidar_data_file.close()

        dane_odleglosci_path = os.path.split(str(dir_lidar_data_custom))[0] + '/dane_odleglosci_lidar.csv'
        print dane_odleglosci_path
        f = open(dane_odleglosci_path, 'w')
        f_csv = csv.writer(f)
        f_csv.writerows(dane_lidar)
        f.close()
        lidar_data_file = open(dane_odleglosci_path, 'r')
        i = 0
        for line in lidar_data_file:
            if i < 1:
                dane_pointcloud = []
                j = -45
                for x in line.split(','):
                    s = np.pi / 180 * j
                    a = float(x) * np.cos(s)
                    b = float(x) * np.sin(s)
                    j = j + 1
                    one_point = [a] + [b] + [0]
                    dane_pointcloud.append(one_point)
                dane_pointcloud = np.array(dane_pointcloud)
                scan = dane_pointcloud.transpose()
                scan = scan.transpose()
                plot_item = gl.GLScatterPlotItem(pos=scan, size=1, color=[0.7, 0.7, 0.7, 1], pxMode=True)
                self.pointcloudArea.addItem(plot_item)
                i = i + 1

        ukl_wsp_line_length = 3
        ukl_wsp_line_width = 4
        ukl_wsp_x = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [ukl_wsp_line_length, 0, 0]]), color=[1, 0, 0, 1],
                                      width=ukl_wsp_line_width,
                                      antialias=True, mode='lines')
        ukl_wsp_y = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, ukl_wsp_line_length, 0]]), color=[0, 1, 0, 1],
                                      width=ukl_wsp_line_width,
                                      antialias=True, mode='lines')
        ukl_wsp_z = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 0, ukl_wsp_line_length]]), color=[0, 0, 1, 1],
                                      width=ukl_wsp_line_width,
                                      antialias=True, mode='lines')
        self.pointcloudArea.addItem(ukl_wsp_x)
        self.pointcloudArea.addItem(ukl_wsp_y)
        self.pointcloudArea.addItem(ukl_wsp_z)

    # Metoda może i dobra, ale nie ma kalibracji magnetometru i dane nieodfiltrowane
    def poniekad_dobrze_metoda_akcelerometr_magnetometr(self):
        k0 = 0.9996
        e = 0.081819
        AA = 6367449.15
        alpha1 = 0.0008377318
        alpha2 = 7.60852780571568E-07
        alpha3 = 1.19764551083372E-09
        alpha4 = 2.42917070093028E-12
        alpha5 = 5.71181842951141E-15
        alpha6 = 1.47999804582115E-17
        zone = 21

        dane_gps = []
        sensors_file = open(dir_pose_data_imu, 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                next_data = [float(x) for x in line.split(',')[2:5]]
                try:
                    x = np.linspace(last_data[0], next_data[0], 15)
                    y = np.linspace(last_data[1], next_data[1], 15)
                    # z = np.linspace(last_data[2], next_data[2], 15)
                    for j in range(0, 15, 1):
                        kH = (y[j] - zone) * np.pi / 180
                        kJ = x[j] * np.pi / 180
                        kM = sinh(e * atanh(e * tan(kJ) / sqrt(1 + tan(kJ) * tan(kJ))))
                        kO = atan(tan(kJ) * sqrt(1 + kM * kM) - kM * sqrt(1 + tan(kJ) * tan(kJ)))
                        kQ = atan(tan(kO) / cos(kH))
                        kR = asinh(sin(kH) / sqrt(tan(kO) * tan(kO) + (cos(kH) * cos(kH))))
                        kS = kQ + alpha1 * sin(2 * kQ) * cosh(2 * kR) + alpha2 * sin(4 * kQ) * cosh(
                            4 * kR) + alpha3 * sin(6 * kQ) * cosh(6 * kR) + alpha4 * sin(8 * kQ) * cosh(
                            8 * kR) + alpha5 * sin(10 * kQ) * cosh(10 * kR) + alpha6 * sin(12 * kQ) * cosh(12 * kR)
                        kT = kR + alpha1 * cos(2 * kQ) * sinh(2 * kR) + alpha2 * cos(4 * kQ) * sinh(
                            4 * kR) + alpha3 * cos(6 * kQ) * sinh(6 * kR) + alpha4 * cos(8 * kQ) * sinh(
                            8 * kR) + alpha5 * cos(10 * kQ) * sinh(10 * kR) + alpha6 * cos(12 * kQ) * sinh(12 * kR)
                        kU = k0 * AA * kT
                        kV = k0 * AA * kS
                        kW = 500000
                        easting = kU + kW
                        if kV > 0:
                            northing = kV
                        else:
                            northing = kV + 10000000
                        xyz = [northing, easting, 0]
                        dane_gps.append(xyz)
                    last_data = next_data
                except:
                    last_data = next_data
        if len(dane_gps) == 0:
            raise ValueError("No GPS data found")
        sensors_file.close()
        print 'Ilość pozycji z GPS:'
        print len(dane_gps)

        #czas do poses.csv
        dane_time = []
        for i in range(0, len(dane_gps), 1):
            dane_time.append([str(i * 66666 ) ])


        start = False
        i = 0
        path = dir_lidar_data_imu
        dane_imu = []
        sensors_file = open(dir_pose_data_imu, 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                start = True
                imu = [float(x) for x in line.split(',')[6:9]] + [float(x) for x in line.split(',')[14:17]]
                roll = np.arctan2((-imu[0]), imu[2])
                pitch = np.arcsin(imu[1] / 9.81)
                yaw = np.arctan2((sin(roll) * imu[5] - cos(roll) * (-imu[3])),
                                 (cos(pitch) * (-imu[4]) + sin(roll) * sin(pitch) * (-imu[3])) +
                                 cos(roll) * sin(pitch) * imu[5])
                #rpy = [roll, pitch, yaw] #to powinno być ale jest masakra więc niech będą te oszukane:
                rpy = [roll * pi / 180, pitch * pi / 180, yaw * pi / 180]
                dane_imu.append(rpy)
            if start == True and i >= 3 and int(id) != 1 and line.split(',')[10:13] != [] and line.split(',')[
                                                                                              10:13] != ['', '', '']:
                imu = [float(x) for x in line.split(',')[2:5]] + [float(x) for x in line.split(',')[10:13]]
                roll = np.arctan2((-imu[0]), imu[2])
                pitch = np.arcsin(imu[1] / 9.81)
                yaw = np.arctan2((sin(roll) * imu[5] - cos(roll) * (-imu[3])),
                                 (cos(pitch) * (-imu[4]) + sin(roll) * sin(pitch) * (-imu[3])) +
                                 cos(roll) * sin(pitch) * imu[5])
                #rpy = [roll , pitch , yaw]
                rpy = [roll * pi / 180, pitch * pi / 180, yaw * pi / 180]
                dane_imu.append(rpy)
                i = 0
            i = i + 1
        sensors_file.close()
        if clear_roll == True:
            for i in range(len(dane_imu)):
                dane_imu[i][0]=0
        if clear_pitch == True:
            for i in range(len(dane_imu)):
                dane_imu[i][1]=0

        # stworzenie poses i obciecie ewentualnych poczatkowycyh pomiarow
        dane = []
        poses_file = open('poses.csv', 'w')
        csv_poses_file = csv.writer(poses_file)
        odjemnik = 0
        for i in range(0, len(dane_time), 1):
            if float(dane_time[i][0]) < float(pose_synch_time)*1000:
                odjemnik = float(dane_time[i][0])
            else:
                dane.append([float(dane_time[i][0])-odjemnik] + dane_gps[i] + dane_imu[i])
        csv_poses_file.writerows(dane)
        poses_file.close()
        print 'Utworzono plik poses.csv'

    # Funkcja jest dobra, ale dane muszą być odfiltrowane (dobre wyniki dla wygładzania wykładniczego)
    def calkowanie_gyro (self):
        k0 = 0.9996
        e = 0.081819
        AA = 6367449.15
        alpha1 = 0.0008377318
        alpha2 = 7.60852780571568E-07
        alpha3 = 1.19764551083372E-09
        alpha4 = 2.42917070093028E-12
        alpha5 = 5.71181842951141E-15
        alpha6 = 1.47999804582115E-17
        zone = 21

        dane_gps = []
        sensors_file = open(dir_pose_data_imu, 'r')
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                next_data = [float(x) for x in line.split(',')[2:5]]
                try:
                    x = np.linspace(last_data[0], next_data[0], 15)
                    y = np.linspace(last_data[1], next_data[1], 15)
                    # z = np.linspace(last_data[2], next_data[2], 15)
                    for j in range(0, 15, 1):
                        kH = (y[j] - zone) * np.pi / 180
                        kJ = x[j] * np.pi / 180
                        kM = sinh(e * atanh(e * tan(kJ) / sqrt(1 + tan(kJ) * tan(kJ))))
                        kO = atan(tan(kJ) * sqrt(1 + kM * kM) - kM * sqrt(1 + tan(kJ) * tan(kJ)))
                        kQ = atan(tan(kO) / cos(kH))
                        kR = asinh(sin(kH) / sqrt(tan(kO) * tan(kO) + (cos(kH) * cos(kH))))
                        kS = kQ + alpha1 * sin(2 * kQ) * cosh(2 * kR) + alpha2 * sin(4 * kQ) * cosh(
                            4 * kR) + alpha3 * sin(6 * kQ) * cosh(6 * kR) + alpha4 * sin(8 * kQ) * cosh(
                            8 * kR) + alpha5 * sin(10 * kQ) * cosh(10 * kR) + alpha6 * sin(12 * kQ) * cosh(12 * kR)
                        kT = kR + alpha1 * cos(2 * kQ) * sinh(2 * kR) + alpha2 * cos(4 * kQ) * sinh(
                            4 * kR) + alpha3 * cos(6 * kQ) * sinh(6 * kR) + alpha4 * cos(8 * kQ) * sinh(
                            8 * kR) + alpha5 * cos(10 * kQ) * sinh(10 * kR) + alpha6 * cos(12 * kQ) * sinh(12 * kR)
                        kU = k0 * AA * kT
                        kV = k0 * AA * kS
                        kW = 500000
                        easting = kU + kW
                        if kV > 0:
                            northing = kV
                        else:
                            northing = kV + 10000000
                        xyz = [northing, easting, 0]
                        dane_gps.append(xyz)
                    last_data = next_data
                except:
                    last_data = next_data
        if len(dane_gps) == 0:
            raise ValueError("No GPS data found")
        sensors_file.close()
        print 'Ilość pozycji z GPS:'
        print len(dane_gps)
        print dane_gps

        ### Czas do poses.csv
        dane_time = []
        for i in range(0, len(dane_gps), 1):
            dane_time.append([str(i * 66666)])

        i = 0
        t = 0.06
        roll = 0
        pitch = 0
        yaw = 0
        start = False
        dane_imu = []
        sensors_file = open(dir_pose_data_imu, 'r')        # tu zmienić na dir_pose_data "/home/qahu/Desktop/Zeszyt212.csv"
        for line in sensors_file:
            id = line.split(',')[1]
            if int(id) == 1:
                start = True
                imu = [float(x) for x in line.split(',')[10:13]]

                r11 = cos(pitch) * cos(yaw)
                r12 = sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw)
                r13 = cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)
                r21 = cos(pitch) * sin(yaw)
                r22 = sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw)
                r23 = cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)
                r31 = -sin(pitch)
                r32 = sin(roll) * cos(pitch)
                r33 = cos(roll) * cos(pitch)

                r11_next = r11 + r12 * imu[2] * t + r13 * imu[0] * t
                r21_next = r21 + r22 * imu[2] * t + r23 * imu[0] * t
                r31_next = r31 + r32 * imu[2] * t + r33 * imu[0] * t
                r32_next = r31 * (-imu[2]) * t + r32 + r33 * (-imu[1]) * t
                r33_next = r31 * (-imu[0]) * t + r32 * imu[1] * t + r33

                roll = np.arctan2(r32_next, r33_next)
                pitch = np.arcsin(-r31_next)
                yaw = np.arctan2(r21_next, r11_next)

                rpy = [roll, pitch, -yaw]
                dane_imu.append(rpy)

            if i>=3 and start == True and int(id) != 1 and line.split(',')[6:9] != [] and line.split(',')[6:9] != ['', '', '']:
                imu = [float(x) for x in line.split(',')[6:9]]

                r11 = cos(pitch) * cos(yaw)
                r12 = sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw)
                r13 = cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)
                r21 = cos(pitch) * sin(yaw)
                r22 = sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw)
                r23 = cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)
                r31 = -sin(pitch)
                r32 = sin(roll) * cos(pitch)
                r33 = cos(roll) * cos(pitch)

                r11_next = r11 + r12 * imu[2] * t + r13 * imu[0] * t
                r21_next = r21 + r22 * imu[2] * t + r23 * imu[0] * t
                r31_next = r31 + r32 * imu[2] * t + r33 * imu[0] * t
                r32_next = r31 * (-imu[2]) * t + r32 + r33 * (-imu[1]) * t
                r33_next = r31 * (-imu[0]) * t + r32 * imu[1] * t + r33

                roll = np.arctan2(r32_next, r33_next)
                pitch = np.arcsin(-r31_next)
                yaw = np.arctan2(r21_next, r11_next)

                rpy = [roll, pitch, -yaw]
                dane_imu.append(rpy)
                i = 0
            i = i + 1
            if len(dane_imu) == len(dane_gps):
                break
        sensors_file.close()
        if clear_roll == True:
            for i in range(len(dane_imu)):
                dane_imu[i][0] = 0
        if clear_pitch == True:
            for i in range(len(dane_imu)):
                dane_imu[i][1] = 0

        dane = []
        poses_file = open('poses.csv', 'w')
        csv_poses_file = csv.writer(poses_file)
        odjemnik = 0
        for i in range(0, len(dane_time), 1):
            if float(dane_time[i][0]) < float(pose_synch_time) * 1000:
                odjemnik = float(dane_time[i][0])
            else:
                dane.append([float(dane_time[i][0]) - odjemnik] + dane_gps[i] + dane_imu[i])
        csv_poses_file.writerows(dane)
        poses_file.close()
        print 'Utworzono plik poses.csv'

        ble = []
        for i in range(len(dane_imu)-1):
            ble.append(dane_imu[i][2]*180/pi)
        pyplot.plot(range(len(ble)),ble)
        pyplot.grid()
        pyplot.show()


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   Nieużywane funkcje   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

    def tworz_pliki_z_lidaru(self):
        # Tworzy plik z kolejnymi scanami z lidaru oraz plik timestampow odpowiadający kolejnym scanom


        # konwersja czasu z lidaru na relatywny do pierwszego pomiaru
        dane_time = []
        pierwsza_wartosc = True
        time_file = open(str(dir_lidar_data_custom), 'r')
        for line in time_file:
            try:
                dane_time.append(float(line.split(',')[0]))
                if pierwsza_wartosc == True:
                    odjemnik = line.split(',')[0]
                    pierwsza_wartosc = False
            except:
                pass
        dane_time_lidar = []
        # obciecie ewentualnych początkowych timestampów lidaru i stworzenie pliku
        usunieto = 0
        for i in range(len(dane_time)):
            time = (int(dane_time[i] - float(odjemnik))) / 1000
            if time >= float(lidar_synch_time) * 1000:
                dane_time_lidar.append([time])
            else:
                usunieto = usunieto + 1
        odjemnik = dane_time_lidar[0][0]
        for i in range(len(dane_time_lidar)):
            dane_time_lidar[i] = [dane_time_lidar[i][0] - odjemnik]
        time_file = open('lidar.timestamps', 'w')
        csv_time_file = csv.writer(time_file)
        csv_time_file.writerows(dane_time_lidar)
        time_file.close()
        print "Utworzono plik lidar.timestamps"

        # obciecie ewentualnych scanów i stworzenie pliku
        dane_lidar = []
        lidar_data_file = open(dir_lidar_data_custom, 'r')
        for line in lidar_data_file:
            if usunieto < 0:
                try:
                    one_scan = [float(x) for x in line.split(',')[11:282]]
                    dane_lidar.append(one_scan)
                except:
                    pass
            else:
                usunieto = usunieto - 1
        lidar_data_file.close()
        f = open('dane_odleglosci_lidar.csv', 'w')
        f_csv = csv.writer(f)
        dane_do_zapisania = []
        for i in range(0,dane_lidar.__len__()):
            dane_do_zapisania.append(dane_time_lidar[i]+dane_lidar[i])
        f_csv.writerows(dane_do_zapisania)
        f.close()
        print "Utworzono plik dane_odleglosci_lidar.csv"

    def view_images(self):
        if sdk:
            timestamps_path = os.path.join(os.path.join(str(dir_data_f), str(camera) + '.timestamps'))
            if not os.path.isfile(timestamps_path):
                timestamps_path = os.path.join(str(dir_data_f),  'stereo.timestamps')
                if not os.path.isfile(timestamps_path):
                    raise IOError("Could not find timestamps file")

            model = None
            if str(dir_models_f) and point3d: #jeśli ma być projekcja punktów na obraz(usunięcie dystorsji wymagane)
                model = CameraModel(str(dir_models_f), str(dir_camera))
                self.imageViewThread = ViewImagesThreadSDK(timestamps_path, real_img_start_time, real_img_end_time, model,
                                                        str(dir_camera), str(dir_ins), str(dir_extr_f),True, self.pointcloud)
            elif str(dir_models_f) and undistort: #jeśli ma być usunięta dystorsja z obrazu
                model = CameraModel(str(dir_models_f), str(dir_camera))
                self.imageViewThread = ViewImagesThreadSDK(timestamps_path, real_img_start_time, real_img_end_time, model,
                                                        str(dir_camera), str(dir_ins), str(dir_extr_f),False)
            else:
                self.imageViewThread = ViewImagesThreadSDK(timestamps_path, real_img_start_time, real_img_end_time, model,
                                                        str(dir_camera), str(dir_ins), str(dir_extr_f),False)
        else:
            if not point3d_custom:
                self.imageViewThread = ViewImagesThreadCustom(str(dir_image_custom), 200, int(start_time_custom)+int(img_start_time_custom),
                                                              int(start_time_custom)+int(img_end_time_custom),False)
            else:
                model = SimpleCustomCameraModel("camera_models/my_camera.txt")
                camera_extr_path = "extrinsics/camera_extr.txt"
                self.imageViewThread = ViewImagesThreadCustom(str(dir_image_custom), 200, int(start_time_custom)+int(img_start_time_custom),
                                                              int(start_time_custom)+int(img_end_time_custom), True, self.pointcloud, model,
                                                              camera_extr_path, str(dir_pose_data),str(dir_pose_extr))

        self.connect(self.imageViewThread, SIGNAL("draw_images(PyQt_PyObject)"), self.draw_images)
        self.connect(self.imageViewThread, SIGNAL("update_progressbar(PyQt_PyObject)"), self.update_progressbar)
        self.imageViewThread.start()
        self.imageButton.setEnabled(False)
        self.imageButton.setText(_translate("MainWindow", "Ładowanie...", None))

    def draw_images(self,images):

        self.imageView.setImage(images)
        self.imageButton.setEnabled(True)
        self.imageButton.setText(_translate("MainWindow", "Załaduj i wyswietl zdjęcia", None))

    def update_progressbar(self,progressbar):
        if progressbar[0] == 1:
            self.progressBar1.setValue(progressbar[1])
        elif progressbar[0] == 2:
            self.progressBar2.setValue(progressbar[1])




    def build_pointcloud(self):
        if sdk:
            self.new_thread = BuildPointcloudThread(str(dir_lidar),
                                                    str(dir_ins),
                                                    str(dir_extr_f),
                                                    real_start_time, real_end_time)
        else:
            self.tworz_pliki_z_lidaru()
            if pose_kind == 1:
                self.marek_wersja_1()
                dir_pose_extr = dir_pose_extr_vo
            elif pose_kind == 2:
                self.vo_imu()
                dir_pose_extr = dir_pose_extr_vo
            elif pose_kind == 3:
                self.madgwick_gyro_akc()
                dir_pose_extr = dir_pose_extr_imu
            self.new_thread = BuildPointcloudThread(str(dir_lidar_data_custom),
                                                    str(dir_pose_data_vo),
                                                    str(dir_lidar_extr),
                                                    int(start_time_custom)*1000, int(end_time_custom)*1000, -1, str(dir_pose_extr), int(pose_kind))

        self.connect(self.new_thread, SIGNAL("drawPointcloud(PyQt_PyObject)"), self.draw_pointcloud)
        self.connect(self.new_thread, SIGNAL("update_progressbar(PyQt_PyObject"),self.update_progressbar)
        self.new_thread.start()
        self.pointcloudButton.setEnabled(False)
        self.pointcloudButton.setText("Budowanie...")


    def draw_pointcloud(self, pointcloud):
        self.pointcloud = pointcloud
        if sdk:
            #odwróć pointclouda, żeby dobrze było oglądać
            pointcloud = np.dot(build_se3_transform(np.array([0,0,0,3.14,0,0])), pointcloud)
        pointcloud = pointcloud[0:3, :].transpose()
        print pointcloud

        plot_item = gl.GLScatterPlotItem(pos=pointcloud, size=(float(points_size)), color=[0.7, 0.7, 0.7, 1], pxMode=pixel_mode)

        #wyczyść obszar rysowania
        if self.pointcloudArea.items.__len__() > 0:
            for i in range(0,self.pointcloudArea.items.__len__()):
                self.pointcloudArea.items.__delitem__(0)

        self.pointcloudArea.addItem(plot_item)
        if uw == True:
            ukl_wsp_line_length = 3
            ukl_wsp_line_width = 4
            ukl_wsp_x = gl.GLLinePlotItem(pos = np.array([[0,0,0],[ukl_wsp_line_length,0,0]]), color=[1, 0, 0, 1], width = ukl_wsp_line_width,
                                          antialias = True, mode='lines')
            ukl_wsp_y = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, ukl_wsp_line_length, 0]]), color=[0, 1, 0, 1], width=ukl_wsp_line_width,
                                          antialias=True, mode='lines')
            ukl_wsp_z = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 0, ukl_wsp_line_length]]), color=[0, 0, 1, 1], width=ukl_wsp_line_width,
                                          antialias=True, mode='lines')
            self.pointcloudArea.addItem(ukl_wsp_x)
            self.pointcloudArea.addItem(ukl_wsp_y)
            self.pointcloudArea.addItem(ukl_wsp_z)
        self.pointcloudButton.setEnabled(True)
        self.pointcloudButton.setText("Buduj i rysuj pointclouda")



def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = Application()                # We set the form to be our Application (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

