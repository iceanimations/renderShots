'''
Created on Aug 1, 2015

@author: qurban.ali
'''
import os
osp = os.path
import renderer
reload(renderer)
import subprocess
import re

homeDir = renderer.homeDir
compPath = osp.join(homeDir, 'comps')
if not osp.exists(compPath):
    os.mkdir(compPath)

compositingFile = osp.join(osp.dirname(__file__), 'compositing.py')

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
    
    def make(self, shots):
        os.chdir(osp.dirname(nukePath))
        values = []
        command = 'python %s'%(compositingFile)
        for shot in shots:
            values.append(shot)
        with open(osp.join(homeDir, 'info1.txt'), 'w') as f:
            f.write(str(values))
        self.setStatus('Creating and rendering comps')
        subprocess.call(command, shell=True)
        
    def rename(self, frames):
        renderPath = osp.join(compPath, 'renders')
        for shot, frame in frames.items():
            shotPath = osp.join(renderPath, shot)
            files = sorted(os.listdir(shotPath))
            for ph, fr in zip(files, frame):
                name = shotPath, re.sub('\.\d+\.', fr, ph)
                os.rename(osp.join(shotPath, ph), osp.join(shotPath, name))