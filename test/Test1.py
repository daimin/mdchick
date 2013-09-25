#!/usr/bin/python

# quitbutton.py

import sys
from PyQt4 import QtGui, QtCore

class QuitButton(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')

        quit = QtGui.QPushButton('Close', self)
        quit.setGeometry(10, 10, 64, 35)
        #连接建立信号和槽
        #信号发射，槽接收并处理
        #发射方和接收方两个对象间进行通讯，发射方为按钮，接收方为application对象
        #QtGui.qApp当前程序的app对象
        self.connect(quit, QtCore.SIGNAL('clicked()'),
            QtGui.qApp, QtCore.SLOT('quit()'))


app = QtGui.QApplication(sys.argv)
qb = QuitButton()
qb.show()
sys.exit(app.exec_())