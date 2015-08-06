'''
Created on Jul 28, 2015

@author: qurban.ali
'''
import pymel.core as pc
import os.path as osp
import renderer
reload(renderer)

homeDir = renderer.homeDir
projectDir = pc.workspace(q=True, o=True)

class CollageMaker(object):
    def __init__(self, parent=None):
        super(CollageMaker, self).__init__()
        self.parentWin = parent
        
    def makeShot(self, shot):
        
        pass
    
    def make(self):
        pass