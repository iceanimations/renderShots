import sys
sys.path.extend([r"R:\Pipe_Repo\Users\Hussain\utilities\loader\command\python",
                 r"R:\Pipe_Repo\Projects\TACTIC"])
import RedshiftAOVTools
import os.path as osp
import pymel.core as pc
import imaya
reload(imaya)

homeDir = osp.join(osp.expanduser('~'), 'render_shots')

def configureScene(parent):
    f = open(osp.join(homeDir, 'info.txt'))
    shot = f.read()
    f.close()
    ws = pc.workspace(o=True, q=True)
    pc.workspace(homeDir, o=True)
    node = pc.PyNode('redshiftOptions')
    
    node.imageFilePrefix.set("%s\<RenderLayer>\<RenderLayer>_<AOV>\<RenderLayer>_<AOV>_"%shot)
    RedshiftAOVTools.fixAOVPrefixes()
    
    try:
        for aov in pc.ls(type=pc.nt.RedshiftAOV):
            aov.filePrefix.set(aov.filePrefix.get().replace('<Camera>', shot))
    except AttributeError:
        parent.showMessage(msg='It seems like Redshift is not installed or not loaded')
        return
    
    pc.setAttr('defaultRenderGlobals.animation', 1)
    pc.setAttr('defaultResolution.width', 960)
    pc.setAttr('defaultResolution.height', 540)
    pc.setAttr('defaultResolution.deviceAspectRatio', 1.778)

    minTime = pc.playbackOptions(q=True, minTime=True) 
    maxTime = pc.playbackOptions(q=True, maxTime=True) 
    diff = maxTime - minTime
    step = diff/2.0
    # configure frame range for each layer
    for layer in imaya.getRenderLayers():
        pc.editRenderLayerGlobals(currentRenderLayer=layer)
        pc.setAttr('defaultRenderGlobals.startFrame', minTime)
        pc.setAttr('defaultRenderGlobals.endFrame', maxTime)
        #pc.editRenderLayerAdjustment('defaultRenderGlobals.byFrameStep', remove=True)
        pc.setAttr('defaultRenderGlobals.byFrameStep', step)

    pc.workspace(ws, o=True)
    if diff%2 != 0:
        step += 0.5
    return [int(minTime), int(minTime + step), int(maxTime)]