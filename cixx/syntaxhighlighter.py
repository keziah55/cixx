#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 16:06:24 2021

@author: keziah
"""
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt5.QtCore import Qt, QRegularExpression

# https://doc.qt.io/qt-5/qtwidgets-richtext-syntaxhighlighter-example.html

class CxxHighlighter(QSyntaxHighlighter):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.rules = []
        
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)
        keywordPatterns = [
            "\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
            "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b",
            "\\bfriend\\b", "\\binline\\b", "\\bint\\b",
            "\\blong\\b", "\\bnamespace\\b", "\\boperator\\b",
            "\\bprivate\\b", "\\bprotected\\b", "\\bpublic\\b",
            "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
            "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
            "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
            "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b",
            "\\bvoid\\b", "\\bvolatile\\b", "\\bbool\\b"]
        
        for pattern in keywordPatterns:
            rule = {'pattern':QRegularExpression(pattern), 'format':keywordFormat}
            self.rules.append(rule)
    
        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        rule = {'pattern':QRegularExpression("\\bQ[A-Za-z]+\\b"), 'format':classFormat}
        self.rules.append(rule)
    
        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        rule = {'pattern':QRegularExpression("\".*\""), 'format':quotationFormat}
        self.rules.append(rule)
    
        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(Qt.blue)
        rule = {'pattern':QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()"), 
                'format':functionFormat}
        self.rules.append(rule)
        
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.red)
        rule = {'pattern':QRegularExpression("//[^\n]*"), 
                'format':singleLineCommentFormat}
        self.rules.append(rule)
    
        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)
        self.commentStartExpression = QRegularExpression("/\\*")
        self.commentEndExpression = QRegularExpression("\\*/")
        
        
    def highlightBlock(self, text):
        
        for rule in self.rules:
            pass
        
        