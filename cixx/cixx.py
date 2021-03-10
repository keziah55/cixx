#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 21:08:25 2021

@author: keziah
"""

import os
import subprocess
from PyQt5.QtWidgets import (QMainWindow, QPlainTextEdit, QAction,  
                             QDockWidget, QDesktopWidget, QFileDialog)
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as Slot


# TODO syntax highlighter (make QPlainTextEdit subclass for input text?)
# TODO preferences dialog for default save/open location, default includes
# TODO set text cursor to right place
# TODO live syntax checking, e.g. semicolons

class Cixx(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.language = 'c++'
        self.langParams = {
            'c++':{'ext':'cxx',
                   'defaultIncludes':["iostream"]}}
        
        fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        
        self.textEdit = QPlainTextEdit()
        self.textEdit.setFont(fixedFont)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(fixedFont)
        
        user = os.path.expanduser('~')
        path = os.path.join(user, '.config', 'cixx')
        os.makedirs(path, exist_ok=True)
        ext = self.langParams[self.language]['ext']
        self.file = os.path.join(path, f"current_contents.{ext}")
        if not os.path.exists(self.file):
            text = self.initTextEdit()
            with open(self.file, 'w') as fileobj:
                fileobj.write(text)
                
        with open(self.file) as fileobj:
            text = fileobj.read()
            
        self.textEdit.setPlainText(text)
        
        self.createDockWidget(self.output, Qt.BottomDockWidgetArea, 
                              title="Output")
        
        self.setCentralWidget(self.textEdit)
        
        self.statusBar()
        
        self.createActions()
        self.createToolBar()
        
        self.setWindowTitle("Cixx")
        self.resize(700,600)
        self.centre()
        
    def centre(self):
        """ Centre window on screen. """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
    def initTextEdit(self):
        defaultIncludes = self.langParams[self.language]['defaultIncludes']
        include = [f"#include <{lib}>" for lib in defaultIncludes]
        s = '\n'.join(include)
        s += """
int main()
{
    
}"""
        return s
      
    @Slot()
    def save(self):
        home = os.path.expanduser('~')
        fileName, _ = QFileDialog.getSaveFileName(self, "Save file", home,
                                                  "C++ files (*cpp *cxx *h)")
        with open(fileName, 'w') as fileobj:
            fileobj.write(self.textEdit.plainText())
        
    
    @Slot()
    def open(self):
        home = os.path.expanduser('~')
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file", home,
                                                  "C++ files (*cpp *cxx *h)")
        with open(fileName) as fileobj:
            text = fileobj.read()
        self.textEdit.setPlainText(text)
    
    @Slot()
    def run(self):
        text = self.textEdit.toPlainText()
        with open(self.file, 'w') as fileobj:
            fileobj.write(text)
        p = subprocess.run(["g++", self.file], stdout=subprocess.PIPE, 
                           stderr=subprocess.STDOUT)
        if p.returncode == 0:
            self.statusBar().showMessage("Successfully compiled!")
            p = subprocess.run(["./a.out"], stdout=subprocess.PIPE, 
                           stderr=subprocess.STDOUT)
            output = p.stdout.decode()
        else:
            self.statusBar().showMessage("Errors")
            output = p.stdout.decode().replace(self.file, 'input')
        self.output.setPlainText(output)
    
    @Slot()
    def clearOutput(self):
        self.output.setPlainText("")
        
    def createDockWidget(self, widget, area, title=None):
        dock = QDockWidget()
        dock.setWidget(widget)
        if title is not None:
            dock.setWindowTitle(title)
        self.addDockWidget(area, dock)
        if not hasattr(self, "dockWidgets"):
            self.dockWidgets = []
        self.dockWidgets.append(dock)
        
    def createActions(self):
        
        self.saveIcon = QIcon().fromTheme("document-save-as")
        self.saveAct = QAction(self.saveIcon, "&Save", self, shortcut="Ctrl+S", 
                               statusTip="Save to file", toolTip= "Save to file", 
                               triggered=self.save)
        
        self.openIcon = QIcon().fromTheme("document-open")
        self.openAct = QAction(self.openIcon, "&Open", self, shortcut="Ctrl+O", 
                               statusTip="Open file", toolTip="Open file", 
                               triggered=self.open)
        
        # self.exitAct = QAction("&Exit", self, shortcut="Ctrl+Q", 
        #                        statusTip="Exit", triggered=self.close)
        
        self.runIcon = QIcon().fromTheme("media-playback-start")
        self.runAct = QAction(self.runIcon, "&Run", self, shortcut="F5", 
                              statusTip="Run the code", toolTip="Run the code", 
                              triggered=self.run)
        
        self.clearIcon = QIcon().fromTheme("edit-clear")
        self.clearAct = QAction(self.clearIcon, "&Clear", self, #hortcut="F5", 
                              statusTip="Clear the console", toolTip="Clear the console", 
                              triggered=self.clearOutput)
    
    def createToolBar(self):
        
        # menubar = self.menuBar()
        # self.fileMenu = menubar.addMenu('&File')
        # self.fileMenu.addAction(self.saveAct)
        # self.fileMenu.addAction(self.openAct)
        # self.fileMenu.addSeparator()
        # self.fileMenu.addAction(self.exitAct)
        
        self.fileToolbar = self.addToolBar("File")
        self.fileToolbar.addAction(self.saveAct)
        self.fileToolbar.addAction(self.openAct)
        
        self.runToolbar = self.addToolBar("Run")
        self.runToolbar.addAction(self.runAct)
        self.runToolbar.addAction(self.clearAct)
        
        