# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'md.ui'
#
# Created: Tue Sep 17 10:50:54 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import dragTextEdit

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        
        Form.resize(911, 688)
        Form.setWindowOpacity(1.0)
        self.horizontalLayout_4 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))

        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.splitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.splitter.setFrameShadow(QtGui.QFrame.Plain)
        self.splitter.setLineWidth(1)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName(_fromUtf8("splitter"))


        
        self.editorBox = QtGui.QGroupBox(self.splitter)
        self.editorBox.setObjectName(_fromUtf8("editorBox"))
        
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.editorBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.plainTextEdit = dragTextEdit.DragTextEdit(self.editorBox)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        
        self.previewerBox = QtGui.QGroupBox(self.splitter)
        self.previewerBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.previewerBox.setObjectName(_fromUtf8("previewerBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.previewerBox)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.webView = QtWebKit.QWebView(self.previewerBox)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.horizontalLayout_3.addWidget(self.webView)
        self.horizontalLayout_4.addWidget(self.splitter)
        #设置扩展因子，为什么右边的要比左边的大这么多
        self.splitter.setStretchFactor(0, 66)
        self.splitter.setStretchFactor(1, 34)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.editorBox.setTitle(_translate("Form", "Edit", None))
        self.previewerBox.setTitle(_translate("Form", "Preview", None))

from PyQt4 import QtWebKit
