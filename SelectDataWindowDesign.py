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
        Dialog.resize(830, 539)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.buttonBox = QtGui.QDialogButtonBox(self.tab)
        self.buttonBox.setGeometry(QtCore.QRect(620, 430, 176, 27))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.toolButton = QtGui.QToolButton(self.tab)
        self.toolButton.setGeometry(QtCore.QRect(310, 60, 21, 21))
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButton.setArrowType(QtCore.Qt.NoArrow)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.lineEdit = QtGui.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(190, 60, 113, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(70, 60, 111, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(67, 110, 131, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.checkBox = QtGui.QCheckBox(self.tab)
        self.checkBox.setGeometry(QtCore.QRect(210, 110, 99, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.tab)
        self.checkBox_2.setGeometry(QtCore.QRect(340, 110, 99, 22))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.tab)
        self.checkBox_3.setGeometry(QtCore.QRect(470, 110, 99, 22))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(47, 150, 151, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.checkBox_4 = QtGui.QCheckBox(self.tab)
        self.checkBox_4.setGeometry(QtCore.QRect(340, 150, 99, 22))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.checkBox_5 = QtGui.QCheckBox(self.tab)
        self.checkBox_5.setGeometry(QtCore.QRect(470, 150, 121, 22))
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.checkBox_6 = QtGui.QCheckBox(self.tab)
        self.checkBox_6.setGeometry(QtCore.QRect(210, 150, 99, 22))
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.checkBox_7 = QtGui.QCheckBox(self.tab)
        self.checkBox_7.setGeometry(QtCore.QRect(470, 190, 121, 22))
        self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
        self.checkBox_8 = QtGui.QCheckBox(self.tab)
        self.checkBox_8.setGeometry(QtCore.QRect(340, 190, 121, 22))
        self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
        self.checkBox_9 = QtGui.QCheckBox(self.tab)
        self.checkBox_9.setGeometry(QtCore.QRect(210, 190, 111, 22))
        self.checkBox_9.setObjectName(_fromUtf8("checkBox_9"))
        self.lineEdit_2 = QtGui.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 240, 113, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_3 = QtGui.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(200, 280, 113, 27))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(120, 240, 91, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(120, 280, 91, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.buttonBox_2 = QtGui.QDialogButtonBox(self.tab_2)
        self.buttonBox_2.setGeometry(QtCore.QRect(610, 440, 176, 27))
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_2.setObjectName(_fromUtf8("buttonBox_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.tabWidget.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>", None))
        self.tabWidget.setWhatsThis(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>", None))
        self.toolButton.setText(_translate("Dialog", "...", None))
        self.label.setText(_translate("Dialog", "Choose Folder:", None))
        self.label_2.setText(_translate("Dialog", "Choose Lidar data:", None))
        self.checkBox.setText(_translate("Dialog", "ldmrs", None))
        self.checkBox_2.setText(_translate("Dialog", "lms_front", None))
        self.checkBox_3.setText(_translate("Dialog", "lms_rear", None))
        self.label_3.setText(_translate("Dialog", "Choose camera data:", None))
        self.checkBox_4.setText(_translate("Dialog", "mono_rear", None))
        self.checkBox_5.setText(_translate("Dialog", "mono_right", None))
        self.checkBox_6.setText(_translate("Dialog", "mono_left", None))
        self.checkBox_7.setText(_translate("Dialog", "stereo_right", None))
        self.checkBox_8.setText(_translate("Dialog", "stereo_center", None))
        self.checkBox_9.setText(_translate("Dialog", "stereo_left", None))
        self.label_4.setText(_translate("Dialog", "Start time:", None))
        self.label_5.setText(_translate("Dialog", "End time:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "RobotCarDataSet data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Custom data", None))

