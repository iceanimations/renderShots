'''
Created on Aug 1, 2015

@author: qurban.ali
'''
import nuke
import sys
import os

def makeComp(shotPath):
    nuke.scriptOpen(r"R:\Pipe_Repo\Users\Qurban\nuke\template_for_render_shots.nk")
    layers = os.listdir(shotPath)
    if layers:
        

if __name__ == '__main__':
    makeComp(sys.argv[1])