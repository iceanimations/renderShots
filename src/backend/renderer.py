'''
Created on Jul 28, 2015

@author: qurban.ali
'''
import pymel.core as pc
import os.path as osp
import os
import rendering
reload(rendering)
import imaya
reload(imaya)
from PyQt4.QtGui import qApp
import subprocess

melPath = osp.join(osp.dirname(__file__), 'rendering.mel').replace('\\', '/')

homeDir = osp.join(osp.expanduser('~'), 'render_shots')
if not osp.exists(homeDir):
    os.mkdir(homeDir)
homeDir = homeDir.replace('/', '\\')
os.environ['PYTHONPATH'] += ';'+osp.dirname(__file__)

class Renderer(object):
    def __init__(self, parent=None):
        self.parentWin = parent
        
    def render(self, filename, batch=False):
        if batch:
            command = r"C:\Program Files\Autodesk\Maya2015\bin\mayabatch.exe -file %s"%osp.normpath(filename)
            command += r' -command "source \"%s\""'%melPath
            subprocess.call(command)
        else:
            self.parentWin.setSubStatus('Opening %s'%filename)
            imaya.openFile(filename)
            self.parentWin.setSubStatus('Configuring scene')
            
            frames = rendering.configureScene(self.parentWin)
            
            layers = imaya.getRenderLayers()
            for layer in layers:
                layer.renderable.set(0)
            length = len(layers)
            i = 1
            for layer in layers:
                layer.renderable.set(1)
                self.parentWin.setSubStatus('rendering: %s (%s of %s)'%(layer.name(), i, length))
                pc.mel.mayaBatchRenderProcedure(1, "", "", "", "")
                self.parentWin.setSubStatus('')
                layer.renderable.set(0)
                i += 1
            return frames