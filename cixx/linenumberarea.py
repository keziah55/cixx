#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:48:40 2021

@author: keziah
"""

from PyQt5.QtWidgets import (QWidget, QPlainTextEdit, QAction,  
                             QDockWidget, QDesktopWidget, QFileDialog)
from PyQt5.QtGui import QFontDatabase, QIcon, QPainter, QTextBlock, QFontMetrics
from PyQt5.QtCore import Qt, QSize, pyqtSlot as Slot

# https://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html

class LineNumberArea(QWidget):
    
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        
    def sizeHint(self):
        return QSize(self.codeEditor.lineNumAreaWidth, 0)
    
    def paintEvent(self, event):
        
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.lightGray)
        
        block = self.editor.firstVisibleBlock()
        blockNumber = block.blockNumber()
        
        bounds = self.editor.blockBoundingGeometry(block)
        rect = self.editor.blockBoundingRect(block)
        offset = self.editor.contentOffset()
        top = bounds.translated(offset).top()
        bottom = top + rect.height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.width(), fontMetrics.height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            rect = self.editor.blockBoundingRect(block)
            bottom = top + rect.height()
            blockNumber += 1
    
    