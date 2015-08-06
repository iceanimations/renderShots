'''
Created on Aug 1, 2015

@author: qurban.ali
'''
import sys
import os
osp = os.path
import renderer
reload(renderer)

homeDir = renderer.homeDir
compPath = osp.join(homeDir, 'comps')
if not osp.exists(compPath):
    os.mkdir(compPath)

nukePath = r"C:\Program Files\Nuke8.0v5\python.exe"
if not osp.exists(nukePath):
    nukePath = r"C:\Program Files\Nuke9.0v4\python.exe"


class CompMaker(object):
    def __init__(self, parent=None):
        self.parentWin = parent
        
    def setStatus(self, status):
        if self.parentWin:
            self.parentWin.setStatus(status)
            
    def setSubStatus(self, msg):
        if self.parentWin:
            self.parentWin.setSubStatus(msg)
    
    def make(self):
        pass