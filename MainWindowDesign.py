# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindowDesign.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(880, 720)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.selectDataButton = QtGui.QPushButton(self.centralwidget)
        self.selectDataButton.setObjectName(_fromUtf8("selectDataButton"))
        self.gridLayout.addWidget(self.selectDataButton, 0, 0, 1, 1)
        self.pointcloudButton = QtGui.QPushButton(self.centralwidget)
        self.pointcloudButton.setObjectName(_fromUtf8("pointcloudButton"))
        self.gridLayout.addWidget(self.pointcloudButton, 1, 0, 1, 1)
        self.testyButton = QtGui.QPushButton(self.centralwidget)
        self.testyButton.setObjectName(_fromUtf8("testyButton"))
        self.gridLayout.addWidget(self.testyButton, 1, 1, 1, 1)
        self.settingButton = QtGui.QPushButton(self.centralwidget)
        self.settingButton.setObjectName(_fromUtf8("settingButton"))
        self.gridLayout.addWidget(self.settingButton, 0, 1, 1, 1)
        self.pointcloudArea = GLViewWidget(self.centralwidget)
        self.pointcloudArea.setObjectName(_fromUtf8("pointcloudArea"))
        self.gridLayout.addWidget(self.pointcloudArea, 2, 0, 1, 1)
        self.imageLabel = QtGui.QLabel(self.centralwidget)
        self.imageLabel.setText(_fromUtf8(""))
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
        self.gridLayout.addWidget(self.imageLabel, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 880, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.selectDataButton.setText(_translate("MainWindow", "Wybierz dane", None))
        self.pointcloudButton.setText(_translate("MainWindow", "Buduj i rysuj pointclouda", None))
        self.testyButton.setText(_translate("MainWindow", "Testy", None))
        self.settingButton.setText(_translate("MainWindow", "Ustawienia widoku", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

from pyqtgraph.opengl import GLViewWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

