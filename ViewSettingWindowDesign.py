# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ViewSettingWindowDesign.ui'
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
        Dialog.resize(488, 274)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(270, 210, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.checkBoxUW = QtGui.QCheckBox(Dialog)
        self.checkBoxUW.setGeometry(QtCore.QRect(70, 40, 251, 22))
        self.checkBoxUW.setObjectName(_fromUtf8("checkBoxUW"))
        self.choosePointsSize = QtGui.QLineEdit(Dialog)
        self.choosePointsSize.setGeometry(QtCore.QRect(210, 100, 41, 27))
        self.choosePointsSize.setObjectName(_fromUtf8("choosePointsSize"))
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(70, 100, 151, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.checkBoxColors = QtGui.QCheckBox(Dialog)
        self.checkBoxColors.setGeometry(QtCore.QRect(70, 70, 161, 22))
        self.checkBoxColors.setObjectName(_fromUtf8("checkBoxColors"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Ustawienia wyświetlania", None))
        self.checkBoxUW.setText(_translate("Dialog", "Początek układu współrzędnych", None))
        self.label_12.setText(_translate("Dialog", "Wielkość punktow", None))
        self.checkBoxColors.setText(_translate("Dialog", "Kolorowe punkty", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

