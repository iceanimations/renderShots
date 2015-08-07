'''
Created on Jul 28, 2015

@author: qurban.ali
'''
from uiContainer import uic
from PyQt4.QtGui import QMessageBox, QFileDialog, QPushButton, qApp, QRadioButton
import os.path as osp
import qtify_maya_window as qtfy
import msgBox
import qutil
reload(qutil)
import os
import re
import cui
reload(cui)
import appUsageApp
reload(appUsageApp)
import backend.renderer as renderer
reload(renderer)
import shutil
import pymel.core as pc
import backend.collageMaker as collageMaker
reload(collageMaker)
import backend.compMaker as compMaker
reload(compMaker)

rootPath = qutil.dirname(__file__, depth=2)
uiPath = osp.join(rootPath, 'ui')

# to import the rendering_helper.py
os.environ['PYTHONPATH'] += os.pathsep + osp.join(rootPath, 'src', 'backend')

title = 'Render Shots'
homeDir = renderer.homeDir

Form, Base = uic.loadUiType(osp.join(uiPath, 'main.ui'))
class RenderShotsUI(Form, Base):
    '''
    Takes input from the user for scene rendering
    '''
    def __init__(self, parent=qtfy.getMayaWindow()):
        super(RenderShotsUI, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowTitle(title)
        self.shotsBox = cui.MultiSelectComboBox(self, '--Select Shots--')
        self.pathLayout.addWidget(self.shotsBox)
        
        self.lastPath = ''
        
        
        self.renderButton.clicked.connect(self.render)
        self.browseButton.clicked.connect(self.setPath)
        self.shotsPathBox.textChanged.connect(self.populateShots)
        if not osp.exists(compMaker.nukePath):
            self.showMessage(msg='It seams like Nuke8.0v5 or Nuke9.0v4 is not installed, please install one',
                             icon=QMessageBox.Information)
            #return

        appUsageApp.updateDatabase('renderShots')
        
        
    def render(self):
        for directory in os.listdir(homeDir):
            name = osp.join(homeDir, directory)
            if osp.isdir(name):
                shutil.rmtree(name)
        errors = {}
        renderableFiles = {}
        for shot in self.shotsBox.getSelectedItems():
            filesDirectory = osp.join(self.getShotsPath(), shot, 'lighting', 'files')
            if not osp.exists(filesDirectory):
                errors[filesDirectory] = 'Directory does not exist'
                continue
            files = [phile for phile in os.listdir(filesDirectory) if osp.isfile(osp.join(filesDirectory, phile)) and osp.splitext(phile)[-1] in ['.ma', '.mb']]
            if not files:
                errors[filesDirectory] = 'No maya file found'
                continue
            if len(files) > 1:
                sb = cui.SelectionBox(self, [QRadioButton(name, self) for name in files], 'More than one files found in %s, please select one'%filesDirectory)
                sb.setCancelToolTip('Press to skip this shot')
                if not sb.exec_():
                    continue
                files = sb.getSelectedItems()
            renderableFiles[shot] = osp.join(filesDirectory, files[0])
        if errors:
            btn = self.showMessage(msg='Problems have been detected in the specified directory',
                                   ques='Do you want to continue?',
                                   icon=QMessageBox.Question,
                                   btns=QMessageBox.Yes|QMessageBox.No,
                                   details=qutil.dictionaryToDetails(errors))
            if btn == QMessageBox.No:
                return
        rdr = renderer.Renderer(self)
        length = len(renderableFiles)
        i = 1
        ws = pc.workspace(q=True, o=True)
        pc.workspace(homeDir, o=True)
        for shot, filename in renderableFiles.items():
            f = open(osp.join(homeDir, 'info.txt'), 'w')
            f.write(shot)
            f.close()
            self.setStatus('<b>Rendering %s (%s of %s)</b>'%(shot, i, length))
            rdr.render(filename)
            i += 1

        pc.workspace(ws, o=True)
        self.setStatus('')
        self.setSubStatus('')
    
    def setStatus(self, msg):
        self.statusLabel.setText(msg)
        qApp.processEvents()
        
    def setSubStatus(self, msg):
        self.subStatusLabel.setText(msg)
        qApp.processEvents()
    
    def setPath(self):
        filename = QFileDialog.getExistingDirectory(self, title, self.lastPath, QFileDialog.ShowDirsOnly)
        if filename:
            self.lastPath = filename
            self.shotsPathBox.setText(filename)
            
    def showMessage(self, **kwargs):
        return cui.showMessage(self, title=title, **kwargs)
            
    def getShotsPath(self, msg=True):
        path = self.shotsPathBox.text()
        if (not path or not osp.exists(path)) and msg:
            self.showMessage(msg='The system could not find the path specified',
                             icon=QMessageBox.Information)
            path = ''
        return path
    
    def populateShots(self):
        path = self.getShotsPath(msg=False)
        if path:
            shots = [shot for shot in os.listdir(path) if re.match('SQ\\d{3}_SH\\d{3}', shot)]
            self.shotsBox.addItems(shots)
    
    def closeEvent(self, event):
        self.deleteLater()
        event.accept()