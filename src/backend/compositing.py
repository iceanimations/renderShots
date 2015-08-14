'''
Created on Aug 6, 2015

@author: qurban.ali
'''
import sys
import nuke
import nukescripts
import os
osp = os.path
import shutil
import re

#homeDir = osp.join(osp.expanduser('~'), 'render_shots')

def createNode(nodeName):
    node = nuke.createNode(nodeName)
    nukescripts.clear_selection_recursive()
    node.setSelected(True)
    
def createReadNode(nodes, layerName):
    for node in nodes:
        if node.name().lower().startswith(layerName):
            node.setSelected(True)
            break

def createComp(shots):
    
    compPath = osp.join(homeDir, 'comps')
    if not osp.exists(compPath):
        os.mkdir(compPath)
    
    for phile in os.listdir(compPath):
        filePath = osp.join(compPath, phile)
        if osp.isfile(filePath):
            try:
                os.remove(filePath)
            except:
                pass
        elif osp.isdir(filePath):
            try:
                shutil.rmtree(filePath)
            except:
                pass
    
    rendersPath = osp.join(compPath, 'renders')
    if not osp.exists(rendersPath):
        os.mkdir(rendersPath)
    
    for shot in shots:
        shotPath = osp.join(homeDir, shot)
        layers = os.listdir(shotPath)
        nodes = []
        if layers:
            for layer in layers:
                layerPath = osp.join(shotPath, layer)
                for aov in os.listdir(layerPath):
                    if aov.lower().endswith('beauty'):
                        node = nuke.createNode('Read')
                        aovPath = osp.join(layerPath, aov)
                        filenames = os.listdir(aovPath)
                        if filenames:
                            match = re.search('\.\d+\.', filenames[0])
                            if match:
                                frames = [int(re.search('\.\d+\.', phile).group()[1:-1]) for phile in filenames]
                                frames = sorted(frames)
                                for i, frame in enumerate(frames):
                                    for phile in filenames:
                                        if str(frame) in phile:
                                            try:
                                                os.rename(osp.join(aovPath, phile), osp.join(aovPath, re.sub('\.\d+\.', '.'+str(i+1)+'.', phile)))
                                            except:
                                                pass
                                frames = [1, 2, 3]
                                #hashes = '.'+'#'* (len(match.group()) -2) +'.'
                                node.knob('file').setValue(osp.join(aovPath, re.sub('\.\d+\.', '.#.', filenames[0])).replace('\\', '/'))
                                node.knob('first').setValue(min(frames)); node.knob('origfirst').setValue(min(frames))
                                node.knob('last').setValue(max(frames)); node.knob('origlast').setValue(max(frames))
                                node.setName(layer)
                                nodes.append(node)
        if nodes:
            
            nukescripts.clear_selection_recursive()
            createReadNode(nodes, 'cont')
            createReadNode(nodes, 'env')
            if len(nuke.selectedNodes()) == 2:
                createNode('Merge')
            try:
                lastNode = nuke.selectedNode()
            except:
                lastNode = None
            nukescripts.clear_selection_recursive()
            createReadNode(nodes, 'shadow')
            if lastNode: lastNode.setSelected(True)
            try:
                if len(nuke.selectedNodes()) == 2:
                    createNode('Merge')
                lastNode = nuke.selectedNode()
                nukescripts.clear_selection_recursive()
            except:
                pass
            createReadNode(nodes, 'char')
            if lastNode: lastNode.setSelected(True)
            try:
                if len(nuke.selectedNodes()) == 2:
                    createNode('Merge')
            except:
                return
            writeNode = nuke.createNode('Write')
            renderShotDir = osp.join(rendersPath, shot)
            if not osp.exists(renderShotDir):
                os.mkdir(renderShotDir)
            writeNode.knob('file').setValue(osp.join(renderShotDir, shot +'.#####.jpg').replace('\\', '/'))
            nuke.scriptSaveAs(osp.join(compPath, shot+'.nk'), 1)
            nuke.execute(writeNode, 1, 3, continueOnError=True)
        nuke.scriptClose()
        
        #TODO: rename the render files to contain their original frame numbers
        

if __name__ == '__main__':
    shots = None
    with open(osp.join(osp.expanduser('~'), 'compositing', 'info.txt')) as f:
        shots = eval(f.read())
    if shots:
        try:
            homeDir = shots[0]
            createComp(shots[1:])
        except Exception as ex:
            print ex