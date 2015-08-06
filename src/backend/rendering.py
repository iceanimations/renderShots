import sys
sys.path.extend([r"R:\Pipe_Repo\Users\Hussain\utilities\loader\command\python",
                 r"R:\Pipe_Repo\Projects\TACTIC"])
import RedshiftAOVTools
import os.path as osp
import pymel.core as pc
import imaya
reload(imaya)

homeDir = osp.join(osp.expanduser('~'), 'render_shots')

def configureScene():
    f = open(osp.join(homeDir, 'info.txt'))
    shot = f.read()
    f.close()
    
    node = pc.PyNode('redshiftOptions')
    
    node.imageFilePrefix.set("<Camera>\<RenderLayer>\<RenderLayer>_<AOV>\<RenderLayer>_<AOV>_")
    RedshiftAOVTools.fixAOVPrefixes()
    
    node.imageFilePrefix.set(node.imageFilePrefix.get().replace('<Camera>', shot))

    for aov in pc.ls(type=pc.nt.RedshiftAOV):
        aov.filePrefix.set(aov.filePrefix.get().replace('<Camera>', shot))
    
    pc.setAttr('defaultRenderGlobals.animation', 1)
    pc.setAttr('defaultResolution.width', 320)
    pc.setAttr('defaultResolution.height', 240)
    pc.setAttr('defaultResolution.deviceAspectRatio', 1.333)
    
    # configure frame range for each layer
    for layer in imaya.getRenderLayers():
        pc.editRenderLayerGlobals(currentRenderLayer=layer)
        minTime = pc.getAttr('defaultRenderGlobals.startFrame')
        maxTime = pc.getAttr('defaultRenderGlobals.endFrame')
        diff = maxTime - minTime
        step = diff/2.0
        if not layer.name().lower().startswith('defaultrenderlayer'):
            pc.editRenderLayerAdjustment('defaultRenderGlobals.byFrameStep')
        pc.setAttr('defaultRenderGlobals.byFrameStep', step)

    layers = imaya.getRenderLayers()
    for layer in layers:
        layer.renderable.set(0)
    for layer in layers:
        layer.renderable.set(1)
        pc.mel.mayaBatchRenderProcedure(1, "", "", "", "")
        layer.renderable.set(0)