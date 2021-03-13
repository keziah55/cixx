#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeEditor widget.
"""

from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot as Slot
from .linenumberarea import LineNumberArea

class CodeEditor(QPlainTextEdit):
    
    def __init__(self):
        super().__init__()
        
        fixedFont = QFont("Monospace")
        self.setFont(fixedFont)
        
        self.lineNumArea = LineNumberArea(self)
        
        self.blockCountChanged.connect(self.updateLineNumAreaWidth)
        self.updateRequest.connect(self.lineNumArea.updateArea)
        self.cursorPositionChanged.connect(self.lineNumArea.update)
        
        self.updateLineNumAreaWidth(0)
        
        
    @Slot(int)
    def updateLineNumAreaWidth(self, count):
        self.setViewportMargins(self.lineNumArea.reqdWidth, 0, 0, 0)
        
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumArea.setGeometry(cr.left(), cr.top(), self.lineNumArea.reqdWidth, 
                                     cr.height())
        
    