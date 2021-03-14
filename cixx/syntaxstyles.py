#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 16:27:56 2021

@author: keziah
"""

from bs4 import BeautifulSoup
import os.path

user = os.path.expanduser('~')
path = os.path.join(user, 'src', 'syntax-highlighting')
syntaxFiles = os.path.join(path, 'data', 'syntax')

cxx = os.path.join(syntaxFiles, 'isocpp.xml')

with open(cxx) as fileobj:
    soup = BeautifulSoup(fileobj, "xml")
    
lsts = soup.language.highlighting.find_all('list')
highlighting = {}

for lst in lsts:
    name = lst['name']
    highlighting[name] = [item.text for item in lst.find_all('item')]