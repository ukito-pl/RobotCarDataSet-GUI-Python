# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectDataWindowDesign.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(924, 648)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.buttonBoxDataSet = QtGui.QDialogButtonBox(self.tab)
        self.buttonBoxDataSet.setEnabled(True)
        self.buttonBoxDataSet.setGeometry(QtCore.QRect(580, 360, 181, 31))
        self.buttonBoxDataSet.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.buttonBoxDataSet.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxDataSet.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBoxDataSet.setCenterButtons(False)
        self.buttonBoxDataSet.setObjectName(_fromUtf8("buttonBoxDataSet"))
        self.browseButton1 = QtGui.QToolButton(self.tab)
        self.browseButton1.setGeometry(QtCore.QRect(740, 40, 31, 31))
        self.browseButton1.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.browseButton1.setArrowType(QtCore.Qt.NoArrow)
        self.browseButton1.setObjectName(_fromUtf8("browseButton1"))
        self.chooseDataFolder = QtGui.QLineEdit(self.tab)
        self.chooseDataFolder.setGeometry(QtCore.QRect(220, 40, 501, 27))
        self.chooseDataFolder.setObjectName(_fromUtf8("chooseDataFolder"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 40, 151, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(30, 180, 131, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(30, 220, 151, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.startTimeF = QtGui.QLineEdit(self.tab)
        self.startTimeF.setGeometry(QtCore.QRect(220, 320, 181, 27))
        self.startTimeF.setObjectName(_fromUtf8("startTimeF"))
        self.endTimeF = QtGui.QLineEdit(self.tab)
        self.endTimeF.setGeometry(QtCore.QRect(220, 360, 181, 27))
        self.endTimeF.setObjectName(_fromUtf8("endTimeF"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(30, 320, 111, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(30, 360, 111, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.chooseLidar = QtGui.QComboBox(self.tab)
        self.chooseLidar.setGeometry(QtCore.QRect(220, 180, 131, 27))
        self.chooseLidar.setObjectName(_fromUtf8("chooseLidar"))
        self.chooseLidar.addItem(_fromUtf8(""))
        self.chooseLidar.setItemText(0, _fromUtf8(""))
        self.chooseLidar.addItem(_fromUtf8(""))
        self.chooseLidar.addItem(_fromUtf8(""))
        self.chooseLidar.addItem(_fromUtf8(""))
        self.chooseCamera = QtGui.QComboBox(self.tab)
        self.chooseCamera.setGeometry(QtCore.QRect(220, 220, 131, 27))
        self.chooseCamera.setObjectName(_fromUtf8("chooseCamera"))
        self.chooseCamera.addItem(_fromUtf8(""))
        self.chooseCamera.setItemText(0, _fromUtf8(""))
        self.chooseCamera.addItem(_fromUtf8(""))
        self.chooseCamera.addItem(_fromUtf8(""))
        self.chooseCamera.addItem(_fromUtf8(""))
        self.chooseCamera.addItem(_fromUtf8(""))
        self.chooseCamera.addItem(_fromUtf8(""))
        self.chooseCamera.addItem(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(30, 80, 191, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(30, 120, 171, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.chooseExtrFolder = QtGui.QLineEdit(self.tab)
        self.chooseExtrFolder.setGeometry(QtCore.QRect(220, 80, 501, 27))
        self.chooseExtrFolder.setObjectName(_fromUtf8("chooseExtrFolder"))
        self.chooseModelsFolder = QtGui.QLineEdit(self.tab)
        self.chooseModelsFolder.setGeometry(QtCore.QRect(220, 120, 501, 27))
        self.chooseModelsFolder.setObjectName(_fromUtf8("chooseModelsFolder"))
        self.browseButton2 = QtGui.QToolButton(self.tab)
        self.browseButton2.setGeometry(QtCore.QRect(740, 80, 31, 31))
        self.browseButton2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.browseButton2.setArrowType(QtCore.Qt.NoArrow)
        self.browseButton2.setObjectName(_fromUtf8("browseButton2"))
        self.browseButton3 = QtGui.QToolButton(self.tab)
        self.browseButton3.setGeometry(QtCore.QRect(740, 120, 31, 31))
        self.browseButton3.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.browseButton3.setArrowType(QtCore.Qt.NoArrow)
        self.browseButton3.setObjectName(_fromUtf8("browseButton3"))
        self.choosePoseF = QtGui.QComboBox(self.tab)
        self.choosePoseF.setGeometry(QtCore.QRect(220, 260, 131, 27))
        self.choosePoseF.setObjectName(_fromUtf8("choosePoseF"))
        self.choosePoseF.addItem(_fromUtf8(""))
        self.choosePoseF.setItemText(0, _fromUtf8(""))
        self.choosePoseF.addItem(_fromUtf8(""))
        self.choosePoseF.addItem(_fromUtf8(""))
        self.label_8 = QtGui.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(30, 260, 151, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.chooseLidarDataFile = QtGui.QLineEdit(self.tab)
        self.chooseLidarDataFile.setGeometry(QtCore.QRect(530, 160, 191, 27))
        self.chooseLidarDataFile.setObjectName(_fromUtf8("chooseLidarDataFile"))
        self.label_15 = QtGui.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(530, 190, 201, 20))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.label_9 = QtGui.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(370, 20, 151, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.chooseLidarData = QtGui.QLineEdit(self.tab_2)
        self.chooseLidarData.setGeometry(QtCore.QRect(220, 50, 501, 27))
        self.chooseLidarData.setObjectName(_fromUtf8("chooseLidarData"))
        self.choosePoseData = QtGui.QLineEdit(self.tab_2)
        self.choosePoseData.setGeometry(QtCore.QRect(230, 200, 501, 27))
        self.choosePoseData.setObjectName(_fromUtf8("choosePoseData"))
        self.browseButton6 = QtGui.QToolButton(self.tab_2)
        self.browseButton6.setGeometry(QtCore.QRect(750, 200, 31, 31))
        self.browseButton6.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.browseButton6.setArrowType(QtCore.Qt.NoArrow)
        self.browseButton6.setObjectName(_fromUtf8("browseButton6"))
        self.browseButton7 = QtGui.QToolButton(self.tab_2)
        self.browseButton7.setGeometry(QtCore.QRect(750, 240, 31, 31))
        self.browseButton7.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.browseButton7.setArrowType(QtCore.Qt.NoArrow)
        self.browseButton7.setObjectName(_fromUtf8("browseButton7"))
        self.label_10 = QtGui.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(60, 200, 191, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.browseButton4 = QtGui.QToolButton(self.tab_2)
        self.browseButton4.setGeometry(QtCore.QRect(750, 50, 31, 31))
        self.browseButton4.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.browseButton4.setArrowType(QtCore.Qt.NoArrow)
        self.browseButton4.setObjectName(_fromUtf8("browseButton4"))
        self.choosePoseExtr = QtGui.QLineEdit(self.tab_2)
        self.choosePoseExtr.setGeometry(QtCore.QRect(230, 240, 501, 27))
        self.choosePoseExtr.setObjectName(_fromUtf8("choosePoseExtr"))
        self.label_11 = QtGui.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(60, 240, 171, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(50, 50, 151, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(50, 80, 151, 20))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.browseButton5 = QtGui.QToolButton(self.tab_2)
        self.browseButton5.setGeometry(QtCore.QRect(750, 80, 31, 31))
        self.browseButton5.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.browseButton5.setArrowType(QtCore.Qt.NoArrow)
        self.browseButton5.setObjectName(_fromUtf8("browseButton5"))
        self.chooseLidarExtr = QtGui.QLineEdit(self.tab_2)
        self.chooseLidarExtr.setGeometry(QtCore.QRect(220, 80, 501, 27))
        self.chooseLidarExtr.setObjectName(_fromUtf8("chooseLidarExtr"))
        self.label_14 = QtGui.QLabel(self.tab_2)
        self.label_14.setGeometry(QtCore.QRect(360, 160, 151, 20))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.choosePoseKind = QtGui.QComboBox(self.tab_2)
        self.choosePoseKind.setGeometry(QtCore.QRect(230, 280, 131, 27))
        self.choosePoseKind.setObjectName(_fromUtf8("choosePoseKind"))
        self.choosePoseKind.addItem(_fromUtf8(""))
        self.choosePoseKind.addItem(_fromUtf8(""))
        self.label_29 = QtGui.QLabel(self.tab_2)
        self.label_29.setGeometry(QtCore.QRect(60, 280, 151, 20))
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.buttonBoxCustom = QtGui.QDialogButtonBox(self.tab_2)
        self.buttonBoxCustom.setEnabled(True)
        self.buttonBoxCustom.setGeometry(QtCore.QRect(660, 520, 181, 31))
        self.buttonBoxCustom.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.buttonBoxCustom.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxCustom.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBoxCustom.setCenterButtons(False)
        self.buttonBoxCustom.setObjectName(_fromUtf8("buttonBoxCustom"))
        self.label_30 = QtGui.QLabel(self.tab_2)
        self.label_30.setGeometry(QtCore.QRect(60, 320, 151, 20))
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.clearHeight = QtGui.QCheckBox(self.tab_2)
        self.clearHeight.setGeometry(QtCore.QRect(340, 320, 21, 22))
        self.clearHeight.setText(_fromUtf8(""))
        self.clearHeight.setObjectName(_fromUtf8("clearHeight"))
        self.label_31 = QtGui.QLabel(self.tab_2)
        self.label_31.setGeometry(QtCore.QRect(50, 110, 171, 17))
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.synchLidarTime = QtGui.QLineEdit(self.tab_2)
        self.synchLidarTime.setGeometry(QtCore.QRect(220, 110, 181, 27))
        self.synchLidarTime.setText(_fromUtf8(""))
        self.synchLidarTime.setObjectName(_fromUtf8("synchLidarTime"))
        self.label_32 = QtGui.QLabel(self.tab_2)
        self.label_32.setGeometry(QtCore.QRect(60, 350, 161, 17))
        self.label_32.setObjectName(_fromUtf8("label_32"))
        self.synchPoseTime = QtGui.QLineEdit(self.tab_2)
        self.synchPoseTime.setGeometry(QtCore.QRect(230, 350, 181, 27))
        self.synchPoseTime.setText(_fromUtf8(""))
        self.synchPoseTime.setObjectName(_fromUtf8("synchPoseTime"))
        self.label_33 = QtGui.QLabel(self.tab_2)
        self.label_33.setGeometry(QtCore.QRect(50, 450, 111, 17))
        self.label_33.setObjectName(_fromUtf8("label_33"))
        self.label_34 = QtGui.QLabel(self.tab_2)
        self.label_34.setGeometry(QtCore.QRect(50, 480, 161, 17))
        self.label_34.setObjectName(_fromUtf8("label_34"))
        self.endTimeCustom = QtGui.QLineEdit(self.tab_2)
        self.endTimeCustom.setGeometry(QtCore.QRect(210, 480, 181, 27))
        self.endTimeCustom.setObjectName(_fromUtf8("endTimeCustom"))
        self.startTimeCustom = QtGui.QLineEdit(self.tab_2)
        self.startTimeCustom.setGeometry(QtCore.QRect(210, 450, 181, 27))
        self.startTimeCustom.setObjectName(_fromUtf8("startTimeCustom"))
        self.label_35 = QtGui.QLabel(self.tab_2)
        self.label_35.setGeometry(QtCore.QRect(260, 320, 81, 20))
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.clearRoll = QtGui.QCheckBox(self.tab_2)
        self.clearRoll.setGeometry(QtCore.QRect(470, 320, 21, 22))
        self.clearRoll.setText(_fromUtf8(""))
        self.clearRoll.setObjectName(_fromUtf8("clearRoll"))
        self.label_36 = QtGui.QLabel(self.tab_2)
        self.label_36.setGeometry(QtCore.QRect(410, 320, 61, 20))
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.clearPitch = QtGui.QCheckBox(self.tab_2)
        self.clearPitch.setGeometry(QtCore.QRect(600, 320, 21, 22))
        self.clearPitch.setText(_fromUtf8(""))
        self.clearPitch.setObjectName(_fromUtf8("clearPitch"))
        self.label_37 = QtGui.QLabel(self.tab_2)
        self.label_37.setGeometry(QtCore.QRect(530, 320, 61, 20))
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.skalaVO = QtGui.QLineEdit(self.tab_2)
        self.skalaVO.setGeometry(QtCore.QRect(500, 280, 111, 27))
        self.skalaVO.setText(_fromUtf8(""))
        self.skalaVO.setObjectName(_fromUtf8("skalaVO"))
        self.label_38 = QtGui.QLabel(self.tab_2)
        self.label_38.setGeometry(QtCore.QRect(430, 280, 91, 20))
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBoxDataSet, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBoxDataSet, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.buttonBoxCustom, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBoxCustom, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.tabWidget.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>", None))
        self.tabWidget.setWhatsThis(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>", None))
        self.browseButton1.setText(_translate("Dialog", "...", None))
        self.label.setText(_translate("Dialog", "Folder danych:", None))
        self.label_2.setText(_translate("Dialog", "Wybierz lidar:", None))
        self.label_3.setText(_translate("Dialog", "Wybierz kamerę:", None))
        self.label_4.setText(_translate("Dialog", "Czas startu [ms]:", None))
        self.label_5.setText(_translate("Dialog", "Czas końca [ms]:", None))
        self.chooseLidar.setItemText(1, _translate("Dialog", "lms_front", None))
        self.chooseLidar.setItemText(2, _translate("Dialog", "ldmrs", None))
        self.chooseLidar.setItemText(3, _translate("Dialog", "lms_rear", None))
        self.chooseCamera.setItemText(1, _translate("Dialog", "mono_left", None))
        self.chooseCamera.setItemText(2, _translate("Dialog", "mono_rear", None))
        self.chooseCamera.setItemText(3, _translate("Dialog", "mono_right", None))
        self.chooseCamera.setItemText(4, _translate("Dialog", "stereo_left", None))
        self.chooseCamera.setItemText(5, _translate("Dialog", "stereo_center", None))
        self.chooseCamera.setItemText(6, _translate("Dialog", "stereo_right", None))
        self.label_6.setText(_translate("Dialog", "Folder extrinsic:", None))
        self.label_7.setText(_translate("Dialog", "Folder modeli:", None))
        self.browseButton2.setText(_translate("Dialog", "...", None))
        self.browseButton3.setText(_translate("Dialog", "...", None))
        self.choosePoseF.setItemText(1, _translate("Dialog", "ins.csv", None))
        self.choosePoseF.setItemText(2, _translate("Dialog", "vo.csv", None))
        self.label_8.setText(_translate("Dialog", "Wybierz plik pozycji:", None))
        self.label_15.setText(_translate("Dialog", "^^^ OKIENKO TESTOWE ^^^", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Dane projektu RobotCar DataSet", None))
        self.label_9.setText(_translate("Dialog", "Lidar ", None))
        self.browseButton6.setText(_translate("Dialog", "...", None))
        self.browseButton7.setText(_translate("Dialog", "...", None))
        self.label_10.setText(_translate("Dialog", "Plik pozycji:", None))
        self.browseButton4.setText(_translate("Dialog", "...", None))
        self.label_11.setText(_translate("Dialog", "Plik extrinsic:", None))
        self.label_12.setText(_translate("Dialog", "Plik lidaru:", None))
        self.label_13.setText(_translate("Dialog", "Plik extrinsic:", None))
        self.browseButton5.setText(_translate("Dialog", "...", None))
        self.label_14.setText(_translate("Dialog", "Pozycje", None))
        self.choosePoseKind.setItemText(0, _translate("Dialog", "gps+imu", None))
        self.choosePoseKind.setItemText(1, _translate("Dialog", "vo", None))
        self.label_29.setText(_translate("Dialog", "Rodzaj pliku:", None))
        self.label_30.setText(_translate("Dialog", "Zeruj:", None))
        self.label_31.setText(_translate("Dialog", "Czas synchronizacji[ms]:", None))
        self.label_32.setText(_translate("Dialog", "Czas synchronizacji[ms]:", None))
        self.label_33.setText(_translate("Dialog", "Czas startu [ms]:", None))
        self.label_34.setText(_translate("Dialog", "Czas zakończenia[ms]:", None))
        self.label_35.setText(_translate("Dialog", "Wysokość", None))
        self.label_36.setText(_translate("Dialog", "Kąt roll", None))
        self.label_37.setText(_translate("Dialog", "Kąt pitch", None))
        self.label_38.setText(_translate("Dialog", "Skala vo:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Dane własne", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

