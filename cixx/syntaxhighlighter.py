#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 16:06:24 2021

@author: keziah
"""
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt5.QtCore import Qt, QRegularExpression

# https://doc.qt.io/qt-5/qtwidgets-richtext-syntaxhighlighter-example.html

# TODO read xml files from https://github.com/KDE/syntax-highlighting
# /home/keziah/src/syntax-highlighting/data/syntax/

class CxxHighlighter(QSyntaxHighlighter):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.rules = []
        
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#0016ba"))
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
            "\\bvoid\\b", "\\bvolatile\\b", "\\bbool\\b",
            "\\bchar8_t\\b", "\\bchar16_t\\b", "\\bchar32_t\\b",]
        
        for pattern in keywordPatterns:
            rule = {'pattern':QRegularExpression(pattern), 'format':keywordFormat}
            self.rules.append(rule)
            
        keyword2Format = QTextCharFormat()
        keyword2Format.setForeground(QColor("#0016ba"))
        keyword2Format.setFontWeight(QFont.Bold)
        keyword2Patterns = [
            "\\balignas\\b", "\\balignof\\b", "\\band\\b", "\\band_eq\\b", 
            "\\basm\\b", "\\batomic_cancel\\b", "\\batomic_commit\\b",
            "\\batomic_noexcept\\b", "\\bauto\\b", "\\bbitand\\b", "\\bbitor\\b",
            "\\bbreak\\b", "\\bcase\\b", "\\bcatch\\b", "\\bcompl\\b", "\\bconcept\\b", 
            "\\bconsteval\\b", "\\bconstexpr\\b", "\\bconstinit\\b", "\\bconst_cast\\b",
            "\\bcontinue\\b", "\\bco_await\\b", "\\bco_return\\b", "\\bco_yield\\b", 
            "\\bdecltype\\b", "\\bdefault\\b", 
            ]
        
        for pattern in keyword2Patterns:
            rule = {'pattern':QRegularExpression(pattern), 'format':keyword2Format}
            self.rules.append(rule)
    
        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        rule = {'pattern':QRegularExpression("\\bQ[A-Za-z]+\\b"), 'format':classFormat}
        self.rules.append(rule)
    
        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor("#c90000"))
        rule = {'pattern':QRegularExpression("\".*\""), 'format':quotationFormat}
        self.rules.append(rule)
        
        directiveFormat = QTextCharFormat()
        directiveFormat.setForeground(QColor("#c95508"))
        rule = {'pattern':QRegularExpression("#.*"), 
                'format':directiveFormat}
        self.rules.append(rule)
        
        stdFormat = QTextCharFormat()
        stdFormat.setForeground(QColor("#8c8c8c"))
        rule = {'pattern':QRegularExpression("std::[A-Za-z]+"), 
                'format':stdFormat}
        self.rules.append(rule)
    
        # functionFormat = QTextCharFormat()
        # functionFormat.setForeground(Qt.blue)
        # rule = {'pattern':QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()"), 
        #         'format':functionFormat}
        # self.rules.append(rule)
        
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.darkGreen)
        rule = {'pattern':QRegularExpression("//[^\n]*"), 
                'format':singleLineCommentFormat}
        self.rules.append(rule)
    
        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)
        self.commentStartExpression = QRegularExpression("/\\*")
        self.commentEndExpression = QRegularExpression("\\*/")
        
        
    def highlightBlock(self, text):
        
        for rule in self.rules:
            matchIter = rule['pattern'].globalMatch(text)
        
            while matchIter.hasNext():
                match = matchIter.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule['format'])
                
        self.setCurrentBlockState(0)
        
        startIdx = 0
        if self.previousBlockState() != 1:
            startIdx = text.find(self.commentStartExpression.pattern())
            
        while startIdx >= 0:
            
            match = self.commentEndExpression.match(text, startIdx)
            endIdx = match.capturedStart()
            commentLength = 0
            if endIdx == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIdx
            else:
                commentLength = endIdx - startIdx + match.capturedLength()
            self.setFormat(startIdx, commentLength, self.multiLineCommentFormat)
            startIdx = text.find(self.commentStartExpression.pattern(), start=startIdx+commentLength)
                
                
                
        