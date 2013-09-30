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
    fil = QtCore.QFile(os.getcwd() + '/qss/%s' % f)
    fil.open(QtCore.QFile.ReadOnly)

    styleSheet = fil.readAll()
    styleSheet = unicode(styleSheet, encoding='utf8')
    fil.close()
    return styleSheet


class MDDialog(QtGui.QDialog):
    
    def __init__(self, parent=None, title='', label='', isImg=False):
        super(MDDialog, self).__init__(parent)

        self.resize(400,80)
        self.setWindowTitle(title)
        
        self.isImg = isImg
        
        titleLabel = None
        # 如果当前对话框是图片对话框
        if self.isImg:
            titleLabel = QtGui.QLabel("Enter your image title: ")
            self.titleEdit = QtGui.QLineEdit()
            self.titleEdit.setObjectName("titleEdit")
            titleLabel.setBuddy(self.titleEdit)
        
        label = QtGui.QLabel(label)
        self.urlEdit = QtGui.QLineEdit()
        self.urlEdit.setText("http://")
        label.setBuddy(self.urlEdit)

        okButton = QtGui.QPushButton("OK")
        okButton.setDefault(True)

        cancelButton = QtGui.QPushButton("Cancel")

        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttonBox.addButton(okButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(cancelButton, QtGui.QDialogButtonBox.ActionRole)
        
        topTitleLayout = None
        if self.isImg:
            topTitleLayout = QtGui.QHBoxLayout()
            topTitleLayout.addWidget(titleLabel)
            topTitleLayout.addWidget(self.titleEdit)

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(label)
        topLayout.addWidget(self.urlEdit)
        


        bottomLayout = QtGui.QHBoxLayout()
        bottomLayout.addWidget(buttonBox)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addSpacing(3)
        if isImg:
            mainLayout.addLayout(topTitleLayout, 1)
        mainLayout.addLayout(topLayout, 2)
        mainLayout.addLayout(bottomLayout, 3)
        #mainLayout.addWidget(buttonBox, 0, 1)
        self.setLayout(mainLayout)
        
        okButton.clicked.connect(self.okClicked)
        cancelButton.clicked.connect(self.cancelClicked)
        
        self.accepted.connect(self.doAccepted)
        self.resText = self.resTitle = ''

    
    @staticmethod
    def getText(parent, title, label, isImg=False):
        dlg = MDDialog(parent, title, label, isImg)
        #dlg.setModal(True)
        #dlg.show()
        #exec_运行的对话框会阻止当前线程的运行
        dlg.exec_()
        return (dlg.resText, dlg.result(), dlg.resTitle)
    
    def doAccepted(self):
        self.resText = self.urlEdit.text()
        self.resTitle = False
        if self.isImg:
            self.resTitle = self.titleEdit.text()
        
        self.close()
    
    def okClicked(self):
        self.accept()
    
    def cancelClicked(self):
        self.reject()
        self.close()
        
        

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
        
    def __updatePreview(self):
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
        self.timer.stop()
        self.timer.timeout()
        self.timer = None
        del self.timer

    def previewMD(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__updatePreview)
        self.timer.start(10)

        


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__baseWindowTitle = "MDChick Editor"
        self.__windowTitle = self.__baseWindowTitle
        self.setWindowTitle(self.__windowTitle)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setMinimumSize(800, 600)
        self.center()
        self.showMaximized()
        self.setDocumentMode(True)
        
        self.createActions()
        self.createMenus()
        self.createToolBar()
        
        self.centralWidget = MDChick(self)
        
        self.setCentralWidget(self.centralWidget)
        
        self.setStartupText()
        QtGui.qApp.setStyleSheet(read_stylesheet("style.qss"))
        
        self.tempDir = self.loadTempDir()
        self.centralWidget.plainTextEdit.setMainWindow(self)
        
        #PyQt 4.5 引入的新的槽机制
        self.centralWidget.plainTextEdit.textChanged.connect(self.MDTextChanged)
        
        ### 当前文件的保存状态
        self.issaved = True
        
    def center(self):
        """使控件居中
        """
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        

       
    def MDTextChanged(self):
        """ MD编辑器的文本发生改变时调用
        """
        self.setWindowTitle(self.__windowTitle + " *")
        ## 每次编辑都会都预览
        self.centralWidget.previewMD()
        self.issaved = False
        
    
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
        
        self.saveAsAct = QtGui.QAction("Save &As", self,
                shortcut=QtGui.QKeySequence.SaveAs,
                statusTip="Save the Markdown file to disk as a other name.", triggered=self.save)

        self.exitAct = QtGui.QAction("E&xit", self,
                shortcut=QtGui.QKeySequence.Quit,
                statusTip="Exit the application", triggered=self.close)
        
        self.boldAct = QtGui.QAction("&Bold", self,
                statusTip="Make the text style to bold",
                triggered=self.bold)
        self.boldAct.setIcon(QtGui.QIcon('bold.png'))
        self.boldAct.setShortcut('Ctrl+B')
        
        self.italicAct = QtGui.QAction("&Italic", self,
                statusTip="Make the text style to italic",
                triggered=self.italic)
        self.italicAct.setIcon(QtGui.QIcon('italic.png'))
        self.italicAct.setShortcut('Ctrl+I')
        
        self.linkAct = QtGui.QAction("&Link", self,
                statusTip="Add link to document",
                triggered=self.addlink)
        self.linkAct.setIcon(QtGui.QIcon('link.png'))
        self.linkAct.setShortcut('Ctrl+L')
        
        self.codeAct = QtGui.QAction("&Code", self,
                statusTip="Add code block to document",
                triggered=self.addCode)
        self.codeAct.setIcon(QtGui.QIcon('code.png'))
        self.codeAct.setShortcut('Ctrl+Shift+C')
        
        self.imageAct = QtGui.QAction("&Image", self,
                statusTip="Add image to document",
                triggered=self.addImage)
        self.imageAct.setIcon(QtGui.QIcon('image.png'))
        self.imageAct.setShortcut('Ctrl+Shift+I')
        

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)
        
        self.mdDocAct = QtGui.QAction("&Markdown Help", self,
                statusTip="Show the help of the markdown.",
                triggered=self.mddoc)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        
        
        self.menuBar().addSeparator()
        
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.boldAct)
        self.editMenu.addAction(self.italicAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.linkAct)
        self.editMenu.addAction(self.codeAct)
        self.editMenu.addAction(self.imageAct)
        
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.mdDocAct)
        
    def createToolBar(self):
        toolbar = self.addToolBar('Edit')
        toolbar.addAction(self.boldAct)        
        toolbar.addAction(self.italicAct)
        toolbar.addSeparator()
        toolbar.addAction(self.linkAct)
        toolbar.addAction(self.codeAct)
        toolbar.addAction(self.imageAct)
        

    def about(self): 
        QtGui.QMessageBox.about(self, u"About MDChick",
                u"<b>MdChick</b> is a editor which can be used to<br/> edit and preview the Markdown text.")
        
    def bold(self):
        cursor = self.centralWidget.plainTextEdit.textCursor()
        selText = cursor.selectedText ()
        cursor.removeSelectedText()
        cursor.insertText ("**%s**" %(selText))
            
    def italic(self):
        cursor = self.centralWidget.plainTextEdit.textCursor()
        selText = cursor.selectedText()
        cursor.removeSelectedText()
        cursor.insertText ("*%s*" %(selText))
        
    def addlink(self):
        """添加链接
        """
        
        url, ok, _t = MDDialog.getText(self, 'Add Link', 'Enter your url:')
        if ok:
            cursor = self.centralWidget.plainTextEdit.textCursor()
            selText = cursor.selectedText()
            cursor.removeSelectedText()
            if selText == "":
                selText = url
            cursor.insertText ("[%s](%s)" %(selText, url))

            
    
    def addImage(self):
        """添加图片
        """
        url, ok, title = MDDialog.getText(self, 'Add Image',
            'Enter your image url:', True)
        if ok:
            cursor = self.centralWidget.plainTextEdit.textCursor()
            cursor.removeSelectedText()
            if title == False or title == None or title == '':
                title = url
            cursor.insertText ("![%s](%s)" %(title, url))
    
    def addCode(self):
        cursor = self.centralWidget.plainTextEdit.textCursor()
        selText = cursor.selectedText()
        cursor.removeSelectedText()
        selTexts = selText.split(u"\u2029")
        selText = u"\u2029    ".join(selTexts)
        cursor.insertText (u"\u2029    %s" % (selText))
    
    def mddoc(self):
        ### 用系统默认浏览器打开指定的网页
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://wowubuntu.com/markdown/"))

    def open(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, directory=self.tempDir,\
                                                           filter = self.tr("Markdown File (*.md *.markdown)"))
        
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
            
            ### 改变窗口的标题
            self.__windowTitle = "%s - %s" %(self.__baseWindowTitle, os.path.basename(self.fileName))
            self.setWindowTitle(self.__windowTitle)
            self.issaved = True

    def save(self):
        content = self.centralWidget.plainTextEdit.toPlainText()

        if not hasattr(self, "fileName") or self.fileName is None or self.fileName == '':
            self.fileName = QtGui.QFileDialog.getSaveFileName(self, caption=self.tr("Save Markdown File"),\
                                                          directory=self.tempDir,
                                                          filter = self.tr("Markdown File (*.md *.markdown)"))
            self.writeDirConfig(os.path.dirname(self.fileName))
            ##改变窗口的标题
            self.__windowTitle = "%s - %s" %(self.__baseWindowTitle, os.path.basename(self.fileName))
            
        fd = None
        
        if self.fileName:
            fd = QtCore.QFile(self.fileName)
                
        if fd is not None and not fd.open(QtCore.QIODevice.WriteOnly):
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
        self.setWindowTitle(self.__windowTitle)
        self.issaved = True
        
    def updateTextEdit(self):
        mainFrame = self.centralWidget.webView.page().mainFrame()
        
        frameText = mainFrame.toHtml()
        self.centralWidget.plainTextEdit.setPlainText(frameText)

    def setStartupText(self):
        """编辑器初始的字符串
        """
        self.centralWidget.previewMD()
        
        
    def writeDirConfig(self, dd):
        if dd is None or dd == "":
            return
        self.tempDir = dd
        cfg = RawConfigParser()
        cfg.add_section("TempDir")
        cfg.set("TempDir", "TempDir", dd)
        cfg.write(open("md.ini","w"))
        
    def closeEvent(self, event):
        """窗口关闭处理函数
        """
        if not self.issaved:
            reply = QtGui.QMessageBox.question(self, 'Message',
                "You have a unsaved file, sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    
            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
