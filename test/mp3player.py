#-------------------------------------------------------------------------------
#-*- coding:gbk -*-
#-------------------------------------------------------------------------------
# Name:        test.mp3player.py
# Purpose:
#
# Author:      daimin
#
# Created:     2013-9-16
# Copyright:   (c) daimin 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------'''
#coding=gbk
import sys
import time
from PyQt4 import  QtGui, QtCore  
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import *

playCss = 'QPushButton#btnPlay{background:url(images/btn_%s.png);border:none;position:relative;}QPushButton#btnPlay:hover{background:url(images/btn_%s_hover.png);position:relative;}QPushButton#btnPlay:pressed{border:none;background:url(images/btn_%s_pressed.png);position:relative;}'
globalCss = 'QPushButton#btnPlay{background:url(images/btn_play.png);border:none;position:relative;}QPushButton#btnPlay:hover{background:url(images/btn_play_hover.png);position:relative;}QPushButton#btnPlay:pressed{border:none;background:url(images/btn_play_pressed.png);position:relative;}QPushButton#btnStop{background:url(images/btn_stop.png);border:none;position:relative;}QPushButton#btnStop:hover{background:url(images/btn_stop_hover.png);position:relative;}QPushButton#btnStop:pressed{border:none;background:url(images/btn_stop_pressed.png);position:relative;}QLabel#title{font-size:bold 14px Arial;color:#7e97ab;width:auto;}QLabel#takeTime{font-size:30px;font-family:Arial;color:#666;text-align:right;}QLabel#timeHour,QLabel#timeMin,QLabel#timeSec{font-size:9px;font-family:Arial;color:#666;text-align:center;}QLabel#timeTotal,QLabel#totalTime{line-height:40px;font-size:14px;font-family:Arial;color:#999;}QPushButton#btnClose{background:red;border-radius:6px;position:absolute;top:10px;}'

class PlayerWindow(QWidget):
    """docstring for PlayerWindow"""
    def __init__(self):
        super(PlayerWindow, self).__init__()
        self.setWindowTitle(QString("Mini Player"))
        #self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow )  #
        bitmap = QtGui.QPixmap("images/bg.png");
        self.resize(bitmap.size())
        self.setMask(bitmap.mask())
        pal=QtGui.QPalette(self)
        pal.setBrush(self.backgroundRole(), QtGui.QBrush(bitmap))
        self.setPalette(pal)

        self.rightButton=False

        self.menu()

        self.initUI()

        self.ph = Phonon.createPlayer(Phonon.MusicCategory)
        self.ph.setTickInterval(1000)
        self.connect(self.ph, SIGNAL("tick(qint64)"), self.tickInterval)
        self.connect(self.ph, SIGNAL("finished()"), self.finished)
        self.connect(self.ph, SIGNAL("currentSourceChanged (const Phonon::MediaSource&)"), self.currentSourceChanged)
        self.connect(self.ph, SIGNAL("metaDataChanged()"), self.metaDataChanged)
        self.ph.setCurrentSource(Phonon.MediaSource(QString("x.mp3")))
        self.playing = False


    def initUI(self):
        self.title = QLabel(self)
        self.title.setObjectName("title")
        self.setTitle("Mini Player")

        self.btnClose = QPushButton(self)
        self.btnClose.setFocusPolicy(Qt.NoFocus) #设置焦点样式
        self.btnClose.setObjectName("btnClose")
        self.btnClose.setToolTip(u"关闭播放器")
        self.btnClose.resize(12,12)
        self.btnClose.move(10,10)
        self.connect(self.btnClose, SIGNAL("clicked()"), qApp.quit)

        self.btnPlay = QPushButton(self)
        self.btnPlay.setFocusPolicy(Qt.NoFocus)
        self.btnPlay.setObjectName("btnPlay")
        self.btnPlay.move(30, 60)
        self.btnPlay.resize(47, 47)
        self.btnPlay.clicked.connect(self.player)

        self.btnStop = QPushButton(self)
        self.btnStop.setFocusPolicy(Qt.NoFocus)
        self.btnStop.setObjectName("btnStop")
        self.btnStop.move(80, 60)
        self.btnStop.resize(47, 47)
        self.btnStop.clicked.connect(self.stopPlay)

        self.takeTime = QLabel("00:00:00",self)
        self.takeTime.setObjectName("takeTime")
        self.takeTime.move(150 + 40, 57)

        self.timeHour = QLabel("HOUR", self)
        self.timeHour.setObjectName("timeHour")
        self.timeHour.move(153 + 40, 93)

        self.timeHour = QLabel("MIN", self)
        self.timeHour.setObjectName("timeMin")
        self.timeHour.move(201 + 40, 93)

        self.timeHour = QLabel("SEC", self)
        self.timeHour.setObjectName("timeSec")
        self.timeHour.move(242 + 40, 93)

        self.timeTotal = QLabel("Totel time", self)
        self.timeTotal.setObjectName("timeTotal")
        self.timeTotal.move(18, 145)

        self.totalTime = QLabel(self)
        self.totalTime.setObjectName("totalTime")
        self.setTotalTime(0,0,0)

    def player(self):
        if self.playing:
            self.playing = False
            self.ph.pause()
            self.btnPlay.setStyleSheet(playCss.replace('%s','play'))
        else:
            self.playing = True
            self.ph.play()
            self.btnPlay.setStyleSheet(playCss.replace('%s','pause'))
    
    def stopPlay(self):
        self.ph.stop()
        self.playing = False
        self.btnPlay.setStyleSheet(playCss.replace('%s','play'))

    def tickInterval(self):
        remainingTime = time.gmtime(self.ph.remainingTime() / 1000)
        self.setCurrentTime(remainingTime.tm_hour, remainingTime.tm_min, remainingTime.tm_sec)

    def finished(self):
        print 'finished'

    def metaDataChanged(self):
        self.setTitle("%s" % unicode(self.ph.metaData("TITLE").takeFirst()))
        totalTime = time.gmtime(self.ph.totalTime() / 1000)
        self.setTotalTime(totalTime.tm_hour, totalTime.tm_min, totalTime.tm_sec)
        self.setCurrentTime(totalTime.tm_hour, totalTime.tm_min, totalTime.tm_sec)

    def currentSourceChanged(self, source):
        print source.deviceName()

    def setTitle(self, title):
        self.title.setText(title)
        self.title.resize(self.title.sizeHint().width(), self.title.sizeHint().height())
        self.title.move(self.width() - self.title.width() - 20,15)
        self.setWindowTitle(u"播放 %s" % title)

    def setTotalTime(self, hour, min, sec):
        self.totalTime.setText("%.2d:%.2d:%.2d" % (hour, min, sec))
        self.totalTime.resize(self.totalTime.sizeHint().width(), self.totalTime.sizeHint().height())
        self.totalTime.move(self.width() - self.totalTime.width() - 16, 145)

    def setCurrentTime(self, hour, min, sec):
        self.takeTime.setText("%.2d:%.2d:%.2d" % (hour, min, sec))

    def menu(self):
        quitAction = QAction(QIcon('quit.png'), u'退出(&Q)', self)
        self.connect(quitAction,SIGNAL("triggered()"),qApp.quit)
        aboutAction = QAction(QIcon(""), u"关于(&A)", self)
        self.connect(aboutAction,SIGNAL("triggered()"),self.about)

        self.popMenu= QtGui.QMenu() 
        self.popMenu.addAction(aboutAction) 
        self.popMenu.addAction(quitAction) 
        
    def about(self):
        about = QMessageBox(self)
        about.setWindowTitle(u'关于Mini Player')
        about.setText(u"Mini Player 是一个使用PyQt编写的简单MP3播放器\n\twapznw@gmail.com")
        about.show()

    def mouseReleaseEvent(self,e): 
        if self.rightButton == True:
            self.rightButton=False
            self.popMenu.popup(e.globalPos())

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.move(e.globalPos()-self.dragPos)
            e.accept()
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton: 
            self.dragPos=e.globalPos()-self.frameGeometry().topLeft() 
            e.accept()
        if e.button() == Qt.RightButton and self.rightButton == False:
            self.rightButton=True

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(globalCss);
    w = PlayerWindow()
    w.show()
    sys.exit(app.exec_())