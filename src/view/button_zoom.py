# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_design/button_zoom.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_zoom_out = QtWidgets.QPushButton(self.centralwidget)
        self.button_zoom_out.setGeometry(QtCore.QRect(40, 10, 25, 25))
        self.button_zoom_out.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_out.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_out.setObjectName("button_zoom_out")
        self.button_zoom_in = QtWidgets.QPushButton(self.centralwidget)
        self.button_zoom_in.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.button_zoom_in.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_in.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_in.setObjectName("button_zoom_in")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_zoom_out.setText(_translate("MainWindow", "-"))
        self.button_zoom_in.setText(_translate("MainWindow", "+"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())