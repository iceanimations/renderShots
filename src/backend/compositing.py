'''
Created on Aug 6, 2015

@author: qurban.ali
'''
import sys
import nuke
import nukescripts
import os
osp = os.path

def createComp(args):
    shotPath = r"C:\Users\qurban.ali\Documents\render_shots"
    compPath = osp.join(shotPath, 'comps')
    if not osp.exists(compPath):
    os.mkdir(compPath)
    shots = ['SQ009_SH003', 'SQ009_SH004']
    
    for shot in shots:
    layers = os.listdir(osp.join(shotPath, shot))
    nodes = []
    if layers:
        for layer in layers:
            layerPath = osp.join(shotPath, layer)
            for aov in os.listdir(layerPath):
                if aov.lower().endswith('beauty'):
                    node = nuke.createNode('Read')
                    node.setName(layer)
                    nodes.append(node)
    else:
        pass
    if nodes:
        mergeNodes = []
        nukescripts.clear_selection_recursive()
        for node in nodes:
            if node.name().lower().startswith('cont'):
                node.setSelected(True)
        for node in nodes:
            if node.name().lower().startswith('env'):
                node.setSelected(True)
        if len(nuke.selectedNodes()) == 2:
            nukescripts.clear_selection_recursive()
            node = nuke.createNode('Merge')
            node.setSelected(True)
            mergeNodes.append(node)
        lastNode = nuke.selectedNode()
        nukescripts.clear_selection_recursive()

if __name__ == '__main__':
    createComp(sys.argv[1:])