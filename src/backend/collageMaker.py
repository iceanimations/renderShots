'''
Created on Jul 28, 2015

@author: qurban.ali
'''
import os.path as osp
import renderer
reload(renderer)
import os
import compMaker
reload(compMaker)
import subprocess

homeDir = renderer.homeDir
collageDir = osp.join(homeDir, 'collage')
if not osp.exists(collageDir):
    os.mkdir(collageDir)
compDir = compMaker.compPath
compRenderDir = osp.join(compDir, 'renders')

class CollageMaker(object):
    def __init__(self, parent=None):
        super(CollageMaker, self).__init__()
        self.parentWin = parent
        
    def makeShot(self, shot):
        path = osp.join(compRenderDir, shot)
        if osp.exists(path):
            command = r"R:\Pipe_Repo\Users\Qurban\applications\ImageMagick\montage.exe -geometry +1+1"
            files = sorted(os.listdir(path))
            if files:
                for phile in files:
                    command += ' %s'%osp.join(path, phile)
                command += ' %s'%osp.join(collageDir, shot+'.png')
                subprocess.call(command, shell=True)
    
    def make(self):
        command = r"R:\Pipe_Repo\Users\Qurban\applications\ImageMagick\montage.exe -geometry +1+1 -label %f -frame 5 -background '#336699'"
        for phile in sorted(os.listdir(collageDir)):
            command += ' %s'%osp.join(collageDir, phile)
        collagePath = osp.join(collageDir, 'collage.png')
        command += ' %s'%collagePath
        subprocess.call(command, shell=True)
        return collagePath