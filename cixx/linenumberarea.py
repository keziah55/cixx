#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:48:40 2021

@author: keziah
"""

from PyQt5.QtWidgets import (QWidget, QPlainTextEdit, QAction,  
                             QDockWidget, QDesktopWidget, QFileDialog)
from PyQt5.QtGui import QFontDatabase, QIcon, QPainter, QTextBlock, QFontMetrics, QColor
from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot as Slot

# https://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html

class LineNumberArea(QWidget):
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        
    def sizeHint(self):
        return QSize(self.reqdWidth, 0)
    
    @property 
    def fontMetrics(self):
        return self.editor.fontMetrics()
    
    @property 
    def reqdWidth(self):
        mx = max(1, self.editor.blockCount())
        digits = len(str(mx))
        space = 5 + self.fontMetrics.horizontalAdvance('0' * digits)
        return space
    
    @Slot(QRect, int)
    def updateArea(self, rect, dy):
        if dy > 0:
            self.scroll(0, dy)
        else:
            self.update(0, rect.y(), self.reqdWidth, rect.height())
        
        if rect.contains(self.editor.viewport().rect()):
            self.editor.updateLineNumAreaWidth(0)
            
    def getBoundingRect(self, block):
        return self.editor.blockBoundingRect(block)
    
    def getBoundingGeometry(self, block):
        return self.editor.blockBoundingGeometry(block)
    
    
    def paintEvent(self, event):
        
        painter = QPainter(self)
        # painter.fillRect(event.rect(), Qt.lightGray)
        
        block = self.editor.firstVisibleBlock()
        num = block.blockNumber()
        
        bounds = self.getBoundingGeometry(block)
        rect = self.getBoundingRect(block)
        offset = self.editor.contentOffset()
        top = bounds.translated(offset).top()
        bottom = top + rect.height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                
                cursor = self.editor.textCursor()
                font = painter.font()
                if num == cursor.blockNumber():
                    bold = True
                    colour = Qt.white
                else:
                    bold = False
                    colour = QColor("#a3a3a3")
                    
                painter.setPen(colour)
                font.setBold(bold)
                painter.setFont(font)
                painter.drawText(0, top, self.width(), 
                                 self.fontMetrics.height(),
                                 Qt.AlignRight, f"{num+1}")
            block = block.next()
            top = bottom
            rect = self.getBoundingRect(block)
            bottom = top + rect.height()
            num += 1
    
    