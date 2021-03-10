#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:48:40 2021

@author: keziah
"""

from PyQt5.QtWidgets import (QWidget, QPlainTextEdit, QAction,  
                             QDockWidget, QDesktopWidget, QFileDialog)
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtCore import Qt, pyqtSlot as Slot

class LineNumberArea(QWidget):
    
    def __init__(self):
        super().__init__()