#!/usr/bin/python

# center.py

import sys
from PyQt4 import QtGui

class Center(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('center')
        self.resize(250, 150)
        self.center()

    def center(self):
        #得到屏幕大小
        screen = QtGui.QDesktopWidget().screenGeometry()
        #自身的大小
        size =  self.geometry()
        #移动自身到指定位置
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


app = QtGui.QApplication(sys.argv)
qb = Center()
qb.show()
sys.exit(app.exec_())