#-------------------------------------------------------------------------------
#-*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        dragTextEditor.py
# Purpose:
#
# Author:      daimin
#
# Created:     2013-9-23
# Copyright:   (c) daimin 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------'''
from PyQt4 import QtCore, QtGui

class DragTextEdit(QtGui.QTextEdit):
    changed = QtCore.pyqtSignal(QtCore.QMimeData)
        
    def __init__(self, parent = None):
        super(DragTextEdit, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.setTabStopWidth(16)
        
    def dragEnterEvent(self, event):
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        event.acceptProposedAction()
        self.changed.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasImage():
            self.setPixmap(QtGui.QPixmap(mimeData.imageData()))
        elif mimeData.hasHtml():
            self.setPlainText(mimeData.html())
        elif mimeData.hasText():
            self.setPlainText(mimeData.text())
        elif mimeData.hasUrls():
            urls = mimeData.urls()
            if urls is not None and len(urls) > 0:
                url = urls[0]
                url = url.toLocalFile()
                self.setPlainText(self.getContentByUrl(url))
                self.minWin.fileName = url
                
            
        else:
            self.setPlainText("Cannot display data")
            
        self.minWin.centralWidget.previewMD()
        self.setBackgroundRole(QtGui.QPalette.Dark)
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.clear()
        event.accept()
        
    def getContentByUrl(self, url):
        
        fd = QtCore.QFile(url)
        if not fd.open(QtCore.QIODevice.ReadOnly):
                QtGui.QMessageBox.information(self, self.tr("Unable to open file"),
                        fd.errorString())
                return
        txtStream = QtCore.QTextStream(fd)
        txtCodec = QtCore.QTextCodec.codecForName("UTF-8")
        txtStream.setCodec(txtCodec)
        output = txtStream.readAll()
        fd.close()
        return output
    
    def setMainWindow(self, win):
        """主窗体
        """
        self.minWin = win
        
    def scrollContentsBy(self, dx, dy):
        #刷新界面
        self.viewport().update()
        super(DragTextEdit, self).scrollContentsBy(dx, dy)
        self.minWin.centralWidget.webView.page().mainFrame().scroll(dx, -20 * dy)
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText ("    ")
        else:
            event.accept()
        
        super(DragTextEdit, self).keyPressEvent(event)
            
        
        
        
        
        