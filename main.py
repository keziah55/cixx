#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run Cixx.
"""
import sys
from PyQt5.QtWidgets import QApplication
from cixx.cixx import Cixx

app = QApplication(sys.argv)
window = Cixx()
window.show()
sys.exit(app.exec_())
