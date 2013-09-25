#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################################################
##
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
###########################################################################
#coding=utf-8

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork

from ui_md import Ui_Form
import markdown

import os
from ConfigParser import RawConfigParser

import sys
reload(sys)

sys.setdefaultencoding('utf-8')


def read_stylesheet(f):
    file = QtCore.QFile(os.getcwd() + '/qss/%s' % f)
    file.open(QtCore.QFile.ReadOnly)

    styleSheet = file.readAll()
    styleSheet = unicode(styleSheet, encoding='utf8')
    file.close()
    return styleSheet

class MDChick(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MDChick, self).__init__(parent)

        self.setupUi(self)
        self.baseUrl = QtCore.QUrl()
        self.htmlCss = read_stylesheet("md.css")
        font = QtGui.QFont("Lucida Console", 10)
        self.plainTextEdit.setFont(font)
 
    def setBaseUrl(self, url):
        self.baseUrl = url

    def previewMD(self):
        # Update the contents in the web viewer.
        text = self.plainTextEdit.toPlainText()
        html = markdown.markdown(text)
       
        html_head =   """
<!DOCTYPE html> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
<meta charset="utf-8"> 
<style type="text/css">
%s
</style>
</head> 
<body>
        """ %(self.htmlCss)
        html = "%s%s</body></html>" %(html_head, html)
        self.webView.page().mainFrame().setHtml(html, self.baseUrl)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MDChick Editor")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.showMaximized()
        
        fd = QtCore.QFile("./jquery.min.js")
        if fd.open(QtCore.QIODevice.ReadOnly | QtCore.QFile.Text):
            self.jQuery = QtCore.QTextStream(fd).readAll()
            fd.close()
        else:
            self.jQuery = ''

        
        self.createActions()
        self.createMenus()
        self.centralWidget = MDChick(self)
        
        self.setCentralWidget(self.centralWidget)
        

        self.setStartupText()
        QtGui.qApp.setStyleSheet(read_stylesheet("style.qss"))
        
        self.tempDir = self.loadTempDir()
        self.centralWidget.plainTextEdit.setMainWindow(self)

       
    def loadTempDir(self):
        """加载ini文件中配置的临时目录
        """
        rcp = RawConfigParser()
        rcp.read('md.ini')
        try:
            temp_dir = rcp.get("TempDir", "TempDir")
            if temp_dir:
                return unicode(temp_dir, encoding='utf8')
        except:
            return None
        
    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self,
                shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an existing Markdown file", triggered=self.open)

        self.saveAct = QtGui.QAction("&Save", self,
                shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the Markdown file to disk", triggered=self.save)

        self.exitAct = QtGui.QAction("E&xit", self,
                shortcut=QtGui.QKeySequence.Quit,
                statusTip="Exit the application", triggered=self.close)
        
        self.boldAct = QtGui.QAction("&Bold", self,
                statusTip="Make the text style to bold",
                triggered=self.bold)
        self.boldAct.setShortcut('Ctrl+B')
        
        self.italicAct = QtGui.QAction("&Italic", self,
                statusTip="Make the text style to italic",
                triggered=self.italic)
        self.italicAct.setShortcut('Ctrl+I')
        
        

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.menuBar().addSeparator()
        
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.boldAct)
        self.editMenu.addAction(self.italicAct)
        
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        

    def about(self):
        QtGui.QMessageBox.about(self, u"About MDChick",
                u"<b>MdChick</b> is a editor which can be used to<br/> edit and preview the Markdown text.")
        
    def bold(self):
        pass
    
    def italic(self):
        pass

    def open(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self,directory=self.tempDir,filter = self.tr("Markdown File (*.md *.markdown)"))
        
        self.writeDirConfig(os.path.dirname(self.fileName) )
        if self.fileName:
            fd = QtCore.QFile(self.fileName)
            if not fd.open(QtCore.QIODevice.ReadOnly):
                QtGui.QMessageBox.information(self, self.tr("Unable to open file"),
                        fd.errorString())
                return
            
            ##解决中文编码问题
            txtStream = QtCore.QTextStream(fd)
            txtCodec = QtCore.QTextCodec.codecForName("UTF-8")
            txtStream.setCodec(txtCodec)
            
            output = txtStream.readAll()
            
            self.centralWidget.plainTextEdit.setPlainText(output)
            fd.close()
            self.centralWidget.previewMD()

    def save(self):
        content = self.centralWidget.plainTextEdit.toPlainText()

        if not hasattr(self, "fileName") or self.fileName is None or self.fileName == '':
            self.fileName = QtGui.QFileDialog.getSaveFileName(self, caption=self.tr("Save Markdown File"),\
                                                          directory=self.tempDir,
                                                          filter = self.tr("Markdown File (*.md *.markdown)"))
            self.writeDirConfig(os.path.dirname(self.fileName))
            
        if self.fileName:
            fd = QtCore.QFile(self.fileName)
                
        if not fd.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, "Unable to open file",
                fd.errorString())
            return
        ##解决中文编码问题
        txtStream = QtCore.QTextStream(fd)
        txtCodec = QtCore.QTextCodec.codecForName("UTF-8")
        txtStream.setCodec(txtCodec)
        txtStream << content
        fd.close()
        self.centralWidget.previewMD()
    
 
    def updateTextEdit(self):
        mainFrame = self.centralWidget.webView.page().mainFrame()
        
        frameText = mainFrame.toHtml()
        self.centralWidget.plainTextEdit.setPlainText(frameText)

    def setStartupText(self):
        #self.centralWidget.plainTextEdit.setPlainText()
        self.centralWidget.previewMD()
        
        
    def writeDirConfig(self, dd):
        if dd is None or dd == "":
            return
        self.tempDir = dd
        cfg = RawConfigParser()
        cfg.add_section("TempDir")
        cfg.set("TempDir", "TempDir", dd)
        cfg.write(open("md.ini","w"))


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
