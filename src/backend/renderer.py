'''
Created on Jul 28, 2015

@author: qurban.ali
'''
import pymel.core as pc
import subprocess
import os.path as osp
import os
import rendering
reload(rendering)
import maya.cmds as cmds
import imaya
reload(imaya)
from PyQt4.QtGui import qApp

melPath = osp.join(osp.dirname(__file__), 'rendering.mel').replace('\\', '/')

homeDir = osp.join(osp.expanduser('~'), 'render_shots')
if not osp.exists(homeDir):
    os.mkdir(homeDir)
homeDir = homeDir.replace('/', '\\')

class Renderer(object):
    def __init__(self, parent=None):
        self.parentWin = parent
        
    def render(self, filename):
        cmds.file(filename, o=True, prompt=False, f=True)
        rendering.configureScene()
        layers = imaya.getRenderLayers()
        for layer in layers:
            layer.renderable.set(0)
        for layer in layers:
            layer.renderable.set(1)
            self.parentWin.setStatus('rendering: %s'%layer.name())
            pc.mel.mayaBatchRenderProcedure(1, "", "", "", "")
            layer.renderable.set(0)